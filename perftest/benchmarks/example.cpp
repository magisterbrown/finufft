#include <benchmark/benchmark.h>

static void TestFunction(benchmark::State &state) {
  int a = 0;
  for (auto _ : state) {
    a += 3;
  }
}

BENCHMARK(TestFunction);
BENCHMARK_MAIN();
