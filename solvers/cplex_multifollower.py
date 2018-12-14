
import cplex


class CplexMultifollower:
    # Benders options:
    # 0 - No decomposition
    # 1 - Decomposition in different subproblems, one for each solver
    # 2 - Single decomposition, all the followers together
    # 3 - Automatic CPLEX decomposition
    benders = 0
    name = "CplexMultifollower"

    def setname(self, name):
        self.name = name

    def setbenders(self, benders):
        self.benders = benders

    def solve(self, datafile):
        """Solve capacitated facility location problem."""
        # Read in data file. If no file name is given on the command line
        # we use a default file name. The data we read is
        # fixedcost  -- a list/array of facility fixed cost
        # cost       -- a matrix for the costs to serve each client by each
        #               facility
        # capacity   -- a list/array of facility capacity
        n, k, m, r0, start_path, end_path, edge_start, edge_end, length_, cost, r = read_dat_file(datafile+".dat")
        num_paths = len(start_path)
        num_edges = len(edge_end)

        # Create the modeler/solver.
        cpx = cplex.Cplex()
        cpx.set_log_stream(None)
        cpx.set_error_stream(None)
        cpx.set_warning_stream(None)
        cpx.set_results_stream(None)
        cpx.parameters.threads.set(4)
        # Create variables. We have variables
        # x[i]              if arc i is interdicted
        # pi[j][k]          minimum distance of j from the source of path k
        x = list(cpx.variables.add(obj=[0.0] * num_edges,
                                   lb=[0.0] * num_edges,
                                   ub=[1.0] * num_edges,
                                   types=["B"] * num_edges))

        pi = [None] * n
        for i in range(n):
            objs = [0.0] * num_paths
            lbs = [0.0] * num_paths
            ubs = [k] * num_paths
            for j in range(num_paths):
                if end_path[j] == i:
                    objs[j] = 1.0
                if start_path[j] == i:
                    ubs[j] = 0.0
            pi[i] = cpx.variables.add(obj=objs, lb=lbs, ub=ubs)

        # Objective: Maximize the sum of all the followers shortest paths.
        cpx.objective.set_sense(cpx.objective.sense.maximize)

        # Constraint: The interdicted edges cost can not exceed the budget of the leader
        cpx.linear_constraints.add(
            lin_expr=[cplex.SparsePair(
                ind=x, val=r)],
            senses=["L"],
            rhs=[r0])

        # Constraint: Dual of the flow model for each follower
        for i in range(num_paths):
            for j in range(num_edges):
                if edge_end[j] != start_path[i]:
                    cpx.linear_constraints.add(
                        lin_expr=[cplex.SparsePair(
                            ind=[pi[edge_end[j]][i], pi[edge_start[j]][i], x[j]], val=[1.0, -1.0, -r[j]])],
                        senses=["L"],
                        rhs=[length_[j]])

        # Type of Benders decomposition required
        if self.benders == 1:
            mastervalue = cpx.long_annotations.benders_mastervalue
            idx = cpx.long_annotations.add(
                name=cpx.long_annotations.benders_annotation,
                defval=mastervalue)
            objtype = cpx.long_annotations.object_type.variable
            for i in range(num_paths):
                cpx.long_annotations.set_values(idx, objtype,
                                                [(pi[x][i], mastervalue+1+i)
                                                 for x in range(n)])
        if self.benders == 2:
            mastervalue = cpx.long_annotations.benders_mastervalue
            idx = cpx.long_annotations.add(
                name=cpx.long_annotations.benders_annotation,
                defval=mastervalue)
            objtype = cpx.long_annotations.object_type.variable
            for i in range(num_paths):
                cpx.long_annotations.set_values(idx, objtype,
                                                [(pi[x][i], mastervalue+1)
                                                 for x in range(n)])
        elif self.benders == 3:
            cpx.parameters.benders.strategy.set(
                cpx.parameters.benders.strategy.values.full)

        cpx.solve()
        print("Solution status =", cpx.solution.get_status_string())
        print("Optimal value:", cpx.solution.get_objective_value())
        tol = cpx.parameters.mip.tolerances.integrality.get()
        values = cpx.solution.get_values()
        # for x in range(num_paths):
        #     print("   Path " + str(x+1) + " has length " + str(values[pi[end_path[x]][x]]))

        print("\n")


def get_words(line):
    """Return a list of the tokens in line."""
    line = line.replace("\t", " ")
    line = line.replace("\v", " ")
    line = line.replace("\r", " ")
    line = line.replace("\n", " ")
    while line.count("  "):
        line = line.replace("  ", " ")
    line = line.strip()
    return [word + " " for word in line.split(" ")]


def read_dat_file(filename):
    """Return a list containing the data stored in the dat file.

    Single integers or floats are stored as their natural type.

    1-d arrays are stored as lists

    2-d arrays are stored as lists of lists.

    NOTE: the 2-d arrays are not in the list-of-lists matrix format
    that the python methods take as input for constraints.

    """
    ret = []
    continuation = False
    with open(filename) as f:
        for line in f:
            for word in get_words(line):
                if continuation:
                    entity = "".join([entity, word])
                else:
                    entity = word
                try:
                    ret.append(eval(entity))
                    continuation = False
                except SyntaxError:
                    continuation = True
    return ret
