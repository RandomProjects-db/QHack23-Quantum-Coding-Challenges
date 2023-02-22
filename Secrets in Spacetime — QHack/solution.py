def U_psi(theta):
    """
    Quantum function that generates |psi>, Zenda's state wants to send to Reece.

    Args:
        theta (float): Parameter that generates the state.

    """
    qml.Hadamard(wires = 0)
    qml.CRX(theta, wires = [0,1])
    qml.CRZ(theta, wires = [0,1])

def is_unsafe(alpha, beta, epsilon):
    """
    Boolean function that we will use to know if a set of parameters is unsafe.

    Args:
        alpha (float): parameter used to encode the state.
        beta (float): parameter used to encode the state.
        epsilon (float): unsafe-tolerance.

    Returns:
        (bool): 'True' if alpha and beta are epsilon-unsafe coefficients. 'False' in the other case.

    """

    dev = qml.device("default.qubit", wires=2)

    @qml.qnode(dev)
    def circuit(alpha, beta, theta):

        U_psi(theta)
        qml.RZ(alpha, wires=0)
        qml.RZ(alpha, wires=1)
        qml.RX(beta, wires=0)
        qml.RX(beta, wires=1)

        
        qml.adjoint(qml.CRZ)(theta, wires = [0,1])
        qml.adjoint(qml.CRX)(theta, wires = [0,1])
        qml.Hadamard(wires=0)

        return qml.probs(wires=[0,1])



    for theta in np.arange(2*np.pi, 4*np.pi, 0.01):
        #print(circuit(alpha, beta, theta))
        if abs(circuit(alpha, beta, theta)[0]) >=  1-epsilon:
            #print(circuit(alpha, beta, theta))
            return True

    return False

        

# These functions are responsible for testing the solution.
def run(test_case_input: str) -> str:
    ins = json.loads(test_case_input)
    output = is_unsafe(*ins)
    return str(output)

def check(solution_output: str, expected_output: str) -> None:
    
    def bool_to_int(string):
        if string == "True":
            return 1
        return 0

    solution_output = bool_to_int(solution_output)
    expected_output = bool_to_int(expected_output)
    assert solution_output == expected_output, "The solution is not correct."



