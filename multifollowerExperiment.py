import time
import numpy as np
import instance
from solvers import minizinc_caller
from solvers import cplex_multifollower


problem = instance.InstanceMultifollower()
solvers = []

models_directory = "/Users/avisentin/PycharmProjects/interdiction/models/"
sol = minizinc_caller.MinizincCaller()
sol.setminizinc("/Applications/MiniZincIDE.app/Contents/Resources/")
sol.setmodel(models_directory + "interdiction_multifollower_CP.mzn")
sol.setsolver("ORTools")
sol.setname("CP with ORTools")
solvers.append(sol)

sol = cplex_multifollower.CplexMultifollower()
sol.setbenders(1)
sol.setname("CPLEX explicit decomposiiton")
solvers.append(sol)

sol = cplex_multifollower.CplexMultifollower()
sol.setbenders(0)
sol.setname("CPLEX no decomposition")
solvers.append(sol)

sol = cplex_multifollower.CplexMultifollower()
sol.setbenders(2)
sol.setname("CPLEX single decomposition")
solvers.append(sol)

sol = cplex_multifollower.CplexMultifollower()
sol.setbenders(3)
sol.setname("CPLEX auto decomposition")
solvers.append(sol)

num_sol = len(solvers)

r = [20, 30, 40, 50]
num_r = len(r)
followers = 3
seeds = [1234, 1989, 290889]#, 251091, 240664, 190364, 120863, 101295, 31089, 3573113]
num_seeds = len(seeds)

problem.set_args(10, 10, 100, 10, 10, 5, 20, followers)
data_directory = "/Users/avisentin/PycharmProjects/interdiction/data/"
output_name = "./test_multifollower" + str(followers) + ".csv"

res = np.zeros((num_r, num_sol, num_seeds))

s_time = time.time()

for k in range(0, num_r):
    problem.set_r0(r[k])
    for i in range(0, num_seeds):
        problem.arcs_creator(seeds[i])
        data_name = data_directory + "data_multi_" + str(followers) + "_" + str(i)
        problem.write_dzn_file(data_name+ ".dzn")
        problem.write_dat_file(data_name+ ".dat")
        for j in range(0, num_sol):
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
