
from ortools.sat.python import cp_model



class ORToolsSatMultifollower:

    name = "ORToolsSatMultifollower"

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
        model = cp_model.CpModel()
        # Create variables. We have variables
        # x[i]              if arc i is interdicted
        # pi[j][k]          minimum distance of j from the source of path k
        x = [model.NewBoolVar('x[%i]' % i)
             for i in range(num_edges)]
        pi = [[model.NewIntVar(0, k, 'pi[%i,%i]' % (i, j))
               for j in range(num_paths)]
              for i in range(n)]

        # Objective: Maximize the sum of all the followers shortest paths.

        model.Maximize(sum(pi[start_path[j]][j] for j in range(num_paths)))

        # Constraint: The interdicted edges cost can not exceed the budget of the leader
        for i in range(n):
            for j in range(num_paths):
                if i == end_path[j]:
                    model.Add(pi[i][j] == 0)
                else:
                    temp = []
                    for e in range(num_edges):
                        if edge_start[e] == i:
                            t = model.NewIntVar(0, k, " ")
                            model.Add(t == pi[edge_end[e]][j] + length_[e] + x[e] * r[e])
                            temp.append(t)
                    model.AddMinEquality(pi[i][j], temp)
        model.Add(r0 >= sum(x[e] * r[e] for e in range(num_edges)))
        solver = cp_model.CpSolver()
        status = solver.Solve(model)

        if status == cp_model.OPTIMAL:
            print('Total cost = %i' % solver.ObjectiveValue())
            print()
            for i in range(num_paths):
                print('Paths ', i, ' length ', solver.Value(pi[start_path[i]][i]))

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
