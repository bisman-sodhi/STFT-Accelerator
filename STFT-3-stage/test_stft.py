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

############################## SIMULATION ######################################


input_len = 16

inputs = [int(float_to_ieee_hp((i+1)/input_len), base=2) for i in range(input_len)]

# Run simulation using specified inputs
sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)

for i in range(input_len):
    sim.step({
        'input_test':inputs[i]
    })



run_synth()
# Print trace
sim_trace.render_trace()


# Verify results against expected results