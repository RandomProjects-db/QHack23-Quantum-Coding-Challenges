dev = qml.device("default.qubit", wires=["hour", "minute"])

@qml.qnode(dev)
def time(hour, minute):
    """Generates the quantum state associated with the time passed as argument.

    Args:
        hour (int): Hour associated with the requested time
        minute (int): Minutes associated with the requested time

    Returns:
        (numpy.tensor): Probabilities associated with the state created.
    """
    # Put your code here #

    angle_h = hour / 12 * (2*np.pi)
    angle_m = minute / 60 * (2*np.pi)

    qml.RY(angle_h, wires="hour")
    qml.RY(angle_m, wires="minute")
    
    return qml.probs(wires=["hour", "minute"])


# These functions are responsible for testing the solution.
def run(test_case_input: str) -> str:
    hour, minute = json.loads(test_case_input)
    state = [float(x) for x in time(hour, minute)]
    return str(state)

def check(solution_output, expected_output: str) -> None:

    solution_output = json.loads(solution_output)
    expected_output = json.loads(expected_output)

    assert np.allclose(
        solution_output, expected_output, atol=0.1
    ), "The solution does not seem to be correct."



