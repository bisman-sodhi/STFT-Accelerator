import pyrtl

def FPMul(input_A, input_B):
    A_s = pyrtl.WireVector(bitwidth=1)
    A_e = pyrtl.WireVector(bitwidth=5)
    A_f = pyrtl.WireVector(bitwidth=10)
    B_s = pyrtl.WireVector(bitwidth=1)
    B_e = pyrtl.WireVector(bitwidth=5)
    B_f = pyrtl.WireVector(bitwidth=10)

    A_s <<= input_A[-1]
    A_e <<= input_A[10:15]
    A_f <<= pyrtl.concat(pyrtl.Const(1, bitwidth=1),  input_A[0:10])

    B_s <<= input_B[-1]
    B_e <<= input_B[10:15]
    B_f <<= pyrtl.concat(pyrtl.Const(1, bitwidth=1),  input_B[0:10])

    #  XOR sign bits to determine product sign.
    oProd_s = pyrtl.WireVector(bitwidth=1)
    oProd_s <<= A_s ^ B_s

    #  Multiply the fractions of A and B
    pre_prod_frac = pyrtl.WireVector(bitwidth=20)
    pre_prod_frac <<= A_f * B_f

    #  Add exponents of A and B
    pre_prod_exp = pyrtl.WireVector(bitwidth=6)
    pre_prod_exp <<= A_e + B_e

    # If top bit of product frac is 0, shift left one
    oProd_e = pyrtl.WireVector(bitwidth=5)
    oProd_f = pyrtl.WireVector(bitwidth=10)


    oProd_e <<= pyrtl.select(pre_prod_frac[-1], pre_prod_exp - pyrtl.Const(14), pre_prod_exp - pyrtl.Const(15))
    oProd_f <<= pyrtl.select(pre_prod_frac[-1], pre_prod_frac[9:19], pre_prod_frac[8:18])
    
    # Detect underflow
    underflow = pyrtl.WireVector(bitwidth=1)

    underflow <<= pre_prod_exp < pyrtl.Const(0x10, bitwidth=6)

    oProd = pyrtl.WireVector(bitwidth=16)
    # Detect zero conditions (either product frac doesn't start with 1, or underflow)
    with pyrtl.conditional_assignment:
        with underflow:
            oProd |= 0
        with B_e == 0:
            oProd |= 0
        with A_e == 0:
            oProd |= 0
        with pyrtl.otherwise:
            oProd |= pyrtl.concat(oProd_s, oProd_e, oProd_f)

    return oProd

    