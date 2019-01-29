import subprocess as sp


class MinizincCaller:
    model_name = ""
    solver = ""
    minizinc_path = "/"
    parameters = ""
    name = "Minizinc"
    datatype = ""
    output = ""

    def setname(self, name):
        self.name = name

    def setmodel(self, model_name):
        self.model_name = model_name

    def setminizinc(self, minizinc_path):
        self.minizinc_path = minizinc_path

    def setsolver(self, solver):
        self.solver = solver

    def setdatatype(self, datatype):
        self.datatype = datatype

    def setparameters(self, parameters):
        self.parameters = parameters

    def getoutput(self):
        return self.output

    def solve(self, datafile):
        proc = sp.Popen(self.minizinc_path + "minizinc --solver " + self.solver + " " + self.model_name +
                        " " +
                        datafile + self.datatype + ".dzn " + self.parameters,
                        shell=True,
                        stdout=sp.PIPE
                        )
        self.output = proc.communicate()[0]
        print(self.output)


