#include <complex>
#include <iostream>
#include <sstream>
#include <string>
#include <tuple>
#include <typeinfo>

#include <finufft_common/kernel.h>

#include <finufft.h>
#include <random>
#ifndef FINUFFT_USE_DUCC0
#include <fftw3.h>
#endif
static const double PI = 3.141592653589793238462643383279502884;

template<typename T> struct InputData {
  std::vector<T> x, y, z;
  std::vector<T> s, t, u;
  std::vector<std::complex<T>> c, fk;
  int type;
  int dim;

  InputData(int type, int dim, int64_t M, long int N)
      : x(M), y(M), z(M), s(N), t(N), u(N), c(M), fk(N), type(type), dim(dim) {
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
void register_benchmark(int type, const long Nd[3], int64_t M, double tol,
                        double upsampfac) {
  const int ntransf = 1;
  const long N = Nd[0] * Nd[1] * Nd[2];
  const int dim = Nd[2] > 1 ? 3 : Nd[1] > 1 ? 2 : 1;
  constexpr int iflag = 1;

  InputData<T> inputs(type, dim, M, N);
  T *x_p, *y_p, *z_p, *s_p, *t_p, *u_p;
  inputs.init_pointer(&x_p, &y_p, &z_p, &s_p, &t_p, &u_p);
  finufft_opts opts;
  finufft_default_opts(&opts);
  opts.upsampfac = upsampfac;
  opts.nthreads = 1;
  opts.showwarn = 0;
  opts.spreadinterponly = 1;

  if constexpr (std::is_same_v<T, double>) {
    finufft_plan_s *plan{nullptr};
    finufft_makeplan(type, dim, Nd, iflag, ntransf, tol, &plan, &opts);
    finufft_setpts(plan, M, x_p, y_p, z_p, N, s_p, t_p, u_p);
    finufft_execute(plan, inputs.c.data(), inputs.fk.data());
    finufft_destroy(plan);
  } else if constexpr (std::is_same_v<T, float>) {
    finufftf_plan_s *plan{nullptr};
    finufftf_makeplan(type, dim, Nd, iflag, ntransf, tol, &plan, &opts);
    finufftf_setpts(plan, M, x_p, y_p, z_p, N, s_p, t_p, u_p);
    finufftf_execute(plan, inputs.c.data(), inputs.fk.data());
    finufftf_destroy(plan);
  }
}

int main(int argc, char **argv) {
  double density = 1;
  long Nd[3] = {100000, 1, 1};
  int64_t M = Nd[0] * Nd[1] * Nd[2] * density;
  double tol = 1e-6;
  register_benchmark<double>(1, Nd, M, tol, 2.0);
}
