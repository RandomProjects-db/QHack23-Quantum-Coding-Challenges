# Put your code here #
dev = qml.device("default.qubit", wires=2)
# Create a default.qubit device with 2 qubits / wires using qml.device

# Turn your circuit into a QNode
@qml.qnode(dev)

def circuit(angles):
    """The quantum circuit that you will simulate.

    Args:
        angles (list(float)): The gate angles in the circuit.

    Returns:
        (numpy.tensor): 
            The probability vector of the underlying quantum state that this circuit produces.
    """
    # Put the rotation gates here
    qml.RY(angles[0], wires=0)
    qml.RY(angles[1], wires=1)
    return qml.probs(wires=[0, 1])


# These functions are responsible for testing the solution. 
def run(test_case_input: str) -> str:
    angles = json.loads(test_case_input)
    output = circuit(angles).tolist()

    return str(output)

def check(solution_output: str, expected_output: str) -> None:
    solution_output = json.loads(solution_output)
    expected_output = json.loads(expected_output)
    assert np.allclose(solution_output, expected_output, rtol=1e-4)
