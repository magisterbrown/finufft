#include <benchmark/benchmark.h>
#include <complex>
#include <finufft.h>
#include <random>
#ifndef FINUFFT_USE_DUCC0
#include <fftw3.h>
#endif

static const double PI = 3.141592653589793238462643383279502884;
template<typename T> void run_test() {
  const int ntransf    = 1;
  const int64_t M      = 2000000;
  const long int Nd[3] = {1000000, 1, 1};
  const long N         = Nd[0] * Nd[1] * Nd[2];
  const int type       = 1;
  const int dim        = Nd[2] > 1 ? 3 : Nd[1] > 1 ? 2 : 1;
  constexpr int iflag  = 1;
  double tol           = 1e-5;
  auto benchmark_name  = "perftest/benchmarks/test_benchmark::FINUFFT";

  std::vector<T> x(M * ntransf), y(M * ntransf), z(M * ntransf);
  std::vector<T> s(N * ntransf), t(N * ntransf), u(N * ntransf);
  std::vector<std::complex<T>> c(M * ntransf), fk(N * ntransf);

  std::default_random_engine eng{42};
  std::uniform_real_distribution<T> dist11(-1, 1);
  auto randm11 = [&eng, &dist11]() {
    return dist11(eng);
  };

  for (int64_t i = 0; i < M; i++) {
    x[i] = PI * randm11();
    y[i] = PI * randm11();
    z[i] = PI * randm11();
  }
  for (int64_t i = M; i < M * ntransf; ++i) {
    int64_t j = i % M;
    x[i]      = x[j];
    y[i]      = y[j];
    z[i]      = z[j];
  }

  if (type == 1) {
    for (int i = 0; i < M * ntransf; i++) {
      c[i].real(randm11());
      c[i].imag(randm11());
    }
  } else if (type == 2) {
    for (int i = 0; i < N * ntransf; i++) {
      fk[i].real(randm11());
      fk[i].imag(randm11());
    }
  } else if (type == 3) {
    for (int i = 0; i < M * ntransf; i++) {
      c[i].real(randm11());
      c[i].imag(randm11());
    }
    for (int i = 0; i < N * ntransf; i++) {
      s[i] = PI * randm11();
      t[i] = PI * randm11();
      u[i] = PI * randm11();
    }
  }

  T *x_p = dim >= 1 ? x.data() : nullptr;
  T *y_p = dim >= 2 ? y.data() : nullptr;
  T *z_p = dim == 3 ? z.data() : nullptr;
  T *s_p = type == 3 && dim >= 1 ? s.data() : nullptr;
  T *t_p = type == 3 && dim >= 2 ? t.data() : nullptr;
  T *u_p = type == 3 && dim == 3 ? u.data() : nullptr;
  finufft_opts opts;
  finufft_default_opts(&opts);
  opts.nthreads = 1;
  if constexpr (std::is_same_v<T, double>) {
    benchmark::RegisterBenchmark(benchmark_name, [&](benchmark::State &state) {
      for (auto _ : state) {
        finufft_plan_s *plan{nullptr};
        finufft_makeplan(type, 1, Nd, iflag, ntransf, tol, &plan, &opts);
        // finufft_setpts(plan, M, x_p, y_p, z_p, N, s_p, t_p, u_p);
        // finufft_execute(plan, c.data(), fk.data());
        state.SetItemsProcessed(N + M);
        finufft_destroy(plan);
        benchmark::ClobberMemory();
      }
    });
  } else if constexpr (std::is_same_v<T, float>) {
    benchmark::RegisterBenchmark(benchmark_name, [&](benchmark::State &state) {
      for (auto _ : state) {
        finufftf_plan_s *plan{nullptr};
        finufftf_makeplan(type, 1, Nd, iflag, ntransf, tol, &plan, &opts);
        finufft_setpts(plan, M, x_p, y_p, z_p, N, s_p, t_p, u_p);
        finufft_execute(plan, c.data(), fk.data());
        state.SetItemsProcessed(N + M);
        finufftf_destroy(plan);
        benchmark::ClobberMemory();
      }
    });
  }
}

int main(int argc, char **argv) {
  run_test<double>();
  benchmark::Initialize(&argc, argv);
  benchmark::RunSpecifiedBenchmarks();
  benchmark::Shutdown();
}
