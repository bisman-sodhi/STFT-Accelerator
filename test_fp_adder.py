
import pyrtl
import numpy as np
import struct
import math
from FPAdder import *

# ==== Simulation Functions ==== #

# returns the bits of a float written into a string
def float_to_ieee_hp(n):
  return bin(np.float16(n).view('H'))[2:].zfill(16)

# returns a float given a binary string
def bin_to_float(binary):
    return struct.unpack('!f',struct.pack('!I', int(binary, 2)))[0]

# returns the sum of two float16s using the "round-to-zero" mode
def fp_add_truncate(a,b):
    if math.isnan(a) or math.isnan(b) or math.isinf(a) or math.isinf(b):
        return math.nan
    # force a and b to half-precision
    a = np.float16(a)
    b = np.float16(b)
    # perform double-precision addition
    a = np.float64(a)
    b = np.float64(b)
    out = a+b
    # get fractional and exponent part
    (fr,exp) = math.frexp(out)
    # get sign
    sign = fr<0
    fr = abs(fr)
    # chop off all but 10 bits of the sum
    mantissa = math.floor(fr * 2**11)
    new_fr = mantissa/(2**10)
    return np.float16( (-1 if sign else 1) * new_fr * 2**(exp-1) )

# returns true iff the float value will not be tested in the autograder
def not_tested(n):
  n = np.float16(n)
  # zero is tested
  if n==0:
    return False
  # not testing infinity, NaN, or denormalized values
  if math.isinf(n) or math.isnan(n) or (math.floor(math.log2(abs(n)))<-14):
    return True
  # testing everything else
  return False

A = pyrtl.Input(bitwidth=16, name="A")
B = pyrtl.Input(bitwidth=16, name="B")
C = pyrtl.Output(bitwidth=16, name="C")

C <<= FPAdder(A, B)

############################## SIMULATION ######################################

if __name__ == '__main__':

  import random
  import numpy as np
  import math

  # Inputs to test
  def rand_f16(sign=math.nan, expo=math.nan, frac=math.nan):
    if math.isnan(sign):
      sign = (random.random() < 0.5)
    if math.isnan(expo):
      expo = int(random.random()*32)
    if math.isnan(frac):
      frac = random.random()*2**11
    return np.float16((-1 if sign else 1) * (1+(frac/2**10)) * (2**(expo-15)))
  random.seed(154)
  # test 10000 random inputs
  a_inputs = [rand_f16() for _ in range(10000)]
  b_inputs = [rand_f16() for _ in range(10000)]
  # test 20 inputs for every difference in exponents that exist
  for i in range(1,31):
    for j in range(1,i+1):
      for _ in range(20):
        a_inputs.append(rand_f16(expo=i))
        b_inputs.append(rand_f16(expo=i))
        a_inputs.append(rand_f16(expo=i))
        b_inputs.append(rand_f16(expo=i-j))
        a_inputs.append(rand_f16(expo=i-j))
        b_inputs.append(rand_f16(expo=i))
  # misc
  for _ in range(100):
    # test when single inputs are zero
    a_inputs.append(rand_f16())
    b_inputs.append(0)
    a_inputs.append(0)
    b_inputs.append(rand_f16())
    # test when output is zero
    a_inputs.append(rand_f16())
    b_inputs.append(-a_inputs[-1])
    # test worst case rounding
    a_inputs.append(rand_f16(sign=0, expo=30))
    b_inputs.append(rand_f16(sign=1, expo=1))
    a_inputs.append(rand_f16(sign=0, expo=1))
    b_inputs.append(rand_f16(sign=1, expo=30))
  # test absolute worst case rounding
  a_inputs.append(rand_f16(sign=1,expo=0b11110,frac=0b1111111111))
  b_inputs.append(rand_f16(sign=0,expo=0b00001,frac=0b0000000000))
  a_inputs.append(rand_f16(sign=0,expo=0b11110,frac=0b1111111111))
  b_inputs.append(rand_f16(sign=1,expo=0b00001,frac=0b0000000000))
  assert(len(a_inputs) == len(b_inputs))



  # Generate expected results
  expected_results = []
  for i in range(len(a_inputs)):
    expected_results.append(fp_add_truncate(a_inputs[i],b_inputs[i]))



  # Run simulation using specified inputs
  sim_trace = pyrtl.SimulationTrace()
  sim = pyrtl.Simulation(tracer=sim_trace)
  for i in range(len(a_inputs)):
    sim.step({
      'A':int(float_to_ieee_hp(a_inputs[i]), base=2),
      'B':int(float_to_ieee_hp(b_inputs[i]), base=2),
    })



  # Print trace
  # sim_trace.render_trace(symbol_len=None, segment_size=1, repr_func=bin, extra_line=False)



  # Verify results against expected results
  passed = True
  num_tests_ran = 0
  num_tests_failed = 0
  for i in range(len(expected_results)):
    # if input or expected result is invalid
    if not_tested(expected_results[i]):
      # print(" {} will not be tested. Skipping test...".format(expected_results[i]))
      continue
    if not_tested(a_inputs[i]):
      # print(" {} will not be tested. Skipping test...".format(a_inputs[i]))
      continue
    if not_tested(b_inputs[i]):
      # print(" {} will not be tested. Skipping test...".format(b_inputs[i]))
      continue
    # if output matched expected result
    
    if float_to_ieee_hp(expected_results[i]) == bin(sim_trace.trace['C'][i])[2:].zfill(16):
      # print("Passed case:", float_to_ieee_hp(a_inputs[i]), "+", float_to_ieee_hp(b_inputs[i]), "=", float_to_ieee_hp(expected_results[i]))
      pass
    else:
      passed = False
      print("Failed case:", float_to_ieee_hp(a_inputs[i]), "+", float_to_ieee_hp(b_inputs[i]))
      print(" expected :", float_to_ieee_hp(expected_results[i]))
      print(" given    :", bin(sim_trace.trace['C'][i])[2:].zfill(16))
      print()
      num_tests_failed += 1
      if num_tests_failed==10: break
    num_tests_ran += 1

  if passed:
    print("All {} test cases passed!".format(num_tests_ran))
  else:
    print("Some test cases failed.")
    exit(1)
