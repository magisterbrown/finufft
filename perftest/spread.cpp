#include <complex>
#include <iostream>
#include <sstream>
#include <string>
#include <tuple>
#include <typeinfo>

#include <benchmark/benchmark.h>
#include <finufft_common/kernel.h>

#include <finufft.h>
#include <random>
#ifndef FINUFFT_USE_DUCC0
#include <fftw3.h>
#endif
static const double PI = 3.141592653589793238462643383279502884;

class SpreadReporter : public benchmark::BenchmarkReporter {
public:
  std::vector<double> time;
  std::vector<double> upsampling_factor;
  double bigo;
  bool ReportContext(const Context &context) override {
    PrintBasicContext(&GetOutputStream(), context);
    GetOutputStream() << "spread benchmark results\n";
    return true;
  }

  void ReportRuns(const std::vector<Run> &reports) override {
    auto &out = GetOutputStream();
    for (const auto &run : reports) {
      if (run.counters.find("upsampfac") != run.counters.end()) {
        time.push_back(run.GetAdjustedCPUTime());
        upsampling_factor.push_back(run.counters.at("upsampfac"));
      } else if (run.benchmark_name().find("BigO") != std::string::npos) {
        bigo = run.GetAdjustedCPUTime();
      }
    }
  }
};

template<typename T> struct InputData {
  std::vector<T> x, y, z;
  std::vector<T> s, t, u;
  std::vector<std::complex<T>> c, fk;
  int type;
  int dim;

  InputData(int type, int dim, int64_t M, long int N, std::default_random_engine &eng,
            std::uniform_real_distribution<T> &dist11)
      : x(M), y(M), z(M), s(N), t(N), u(N), c(M), fk(N), type(type), dim(dim) {
    auto randm11 = [&eng, &dist11]() {
      return dist11(eng);
    };

    for (int64_t i = 0; i < M; i++) {
      x[i] = PI * randm11();
      y[i] = PI * randm11();
      z[i] = PI * randm11();
    }
    if (type == 1) {
      for (int i = 0; i < M; i++) {
        c[i].real(randm11());
        c[i].imag(randm11());
      }
    } else if (type == 2) {
      for (int i = 0; i < N; i++) {
        fk[i].real(randm11());
        fk[i].imag(randm11());
      }
    } else if (type == 3) {
      for (int i = 0; i < M; i++) {
        c[i].real(randm11());
        c[i].imag(randm11());
      }
      for (int i = 0; i < N; i++) {
        s[i] = PI * randm11();
        t[i] = PI * randm11();
        u[i] = PI * randm11();
      }
    }
  }

  void init_pointer(T **x_p, T **y_p, T **z_p, T **s_p, T **t_p, T **u_p) {
    *x_p = x.data();
    *y_p = y.data();
    *z_p = z.data();
    *s_p = type == 3 && dim >= 1 ? s.data() : nullptr;
    *t_p = type == 3 && dim >= 2 ? t.data() : nullptr;
    *u_p = type == 3 && dim == 3 ? u.data() : nullptr;
  }
};

template<typename T>
void register_benchmark(int type, const long Nd[3], int64_t M, double tol) {
  const int ntransf   = 1;
  const long N        = Nd[0] * Nd[1] * Nd[2];
  const int dim       = Nd[2] > 1 ? 3 : Nd[1] > 1 ? 2 : 1;
  constexpr int iflag = 1;

  std::default_random_engine eng{42};
  std::uniform_real_distribution<T> dist11(-1, 1);

  InputData<T> inputs(type, dim, M, N, eng, dist11);
  auto *bm = benchmark::RegisterBenchmark(
      "benchmark_name.str()", [=](benchmark::State &state) mutable {
        T *x_p, *y_p, *z_p, *s_p, *t_p, *u_p;
        inputs.init_pointer(&x_p, &y_p, &z_p, &s_p, &t_p, &u_p);
        finufft_opts opts;
        finufft_default_opts(&opts);
        opts.upsampfac              = state.range(0) / 100.0;
        opts.nthreads               = 1;
        opts.showwarn               = 0;
        opts.spreadinterponly       = 1;
        state.counters["upsampfac"] = benchmark::Counter(opts.upsampfac);
        finufft_spread_opts inner_opts{.upsampfac = opts.upsampfac, .kerformula = 0};
        int nspread =
            finufft::kernel::theoretical_kernel_ns(tol, dim, type, 0, inner_opts);
        int spread_complexity = M * std::pow(nspread, dim);
        state.SetComplexityN(spread_complexity);
        for (auto _ : state) {
          if constexpr (std::is_same_v<T, double>) {
            finufft_plan_s *plan{nullptr};
            finufft_makeplan(type, dim, Nd, iflag, ntransf, tol, &plan, &opts);
            finufft_setpts(plan, M, x_p, y_p, z_p, N, s_p, t_p, u_p);
            finufft_execute(plan, inputs.c.data(), inputs.fk.data());
            finufft_destroy(plan);
            benchmark::ClobberMemory();
          } else if constexpr (std::is_same_v<T, float>) {
            finufftf_plan_s *plan{nullptr};
            finufftf_makeplan(type, dim, Nd, iflag, ntransf, tol, &plan, &opts);
            finufftf_setpts(plan, M, x_p, y_p, z_p, N, s_p, t_p, u_p);
            finufftf_execute(plan, inputs.c.data(), inputs.fk.data());
            finufftf_destroy(plan);
            benchmark::ClobberMemory();
          }
        }
      });
  for (int i = 125; i <= 200; i += 5) {
    bm->Args({i});
  }
  bm->Complexity(benchmark::oN);
}

int main(int argc, char **argv) {
  benchmark::Initialize(&argc, argv);
  long Nd[3] = {10000, 1, 1};
  int64_t M  = 10000000;
  double tol = 1e-4;
  register_benchmark<double>(1, Nd, M, tol);
  SpreadReporter reporter;
  // benchmark::RunSpecifiedBenchmarks(&reporter);
  benchmark::RunSpecifiedBenchmarks();
  std::cout << "time = [";
  for (size_t i = 0; i < reporter.time.size(); ++i) {
    if (i > 0) std::cout << ", ";
    std::cout << reporter.time[i];
  }
  std::cout << "]\n";

  std::cout << "upsampling_factor = [";
  for (size_t i = 0; i < reporter.upsampling_factor.size(); ++i) {
    if (i > 0) std::cout << ", ";
    std::cout << reporter.upsampling_factor[i];
  }
  std::cout << "]\n";

  std::cout << "bigo = " << reporter.bigo << '\n';
  benchmark::Shutdown();
}
