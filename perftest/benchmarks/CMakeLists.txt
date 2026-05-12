if(CODSPEED_MODE)
    # CodSpeed compatibility layer (wraps Google Benchmark with instrumentation).
    # The instrument-hooks C file requires Clang; use this path only in CI.
    CPMAddPackage(
        NAME
        google_benchmark
        GIT_REPOSITORY
        https://github.com/CodSpeedHQ/codspeed-cpp
        GIT_TAG
        v2.1.0
        SOURCE_SUBDIR
        google_benchmark
        OPTIONS
        "BENCHMARK_ENABLE_TESTING OFF"
        "BENCHMARK_ENABLE_INSTALL OFF"
        "BENCHMARK_ENABLE_WERROR OFF"
    )
else()
    # Upstream Google Benchmark for local development (works with any compiler).
    CPMAddPackage(
        NAME
        google_benchmark
        GIT_REPOSITORY
        https://github.com/google/benchmark.git
        GIT_TAG
        v1.9.5
        OPTIONS
        "BENCHMARK_ENABLE_TESTING OFF"
        "BENCHMARK_ENABLE_INSTALL OFF"
    )
endif()

add_executable(perftest_bench perftest_bench.cpp)
target_link_libraries(perftest_bench PRIVATE benchmark::benchmark)

finufft_link_test(test_benchmark)
