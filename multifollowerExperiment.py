import time
import numpy as np
import instance
import subprocess as sp


problem = instance.InstanceMultifollower()

r = [20, 30, 40, 50]
n_r = len(r)
followers = 3
models = ["test_multifollower_" + followers + ".mzn"]
n_models = len(models)

problem.set_args(10, 10, 100, 10, 10, 5, 20, followers)

models_directory = "/home/andrea/PycharmProjects/interdiction/models/"
data_directory = "/home/andrea/PycharmProjects/interdiction/"
solver = "ORTools"
output_name = "./test_multifollower" + followers + ".csv"
parameters = ""

res = np.zeros((len(models), 5, 3))

seeds = [1234, 1989, 290889]#, 251091, 240664, 190364, 120863, 101295, 31089, 3573113]
s_time = time.time()

for k in range(0, n_r):
    problem.set_r0(r[k])
    for i in range(0, len(seeds)):
        problem.arcs_creator(seeds[i])
        data_name = data_directory + "data_multi_" + followers + "_" + str(i) + ".dzn"
        problem.write_dzn_file(data_name)

        for j in range(0, n_models):
            start_time = time.time()
            proc = sp.Popen("minizinc --solver " + solver + " " + models_directory + models[j] + " " +
                            data_name + parameters,
                            shell=True,
                            stdout=sp.PIPE
                            )
            end_time = time.time() - start_time
            print(proc.communicate()[0])

            res[r][j - 1][i] = end_time


file = open(output_name, "w+")
file.write(",")
for i in range(0, n_models):
    file.write(models[i] + ",")
file.write("\n")
for i in range(0, n_r):
    line = str(r[i]) + ","
    for j in range(0, 5):
        line += str(np.mean(res[i][j])) + ","
    file.write(line + "\n")

file.close()

print(time.time() - s_time)
print(res.sum())
