# Welcome to the QHack 2023 coding challenges!
def add_numbers(x, y):
    """This function adds two numbers together.

    Args:
        x (float): A number.
        y (float): A number.

    Returns:
        (float): The result of adding x and y.
    """
    return(x+y)

# These functions are responsible for testing the solution.

def run(test_case_input: str) -> str:
    x, y = json.loads(test_case_input)
    result = add_numbers(x, y)
    return str(result)

def check(solution_output: str, expected_output: str) -> None:
    solution_output = json.loads(solution_output)
    expected_output = json.loads(expected_output)
    assert np.allclose(
        solution_output, expected_output, rtol=1e-4
    ), "Your addition function isn't quite right!"
