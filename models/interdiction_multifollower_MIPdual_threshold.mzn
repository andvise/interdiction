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
    % Number of edges (directed arcs)
int: M;
    % Number of followers
int: P;
    %  The actual nodes
set of int: Nodes = 1..N;
    %  The actual edges
set of int: Edges = 1..M; 
    %  The actual paths
set of int: Paths = 1..P;

    % Sources of Paths
array[Paths] of int: Start;
    % Targets of Paths
array[Paths] of int: End;

    % Interdiction budget
int: R0;
    % Edge lengths
array[Edges] of int: L;
    % Edge interdiction value
array[Edges] of int: D;
    % Edge interdiction cost
array[Edges] of int: R;
    % Edge start node
array[Edges] of 1..N: Edge_Start;
array[Edges] of 1..N: Edge_End;

    % Variable indicating the shortest paths 
array[Nodes,Paths] of var 0..K: pi;

    % Variable indicating if the arc is interdicted
array[Edges] of var 0..1: x;

constraint
    forall(p in 1..P) (
        forall(e in Edges where Edge_End[e] != Start[p]) (
            pi[Edge_End[e],p] - pi[Edge_Start[e],p] - x[e] * R[e] <= L[e]
        )
    );

constraint
    forall(p in 1..P) (
        pi[End[p],p] >= R0
    );


constraint
    forall(p in 1..P ) (
        pi[Start[p],p] = 0
    );
    

solve minimize sum(e in Edges)(x[e] * R[e]);

output ["Total length: ", show(sum(p in Paths)(pi[End[p],p])), "\n"] ++ 
       [show(pi[End[t],t]) ++ "  " | t in Paths] ++
       ["\nTotal cost: ", show(sum(e in Edges)(x[e] * R[e])), "\n"] ;

%------------------------------------------------------------------------------%
%------------------------------------------------------------------------------%