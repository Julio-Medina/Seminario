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
#IBMQ.save_account('8c6e5a235145cbc4748433e0c3d23a43ca09c75589aeb75be372d765e3d5736d50340ad228f8262555d919b5b9499edae27cf625e7973462a6a9beaf3c685ef9')
provider=IBMQ.load_account()
from qiskit.visualization import plot_histogram

def dj_oracle(case, n):
# A QuantumCircuit object is needed, the size of the input is n+1 qubits
# The size of the input is n plus one addiotal qubit to make the oracle unitary
    oracle_qc=QuantumCircuit(n+1)
    
    #case for a balanced oracle, this means that half the outputs are 1 and half are 0
    if case=="balanced":
        # controlled-NOT is applied to the each qubit
        # using the output qubit as the target
        for qubit in range(n):
            oracle_qc.cx(qubit, n)
    
    # case when the oracle is constant, this means it is either 0 or 1        
    if case=="constant":
        output=np.random.randint(2)
        if output ==1:
            oracle_qc.x(n)
    oracle_gate=oracle_qc.to_gate()
    oracle_gate.name="Oracle"# to label the gate in the q. circuit
    return oracle_gate

def dj_algorithm(n, case='random'):
    # first parameter is the number of qubits, 
    #second parameter is number of classical bits
    dj_circuit=QuantumCircuit(n+1,n)
    
    # First step of the Deutch-Jozsa Algorith 
    # Apply the Hadamard gate to the input qubits
    #dj_circuit.x(3)
    for qubit in range(n):
        dj_circuit.h(qubit)
        
    # Preparing the n+1 qubit in the |-> state
    # by applying the X|0> and then HX|0>
    dj_circuit.x(n)
    dj_circuit.h(n)
   
    # checks which case of the Oracle is applied
    if case=='random':
        random=np.random.randint(2)
        if random==0:
            case='constant'
        else:
            case='balanced'
    # creates the Oracle for n inputs
    oracle=dj_oracle(case,n)
    # appends the oracle to the circuit
    dj_circuit.append(oracle,range(n+1))
    
    
    for i in range(n):
        # Apply the n Hadamard gates after applying the Oracle
        dj_circuit.h(i)
        # Do the measurement, in the base x |+>,|->
        # the measurement is done on the qubit i and stored on the classical bit i
        dj_circuit.measure(i,i)
        
    return dj_circuit
"""
def test_circuit(n=4):
    test_Qcircuit=QuantumCircuit(n+1,n)
    test_Qcircuit.x(n)
    test_Qcircuit.h(n)
    for qubit in range(n):
        test_Qcircuit.h(qubit)
    oracle=dj_oracle('balanced',n)
    test_Qcircuit.append(oracle, range(n+1))
    for i in range(n):
        test_Qcircuit.h(i)
        test_Qcircuit.measure(i,i)
    return test_Qcircuit
"""    
    

n=4
backend=BasicAer.get_backend('qasm_simulator')
shots=1024
dj_circuit=dj_algorithm(n, 'constant')
dj_circuit.draw(output='mpl')
#results=execute(dj_circuit, backend=backend, shots=shots).result()
#test=test_circuit()
#test.draw(output='mpl')
results=execute(dj_circuit, backend=backend, shots=shots).result()
"""
backend=least_busy(provider.backends(filters=lambda x: x.configuration().n_qubits>=(n+1) and
                                     not x.configuration().simulator and x.status().operational==True))

#%qiskit_job_watcher
print("Least busy backend: ", backend)
dj_circuit=dj_algorithm(n,'constant')
job=execute(dj_circuit, backend=backend, shots=shots, optimizer_level=3)
results=job.result()
"""
answer=results.get_counts()

plot_histogram(answer)