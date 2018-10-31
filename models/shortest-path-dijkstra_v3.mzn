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
    % Start node
1..N: Start;
    % End node
1..N: End;
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

    % Variable indicating the shortest path from that node to the sink
array[Nodes] of var 0..K: z;
    % Variable indicating the shortest path from the source to that node
array[Nodes] of var 0..K: zs;
    % Variable indicating if the arc is interdicted
array[Edges] of var 0..1: x;

constraint
    forall(i in 1..N ) (
        if i = End then
            z[i] = 0
        else
            z[i] = min(e in Edges where Edge_Start[e] = i)(z[Edge_End[e]] + L[e] + x[e] * R[e])
        endif
    );
    
constraint
    forall(i in 1..N ) (
        if i = Start then
            zs[i] = 0
        else
            zs[i] = min(e in Edges where Edge_End[e] = i)(zs[Edge_Start[e]] + L[e] + x[e] * R[e])
        endif
    );
    
constraint
    forall(i in 1..N ) (
        if i != Start /\ i != End then
            zs[i] + z[i] >= z[Start]
        else
            true
        endif
    );
    
constraint z[Start] = zs[End];

constraint
    forall(e in Edges ) (
            if z[Edge_End[e]] + L[e] + zs[Edge_Start[e]] > z[Start] then
            x[e] = 0
        else
            true
        endif
    );

constraint sum(e in Edges)(x[e] * R[e]) <= R0;

solve maximize z[Start];

output ["Length: ", show(z[Start]), "\n"];

%------------------------------------------------------------------------------%
%------------------------------------------------------------------------------%