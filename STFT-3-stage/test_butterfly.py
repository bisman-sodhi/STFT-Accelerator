import pyrtl
from STFT import *

pyrtl.set_debug_mode()

buffer_0_real = pyrtl.MemBlock(bitwidth=8, addrwidth=3, asynchronous=True, name="buffer_0_real")
buffer_0_imag = pyrtl.MemBlock(bitwidth=8, addrwidth=3, asynchronous=True, name="buffer_0_imag")

# Inputs
a_real = pyrtl.Input(bitwidth=8, name="a_real")
a_imag = pyrtl.Input(bitwidth=8, name="a_imag")

buffer_input = pyrtl.Input(bitwidth=8, name="buffer_input")
buffer_index = pyrtl.Input(bitwidth=3, name="buffer_index")
ready = pyrtl.Input(bitwidth=8, name="ready")

# Outputs
c_real = pyrtl.Output(bitwidth=8, name="c_real")
c_imag = pyrtl.Output(bitwidth=8, name="c_imag")

d_real = pyrtl.Output(bitwidth=8, name="d_real")
d_imag = pyrtl.Output(bitwidth=8, name="d_imag")

# Twiddle factor
t_real = pyrtl.Input(bitwidth=8, name="t_real")
t_imag = pyrtl.Input(bitwidth=8, name="t_imag")


T = Complex(t_real, t_imag)

A = Complex(a_real, a_imag)

with pyrtl.conditional_assignment:
    with ready == 0:
        buffer_0_real[buffer_index] |= buffer_input
        buffer_0_imag[buffer_index] |= buffer_input
    with pyrtl.otherwise:
        result1, result2 = butterfly(A, T, pyrtl.Const(1), buffer_0_real, buffer_0_imag, pyrtl.Const(1), pyrtl.Const(1), pyrtl.Const(4))

        c_real |= result1.real
        c_imag |= result1.imag

        d_real |= result2.real
        d_imag |= result2.imag


############################## SIMULATION ######################################

a_inputs_real = [1, 1, 1] 
a_inputs_imag = [0, 0, 0]
t_inputs_real = [1, 1, 1]
t_inputs_imag = [0, 0, 0] 

# Run simulation using specified inputs
sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)

for i in range(8):
    sim.step({
        'buffer_input': 1,
        'buffer_index': i,
        'ready': 0,
        'a_real':0,
        'a_imag':0,
        't_real':0,
        't_imag':0,
    })

for i in range(len(a_inputs_real)):
    sim.step({
        'buffer_input': 0,
        'buffer_index': 0,        
        'ready': 1,
        'a_real':a_inputs_real[i],
        'a_imag':a_inputs_imag[i],
        't_real':t_inputs_real[i],
        't_imag':t_inputs_imag[i],
    })



# Print trace
sim_trace.render_trace()
