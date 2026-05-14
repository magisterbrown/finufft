#include <complex>
#include <iostream>
#include <sstream>
#include <string>
#include <tuple>
#include <typeinfo>

#include <benchmark/benchmark.h>
#include <finufft.h>
#include <random>
#ifndef FINUFFT_USE_DUCC0
#include <fftw3.h>
#endif

using namespace std;

static const double PI       = 3.141592653589793238462643383279502884;
static const auto BENCH_NAME = "perftest/benchmarks/test_benchmark::FINUFFT";

template<typename T> void register_benchmark(int M_max, int N_max, int n_samples) {
  int type     = 1;
  double sigma = 0;
  std::stringstream benchmark_name;
  benchmark_name << BENCH_NAME;
  auto *bm =
      benchmark::RegisterBenchmark(benchmark_name.str(), [=](benchmark::State &state) {
        const int ntransf    = 1;
        const int64_t M      = state.range(0);
        const long int Nd[3] = {state.range(1), 1, 1};
        const long N         = Nd[0] * Nd[1] * Nd[2];
        const int dim        = Nd[2] > 1 ? 3 : Nd[1] > 1 ? 2 : 1;
        constexpr int iflag  = 1;
        double tol           = 1e-4;

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
        opts.upsampfac = sigma;
        opts.nthreads  = 1;
        opts.showwarn  = 0;
        for (auto _ : state) {
          if constexpr (std::is_same_v<T, double>) {
            finufft_plan_s *plan{nullptr};
            finufft_makeplan(type, dim, Nd, iflag, ntransf, tol, &plan, &opts);
            finufft_setpts(plan, M, x_p, y_p, z_p, N, s_p, t_p, u_p);
            finufft_execute(plan, c.data(), fk.data());
            finufft_destroy(plan);
            benchmark::ClobberMemory();
          } else if constexpr (std::is_same_v<T, float>) {
            finufftf_plan_s *plan{nullptr};
            finufftf_makeplan(type, dim, Nd, iflag, ntransf, tol, &plan, &opts);
            finufftf_setpts(plan, M, x_p, y_p, z_p, N, s_p, t_p, u_p);
            finufftf_execute(plan, c.data(), fk.data());
            finufftf_destroy(plan);
            benchmark::ClobberMemory();
          }
        }
        state.SetComplexityN(state.range(0) + state.range(1));
      });
  double log_start = log10(100);
  double M_step    = (log10(M_max) - log_start) / (double)n_samples;
  double N_step    = (log10(N_max) - log_start) / (double)n_samples;

  for (int i = 0; i <= n_samples; i++) {
    int M = pow(10, log_start + i * M_step);
    int N = pow(10, log_start + i * N_step);
    bm->Args({M, N});
  }
  bm->Complexity(benchmark::oN);
}

int main(int argc, char **argv) {
  benchmark::Initialize(&argc, argv);
  register_benchmark<float>(10000000, 10000, 7);
  benchmark::RunSpecifiedBenchmarks();
  benchmark::Shutdown();
}
