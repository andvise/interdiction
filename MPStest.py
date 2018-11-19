import time
import numpy as np
import instance
import subprocess as sp



problem = instance.Instance()

problem.set_args(10,10,100,10,10,5,20)

r_range = [20,30,40,50]

models_directory = "/home/andrea/PycharmProjects/interdiction/models/"
data_directory = "/home/andrea/PycharmProjects/interdiction/models/"
solver = "ORTools"
output_name = "./Gurobi.csv"
parameters = ""

res = np.zeros((4, 5, 3))

seeds = [1234, 1989, 290889]#, 251091, 240664, 190364, 120863, 101295, 31089, 3573113]
s_time = time.time()

for r in range(0, len(r_range)):
    problem.set_r0(r_range[r])
    for i in range(0, len(seeds)):
        problem.arcs_creator(seeds[i])
        data_name = data_directory + "data_" + str(i) + ".dzn"
        problem.write_dzn_file(data_name)

        for j in range(1, 6):
            start_time = time.time()
            model_name = "shortest-path-dijkstra_v" + str(j) + ".mzn"
            proc = sp.Popen("minizinc --solver " + solver + " " +  models_directory + model_name + " " +
                            data_name + parameters,
                            shell=True,
                            stdout=sp.PIPE
                            )
            end_time = time.time() - start_time
            print(proc.communicate()[0])

            res[r][j - 1][i] = end_time


file = open(output_name, "w+")
file.write(",v1,v2,v3,v4,v5,\n")
for i in range(0, len(r_range)):
    line = str(r_range[i]) + ","
    for j in range(0, 5):
        line += str(np.mean(res[i][j])) + ","
    file.write(line + "\n")

file.close()

print(time.time() - s_time)
print(res.sum())
