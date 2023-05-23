cmake_minimum_required(VERSION 3.20)
project(Project_M C)

set(CMAKE_C_STANDARD 11)

add_executable(Project_M
        dft_idft_1d.c
        dft_idft_2d.c
        fft_ifft_1d.cpp)
