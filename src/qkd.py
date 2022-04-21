from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, execute, BasicAer, Aer, transpile, assemble
from qiskit.tools.visualization import plot_histogram

import numpy as np
from numpy.random import randint
import panel as pn

pn.extension()

def n_bits():
    return pn.widgets.IntInput(name="Number of Qubits", value=10, step=1, start=10, end=1000000)