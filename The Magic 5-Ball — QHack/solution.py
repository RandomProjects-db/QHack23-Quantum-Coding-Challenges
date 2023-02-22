def noisy_Hadamard(lmbda, wire):
    """A Hadamard gate with depolarizing noise on either side.
    
    Args:
        lmbda (float): The parameter defining the depolarizing channel.
        wire (int): The wire the depolarizing channel acts on.
    """
    qml.DepolarizingChannel(lmbda, wires=wire)
    qml.Hadamard(wire)
    qml.DepolarizingChannel(lmbda, wires=wire)

# Oracle matrix for Doc Trine's cell number

flips = [1, 3, 5, 7, 8, 10, 12, 14, 16, 18, 20, 22, 25, 27, 29, 31]

oracle_matrix = np.eye(2**5)
for i in flips:
    oracle_matrix[i, i] = -1

# Implement the Bernstein-Vazirani algorithm with depolarizing noise

dev = qml.device("default.mixed", wires = 5)
@qml.qnode(dev)
def noisy_BernsteinVazirani(lmbda):
    """Runs the Bernstein-Vazirani algorithm with depolarizing noise.

    Args:
        lmbda (float): The probability of erasing the state of a qubit.

    Returns:
        (list(float)): Expectation values for PauliZ on all n wires.
    """

    noisy_Hadamard(lmbda, 0)
    noisy_Hadamard(lmbda, 1)
    noisy_Hadamard(lmbda, 2)
    noisy_Hadamard(lmbda, 3)
    noisy_Hadamard(lmbda, 4)
    
    qml.QubitUnitary(oracle_matrix, wires = range(5))
    
    noisy_Hadamard(lmbda, 0)
    noisy_Hadamard(lmbda, 1)
    noisy_Hadamard(lmbda, 2)
    noisy_Hadamard(lmbda, 3)
    noisy_Hadamard(lmbda, 4)


    return [qml.expval(qml.PauliZ(i)) for i in range(5)]
        



# These functions are responsible for testing the solution.
def run(test_case_input: str) -> str:

    lmbda = json.loads(test_case_input)
    output = noisy_BernsteinVazirani(lmbda).tolist()

    return str(output)

def check(solution_output: str, expected_output: str) -> None:
    
    solution_output = json.loads(solution_output)
    expected_output = json.loads(expected_output)
    assert np.allclose(
        solution_output, expected_output, rtol=1e-4
    ), "Your noisy Bernstein-Vazirani algorithm isn't giving the right answers!"



