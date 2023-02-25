import json
import pennylane as qml
import pennylane.numpy as np
import scipy

def abs_dist(rho, sigma):
    """A function to compute the absolute value |rho - sigma|."""
    polar = scipy.linalg.polar(rho - sigma)
    return polar[1]

def word_dist(word):
    """A function which counts the non-identity operators in a Pauli word"""
    return sum(word[i] != "I" for i in range(len(word)))


# Produce the Pauli density for a given Pauli word and apply noise

def noisy_Pauli_density(word, lmbda):
    """
       A subcircuit which prepares a density matrix (I + P)/2**n for a given Pauli
       word P, and applies depolarizing noise to each qubit. Nothing is returned.

    Args:
            word (str): A Pauli word represented as a string with characters I, X, Y and Z.
            lmbda (float): The probability of replacing a qubit with something random.
    """
   # Put your code here #
    den = 1
    num_wires = len(word)
    for j,i in enumerate(word):
        if i == 'X' and j == 0:
            den = qml.PauliX(j)
        elif i == 'Y' and j == 0:
            den = qml.PauliY(j)
        elif i == 'Z' and j == 0:
            den = qml.PauliZ(j)
        elif i == 'I' and j == 0:
            den = qml.Identity(0)
        elif i == 'X':
            den = den@qml.PauliX(j)
        elif i == 'Y':
            den = den@qml.PauliY(j)
        elif i == 'Z':
            den = den@qml.PauliZ(j)
        elif i == 'I':
            den = den@qml.Identity(j)
    den = (qml.pauli.pauli_word_to_matrix(den) + np.eye(2**num_wires))/(2**num_wires)
    
    dev = qml.device('default.mixed',wires = num_wires)
    @qml.qnode(dev)
    def circuit(word,lmbda):
        qml.QubitDensityMatrix(den,wires=range(num_wires))
        for i in range(num_wires):
            qml.DepolarizingChannel(lmbda,i)
        return qml.density_matrix(range(num_wires))
    #print(qml.drawer.draw(circuit,max_length=200)(word,lmbda))
    return circuit(word,lmbda)


# Compute the trace distance from a noisy Pauli density to the maximally mixed density
def maxmix_trace_dist(word, lmbda):
    """
       A function compute the trace distance between a noisy density matrix, specified
       by a Pauli word, and the maximally mixed matrix.

    Args:
            word (str): A Pauli word represented as a string with characters I, X, Y and Z.
            lmbda (float): The probability of replacing a qubit with something random.

    Returns:
            float: The trace distance between two matrices encoding Pauli words.
    """
    num_wires = len(word)

    noisy_den = noisy_Pauli_density(word,lmbda)
    max_ent = np.eye(2**num_wires)*1/(2**num_wires)

    trace_distance = 0.5*(np.trace(abs_dist(noisy_den,max_ent)))
    return trace_distance



def bound_verifier(word, lmbda):
    """
       A simple check function which verifies the trace distance from a noisy Pauli density
       to the maximally mixed matrix is bounded by (1 - lambda)^|P|.

    Args:
            word (str): A Pauli word represented as a string with characters I, X, Y and Z.
            lmbda (float): The probability of replacing a qubit with something random.

    Returns:
            float: The difference between (1 - lambda)^|P| and T(rho_P(lambda), rho_0).
    """
    bound = np.power((1-lmbda),word_dist(word))

    diff = bound - maxmix_trace_dist(word,lmbda) 

    return  diff



# These functions are responsible for testing the solution.
def run(test_case_input: str) -> str:

    word, lmbda = json.loads(test_case_input)
    output = np.real(bound_verifier(word, lmbda))

    return str(output)


def check(solution_output: str, expected_output: str) -> None:

    solution_output = json.loads(solution_output)
    expected_output = json.loads(expected_output)
    assert np.allclose(
        solution_output, expected_output, rtol=1e-4
    ), "Your trace distance isn't quite right!" 
    
    



test_cases = [['["XXI", 0.7]', '0.0877777777777777'], ['["XXIZ", 0.1]', '0.4035185185185055'], ['["YIZ", 0.3]', '0.30999999999999284'], ['["ZZZZZZZXXX", 0.1]', '0.22914458207245006']]


for i, (input_, expected_output) in enumerate(test_cases):
    print(f"Running test case {i} with input '{input_}'...")

    try:
        output = run(input_)

    except Exception as exc:
        print(f"Runtime Error. {exc}")

    else:
        if message := check(output, expected_output):
            print(f"Wrong Answer. Have: '{output}'. Want: '{expected_output}'.")

        else:
            print("Correct!")
