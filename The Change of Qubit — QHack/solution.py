def circuit_left():
    """
    This function corresponds to the circuit on the left-hand side of the diagram in the 
    description. Simply place the necessary operations, you do not have to return anything.
    """
    pass

def circuit_right():
    """
    This function corresponds to the circuit on the right-hand side of the diagram in the 
    description. Simply place the necessary operations, you do not have to return anything.
    """
    U = np.array([[1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])

    #qml.PauliX(wires=1)
    #qml.PauliX(wires=2)
    #qml.Toffoli(wires=[2,1,0])
    #qml.PauliX(wires=2)
    #qml.PauliX(wires=1)

    qml.CNOT(wires=[2,1])
    qml.PauliX(wires=1)
    qml.CNOT(wires=[1,0])
    qml.adjoint(qml.PauliX)(wires=1)
    qml.CNOT(wires=[2,1])

    # apply U
    qml.QubitUnitary(U, wires=[1, 2])

   
    
    

    #qml.adjoint(qml.MultiControlledX)(wires=[1,2,0], control_values="00")

    # Entanglement
    qml.Hadamard(wires=1)
    qml.CNOT(wires=[1,2])

    # Basis change to Bell
    qml.CNOT(wires=[0,1])
    qml.Hadamard(wires=0)  

    # Error correction
    qml.CNOT(wires=[1,2])
    #qml.CZ(wires=[0,2])
    
    qml.CZ(wires=[1,2])
    qml.CNOT(wires=[0,1])
    qml.CZ(wires=[1,2])
    qml.adjoint(qml.CNOT)(wires=[0,1])


def U():
    """This operator generates a PauliX gate on a random qubit"""
    qml.PauliX(wires=np.random.randint(3))


dev = qml.device("default.qubit", wires=3)

@qml.qnode(dev)
def circuit(alpha, beta, gamma):
    """Total circuit joining each block.

    Args: 
        alpha (float): The first parameter of a U3 gate.
        beta (float):The second parameter of a U3 gate. 
        gamma (float): The third parameter of a U3 gate. 
    
    Returns:
        (float): The expectation value of an observable.
    """
    qml.U3(alpha, beta, gamma, wires=0)
    circuit_left()
    U()
    circuit_right()

    # Here we are returning the expected value with respect to any observable,
    # the choice of observable is not important in this exercise.

    return qml.expval(0.5 * qml.PauliZ(2) - qml.PauliY(2))


# These functions are responsible for testing the solution.
def run(test_case_input: str) -> str:
    angles = json.loads(test_case_input)
    output = circuit(*angles)
    return str(output)

def check(solution_output: str, expected_output: str) -> None:

    solution_output = json.loads(solution_output)
    expected_output = json.loads(expected_output)
    assert np.allclose(
        solution_output, expected_output, atol=2e-1
    ), "The expected output is not quite right."

    ops = circuit.tape.operations

    for op in ops:
        assert not (0 in op.wires and 2 in op.wires), "Invalid connection between qubits."

    assert circuit.tape.observables[0].wires == qml.wires.Wires(2), "Measurement on wrong qubit."



