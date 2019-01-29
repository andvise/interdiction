%------------------------------------------------------------------------------%
% Andrea Visentin <andrea.visentin@insight-centre.org>
% July 2018
% vim: ft=zinc ts=4 sw=4 et tw=0
%
% Shortest Path Problem using Dijkstra.
% 
%------------------------------------------------------------------------------%

include "globals.mzn";

    % Number of nodes
int: N;
    % Number of edges (directed arcs)
int: M;
    % Big M
int: BM = 1000;
    % K
int: K = 10000;

    %  The actual nodes
set of int: Nodes = 1..N;
    %  The actual edges
set of int: Edges = 1..M; 

    % Source of Path
1..N: Start;
    % Target of Path
1..N: End;

    % Interdiction budget
int: R0;
    % Edge lengths
array[Edges] of int: L;
    % Edge interdiction value
array[Edges] of int: D;
    % Edge interdiction cost
array[Edges] of int: R;
    % Balance
array[Nodes] of int: Balance;
    % Edge start node
array[Edges, 1..2] of 1..N: Edge;

    % Variable indicating the shortest paths 
array[Nodes] of var 0..K: pi;
array[Nodes] of var 0..1: ro;

var int: cost;

    % Variable indicating if the arc is interdicted
array[Edges] of var 0..1: x;
array[Edges] of var 0..1: z;



constraint network_flow_cost(Edge, Balance, L, x, cost);


constraint
    forall(i in 1..N ) (
        if i != Start then
            pi[i] = min(e in Edges where Edge[e,2] = i)(pi[Edge[e,1]] + L[e] + x[e] * R[e])
        endif        
    );
    
constraint  pi[Start] = 0;

    
constraint sum(e in Edges)(x[e] * R[e]) <= R0;

solve minimize cost;

output ["Leader_length: ", show(cost), " ", 
        "Follower_length: ", show(pi[End]), " ",
        "Cost: ", show(sum(e in Edges)(x[e] * R[e])), " "] ;
