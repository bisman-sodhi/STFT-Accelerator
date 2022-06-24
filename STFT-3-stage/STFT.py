import pyrtl
pyrtl.set_debug_mode()

from pyrtl.analysis import area_estimation, TimingAnalysis

from FPAdder import *
from FpMul import *

import pyrtl
import numpy as np

######################################### STAGE 1 BUFFER #########################################
buffer_10_real = pyrtl.MemBlock(bitwidth=16, addrwidth=3, asynchronous=True, name="buffer_10_real")
buffer_10_imag = pyrtl.MemBlock(bitwidth=16, addrwidth=3, asynchronous=True, name="buffer_10_imag")

######################################### STAGE 2 BUFFERS #########################################
buffer_20_real = pyrtl.MemBlock(bitwidth=16, addrwidth=3, asynchronous=True, name="buffer_20_real")
buffer_20_imag = pyrtl.MemBlock(bitwidth=16, addrwidth=3, asynchronous=True, name="buffer_20_imag")

buffer_21_real = pyrtl.MemBlock(bitwidth=16, addrwidth=3, asynchronous=True, name="buffer_21_real")
buffer_21_imag = pyrtl.MemBlock(bitwidth=16, addrwidth=3, asynchronous=True, name="buffer_21_imag")

######################################### STAGE 3 BUFFERS #########################################
buffer_30_real = pyrtl.MemBlock(bitwidth=16, addrwidth=3, asynchronous=True, name="buffer_30_real")
buffer_30_imag = pyrtl.MemBlock(bitwidth=16, addrwidth=3, asynchronous=True, name="buffer_30_imag")

buffer_31_real = pyrtl.MemBlock(bitwidth=16, addrwidth=3, asynchronous=True, name="buffer_31_real")
buffer_31_imag = pyrtl.MemBlock(bitwidth=16, addrwidth=3, asynchronous=True, name="buffer_31_imag")

buffer_32_real = pyrtl.MemBlock(bitwidth=16, addrwidth=3, asynchronous=True, name="buffer_32_real")
buffer_32_imag = pyrtl.MemBlock(bitwidth=16, addrwidth=3, asynchronous=True, name="buffer_32_imag")

buffer_33_real = pyrtl.MemBlock(bitwidth=16, addrwidth=3, asynchronous=True, name="buffer_33_real")
buffer_33_imag = pyrtl.MemBlock(bitwidth=16, addrwidth=3, asynchronous=True, name="buffer_33_imag")


cycle = pyrtl.Register(bitwidth=4, name="cycle")
cycle.next <<= cycle + 1 # Increment counter each cycle

def float_to_ieee_hp(n):
  return bin(np.float16(n).view('H'))[2:].zfill(16)

# Inputs are all IEEE, half-precision floating point numbers 
class Complex:
    def __init__(self, real, imag):
        self.real = real
        self.imag = imag

def ComplexAdd(input_A, input_B):
    add_real = pyrtl.WireVector(bitwidth=16)
    add_imag = pyrtl.WireVector(bitwidth=16)

    add_real <<= FPAdder(input_A.real, input_B.real)
    add_imag <<= FPAdder(input_A.imag, input_B.imag)

    return Complex(add_real, add_imag)

def ComplexSub(input_A, input_B):
    sub_real = pyrtl.WireVector(bitwidth=16)
    sub_imag = pyrtl.WireVector(bitwidth=16)

    sub_real <<= FPAdder(input_A.real, pyrtl.concat(~input_B.real[-1], input_B.real[0:15]))
    sub_imag <<= FPAdder(input_A.imag, pyrtl.concat(~input_B.imag[-1], input_B.imag[0:15]))

    return Complex(sub_real, sub_imag)

def ComplexMul(input_A, input_B):
    mult_real = pyrtl.WireVector(bitwidth=16)
    mult_imag = pyrtl.WireVector(bitwidth=16)

    mult_real <<= FPAdder(FPMul(input_A.real, input_B.real), FPMul(input_A.imag, pyrtl.concat(~input_B.imag[-1], input_B.imag[0:15])))
    mult_imag <<= FPAdder(FPMul(input_A.real, input_B.imag), FPMul(input_A.imag, input_B.real))

    return Complex(mult_real, mult_imag)


def butterfly(input_A, index, buffer_real, buffer_imag, s, k, n):
    add_output = Complex(pyrtl.Register(bitwidth=16), pyrtl.Register(bitwidth=16))
    sub_output = Complex(pyrtl.Register(bitwidth=16), pyrtl.Register(bitwidth=16))

    m = pyrtl.WireVector(bitwidth=3) 

    mod_by = pyrtl.WireVector(bitwidth=16)
    mod_by <<= (n - s) 
    m1 = (pyrtl.shift_right_logical(index, mod_by))
    m2 = pyrtl.shift_left_logical(pyrtl.Const(1), mod_by)
    m <<= index - (m1 * m2)

    input_B = Complex(pyrtl.WireVector(bitwidth=16), pyrtl.WireVector(bitwidth=16))

    input_B.real <<= buffer_real[m]
    input_B.imag <<= buffer_imag[m]
    twiddle_real = pyrtl.WireVector(bitwidth=16)
    twiddle_imag = pyrtl.WireVector(bitwidth=16)

    with pyrtl.conditional_assignment:
        with k == 0:
            twiddle_real |= 0x3C00      # FP representation of '1'
            twiddle_imag |= 0           # FP representation of '0'
        with k == 1:
            twiddle_real |= 0           # FP representation of '0'
            twiddle_imag |= 0xBC00      # FP representation of '-1'
        with k == 2:
            twiddle_real |= 0x39A8      # FP representation of '0.7071'
            twiddle_imag |= 0xB9A8      # FP representation of '-0.7071'
        with k == 3:
            twiddle_real |= 0xB9A8      # FP representation of '-0.7071'
            twiddle_imag |= 0xB9A8      # FP representation of '-0.7071'
        with k == 4:
            twiddle_real |= 0x3B64      # FP representation of '0.9239'
            twiddle_imag |= 0xB620      # FP representation of '-0.3827'
        with k == 5:
            twiddle_real |= 0xB620      # FP representation of '-0.3827'
            twiddle_imag |= 0xBB64      # FP representation of '-0.9239'
        with k == 6:
            twiddle_real |= 0x3620      # FP representation of '0.3827'
            twiddle_imag |= 0xBB64      # FP representation of '-0.9239'
        with k == 7:
            twiddle_real |= 0xBB64      # FP representation of '-0.9239'
            twiddle_imag |= 0xB620      # FP representation of '-0.3827'
        
        
    add_result = ComplexAdd(input_B, ComplexMul(Complex(twiddle_real, twiddle_imag), input_A))
    add_output.real.next <<= add_result.real
    add_output.imag.next <<= add_result.imag

    sub_result = ComplexSub(input_B, ComplexMul(Complex(twiddle_real, twiddle_imag), input_A))
    sub_output.real.next <<= sub_result.real
    sub_output.imag.next <<= sub_result.imag

    buffer_real[m] <<= input_A.real
    buffer_imag[m] <<= input_A.imag

    return add_output, sub_output


def top(input_A):
    n = pyrtl.Const(4, bitwidth=3) 
    s1 = pyrtl.Const(1)
    s2 = pyrtl.Const(2)
    s3 = pyrtl.Const(3)
    s4 = pyrtl.Const(4)
    # Stage 1
    x10, x11 = butterfly(input_A, cycle, buffer_10_real, buffer_10_imag, s1, pyrtl.Const(0), n)
        
    # Stage 2
    x20, x21 = butterfly(x10, cycle, buffer_20_real, buffer_20_imag, s2, pyrtl.Const(0), n)
    x22, x23 = butterfly(x11, cycle, buffer_21_real, buffer_21_imag, s2, pyrtl.Const(1), n)
    
    # Stage 3
    x30, x31 = butterfly(x20, cycle, buffer_30_real, buffer_30_imag, s3, pyrtl.Const(0), n)
    x32, x33 = butterfly(x21, cycle, buffer_31_real, buffer_31_imag, s3, pyrtl.Const(1), n)
    x34, x35 = butterfly(x22, cycle, buffer_32_real, buffer_32_imag, s3, pyrtl.Const(2), n)
    x36, x37 = butterfly(x23, cycle, buffer_33_real, buffer_33_imag, s3, pyrtl.Const(3), n)

    return x30, x34, x32, x36, x31, x35, x33, x37

def run_synth():
    print("logic = {:2f} mm^2, mem={:2f} mm^2".format(*area_estimation()))
