import subprocess as sp


class MinizincCaller:
    model_name = ""
    solver = ""
    minizinc_path = "/"
    parameters = ""
    name = "Minizinc"

    def setname(self, name):
        self.name = name

    def setmodel(self, model_name):
        self.model_name = model_name

    def setminizinc(self, minizinc_path):
        self.minizinc_path = minizinc_path

    def setsolver(self, solver):
        self.solver = solver

    def setparameters(self, parameters):
        self.parameters = parameters

    def solve(self, datafile):
        """Solve capacitated facility location problem."""
        proc = sp.Popen(self.minizinc_path + "minizinc --solver " + self.solver + " " + self.model_name +
                        " " +
                        datafile + ".dzn " + self.parameters,
                        shell=True,
                        stdout=sp.PIPE
                        )
        print(proc.communicate()[0])


