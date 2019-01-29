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
    % Edge start node
array[Edges] of 1..N: Edge_Start;
array[Edges] of 1..N: Edge_End;

    % Variable indicating the shortest paths 
array[Nodes] of var 0..K: pi;
array[Nodes] of var 0..1: ro;

    % Variable indicating if the arc is interdicted
array[Edges] of var 0..1: x;

constraint
      forall(e in Edges where Edge_End[e] != Start) (
          pi[Edge_End[e]] - pi[Edge_Start[e]] - x[e] * R[e] <= L[e]
  );


constraint
      forall(n in Nodes) (
          if n = Start then
            ro[n] = 1
          else
            ro[n] = max (e in Edges where Edge_End[e] = n)(x[e] * ro[Edge_Start[e]])
          endif
  );

constraint pi[Start] = 0;

    
constraint sum(e in Edges)(x[e] * R[e]) <= R0;

solve maximize pi[End] - sum(e in Edges)(x[e] * R[e]) - (1 - ro[End]) * BM;

output ["Length path for the leader: ", show(sum(e in Edges)(x[e] * L[e])), "\n", 
        "Length path for the follower: ", show(pi[End]), "\n"] ++ 
       [show(Edge_Start[i]) ++ "  " ++ show(Edge_End[i]) ++ "  " ++ show(x[i]) ++ "\n"| i in Edges]++ 
       [show(i) ++ "  " ++ show(ro[i]) ++ "  " ++ "\n"| i in Nodes] ;

%------------------------------------------------------------------------------%
%------------------------------------------------------------------------------%