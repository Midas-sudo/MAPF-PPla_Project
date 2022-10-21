# Search and Planning Project - Multi-Agent Path Finding
## Constraint programing with Minizinc

This project is a constraint programing implementation of the multi-agent path finding problem using the Minizinc language. The problem given is composed by a graph of nodes connected by edges and a set of agents that need to find a path from a start node to a goal node. 
The agents can only move on the edges of the graph and can't cross each other. The goal is to find a path for each agent that doesn't cross any other agent's path.

----------------------

### How to run

<details open>
<summary><h4 style="display:inline-block">Minizinc IDE</h4></summary>
To run the program you need to have the Minizinc IDE installed. You can download it from [here](http://www.minizinc.org/software.html).

Once you have the IDE installed, you can run the program by opening the file `multi_agent_path_finding.mzn` and clicking on the "Run" button. The IDE will ask you to select a data file. You can select any of the previously made data files in the `data` folder. The IDE will then run the program and show you the results.
</details>

<details open>
<summary><h4 style="display:inline-block">Minizinc from terminal</h4></summary>
Another way to run the program is to use the command line. To do this, you need to have the Minizinc compiler installed or the Minizinc IDE. You can download it from [here](http://www.minizinc.org/software.html). Once you have the compiler installed, you can run the program by running the following command:

    minizinc multi_agent_path_finding.mzn data/<data_file>

where `<data_file>` is the name of, the previously made, data file you want to use. The program will then run and show you the results.
</details>

<details open>
<summary><h4 style="display:inline-block">Python script</h4></summary>

Lastly you can also run the python script created to make new data files from a graph file and a scene file. The script will also run the example through Minizinc giving you the answear of the minimun time steps needed for all the agents to be able to reach their goal.
To do this, you need to have python 3 installed. You can download it from [here](https://www.python.org/downloads/). Once you have python installed, you can run the program by running the following command:

    python3 MAPF_Loader.py <graph_file> <scene_file>

where `<graph_file>` is the name of the graph file you want to use and `<scene_file>` is the name of the scene file you want to use. The program will then run and create a data file with the same name as the scene file in the `data` folder.

</details>

--------------------------------

## Minizinc Aproach Taken
<a name="Aproachtaken"></a>

<h5>Version 1 & 2</h5>
Through out the development of the Minizinc script alot of optimization trick were learnt. 
Versions 1 and 2 were implemented with a boolen aprroach, having a 3 dimensional matrix [Time Step, Agent, Edge] where the value of each cell was a boolean that indicated if the agent was on the edge at that time step. Version 1 and 2 was also composed of 7 separated constraints.
The times for version 1 were absordly high even for simple graphs. Version 2 improved on the timing thanks to the implementation of `search_notations` with reduced the time of some of the examples, but stil not ideal for the bigger graphs.

<h5>Version 3</h5>

The need for better time values lead me to try and find a better data structure and a better way to implement the constraints. Version 3 was the first attempt at this. The data structure was changed to a 2 dimensional matrix [Time Step, Agent] where the value of each cell was the node where the Agent was at that specific time. 
This data structure allowed for a better implementation of the constraints, with the trade-off of a worst memory requirement since for each position of the matrix instead of a 0 or a 1 there could be any value between 1 and the number of nodes. THis memory requirement turnned out to be a problem for the bigger graphs with one of the solvers (Explained in the [Results](#results) section).
Over all the number of constraints were reduced to 5, and eventhough the time for version 3 was still not ideal for the bigger graphs it reduced significantly the time for smaller graphs.

<h5>Version 4</h5>

In version 4 some searches were made to try and find the best optimization practices, leading me to find that Minizinc, when compiling, unfolds the constraints into the possible cases and so having two constraints that interate over the same object is basically a duplication of the operations. Because of this some of the constraints were merged into one, reducing the number of constraints from 5 to 3.

This change made a huge difference in the time taken by the bigger examples. 

<h5>Version 5</h5>

The search for the best performace also revealed some other optimization tricks. One of them was the use of low level functions like `row` to access the rows of the position matrix, instead of having to iterate in the x axis of the matrix as well, when evaluating the `all_different`. This function was very usefull and in the best case reduced some of the examples time in around 350ms.

Another possible change found in some papers about MAPF was the implementation of a bi-directional search. What this basically mean is that instead of searching the agent path from the begining towards the end, the search is done from both ends, and the two paths are then merged. This change improved greatly the time of the bigger examples, but it also created some unwanted behaviour on examples 9, 11, 12. This problem is explained in the [Results](#results) section.



### Results
| Example  |Image |Project Version   |  Time (Minizinc with Gecode) [ms] | Time (Minizinc with Chuffed) [ms] |Time (Full Program with Gecode) [sec]  |Time (Full Program with Chuffed) [sec]  | 
| :------------: | :------------: | :------------: | :------------: | :------------: | :------------: | :------------: | 
|1|<img src="./examples/imgs/01.png" alt="Example 1" style="width:200px;"/>|5.0|284|256|2.127|||
|2|<img src="./examples/imgs/02.png" alt="Example 2" style="width:200px;"/>|5.0|315|3595|3.325|
|3|<img src="./examples/imgs/03.png" alt="Example 3" style="width:200px;"/>|5.0|267|253|2.148| 
|4|<img src="./examples/imgs/04.png" alt="Example 4" style="width:200px;"/>|5.0|267|258|2.175| 
|5|<img src="./examples/imgs/05.png" alt="Example 5" style="width:200px;"/>|5.0|281|260|3.498| 
|6|<img src="./examples/imgs/06.png" alt="Example 6" style="width:200px;"/>|5.0|271|269|2.180| 
|7|<img src="./examples/imgs/07.png" alt="Example 7" style="width:200px;"/>|5.0|313|287|3.800| 
|8|<img src="./examples/imgs/08.png" alt="Example 8" style="width:200px;"/>|5.0|281|287|4.129| 
|9|<img src="./examples/imgs/09.png" alt="Example 9" style="width:200px;"/>|5.1|598000 (9min 58s)|1034|NT<sup>(2)</sup>| 
|10|<img src="./examples/imgs/10.png" alt="Example 10" style="width:200px;"/>|5.0|4598|DNF<sup>(1)</sup>|3.574|
|11|<img src="./examples/imgs/11.png" alt="Example 11" style="width:200px;"/>|5.1|DNF<sup>(1)</sup>|DNF<sup>(1)</sup>|NT<sup>(2)</sup>| 
|12|<img src="./examples/imgs/12.png" alt="Example 12" style="width:200px;"/>|5.0|DNF<sup>(1)</sup>|DNF<sup>(1)</sup>|NT<sup>(2)</sup>| 
|13|<img src="./examples/imgs/13.png" alt="Example 13" style="width:200px;"/>|5.0|942|DNF<sup>(1)</sup>|3.775| 
|14|<img src="./examples/imgs/14.png" alt="Example 14" style="width:200px;"/>|5.0|1741|DNF<sup>(1)</sup>|5.563| 
|15|<img src="./examples/imgs/15.png" alt="Example 15" style="width:200px;"/>|5.0|629|DNF<sup>(1)</sup>|3.119| 
|16|<img src="./examples/imgs/16.png" alt="Example 16" style="width:200px;"/>|5.0|1205|DNF<sup>(1)</sup>|4.318| 
|17|<img src="./examples/imgs/17.png" alt="Example 17" style="width:200px;"/>|5.0|830|DNF<sup>(1)</sup>|3.785| 
|18|<img src="./examples/imgs/18.png" alt="Example 18" style="width:200px;"/>|5.0|948|DNF<sup>(1)</sup>|3.826| 
|19|<img src="./examples/imgs/19.png" alt="Example 19" style="width:200px;"/>|5.0|1809|DNF<sup>(1)</sup>|5.320| 
|20|<img src="./examples/imgs/20.png" alt="Example 20" style="width:200px;"/>|5.0|64000 (1min 4s)|DNF<sup>(1)</sup>|  | |

<sup>(1)</sup> The Minizinc did not find a solution under five hours or it crashed.
<sup>(2)</sup> The program was not testes due to the high value of time used in Minizinc, or because of the absence of a solution with Minizinc.

<h3>Results Analysis</h3>

- Like mentioned in ['Aproach taken'](#Aproachtaken) section there where 2 changes that created some unwanted behaviour. One of the changes was the implementation of the <b>bi-directional search</b>. This change improved greatly the time of the bigger examples, but it also created some unwanted behaviour on examples 9, 11, 12. 

- The use of the <b>bi-directional search</b> creates, in very agent dense problems, a higher probability of the inability of merging both paths leading to more dead-ends / backtracking. This is the reason why the time of the example  9 is so high (for the gecode compilation) and why examples 11 and 12 wont run on decent times. 

- Eventhough the <b>bi-directional search</b> created the previously mention problem, the problem only occurs with the Gecode compilation engine, since its pretty easy to observe that for example 9 instead of the almost 10 minutes of run time, with chuffed it only takes 1 second. This would lead me to belive that the solution to my problem would be in using the chuffed engine with the current solution.

- The use of chuffed engine turnned out to be a bad option due to the first change made in version 3. The use of a 2 dimension matrix, like it was explain in the 'Approach' section, increased the size of the variables used, something that is very penalized in the chuffed engine like it can be see in the following image:


Gecode Compilation Profile | Chuffed Compilation Profile
- | - 
![Gecode Compilation Profile](./gecode_ex9.jpg) | ![Chuffed Compilation Profile](./chuffed_ex9.jpg)

- This situation lead to absurdly long times for example with big graphs.

### Minizinc Conclusion
Other versions with smaller changes were made in order to try and improve the current results of version 5 but with no success. Due to the lack of more time and ideias to improve the current minizinc implementation I decided to try and improve the current program through the python script.

<h2>Python Script</h2>

The script of python developed can be divided into 3 parts:

- The first part is the reception of the graph and scen of the problem to be analysed.

- The second part is the analysis of every single agent and the calculation of its shortest path without any type of restrictions.

- Lastly the scrip calls the minizinc in sucession increasing for each of the runs the limit number of steps, stopping only when the minizinc returns a solution.

This last part also has some logic in place in order to try the mnizinc both with the gecode engine as well as the chuffed engine, in order to try and find a solution faster for examples like 9. 

The way it is implemented is based on the time it has run on one of the engines and if the run time is above a certain threshold it will try the other engine. If the other engine is also above the threshold it will try the other engine again, but this time with a higher limit of steps.