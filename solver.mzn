include "globals.mzn";
%Multiagent pathfinder
%int: N = 1; %number of agents 
int: E = 4; %number of edges
int: N = 5; %number of vertices
int: A = 3; %number of agents


array[1..E] of int: from = [1, 2, 3, 2];
array[1..E] of int: to = [2, 3, 4, 5];
array[1..A, 1..N] of var bool: ns;
array[1..A, 1..E] of var bool: es;


array[1..A] of int: s = [1,2,5]; %source
array[1..A] of int: t = [5,2,1]; %target



predicate path(int: N,
               int: E,
               array [int] of int: from,
               array [int] of int: to,
               var int: s,
               var int: t,
               array [int] of var bool: ns,
               array [int] of var bool: es);
constraint forall(i in 1..A)(path(N, E, from, to, s[i], t[i], [ns[i, n] | n in 1..N], [es[i, e] | e in 1..E]));


solve satisfy
  
