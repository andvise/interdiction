import time
import numpy as np
import instance
from solvers import minizinc_caller
from solvers import cplex_multifollower
from solvers import ortools_sat_multifollower
from solvers import ortools_cp_multifollower


problem = instance.InstanceCompetitors()
solvers = []

# models_directory = "/home/andrea/interdiction/models/"
models_directory = "/Users/avisentin/PycharmProjects/interdiction/models/"

sol = minizinc_caller.MinizincCaller()
sol.setminizinc("/Applications/MiniZincIDE.app/Contents/Resources/")
sol.setmodel(models_directory + "no_interdiction.mzn")
sol.setsolver("ORTools")
sol.setname("No interdiction")
solvers.append(sol)

sol = minizinc_caller.MinizincCaller()
sol.setminizinc("/Applications/MiniZincIDE.app/Contents/Resources/")
sol.setmodel(models_directory + "interdiction_competitors_balance.mzn")
sol.setsolver("ORTools")
sol.setdatatype("_flow")
sol.setname("Balance with ORTools")
solvers.append(sol)

sol = minizinc_caller.MinizincCaller()
sol.setminizinc("/Applications/MiniZincIDE.app/Contents/Resources/")
sol.setmodel(models_directory + "interdiction_competitors_balance.mzn")
sol.setsolver("CPLEX")
sol.setdatatype("_flow")
sol.setname("Balance with CPLEX")
solvers.append(sol)

sol = minizinc_caller.MinizincCaller()
sol.setminizinc("/Applications/MiniZincIDE.app/Contents/Resources/")
sol.setmodel(models_directory + "interdiction_competitors_balance_interdiction.mzn")
sol.setsolver("ORTools")
sol.setdatatype("_flow")
sol.setname("Balance interdiction with ORTools")
#solvers.append(sol)

sol = minizinc_caller.MinizincCaller()
sol.setminizinc("/Applications/MiniZincIDE.app/Contents/Resources/")
sol.setmodel(models_directory + "interdiction_competitors_balance_interdiction.mzn")
sol.setsolver("CPLEX")
sol.setdatatype("_flow")
sol.setname("Balance interdiction with CPLEX")
solvers.append(sol)

sol = minizinc_caller.MinizincCaller()
sol.setminizinc("/Applications/MiniZincIDE.app/Contents/Resources/")
sol.setmodel(models_directory + "interdiction_competitors_MIP.mzn")
sol.setsolver("ORTools")
sol.setname("Normal MIP with OR Tools")
solvers.append(sol)

sol = minizinc_caller.MinizincCaller()
sol.setminizinc("/Applications/MiniZincIDE.app/Contents/Resources/")
sol.setmodel(models_directory + "interdiction_competitors_MIP.mzn")
sol.setsolver("CPLEX")
sol.setname("Normal MIP with CPLEX")
solvers.append(sol)



num_sol = len(solvers)

r = [30]
num_r = len(r)
followers = 1
n = 10
m = 10
seeds = [1234, 1989, 290889]#, 251091, 240664, 190364, 120863, 101295, 31089, 3573113]
num_seeds = len(seeds)

problem.set_args(n,m , 100, 10, 10, 5, 20)
data_directory = "./data/"
output_name = "./test_competitors_" + str(n) + "_" + str(m) + ".csv"

res = np.zeros((num_r, num_sol, num_seeds))

s_time = time.time()

for k in range(0, num_r):
    problem.set_r0(r[k])
    for i in range(0, num_seeds):
        problem.arcs_creator(seeds[i])
        data_name = data_directory + "data_multi_" + str(followers) + "_" + str(i)
        problem.write_dzn_file(data_name + ".dzn")
        problem.write_dzn_file_flow(data_name + "_flow.dzn")
        for j in range(0, num_sol):
            print("\n" + solvers[j].name)
            start_time = time.time()
            solvers[j].solve(data_name)
            end_time = time.time() - start_time

            res[k][j][i] = end_time


file = open(output_name, "w+")
file.write(",")
for i in range(0, num_sol):
    file.write(solvers[i].name + ",")
file.write("\n")
for i in range(0, num_r):
    line = str(r[i]) + ","
    for j in range(0, num_sol):
        line += str(np.mean(res[i][j])) + ","
    file.write(line + "\n")

file.close()

print(time.time() - s_time)
print(res.sum())
