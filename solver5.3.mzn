include "alldifferent.mzn";
int: A; %Number of Agents
int: V; %Number of Vertices
int: E; %Number of Edges
int: maxTime; %Max numeber of steps
array[1..A, 1..2] of 1..V: input;

array[1..V] of set of int: edges; %edges[i] is the set of vertices connected to vertex i
array[1..maxTime, 1..A] of var 1..V: tpos; %position in timesni




constraint 
      forall(j in 1..A) (tpos[1,j] = input[j, 1] /\ tpos[maxTime,j] = input[j, 2])
      /\
      forall(i in 1..maxTime) (alldifferent(row(tpos, i)))
      /\
      forall(i in 1..maxTime-1, j in 1..A) (tpos[maxTime-i,j] in edges[tpos[maxTime-i+1,j]] 
                                            /\ 
                                            tpos[i+1,j] in edges[tpos[i,j]] 
                                            /\ 
                                            forall([tpos[i,j] != tpos[i+1,a] | a in 1..A where j != a]));


%solve :: seq_search([int_search([tpos[i, j] | i in 1..maxTime, j in 1..A], dom_w_deg, indomain_min, complete)]) satisfy;
solve :: seq_search([int_search([tpos[i, j] | i in 1..maxTime, j in 1..A], dom_w_deg, indomain_min, complete)]) satisfy;
%solve satisfy;

output["i=0 "];

output["\(j):" ++ show(tpos[i,j]) ++ 
         if j == A then (if i == maxTime then "" else "\ni=\(i) " endif) else "  " endif |
         i in 1..maxTime, j in 1..A];




%solve minimize maxTime;