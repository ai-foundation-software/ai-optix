#include <vector>
#include <iostream>
#include <omp.h>

extern "C" {

    void mat_mul_cpu(const float* a, const float* b, float* c, int M, int N, int K) {
        // A is MxK, B is KxN, C is MxN
        
        #pragma omp parallel for collapse(2)
        for (int i = 0; i < M; ++i) {
            for (int j = 0; j < N; ++j) {
                float sum = 0.0f;
                // Naive implementation - can be optimized with blocking/SIMD
                for (int k = 0; k < K; ++k) {
                    sum += a[i * K + k] * b[k * N + j];
                }
                c[i * N + j] = sum;
            }
        }
    }

}
