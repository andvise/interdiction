%------------------------------------------------------------------------------%
% Andrea Visentin <andrea.visentin@insight-centre.org>
% July 2018
% vim: ft=zinc ts=4 sw=4 et tw=0
%
% Shortest Path Problem using Dijkstra.
% 
%------------------------------------------------------------------------------%

    % Max Value
int: K;
    % Number of nodes
int: N;
    %  The actual nodes
set of int: Nodes = 1..N;

    % Start  and End node path_a
1..N: Start_a;
1..N: End_a;
    % Start  and End node path_b
1..N: Start_b;
1..N: End_b;
    % Start  and End node path_c
1..N: Start_c;
1..N: End_c;


    % Number of edges (directed arcs)
int: M;
    % Interdiction budget
int: R0;
    %  The actual edges
set of int: Edges = 1..M; 
    % Edge lengths
array[Edges] of int: L;
    % Edge interdiction value
array[Edges] of int: D;
    % Edge interdiction cost
array[Edges] of int: R;
    % Edge start node
array[Edges] of 1..N: Edge_Start;
array[Edges] of 1..N: Edge_End;

    % Variable indicating the shortest path from Start_a that node 
array[Nodes] of var 0..K: z_a;
    % Variable indicating the shortest path from Start_b that node 
array[Nodes] of var 0..K: z_b;
    % Variable indicating the shortest path from Start_c that node 
array[Nodes] of var 0..K: z_c;


    % Variable indicating if the arc is interdicted
array[Edges] of var 0..1: x;

    % Dijkstra on path a
constraint
    forall(i in 1..N ) (
        if i = End_a then
            z_a[i] = 0
        else
            z_a[i] = min(e in Edges where Edge_Start[e] = i)(z_a[Edge_End[e]] + L[e] + x[e] * R[e])
        endif
    );

    % Dijkstra on path b
constraint
    forall(i in 1..N ) (
        if i = End_b then
            z_b[i] = 0
        else
            z_b[i] = min(e in Edges where Edge_Start[e] = i)(z_b[Edge_End[e]] + L[e] + x[e] * R[e])
        endif
    );

    % Dijkstra on path c
constraint
    forall(i in 1..N ) (
        if i = End_c then
            z_c[i] = 0
        else
            z_c[i] = min(e in Edges where Edge_Start[e] = i)(z_c[Edge_End[e]] + L[e] + x[e] * R[e])
        endif
    );
    
    
constraint sum(e in Edges)(x[e] * R[e]) <= R0;

solve maximize z_a[Start_a] + z_b[Start_b] + z_c[Start_c];

output ["Length a: ", show(z_a[Start_a]), "\n", 
	"Length b: ", show(z_b[Start_b]), "\n",
	"Length c: ", show(z_c[Start_c]), "\n"];

%------------------------------------------------------------------------------%
%------------------------------------------------------------------------------%
