def half_life(gamma, p):
    """Calculates the relaxation half-life of a quantum system that exchanges energy with its environment.
    This process is modeled via Generalized Amplitude Damping.

    Args:
        gamma (float): 
            The probability per unit time of the system losing a quantum of energy
            to the environment.
        p (float): The de-excitation probability due to environmental effect

    Returns:
        (float): The relaxation haf-life of the system, as explained in the problem statement.
    """

    num_wires = 1

    dev = qml.device("default.mixed", wires=num_wires)

    # Feel free to write helper functions or global variables here

    @qml.qnode(dev)
    def noise(
        gamma, T # add optional parameters, delete if you don't need any
    ):
        """Implement the sequence of Generalized Amplitude Damping channels in this QNode
        You may pass instead of return if you solved this problem analytically, it's possible!

        Args:
            gamma (float): The probability per unit time of the system losing a quantum of energy
            to the environment.
        
        Returns:
            (float): The relaxation half-life.
        """
        # Don't forget to initialize the state
        # Put your code here #
        qml.Hadamard(wires=0)

        dt = T / 50
        for i in range(50):
            qml.GeneralizedAmplitudeDamping(gamma * dt, p, wires=0)
        return qml.probs(wires=0)

    l = 0
    r = 100
    res = 0
    for i in range(100):
        m = (l + r) / 2
 
        if noise(gamma, m)[1] >= 0.25:
            res = m
            l = m + 1
        else:
            r = m - 1
    # Write any subroutines you may need to find the relaxation time here
    #print(noise(gamma, m), m)

    return res
    # Return the relaxation half-life


# These functions are responsible for testing the solution.
def run(test_case_input: str) -> str:

    ins = json.loads(test_case_input)
    output = half_life(*ins)

    return str(output)

def check(solution_output: str, expected_output: str) -> None:
    solution_output = json.loads(solution_output)
    expected_output = json.loads(expected_output)
    assert np.allclose(
        solution_output, expected_output, atol=2e-1
    ), "The relaxation half-life is not quite right."



