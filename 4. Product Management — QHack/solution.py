def is_product(state, subsystem, wires):
    """Determines if a pure quantum state can be written as a product state between 
    a subsystem of wires and their compliment.

    Args:
        state (numpy.array): The quantum state of interest.
        subsystem (list(int)): The subsystem used to determine if the state is a product state.
        wires (list(int)): The wire/qubit labels for the state. Use these for creating a QNode if you wish!

    Returns:
        (str): "yes" if the state is a product state or "no" if it isn't.
    """


    dev = qml.device("default.qubit", wires=len(wires))
    cwires = []
    for wire in wires:
        if wire not in subsystem:
            cwires.append(wire)

    @qml.qnode(dev)
    def circuit():
        qml.QubitStateVector(state, wires)

        return qml.density_matrix(wires=subsystem)


    if np.linalg.matrix_rank(circuit()) == 1:
        return "yes"
    else:
        return "no"



# These functions are responsible for testing the solution.
def run(test_case_input: str) -> str:
    ins = json.loads(test_case_input)
    state, subsystem, wires = ins
    state = np.array(state)
    output = is_product(state, subsystem, wires)
    return output

def check(solution_output: str, expected_output: str) -> None:
    assert solution_output == expected_output


