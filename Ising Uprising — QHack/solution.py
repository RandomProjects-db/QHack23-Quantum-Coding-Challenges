def create_Hamiltonian(h):
    """
    Function in charge of generating the Hamiltonian of the statement.

    Args:
        h (float): magnetic field strength

    Returns:
        (qml.Hamiltonian): Hamiltonian of the statement associated to h
    """


    obs = []
    coeffs = []

    for i in range(4):
        obs.append(qml.PauliX(i))
        coeffs.append(-h)

        obs.append(qml.PauliZ(i) @ qml.PauliZ((i+1)%4))
        coeffs.append(-1)
    # Combine Hamiltonian terms
    
    #print(H)
    
    #return H
    #print("Hamiltonian terms:", qml.Hamiltonian(coeffs, obs))
    return qml.Hamiltonian(coeffs, obs)


dev = qml.device("default.qubit", wires=4)

@qml.qnode(dev)
def model(params, H):
    """
    To implement VQE you need an ansatz for the candidate ground state!
    Define here the VQE ansatz in terms of some parameters (params) that
    create the candidate ground state. These parameters will
    be optimized later.

    Args:
        params (numpy.array): parameters to be used in the variational circuit
        H (qml.Hamiltonian): Hamiltonian used to calculate the expected value

    Returns:
        (float): Expected value with respect to the Hamiltonian H
    """



    qml.Rot(*params[0], wires=0)
    qml.Rot(*params[1], wires=1)
    qml.Rot(*params[2], wires=2)
    qml.Rot(*params[3], wires=3)
    return qml.expval(H)




def train(h):
    """
    In this function you must design a subroutine that returns the
    parameters that best approximate the ground state.

    Args:
        h (float): magnetic field strength

    Returns:
        (numpy.array): parameters that best approximate the ground state.
    """


    H = create_Hamiltonian(h)

    def cost(params):
        return model(params, H)

    opt = qml.GradientDescentOptimizer(stepsize=0.4)
    params = np.zeros((4, 3))

    energy = 0
    steps = 100
    for i in range(steps):
        params, H_evol = opt.step_and_cost(cost, params)
        energy += H_evol
        #if (i + 1) % 20 == 0:
            #print(f"Step {i + 1}, Energy: {H_evol}")

    #print("Final energy:", model(params, H))
    #print(f"Total energy: {energy}")
    return params


# These functions are responsible for testing the solution.
def run(test_case_input: str) -> str:
    ins = json.loads(test_case_input)
    params = train(ins)
    return str(model(params, create_Hamiltonian(ins)))


def check(solution_output: str, expected_output: str) -> None:
    solution_output = json.loads(solution_output)
    expected_output = json.loads(expected_output)
    assert np.allclose(
        solution_output, expected_output, rtol=1e-1
    ), "The expected value is not correct."



