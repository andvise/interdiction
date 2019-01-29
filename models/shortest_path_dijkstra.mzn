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

    % Variable indicating if the arc is interdicted

constraint
      forall(e in Edges where Edge_End[e] != Start) (
          pi[Edge_End[e]] - pi[Edge_Start[e]] <= L[e]
  );


constraint pi[Start] = 0;
    

solve maximize pi[End] ;

output ["Length path: ", show(pi[End]), "\n"] ;

%------------------------------------------------------------------------------%
%------------------------------------------------------------------------------%