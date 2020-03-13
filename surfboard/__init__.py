# Copyright (C) Yuki Takagi 2020
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE_1_0.txt or copy at
# https://www.boost.org/LICENSE_1_0.txt)

import numpy as _d
import math as _s

class Transformed:
    def __init__(self, closure):
        self.closure = closure

    def __getitem__(self, key):
        return self.closure(key)

def lin_interpolated(array):
    def closure(n):
        if round(n) == n:
            return array[round(n)]
        else:
            nl = int(_s.floor(n))
            nh = int(_s.ceil(n))
            return array[nl] * (n - nl) + array[nh] * (nh - n)
    return Transformed(closure)

def stretched(array, length):
    a = lin_interpolated(array)
    def closure(n):
        return a[n / length]
    return Transformed(closure)

def reform(wave, target_frequency, target_seconds):
    framerate = wave.parameter.framerate
    lengthr = round(target_seconds * framerate)

    frq = stretched(wave.frq.frq_samples, lengthr)

    t0 = 1 / frq[0] * framerate
    tn = 1 / frq[lengthr] * framerate
    amp = lin_interpolated(_d.frombuffer(wave.frames, 'int16'))

    f0 = _d.mean(wave.frq.frq_samples)
    speed = target_frequency / f0

    reformed = _d.zeros(lengthr)
    ratiot = lengthr / (len(wave) -t0 -tn)
    j = t0

    for i in range(0, lengthr):
        l = i / ratiot + t0
        t = 1 / frq[i] * framerate

        k = j - t if j > l else j + t
        reformed[i] += amp[j] * (t - abs(l - j)) / t
        reformed[i] += amp[k] * (t - abs(l - k)) / t

        j += speed
        if j > l + t:
            j -= 2 * t
        elif j < l -t:
            j += 2 * t

    return reformed
