from data_schema import Instance, Solution
from ortools.sat.python import cp_model


def solve(instance: Instance) -> Solution:
    """
    Implement your solver for the problem here!
    """
    numbers = instance.numbers
    model = cp_model.CpModel()

    x = max(numbers)
    y = min(numbers)

    model.add(x - y >= 0)
    model.maximize(x - y)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)


    return Solution(
        number_a = x,
        number_b = y,
        distance = abs(x - y),
    )
