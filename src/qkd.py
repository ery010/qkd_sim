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
receiver = pn.widgets.Select(name="Target", options=['Bob'])


# Generate key
def generate_key(event=None):
    """
    Function for generating a random key and bases of length n.
    
    :param n: length of bitstring to generate
    """
    n = n_bits.value
    bit_key = randint(2, size=n)
    bit_basis = randint(2, size=n)
    
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

# Outputs
terminal = pn.widgets.Terminal("Welcome to the QKD Simulator.\n\n", height=350, sizing_mode='stretch_width', options={"cursorBlink": True})
clear_terminal = pn.widgets.Button(name="Clear terminal")

def delete_text(event=None):
    terminal.clear()

clear_terminal.on_click(delete_text)

dashboard = pn.Row(
    pn.WidgetBox(n_bits, decoherence, displacement, receiver, generate_button, clear_terminal, height=310),
    terminal)