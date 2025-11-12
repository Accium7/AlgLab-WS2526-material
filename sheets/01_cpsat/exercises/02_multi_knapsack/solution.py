import math
from typing import List

from data_schema import Instance, Item, Solution
from ortools.sat.python.cp_model import FEASIBLE, OPTIMAL, CpModel, CpSolver


class MultiKnapsackSolver:
    """
    This class can be used to solve the Multi-Knapsack problem
    (also the standard knapsack problem, if only one capacity is used).

    Attributes:
    - instance (Instance): The multi-knapsack instance
        - items (List[Item]): a list of Item objects representing the items to be packed.
        - capacities (List[int]): a list of integers representing the capacities of the knapsacks.
    - model (CpModel): a CpModel object representing the constraint programming model.
    - solver (CpSolver): a CpSolver object representing the constraint programming solver.
    """

    def __init__(self, instance: Instance, activate_toxic: bool = True):
        """
        Initialize the solver with the given Multi-Knapsack instance.

        Args:
        - instance (Instance): an Instance object representing the Multi-Knapsack instance.
        """
        self.items = instance.items
        self.activate_toxic = activate_toxic
        self.capacities = instance.capacities
        self.model = CpModel()
        self.solver = CpSolver()
        self.solver.parameters.log_search_progress = True
        # TODO: Implement me!
        self.x = [
            [self.model.new_bool_var(f"x[{i}_{j}]")
            for j in range(len(self.capacities))]
            for i in range(len(self.items))
        ]

        self.y = [self.model.new_bool_var(f"y[{j}]") for j in range(len(self.capacities))]

        for j in range(len(self.capacities)):
            self.model.add(sum(self.x[i][j] * self.items[i].weight for i in range(len(self.items))) <= self.capacities[j])

        for i in range(len(self.items)):
            self.model.add_at_most_one(self.x[i][j] for j in range(len(self.capacities)))

        for i in range(len(self.items)):
            for j in range(len(self.capacities)):
                if self.items[i].toxic:
                    self.model.add_implication(self.x[i][j], self.y[j])
                else:
                    self.model.add_implication(self.y[j], ~self.x[i][j])



        accumulated_value = sum(self.x[i][j]  * self.items[i].value for i in range(len(self.items)) for j in range(len(self.capacities)))

        self.model.maximize(accumulated_value)






    def solve(self, timelimit: float = math.inf) -> Solution:
        """
        Solve the Multi-Knapsack instance with the given time limit.

        Args:
        - timelimit (float): time limit in seconds for the cp-sat solver.

        Returns:
        - Solution: a list of lists of Item objects representing the items packed in each knapsack
        """
        # handle given time limit
        if timelimit <= 0.0:
            return Solution(trucks=[])  # empty solution
        if timelimit < math.inf:
            self.solver.parameters.max_time_in_seconds = timelimit
        # TODO: Implement me!
        status = self.solver.solve(self.model)
        assert status == OPTIMAL or status == FEASIBLE


        trucks = [[] for _ in range(len(self.capacities))]
        for i in range(len(self.items)):
            for j in range(len(self.capacities)):
                if self.solver.boolean_value(self.x[i][j]):
                    trucks[j].append(self.items[i])
        return Solution(trucks=trucks)
        #return Solution(trucks=[])  # empty solution
