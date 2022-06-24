import pyrtl
from STFT import *


######################################### INPUTS #########################################
input_test = pyrtl.Input(bitwidth=16, name="input_test")

######################################### OUTPUTS #########################################
output_0_real = pyrtl.Output(bitwidth=16, name="output_0_real")
output_0_imag = pyrtl.Output(bitwidth=16, name="output_0_imag")
output_1_real = pyrtl.Output(bitwidth=16, name="output_1_real")
output_1_imag = pyrtl.Output(bitwidth=16, name="output_1_imag")
output_2_real = pyrtl.Output(bitwidth=16, name="output_2_real")
output_2_imag = pyrtl.Output(bitwidth=16, name="output_2_imag")
output_3_real = pyrtl.Output(bitwidth=16, name="output_3_real")
output_3_imag = pyrtl.Output(bitwidth=16, name="output_3_imag")
output_4_real = pyrtl.Output(bitwidth=16, name="output_4_real")
output_4_imag = pyrtl.Output(bitwidth=16, name="output_4_imag")
output_5_real = pyrtl.Output(bitwidth=16, name="output_5_real")
output_5_imag = pyrtl.Output(bitwidth=16, name="output_5_imag")
output_6_real = pyrtl.Output(bitwidth=16, name="output_6_real")
output_6_imag = pyrtl.Output(bitwidth=16, name="output_6_imag")
output_7_real = pyrtl.Output(bitwidth=16, name="output_7_real")
output_7_imag = pyrtl.Output(bitwidth=16, name="output_7_imag")

output_8_real  = pyrtl.Output(bitwidth=16, name="output_8_real")
output_8_imag  = pyrtl.Output(bitwidth=16, name="output_8_imag")
output_9_real  = pyrtl.Output(bitwidth=16, name="output_9_real")
output_9_imag  = pyrtl.Output(bitwidth=16, name="output_9_imag")
output_10_real = pyrtl.Output(bitwidth=16, name="output_10_real")
output_10_imag = pyrtl.Output(bitwidth=16, name="output_10_imag")
output_11_real = pyrtl.Output(bitwidth=16, name="output_11_real")
output_11_imag = pyrtl.Output(bitwidth=16, name="output_11_imag")
output_12_real = pyrtl.Output(bitwidth=16, name="output_12_real")
output_12_imag = pyrtl.Output(bitwidth=16, name="output_12_imag")
output_13_real = pyrtl.Output(bitwidth=16, name="output_13_real")
output_13_imag = pyrtl.Output(bitwidth=16, name="output_13_imag")
output_14_real = pyrtl.Output(bitwidth=16, name="output_14_real")
output_14_imag = pyrtl.Output(bitwidth=16, name="output_14_imag")
output_15_real = pyrtl.Output(bitwidth=16, name="output_15_real")
output_15_imag = pyrtl.Output(bitwidth=16, name="output_15_imag")

outputs = top(Complex(input_test, pyrtl.Const(0, bitwidth=16)))

output_0_real <<= outputs[0].real
output_0_imag <<= outputs[0].imag
output_1_real <<= outputs[1].real
output_1_imag <<= outputs[1].imag
output_2_real <<= outputs[2].real
output_2_imag <<= outputs[2].imag
output_3_real <<= outputs[3].real
output_3_imag <<= outputs[3].imag
output_4_real <<= outputs[4].real
output_4_imag <<= outputs[4].imag
output_5_real <<= outputs[5].real
output_5_imag <<= outputs[5].imag
output_6_real <<= outputs[6].real
output_6_imag <<= outputs[6].imag
output_7_real <<= outputs[7].real
output_7_imag <<= outputs[7].imag

output_8_real  <<= outputs[8].real
output_8_imag  <<= outputs[8].imag
output_9_real  <<= outputs[9].real
output_9_imag  <<= outputs[9].imag
output_10_real <<= outputs[10].real 
output_10_imag <<= outputs[10].imag
output_11_real <<= outputs[11].real 
output_11_imag <<= outputs[11].imag
output_12_real <<= outputs[12].real 
output_12_imag <<= outputs[12].imag
output_13_real <<= outputs[13].real 
output_13_imag <<= outputs[13].imag
output_14_real <<= outputs[14].real 
output_14_imag <<= outputs[14].imag
output_15_real <<= outputs[15].real 
output_15_imag <<= outputs[15].imag

############################## SIMULATION ######################################

# Generate expected results
# expected_results = []
# for i in range(len(a_inputs)):
#   expected_results.append(util.fp_add_truncate(a_inputs[i],b_inputs[i]))

input_len = 16

inputs = [int(float_to_ieee_hp((i+1)/input_len), base=2) for i in range(input_len)]

# Run simulation using specified inputs
sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)

for i in range(input_len):
    sim.step({
        'input_test':inputs[i]
    })



# run_synth()
# Print trace
sim_trace.render_trace()


# Verify results against expected results