def noisy_PauliX(wire, lmbda):
    """A Pauli-X gate followed by depolarizing noise.

    Args:
        lmbda (float): The parameter defining the depolarizing channel.
        wire (int): The wire the depolarizing channel acts on.
    """
    qml.PauliX(wire)
    qml.DepolarizingChannel(lmbda, wires=wire)

def Toffoli_cascade(in_wires, aux_wires, lmbda):
    """A cascade of noisy Toffolis to help compute the product.
    
    Args:
        in_wires (list(int)): The input qubits.
        aux_wires (list(int)): The auxiliary qubits.
        lmbda (float): The probability of erasing the state of a qubit.
    """
    n = len(in_wires)
    qml.Toffoli(wires=[in_wires[0], in_wires[1], aux_wires[0]])
    qml.DepolarizingChannel(lmbda, wires=in_wires[0])
    qml.DepolarizingChannel(lmbda, wires=in_wires[1])
    qml.DepolarizingChannel(lmbda, wires=aux_wires[0])
    for i in range(n - 2):
        qml.Toffoli(wires=[in_wires[i + 2], aux_wires[i], aux_wires[i + 1]])
        qml.DepolarizingChannel(lmbda, wires=in_wires[i + 2])
        qml.DepolarizingChannel(lmbda, wires=aux_wires[i])
        qml.DepolarizingChannel(lmbda, wires=aux_wires[i + 1])

# Build a quantum radar to check how much attention is on Trine's cell
def cascadar(guard_state, lmbda):
    """Return the squared amplitude |g_c|^2 of the guard state, for c = (1, 1, 0, 0, 1).

    Args:
        guard_state (numpy.tensor): A 2**5 = 32 component vector encoding the guard state.
        lmbda (float): The probability of erasing the state of a qubit.

    Returns:
        (float): The squared amplitude of the guard state on the cell c.
    """
    dev = qml.device("default.mixed", wires = 5 + 4)
    
    @qml.qnode(dev)
    def circuit():
        """
        Circuit that will use the Toffoli_cascade and the noisy_PauliX.
        It will return a measurement on the last qubit.
        """

        qml.QubitStateVector(guard_state, range(5))



        noisy_PauliX(2, lmbda=lmbda)
        noisy_PauliX(3, lmbda=lmbda)

        Toffoli_cascade(in_wires=[0, 1, 2, 3, 4], aux_wires=[5, 6, 7, 8], lmbda=lmbda)
 
        return qml.probs(wires=8)

    output = circuit()
    #print(output[1])
    # if you want to post-process the output, put code here also #

    return output[1]



# These functions are responsible for testing the solution.
def run(test_case_input: str) -> str:

    guard_state, lmbda = json.loads(test_case_input)
    output = cascadar(guard_state, lmbda)

    return str(output)

def check(solution_output: str, expected_output: str) -> None:

    solution_output = json.loads(solution_output)
    expected_output = json.loads(expected_output)
    assert np.allclose(
        solution_output, expected_output, rtol=1e-4
    ), "Your quantum radar isn't quite working properly!"




