from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, execute, BasicAer, Aer, transpile, assemble
from qiskit.tools.visualization import plot_histogram

import numpy as np
from numpy.random import randint
import panel as pn

import time

pn.extension()
pn.extension('terminal')

# Parameter selectors
n_bits = pn.widgets.IntInput(name="Number of Qubits", value=10, step=1, start=10, end=1000000)
decoherence = pn.widgets.FloatSlider(name="Decoherence rate", value=0, step=0.01, start=0, end=0.75)
displacement = pn.widgets.FloatSlider(name="Displacement (km)", value=100, step=100, start=100, end=1000)
receiver = pn.widgets.Select(name="Target", options=['Bob', 'Test'])

keys = []
bases = []
encoded_output = []

bob_results = []
# Generate key
def generate_key(event=None):
    """
    Function for generating a random key and bases of length n.
    
    :param n: length of bitstring to generate
    """
    n = n_bits.value
    bit_key = randint(2, size=n)
    bit_basis = randint(2, size=n)
    
    keys.append(bit_key)
    bases.append(bit_basis)
    
    terminal.write("\nGenerating " + str(n) + "-qubit key and basis ")
    for i in range(3):
        time.sleep(0.25)
        terminal.write(".")
    time.sleep(0.25)
    terminal.write(" Finished")
    time.sleep(0.4)
    
    terminal.write("\nKey: " + str(bit_key) + "\nBasis: " + str(bit_basis))
    
generate_button = pn.widgets.Button(name="Generate key")
generate_button.on_click(generate_key)

qubit_select = pn.widgets.Select(name="Qubit", options=[])

measure_button = pn.widgets.Button(name="Measure")

# Outputs
terminal = pn.widgets.Terminal("Welcome to the QKD Simulator.\n\n", height=390, sizing_mode='stretch_width', options={"cursorBlink": True})
clear_terminal = pn.widgets.Button(name="Clear terminal")

send_button = pn.widgets.Button(name="Send")

measure_terminal = pn.widgets.Terminal(height=120, sizing_mode='stretch_width', options={"cursorBlink": True})

def send(event=None):
    msg_receiver = receiver.value
    
    terminal.write("\nEncoding ")
    encode()
    for i in range(3):
        time.sleep(0.25)
        terminal.write(".")
    time.sleep(0.25)
    terminal.write(" Sent")
    time.sleep(0.4)
    
def encode(event=None):
    """
    Function for encoding a message.
    
    :param bit_key: Randomly generated bitstring key
    :param bit_bases: Bases for each bit in bit_key
    """
    bit_key = keys[-1]
    bit_bases = bases[-1]
    output = []
    
    # length of bit_key and bit_bases should be the same
    assert len(bit_key) == len(bit_bases), "Key and bases sequence should be equivalent."
    
    for i in range(len(bit_key)):
        qc = QuantumCircuit(1, 1)
        
        # Encode qubit in Z-basis (horizontal-vertical)
        if bit_bases[i] == 0:
            if bit_key[i] == 0:
                pass
            else:
                qc.x(0)
        
        # Encode qubit in X-basis (diagonal)
        else:
            if bit_key[i] == 0:
                qc.h(0)
            else:
                qc.x(0)
                qc.h(0)
                
        qc.barrier()
        output.append(qc)
        
    encoded_output.append(output)
    qubit_select.options += ["Qubit " + str(i) for i in range(len(output))]

send_button.on_click(send)
    
def delete_text(event=None):
    terminal.clear()

clear_terminal.on_click(delete_text)


def measure_qubits(event=None):
    measure_terminal.clear()
    measure_terminal.write("\nMeasuring ")
    for i in range(3):
        time.sleep(0.25)
        measure_terminal.write(".")
    time.sleep(0.25)
    measure_terminal.write(" Finished")
    time.sleep(0.4)
    
    noise = decoherence.value
    msg = encoded_output[-1]
    n = n_bits.value
    bases = randint(2, size=n)
    
    if noise > 0:
        
        temp_backend = Aer.get_backend("aer_simulator")
        temp_results = []
        
        noise_idx = []
        for i_n in range(int(len(msg)*noise)):
            noise_idx.append(random.randint(0, len(msg)-1))
            
        for n_idx in noise_idx:
            # Z-basis
            if bases[n_idx] == 0: 
                msg[n_idx].measure(0, 0)

             # X-basis
            if bases[n_idx] == 1:
                msg[n_idx].h(0)
                msg[n_idx].measure(0, 0)
                
            temp_aer_sim = Aer.get_backend("aer_simulator")
            temp_qobj = assemble(msg[n_idx], shots=1, memory=True)
            temp_sim_results = temp_aer_sim.run(temp_qobj).result()
            temp_measured_bit = int(temp_sim_results.get_memory()[0])
            temp_results.append(temp_measured_bit)
         
    backend = Aer.get_backend("aer_simulator")
    results = []
    
    for i in range(len(msg)):
        # Z-basis
        if bases[i] == 0: 
            msg[i].measure(0, 0)
            
         # X-basis
        if bases[i] == 1:
            msg[i].h(0)
            msg[i].measure(0, 0)
            
        aer_sim = Aer.get_backend("aer_simulator")
        qobj = assemble(msg[i], shots=1, memory=True)
        sim_results = aer_sim.run(qobj).result()
        measured_bit = int(sim_results.get_memory()[0])
        results.append(measured_bit)
        
    bob_results.append(results)
    
    measure_terminal.write("\nGenerated Key: "+ str(results))


measure_button.on_click(measure_qubits)  

dashboard = pn.Row(
    pn.WidgetBox(n_bits, decoherence, displacement, receiver, generate_button, clear_terminal, send_button, height=350),
    terminal
)

measurement = pn.Row(pn.WidgetBox(measure_button, height=100), measure_terminal)