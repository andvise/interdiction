import random


class Arc:

    start = 0
    end = 0
    length = 0
    disruption = 0
    cost = 0


class Instance:
    m = 10
    n = 10
    N = n * m + 2
    K = 1000
    a = (n - 2) * (5 * m - 4) + 5 * m - 2
    c = 10
    d = 10
    r = 5
    r0 = 20
    arcs = []

    def set_r0(self, r0):
        self.r0 = r0

    def set_args(self, m, n, K, c, d, r, r0):
        self.m = m
        self.n = n
        self.K = K
        self.c = c
        self.d = d
        self.r = r
        self.r0 = r0
        self.N = n * m + 2
        self.a = (n - 2) * (5 * m - 4) + 5 * m - 2

    def node_nr(self, x, y):
        return self.m * (y - 1) + x + 1

    def arcs_creator(self, seed):
        self.arcs = []
        random.seed(seed)
        for j in range(1, self.m + 1):
            for i in range(1, self.n + 1):
                if i + 1 <= self.n and j != 1 and j != self.m:
                    arc = Arc()
                    arc.start = self.node_nr(i, j)
                    arc.end = self.node_nr(i + 1, j)
                    arc.length = random.randint(1, self.c)
                    arc.disruption = random.randint(1, self.d)
                    arc.cost = random.randint(1, self.r)
                    self.arcs.append(arc)
                if i - 1 > 0 and j != 1 and j != self.m:
                    arc = Arc()
                    arc.start = self.node_nr(i, j)
                    arc.end = self.node_nr(i - 1, j)
                    arc.length = random.randint(1, self.c)
                    arc.disruption = random.randint(1, self.d)
                    arc.cost = random.randint(1, self.r)
                    self.arcs.append(arc)
                if j + 1 <= self.m:
                    arc = Arc()
                    arc.start = self.node_nr(i, j)
                    arc.end = self.node_nr(i, j + 1)
                    arc.length = random.randint(1, self.c)
                    arc.disruption = random.randint(1, self.d)
                    arc.cost = random.randint(1, self.r)
                    self.arcs.append(arc)
                if j + 1 <= self.m and i + 1 <= self.n:
                    arc = Arc()
                    arc.start = self.node_nr(i, j)
                    arc.end = self.node_nr(i + 1, j + 1)
                    arc.length = random.randint(1, self.c)
                    arc.disruption = random.randint(1, self.d)
                    arc.cost = random.randint(1, self.r)
                    self.arcs.append(arc)
                if j + 1 <= self.m and i - 1 > 0:
                    arc = Arc()
                    arc.start = self.node_nr(i, j)
                    arc.end = self.node_nr(i - 1, j + 1)
                    arc.length = random.randint(1, self.c)
                    arc.disruption = random.randint(1, self.d)
                    arc.cost = random.randint(1, self.r)
                    self.arcs.append(arc)

        for i in range(1, self.m + 1):
            arc = Arc()
            arc.start = 1
            arc.end = i + 1
            arc.length = 0
            arc.disruption = 0
            arc.cost = 500
            self.arcs.append(arc)

        for i in range(1, self.m + 1):
            arc = Arc()
            arc.start = self.node_nr(i, self.n)
            arc.end = self.N
            arc.length = 0
            arc.disruption = 0
            arc.cost = 500
            self.arcs.append(arc)

        return self.arcs

    def write_dzn_file(self, name):
        file = open(name, "w+")
        file.write("N = " + str(self.N) + ";\n")
        file.write("K = " + str(self.K) + ";\n")
        file.write("M = " + str(self.a) + ";\n")
        file.write("R0 = " + str(self.r0) + ";\n")
        file.write("Start = 1;\n")
        file.write("End = " + str(self.N) + ";\n")

        line = "Edge_Start =  ["
        for i in self.arcs[:-1]:
            line = line + str(i.start) + " ,"
        line = line + str(self.arcs[-1].start) + "];\n"
        file.write(line)

        line = "Edge_End =  ["
        for i in self.arcs[:-1]:
            line = line + str(i.end) + " ,"
        line = line + str(self.arcs[-1].end) + "];\n"
        file.write(line)

        line = "L =  ["
        for i in self.arcs[:-1]:
            line = line + str(i.length) + " ,"
        line = line + str(self.arcs[-1].length) + "];\n"
        file.write(line)

        line = "D =  ["
        for i in self.arcs[:-1]:
            line = line + str(i.disruption) + " ,"
        line = line + str(self.arcs[-1].disruption) + "];\n"
        file.write(line)

        line = "R =  ["
        for i in self.arcs[:-1]:
            line = line + str(i.cost) + " ,"
        line = line + str(self.arcs[-1].cost) + "];\n"
        file.write(line)

        file.close()


class InstanceMultifollower:
    m = 10
    n = 10
    N = n * m
    K = 1000
    a = 2 * ((n - 2) * (5 * m - 4) + 3 * m - 2)
    c = 10
    d = 10
    r = 5
    r0 = 20
    arcs = []
    paths = []
    npaths = 2;

    def set_r0(self, r0):
        self.r0 = r0

    def set_args(self, m, n, k, c, d, r, r0, npaths):
        self.m = m
        self.n = n
        self.K = k
        self.c = c
        self.d = d
        self.r = r
        self.r0 = r0
        self.N = n * m
        self.a = 2 * ((n - 2) * (5 * m - 4) + 3 * m - 2)
        self.npaths = npaths

    def node_nr(self, x, y):
        return self.m * (y - 1) + x

    def arcs_creator(self, seed):
        self.arcs = []
        random.seed(seed)
        self.paths = random.sample(range(1, self.N), self.npaths * 2)

        for j in range(1, self.m + 1):
            for i in range(1, self.n + 1):
                if i + 1 <= self.n and j != 1 and j != self.m:
                    arc = Arc()
                    arc.start = self.node_nr(i, j)
                    arc.end = self.node_nr(i + 1, j)
                    arc.length = random.randint(1, self.c)
                    arc.disruption = random.randint(1, self.d)
                    arc.cost = random.randint(1, self.r)
                    self.arcs.append(arc)
                if i - 1 > 0 and j != 1 and j != self.m:
                    arc = Arc()
                    arc.start = self.node_nr(i, j)
                    arc.end = self.node_nr(i - 1, j)
                    arc.length = random.randint(1, self.c)
                    arc.disruption = random.randint(1, self.d)
                    arc.cost = random.randint(1, self.r)
                    self.arcs.append(arc)
                if j + 1 <= self.m:
                    arc = Arc()
                    arc.start = self.node_nr(i, j)
                    arc.end = self.node_nr(i, j + 1)
                    arc.length = random.randint(1, self.c)
                    arc.disruption = random.randint(1, self.d)
                    arc.cost = random.randint(1, self.r)
                    self.arcs.append(arc)
                if j + 1 <= self.m and i + 1 <= self.n:
                    arc = Arc()
                    arc.start = self.node_nr(i, j)
                    arc.end = self.node_nr(i + 1, j + 1)
                    arc.length = random.randint(1, self.c)
                    arc.disruption = random.randint(1, self.d)
                    arc.cost = random.randint(1, self.r)
                    self.arcs.append(arc)
                if j + 1 <= self.m and i - 1 > 0:
                    arc = Arc()
                    arc.start = self.node_nr(i, j)
                    arc.end = self.node_nr(i - 1, j + 1)
                    arc.length = random.randint(1, self.c)
                    arc.disruption = random.randint(1, self.d)
                    arc.cost = random.randint(1, self.r)
                    self.arcs.append(arc)

        return self.arcs

    def write_dzn_file(self, name):
        file = open(name, "w+")
        file.write("N = " + str(self.N) + ";\n")
        file.write("K = " + str(self.K) + ";\n")
        file.write("M = " + str(self.a) + ";\n")
        file.write("R0 = " + str(self.r0) + ";\n")
        for i in range(0, len(self.paths)//2):
            file.write("Start_" + chr(97 + i) + " = " + str(self.paths[2*i]) + ";\n")
            file.write("End_" + chr(97 + i) + " = " + str(self.paths[2*i+1]) + ";\n")

        # Edge Start
        file.write("Edge_Start =  [" + (" ,".join(str(x.start) + " ," + str(x.end) for x in self.arcs)) + "]\n")

        # Edge End
        file.write("Edge_End =  [" + (" ,".join(str(x.end) + " ," + str(x.start) for x in self.arcs)) + "]\n")

        # L
        file.write("L = [" + (" ,".join(str(x.length) + " ," + str(x.length) for x in self.arcs)) + "]\n")

        # D
        file.write("D = [" + (" ,".join(str(x.disruption) + " ," + str(x.disruption) for x in self.arcs)) + "]\n")

        # Cost
        file.write("R = [" + (" ,".join(str(x.cost) + " ," + str(x.cost) for x in self.arcs)) + "]\n")


        file.close()

    def write_dat_file(self, name):
        file = open(name, "w+")
        file.write(str(self.N) + "\n")
        file.write(str(self.K) + "\n")
        file.write(str(self.a) + "\n")
        file.write(str(self.r0) + "\n")

        # Path start and end
        file.write("[" + (" ,".join(str(x) for x in self.paths[::2])) + "]\n")
        file.write("[" + (" ,".join(str(x) for x in self.paths[1::2])) + "]\n")

        # Edge Start
        file.write("[" + (" ,".join(str(x.start) + " ," + str(x.end) for x in self.arcs)) + "]\n")

        # Edge End
        file.write("[" + (" ,".join(str(x.end) + " ," + str(x.start) for x in self.arcs)) + "]\n")

        # L
        file.write("[" + (" ,".join(str(x.length) + " ," + str(x.length) for x in self.arcs)) + "]\n")

        # D
        file.write("[" + (" ,".join(str(x.disruption) + " ," + str(x.disruption) for x in self.arcs)) + "]\n")

        # Cost
        file.write("[" + (" ,".join(str(x.cost) + " ," + str(x.cost) for x in self.arcs)) + "]\n")

        file.close()
