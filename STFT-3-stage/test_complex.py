import pyrtl
from STFT import *

pyrtl.set_debug_mode()

# Inputs
a_real = pyrtl.Input(bitwidth=8, name="a_real")
a_imag = pyrtl.Input(bitwidth=8, name="a_imag")
b_real = pyrtl.Input(bitwidth=8, name="b_real")
b_imag = pyrtl.Input(bitwidth=8, name="b_imag")

# Outputs
c_real = pyrtl.Output(bitwidth=8, name="c_real")
c_imag = pyrtl.Output(bitwidth=8, name="c_imag")

A = Complex(a_real, a_imag)
B = Complex(b_real, b_imag)

sub_result = ComplexAdd(A, B)
c_real <<= sub_result.real
c_imag <<= sub_result.imag

############################## SIMULATION ######################################

# Inputs to test
a_inputs_real = [1, int('0b11111101', 2),1] # -3
a_inputs_imag = [1, 2, 0]
b_inputs_real = [2, 1, 2]
b_inputs_imag = [2, int("0b11111111", 2), 0] # -1

# Run simulation using specified inputs
sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)
for i in range(len(a_inputs_real)):
    sim.step({
        'a_real':a_inputs_real[i],
        'a_imag':a_inputs_imag[i],
        'b_real':b_inputs_real[i],
        'b_imag':b_inputs_imag[i],
    })



# Print trace
sim_trace.render_trace()
