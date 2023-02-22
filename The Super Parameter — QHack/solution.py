dev = qml.device("default.qubit", wires=3)


@qml.qnode(dev)
def model(alpha):
    """In this qnode you will define your model in such a way that there is a single 
    parameter alpha which returns each of the basic states.

    Args:
        alpha (float): The only parameter of the model.

    Returns:
        (numpy.tensor): The probability vector of the resulting quantum state.
    """
    angles = [0] * 3

    if(alpha < 0):
        angles[0] += alpha
    else:
        
        alpha2 = int(alpha) + 1
        rest = alpha - int(alpha)
        alpha = int(alpha)

        for i in range(3):

            if (1 << i) & alpha and not ((1 << i) & alpha2):
                angles[i] = (1 - rest)
            elif not ((1 << i) & alpha) and ((1 << i) & alpha2):
                angles[i] = rest
            else:
                if (1 << i) & alpha:
                    angles[i] = 1
                else:
                    angles[i] = 0

    qml.RX(np.pi * angles[2], wires=0)
    qml.RX(np.pi * angles[1], wires=1)
    qml.RX(np.pi * angles[0], wires=2)
    return qml.probs(wires=range(3))

def generate_coefficients():
    """This function must return a list of 8 different values of the parameter that
    generate the states 000, 001, 010, ..., 111, respectively, with your ansatz.

    Returns:
        (list(int)): A list of eight real numbers.
    """
    return range(8)



# These functions are responsible for testing the solution.
def run(test_case_input: str) -> str:
    return None

def check(solution_output, expected_output: str) -> None:
    coefs = generate_coefficients()
    output = np.array([model(c) for c in coefs])
    epsilon = 0.001

    for i in range(len(coefs)):
        assert np.isclose(output[i][i], 1)

    def is_continuous(function, point):
        limit = calculate_limit(function, point)

        if limit is not None and sum(abs(limit - function(point))) < epsilon:
            return True
        else:
            return False

    def is_continuous_in_interval(function, interval):
        for point in interval:
            if not is_continuous(function, point):
                return False
        return True

    def calculate_limit(function, point):
        x_values = [point - epsilon, point, point + epsilon]
        y_values = [function(x) for x in x_values]
        average = sum(y_values) / len(y_values)

        return average

    assert is_continuous_in_interval(model, np.arange(0,10,0.001))

    for coef in coefs:
        assert coef >= 0 and coef <= 10



