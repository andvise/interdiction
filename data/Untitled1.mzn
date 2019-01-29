%------------------------------------------------------------------------------%
% Andrea Visentin <andrea.visentin@insight-centre.org>
% July 2018
% vim: ft=zinc ts=4 sw=4 et tw=0
%
% Shortest Path Problem using Dijkstra.
% 
%------------------------------------------------------------------------------%


    % Number of nodes
int: N;
    % Number of edges (directed arcs)
int: M;
    % Big M
int: BM = 10000;

    %  The actual nodes
set of int: Nodes = 1..N;
    %  The actual edges
set of int: Edges = 1..M; 

    % Source of Path
int: Start;
    % Target of Path
int: End;

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
array[Nodes] of var int: pi;
array[Nodes] of var int: ro;

    % Variable indicating if the arc is interdicted
array[Edges] of var 0..1: x;

constraint
      forall(i in 1..N ) (
          if i = Start then
              pi[i] = 0
          else
              pi[i] = min(e in Edges where Edge_Start[e] = i)(pi[Edge_End[e]] + L[e] + x[e] * R[e])
          endif
  );

constraint
      forall(i in 1..N ) (
          if i = Start then
              ro[i] = 0
          else
              ro[i] = min(e in Edges where Edge_Start[e] = i)(ro[Edge_End[e]] + L[e] + x[e] * R[e])
          endif
  );
      forall(e in Edges where Edge_End[e] != Start) (
          ro[Edge_End[e]] - ro[Edge_Start[e]] + x[e] * BM >= L[e] + BM
  );

    
constraint sum(e in Edges)(x[e] * R[e]) <= R0;

solve maximize pi[End] - ro[End];

output ["Length path for the leader: ", show(ro[End]), "\n", 
        "Length path for the follower: ", show(pi[End]), "\n"];

%------------------------------------------------------------------------------%
%------------------------------------------------------------------------------%