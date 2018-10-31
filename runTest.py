import time
import pymzn
import numpy as np
import pymzn.config
import instance

#pymzn.debug()
problem = instance.Instance()

problem.set_args(10,10,100,10,10,5,20)
sol = pymzn.ORTools()

r_range = [20,30,40,50]

pymzn.config.set('mzn2fzn', '/home/andrea/MiniZincIDE/mzn2fzn')
pymzn.config.set('solns2out', '/home/andrea/MiniZincIDE/solns2out')

output_name = "./Gurobi.csv"

res = np.zeros((4, 5, 3))

seeds = [1234, 1989, 290889]#, 251091, 240664, 190364, 120863, 101295, 31089, 3573113]
s_time = time.time()

for r in range(0, len(r_range)):
    problem.set_r0(r_range[r])
    for i in range(0, len(seeds)):
        problem.arcs_creator(seeds[i])
        name = "./data/data_" + str(i) + ".dzn"
        problem.write_dzn_file(name)

        for j in range(1, 6):
            start_time = time.time()
            s = pymzn.minizinc('./models/shortest-path-dijkstra_v' + str(j) + '.mzn', name, solver=sol)
            end_time = time.time() - start_time
            print(s)
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
