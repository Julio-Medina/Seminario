#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 22:39:01 2022

@author: julio
"""

import numpy as np

from qiskit import IBMQ, BasicAer
from qiskit.providers.ibmq import least_busy
from qiskit import QuantumCircuit, execute
#provider=IBMQ.load_account()
from qiskit.visualization import plot_histogram

def dj_oracle(case, n):
    oracle_qc=QuantumCircuit(n+1)
    
    if case=="balanced":
        for qubit in range(n):
            oracle_qc.cx(qubit, n)
            
    if case=="constant":
        output=np.random.randint(2)
        if output ==1:
            oracle_qc.x(n)
    oracle_gate=oracle_qc.to_gate()
    oracle_gate.name="Oracle"
    return oracle_gate

def dj_algorithm(n, case='random'):
    dj_circuit=QuantumCircuit(n+1,n)
    
    for qubit in range(n):
        dj_circuit.h(qubit)
        
    dj_circuit.x(n)
    dj_circuit.h(n)
    
    if case=='random':
        random=np.random.randint(2)
        if random==0:
            case='constant'
        else:
            case='balanced'
    oracle=dj_oracle(case,n)
    dj_circuit.append(oracle,range(n+1))
    
    for i in range(n):
        dj_circuit.h(i)
        dj_circuit.measure(i,i)
        
    return dj_circuit

n=4
dj_circuit=dj_algorithm(n)
dj_circuit.draw(output='mpl')


backend=BasicAer.get_backend('qasm_simulator')
shots=1024
dj_circuit=dj_algorithm(n, 'constant')
results=execute(dj_circuit, backend=backend, shots=shots).result()
answer=results.get_counts()

plot_histogram(answer)