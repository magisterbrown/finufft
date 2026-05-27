# Each source test file is instantiated in single and double precision
set(PERFTESTS guru_timing_test manysmallprobs spreadtestnd spreadtestndall)
# Other than that, it looks like no actual tests executed here by CMake

foreach(TEST ${PERFTESTS})
    add_executable(${TEST} ${TEST}.cpp)
    if(FINUFFT_USE_DUCC0)
        target_compile_definitions(${TEST} PRIVATE -DFINUFFT_USE_DUCC0)
    endif()
    finufft_link_test(${TEST})

    add_executable(${TEST}f ${TEST}.cpp)
    target_compile_definitions(${TEST}f PRIVATE -DSINGLE)
    if(FINUFFT_USE_DUCC0)
        target_compile_definitions(${TEST}f PRIVATE -DFINUFFT_USE_DUCC0)
    endif()
    finufft_link_test(${TEST}f)
endforeach()

include(CheckIncludeFile)
check_include_file("getopt.h" HAVE_GETOPT_H)
if(HAVE_GETOPT_H)
    add_executable(perftest perftest.cpp)
    if(FINUFFT_USE_DUCC0)
        target_compile_definitions(perftest PRIVATE -DFINUFFT_USE_DUCC0)
    endif()
    finufft_link_test(perftest)
endif()

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

add_executable(complexity complexity.cpp)
if(FINUFFT_USE_DUCC0)
    target_compile_definitions(complexity PRIVATE -DFINUFFT_USE_DUCC0)
endif()
target_link_libraries(complexity PRIVATE benchmark::benchmark)
finufft_link_test(complexity)
