
import pyrtl

# ==== Pyrtl functions ==== #

# counts the number of wires that come before the first 1
def count_zeroes_from_end(x, start='msb'):
    if start not in ('msb', 'lsb'):
        raise pyrtl.PyrtlError('Invalid start parameter')

    def _count(x, found):
        end = x[-1] if start == 'msb' else x[0]
        is_zero = end == 0
        to_add = ~found & is_zero
        if len(x) == 1:
            return to_add
        else:
            rest = x[:-1] if start == 'msb' else x[1:]
            rest_to_add = _count(rest, found | ~is_zero)
            return to_add + rest_to_add
    return _count(x, pyrtl.as_wires(False))

def FPAdder(input_A, input_B):
    a_sign = input_A[15]
    a_expo = input_A[10:15]
    a_frac = input_A[0:10]

    b_sign = input_B[15]
    b_expo = input_B[10:15]
    b_frac = input_B[0:10]

    c_sign = pyrtl.WireVector(bitwidth=1)
    c_expo = pyrtl.WireVector(bitwidth=5)
    c_frac = pyrtl.WireVector(bitwidth=10)

    c = pyrtl.WireVector(bitwidth=16)
    c <<= pyrtl.concat(c_sign, c_expo, c_frac)

    # max exponant
    max_expo = pyrtl.WireVector(bitwidth=a_expo.bitwidth)
    max_expo <<= pyrtl.select( (a_expo>b_expo), a_expo, b_expo )

    # mantissas
    a_prepend_value = (a_expo != 0)
    b_prepend_value = (b_expo != 0)
    extra_zeros = pyrtl.Const(0, bitwidth=(2**a_expo.bitwidth))
    a_mant = pyrtl.concat(a_prepend_value,a_frac,extra_zeros)
    b_mant = pyrtl.concat(b_prepend_value,b_frac,extra_zeros)

    # normalized mantissas
    normalized_a_mant = pyrtl.shift_right_logical( a_mant, max_expo-a_expo )
    normalized_b_mant = pyrtl.shift_right_logical( b_mant, max_expo-b_expo )

    # signed normalized mantissas
    signed_normalized_a_mant = pyrtl.select(a_sign,0-normalized_a_mant,normalized_a_mant).sign_extended(normalized_a_mant.bitwidth+2)
    signed_normalized_b_mant = pyrtl.select(b_sign,0-normalized_b_mant,normalized_b_mant).sign_extended(normalized_b_mant.bitwidth+2)

    # calculate sum of mantissas
    sm = pyrtl.WireVector(bitwidth=(signed_normalized_a_mant.bitwidth))
    sm <<= signed_normalized_a_mant + signed_normalized_b_mant

    # sign
    c_sign <<= sm[-1]

    # absolute value of sum
    abs_sm = pyrtl.WireVector(bitwidth=(sm.bitwidth-1))
    abs_sm <<= pyrtl.select(c_sign, 0-sm, sm)

    # first set 1 index
    num_zeros = count_zeroes_from_end(abs_sm)

    # normalized sum
    normalized_abs_sm = pyrtl.shift_left_logical(abs_sm, num_zeros)

    # get c's exponent and fraction
    is_zero = (abs_sm==0)
    with pyrtl.conditional_assignment:
        with is_zero:
            c_expo |= 0
            c_frac |= 0
        with pyrtl.otherwise:
            c_expo |= max_expo + 1 - num_zeros
            c_frac |= normalized_abs_sm[-11:-1]

    return c
