include "alldifferent.mzn";
int: A; %Number of Agents
int: V; %Number of Vertices
int: E; %Number of Edges
int: maxTime; %Max numeber of steps

array[1..A, 1..2] of var int: input;

array[1..maxTime, 1..A, 1..V] of var 0..1: steps; %steps[i,j,k] is the vertex visited by agent j at time i
array[1..V] of set of int: edges; %edges[i] is the set of vertices connected to vertex i
array[1..maxTime, 1..A] of var int: final;




constraint forall(j in 1..A) (steps[1,j,input[j, 1]] = 1); %Starting vertex
constraint forall(j in 1..A) (steps[maxTime,j,input[j, 2]] = 1); %End vertex
constraint forall(i in 1..maxTime, j in 1..A, k in 1..V)(steps[i, j, k] == 1 <-> final[i, j] = k);


constraint forall(i in 1..maxTime, k in 1..V) (sum([steps[i,j,k] | j in 1..A]) <= 1); %Each vertex is visited by exactly one agent at each time step
constraint forall(i in 1..maxTime, j in 1..A) (sum([steps[i,j,k] | k in 1..V]) = 1); %Each agent visits exactly one vertex at each time step


constraint forall(i in 1..maxTime-1, j in 1..A, k in 1..V) (steps[i,j,k] = 1 -> (sum([steps[i+1,j,u] | u in edges[k]]) >= 1 \/ steps[i+1,j,k] = 1)); %If agent j visits vertex v at time i, then at least one of its neighbors is visited at time i+1         
%constraint forall(i in 1..maxTime-1, j in 1..A, k in 1..V)(forall([final[i,j] == final[i+1,a] -> final[i+1,j] != final[i,a] | a in 1..A where j != a]));

constraint forall(i in 2..maxTime, j in 1..A, k in 1..V)(forall([final[i,j] != final[i-1,a] | a in 1..A where j != a]));

%constraint redundant_constraint(forall( i in 1..maxTime)(all_different([final[i,j]| j in 1..A])));
%constraint redundant_constraint(forall( i in 1..A)(final[1,i] = input[i,1] /\ final[maxTime,i] = input[i,2]));

solve :: seq_search([int_search([final[i, j] | i in 1..maxTime, j in 1..A], dom_w_deg, indomain_split, complete)]) satisfy;

%solve satisfy;

output["i=0 "];

output["\(j):" ++ show(final[i,j]) ++ 
         if j == A then (if i == maxTime then "" else "\ni=\(i) " endif) else "  " endif |
         i in 1..maxTime, j in 1..A];




%solve minimize maxTime;