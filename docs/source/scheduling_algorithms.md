# Scheduling Algorithms

The scheduling algorithms covered and to be implemented are:

1. Earliest Deadline First (EDF) for Single-Node
2. Latest Deadline First (LDF) for Single-Node
3. Earliest Deadline First (EDF) for Multi-Node.
4. Latest Deadline First (LDF) for Multi-Node
5. Least Laxity (LL) for Multi-Node

## Application Model

shift everything here and also describe deadliune , wcet and stuff

![Application Model](application.png)

The application model is illustrated as a Directed Acyclic Graph (DAG), highlighting the tasks and their dependencies. Nodes within the DAG represent individual tasks, each annotated with attributes such as deadlines and execution times. Directed edges between nodes depict the dependency relationships among tasks, signifying that a task can only commence once all its prerequisite tasks (predecessors) have been completed.

## Platform Model:
![Platform Model](platform.png)
The platform model showcases a single computational node responsible for executing the scheduled operations. Within this model, the node's scheduling decisions are guided by task deadlines to ensure that tasks with the nearest deadlines are given priority. The platform model emphasizes sequential task execution on the single computational node, maintaining adherence to the task dependencies defined in the application model.
## JSON Input
we describe the json input for the figure above. 
The input to the scheduling algorithms is a JSON object that describes the application and platform models. The application model includes tasks and messages, while the platform model includes nodes and links. The JSON input contains following objects and should conform to the [input JSON schema](README.md#api-input-schema-for-schedule-jobs).

- **Tasks**: Represent the tasks to be scheduled.
- **Messages**: Represent dependencies between tasks.
- **Nodes**: Represent the either a compute node where tasks can be executed or router in the network or a sensor or a actuators.
- **Links**: Represent the communication links between nodes.









## Earliest Deadline First (EDF) for Single Node

The Earliest Deadline First (EDF) algorithm is used to schedule tasks on a single computational node by prioritizing tasks based on their deadlines. The primary objective is to ensure tasks with the nearest deadlines are executed first, optimizing the schedule to meet critical time constraints and minimizing the risk of missed deadlines.

#### Scheduling Mechanism

##### Initialization

- The process begins with the identification and representation of all tasks and their dependencies within the Directed Acyclic Graph (DAG). Initial tasks, which have no dependencies (root nodes), are identified and marked as ready for scheduling.

##### Selection of Tasks

- Among the tasks that are ready for execution, the task with the earliest deadline is selected. This task is prioritized to ensure that the most time-sensitive operations are addressed first.

##### Task Execution

- The selected task is then scheduled on the computational node. The start time is determined based on the node's availability, and the task is executed for a duration corresponding to its WCET. The end time is calculated and recorded.

##### Dependency Resolution

- Upon the completion of a task, the scheduler evaluates its dependent tasks. If all dependencies of a subsequent task are resolved (i.e., all predecessor tasks are completed), this task becomes eligible for scheduling.

##### Iterative Scheduling

- The scheduling process iterates through the available tasks, continuously selecting and scheduling tasks based on their deadlines. The system dynamically updates the status of tasks and their dependencies, ensuring that at each step, the task with the nearest deadline is chosen.

##### Handling Deadline Misses

- If a task's execution is anticipated to exceed its deadline, it is marked as a missed deadline. The scheduler records such instances and evaluates the impact on subsequent tasks. Efforts are made to minimize the cascading effects of missed deadlines on the overall schedule.

##### Final Schedule Compilation

- At the conclusion of the scheduling process, a comprehensive schedule is compiled. This includes detailed records of task start and end times, deadlines, and any instances of missed deadlines. The final schedule provides a clear overview of task execution and node utilization.

#### Example
use figure and json input as reference and we keep the example output below.
Let's understand EDF scheduling for a single node with an example .

``` json
{
    "schedule": [
        {
            "task_id": 1,
            "node_id": 1,
            "start_time": 0,
            "end_time": 1,
            "deadline": 2
        },
        {
            "task_id": 3,
            "node_id": 1,
            "start_time": 1,
            "end_time": 2,
            "deadline": 4
        },
        {
            "task_id": 2,
            "node_id": 1,
            "start_time": 2,
            "end_time": 3,
            "deadline": 5
        },
        {
            "task_id": 4,
            "node_id": 1,
            "start_time": 3,
            "end_time": 4,
            "deadline": 3
        },
        {
            "task_id": 5,
            "node_id": 1,
            "start_time": 4,
            "end_time": 5,
            "deadline": 5
        },
        {
            "task_id": 6,
            "node_id": 1,
            "start_time": 5,
            "end_time": 6,
            "deadline": 6
        }

    ]
}
```

Consider the application model described above. Analyzing the order of tasks:

- **Task 1** must be completed first because it is the starting task with no dependencies.
- Next, based on available dependencies, **Tasks 3 and 2** are considered. Task 3 ($d_3=4$) has an earlier deadline than Task 2 ($d_2=5$).
- Task 2 is scheduled after Task 3 as the next available task with the next closest deadline.
- **Task 4** can only be scheduled after Task 2 is complete due to its dependency on Task 2, even though Task 4 has an earlier deadline ($d_4=3$) than Task 2.
- **Tasks 5 and 6** follow based on their deadlines, $d_5=5$ and $d_6=6$, and dependencies.


## Latest Deadline First (LDF) for Single Node

The Latest Deadline First (LDF) scheduling algorithm for a single node prioritizes tasks based on their latest deadlines, ensuring that tasks with the furthest deadlines are scheduled first. This strategy allows for more flexibility in handling tasks with earlier deadlines.

#### Scheduling Mechanism

##### Initialization

- The algorithm begins by identifying all tasks with no successors (leaf nodes) in the Directed Acyclic Graph (DAG). These tasks are initially added to the set of tasks that can be scheduled.

##### Selection of Tasks

- Among the tasks that can be scheduled, the task with the latest deadline is selected for execution. This ensures that tasks with the furthest deadlines are given priority.

##### Task Execution

- Once a task is selected, it is scheduled for execution on the single computational node. The start time is determined based on the completion time of the previously scheduled task, ensuring no overlap.

##### Dependency Management

- After scheduling a task, the algorithm updates the set of tasks that can be scheduled next. This involves checking the predecessors of the currently scheduled task. If all successors of a predecessor task have been scheduled, the predecessor task becomes eligible for scheduling.

##### Iterative Scheduling

- The scheduling process iterates through the available tasks, continuously selecting and scheduling tasks based on their latest deadlines. The system dynamically updates the status of tasks and their dependencies, ensuring that at each step, the task with the latest deadline is chosen.

##### Handling Task Completion and Deadlines

- The end time of each task is calculated based on its Worst-Case Execution Time (WCET). If a task's completion time exceeds its deadline, it is marked as a missed deadline. The algorithm continues this process until all tasks are scheduled.

This method maximizes the utilization of available time before their deadlines, while allowing tasks with earlier deadlines to be handled with the flexibility provided by scheduling tasks with later deadlines first. The LDF algorithm is particularly useful in scenarios where tasks with later deadlines are more critical or have higher priority for completion.

#### Example

do same as edf

Consider the application model described by the DAG in Figure 1. Analyzing the order of tasks:

``` json
{
    "schedule": [
        {
            "task_id": 1,
            "node_id": 1,
            "start_time": 0,
            "end_time": 1,
            "deadline": 2
        },
        {
            "task_id": 3,
            "node_id": 1,
            "start_time": 1,
            "end_time": 2,
            "deadline": 4
        },
        {
            "task_id": 2,
            "node_id": 1,
            "start_time": 2,
            "end_time": 3,
            "deadline": 5
        },
        {
            "task_id": 4,
            "node_id": 1,
            "start_time": 3,
            "end_time": 4,
            "deadline": 3
        },
        {
            "task_id": 5,
            "node_id": 1,
            "start_time": 4,
            "end_time": 5,
            "deadline": 5
        },
        {
            "task_id": 6,
            "node_id": 1,
            "start_time": 5,
            "end_time": 6,
            "deadline": 6
        }

    ]
}
```

- **Task 1** must be completed first because it is the starting task with no dependencies.
- Next, based on available dependencies, **Tasks 3 and 2** are considered. Task 2 ($d_2=5$) has a later deadline than Task 3 ($d_3=4$), so Task 2 is scheduled next.
- **Task 4** can only be scheduled after Task 2 is complete. Although Task 4 has a deadline of $d_4=3$, it cannot be executed until its predecessor (Task 2) has finished.
- **Tasks 5 and 6** follow based on their deadlines, $d_5=5$ and $d_6=6$, and dependencies.




### Earliest Deadline First (EDF) Multi-node

The Earliest Deadline First (EDF) scheduling algorithm for multiple nodes extends the single-node EDF strategy to a multi-node environment. Tasks are distributed across multiple computational nodes, with the goal of meeting task deadlines by prioritizing tasks with the earliest deadlines.

#### Scheduling Mechanism

##### Initialization

- **Identify Root Tasks:** The algorithm starts by scheduling tasks with no dependencies (root nodes). These tasks are distributed across available nodes for immediate execution.

##### Node Selection

- Tasks are assigned to nodes based on their availability, ensuring that tasks are scheduled on the first available node.

##### Task Distribution and Execution

- As root tasks are completed, the algorithm identifies tasks whose dependencies have been satisfied. Among these available tasks, the one with the earliest deadline is selected for scheduling.
- Tasks are executed on nodes based on the earliest available time, allowing for concurrent execution of independent tasks across multiple nodes.

##### Managing Dependencies

- The algorithm continuously updates the set of available tasks as each task gets scheduled and completed.
- Dependent tasks are scheduled only when all their prerequisite tasks have been completed, respecting task dependencies.

##### Handling Concurrent Execution

- EDF leverages the multi-node environment by scheduling independent tasks concurrently on different nodes.
- This parallel execution capability enhances scheduling efficiency, enabling more tasks to meet their deadlines.

##### Scheduling and Deadline Management

- Each task's start time depends on the completion time of preceding tasks on the assigned node.
- Task end times are calculated based on their Worst-Case Execution Time (WCET). Tasks exceeding their deadlines are marked as missed deadlines.
- By prioritizing tasks with the earliest deadlines, the algorithm reduces the likelihood of missed deadlines.

#### Example

Let's understand EDF scheduling in a multi-node environment with the same example used in previous sections.

Consider the application model described by the DAG in Figure 1. Analyzing the order of tasks:


- **Task 1** must be completed first because it is the starting task with no dependencies.
- Next, the algorithm considers **Tasks 2 and 3**. Task 3 ($d_3=4$) has an earlier deadline than Task 2 ($d_2=5$), so Task 3 is scheduled next.
- **Task 4** can only be scheduled after Task 2 is complete, despite Task 4 having a deadline of $d_4=3$.
- Finally, **Tasks 5 and 6** are scheduled based on their deadlines, $d_5=5$ and $d_6=6$, and dependencies.


### Latest Deadline First (LDF) Multi-node

The Latest Deadline First (LDF) scheduling algorithm for multiple nodes prioritizes tasks based on their latest deadlines in a distributed computing environment, ensuring tasks with imminent deadlines are processed first.

#### Scheduling Mechanism

##### Initialization

- **Initialize the Task Graph:** Start by constructing a directed acyclic graph (DAG) with nodes representing individual tasks and edges denoting task dependencies.

##### Identifying Leaf Nodes

- **Identify Leaf Nodes:** Begin by identifying leaf nodes—tasks without successors—indicating the tasks that can be scheduled first.

##### Task Scheduling Based on Latest Deadline

- **Schedule Leaf Nodes:** Schedule the leaf nodes based on their latest deadlines to prioritize tasks with closer deadlines for timely completion.

##### Node Selection and Assignment

- **Select Nodes for Execution:** Choose nodes for task execution based on their availability and the earliest start time, considering both node readiness and communication delays.
- **Utilize Shortest Path Algorithms:** Apply shortest path algorithms to determine minimal communication delays between nodes for tasks spanning across different nodes.

##### Dependency Management

- **Manage Task Dependencies:** Ensure that prerequisite tasks (predecessors) are completed before scheduling dependent tasks (successors).

##### Handling Concurrent Execution

- **Leverage Multi-node Environment:** Execute independent tasks concurrently across different nodes, maximizing parallelism and system efficiency.
- **Coordinate Task Execution:** Minimize idle time and maximize computational resource utilization during task execution.

##### Deadline Management and Missed Deadlines

- **Monitor Task Execution:** Track task execution against deadlines, recording instances where tasks exceed their deadlines as missed deadlines.
- **Adjust Scheduling Priorities:** Modify scheduling priorities based on missed deadlines to optimize task sequence and resource allocation.

#### Example

Let's understand LDF scheduling in a multi-node environment using the following example.

Consider the application model described by the DAG in Figure 1. Analyzing the order of tasks:


- **Task 1** must be completed first because it is the starting task with no dependencies.
- Next, the algorithm evaluates **Tasks 2 and 3**. Task 2 ($d_2=5$) has a later deadline than Task 3 ($d_3=4$), so Task 2 is scheduled next.
- **Task 4** can only be scheduled after Task 2 is complete. Although Task 4 has a deadline of $d_4=3$, it will not be executed until its predecessor (Task 2) has finished.
- Finally, **Tasks 5 and 6** are scheduled based on their deadlines, with $d_5=5$ and $d_6=6$, and dependencies.

### Least Laxity First (LLF)

The Least Laxity First (LLF) scheduling algorithm is designed for multi-node systems to prioritize tasks based on their laxity—the difference between a task’s deadline and its required execution time. LLF aims to minimize laxity by scheduling tasks with the least remaining time until their deadline first, thereby reducing the likelihood of missed deadlines.

#### Scheduling Mechanism

##### Initial Task Scheduling

1. **Identify Root Tasks:**
   - Start by identifying tasks with no unsatisfied dependencies (root nodes) that can be immediately scheduled.
   - Root tasks are prioritized for execution since they do not depend on any other tasks within the DAG.

2. **Calculate Laxity:**
   - Compute the laxity of each root task based on the current time and its attributes (deadline, WCET).
   - Laxity \( L_i \) for a task \( i \) is calculated as: 
   \[
   L_i = \text{deadline}_i - (\text{current time} + \text{WCET}_i)
   \]

##### Task Distribution and Execution

3. **Select Task with Least Laxity:**
   - From the set of root tasks, select the task with the smallest laxity value. This task is referred to as \( \text{task}_\text{min} \).

4. **Assign Task to Node:**
   - Allocate \( \text{task}_\text{min} \) to the node that has the earliest availability among the computational nodes.
   - Consider communication delays when scheduling tasks on different nodes to optimize execution time.

5. **Update Node Availability:**
   - Update the availability of the assigned node based on the scheduled task’s execution time.
   - \( \text{Node}_\text{avail} = \text{current time} + \text{WCET}_\text{min} \), where \( \text{WCET}_\text{min} \) is the execution time of \( \text{task}_\text{min} \).

##### Managing Dependencies

6. **Handle Task Dependencies:**
   - As tasks complete, evaluate the readiness of dependent tasks.
   - Schedule dependent tasks only when all prerequisite tasks have been successfully executed.

##### Deadline Management

7. **Monitor Deadlines:**
   - Continuously monitor task execution against deadlines.
   - If a task’s completion time exceeds its deadline, mark it as a missed deadline and adjust scheduling priorities accordingly.

##### Platform Data and Communication Delays

8. **Utilize Shortest Paths:**
   - Use shortest path algorithms (like Dijkstra's algorithm) to calculate communication delays between nodes.
   - Optimize task scheduling by selecting paths with minimal delays, ensuring efficient communication across the multi-node platform.

#### Example

Let’s understand LLF scheduling in a multi-node environment using the following example.

Consider the application model described by the DAG in Figure 1. Analyzing the order of tasks:


- **Task 1** must be completed first because it is the starting task with no dependencies.
- Next, the algorithm evaluates **Tasks 3 and 2**. Task 3 ($d_3=4$) has a later laxity than Task 2 ($d_2=5$), so Task 2 is scheduled next.
- **Task 4** can only be scheduled after Task 2 is complete, even though Task 4 has a deadline of $d_4=3$.
- Finally, **Tasks 5 and 6** are scheduled based on their deadlines, with $d_5=5$ and $d_6=6$, and dependencies.


### List Scheduling Algorithm for Multi-Node
The List Scheduling Algorithm for Multi-Node systems prioritizes tasks based on a pre-defined order, typically determined by task dependencies and deadlines. The primary goal is to ensure that no task misses its deadline, if possible, while considering task dependencies and the available nodes.

Scheduling Mechanism
Initialization
Task Priority List: The algorithm begins by constructing a list of tasks based on their priority. Tasks are arranged in this list according to a combination of factors, including:

Deadline: Tasks with earlier deadlines are prioritized.
Dependency Constraints: Tasks that depend on other tasks are scheduled only after their prerequisites are completed.
Identify Available Tasks: At the start, tasks with no unresolved dependencies (root tasks) are identified and marked as ready for execution.

Node Assignment and Task Scheduling
Task Selection: Among the ready tasks, the highest-priority task is selected from the task list.

The task with the nearest deadline or highest priority (based on the task list) is scheduled first.
Node Assignment: The selected task is assigned to the earliest available computational node.

Tasks are scheduled on the first node that becomes available, with communication delays between nodes taken into account.
Task Execution: Once assigned to a node, the task begins execution. The execution time depends on the node's availability and the task’s WCET.

Dependency Management
Update Dependencies: As tasks are completed, the algorithm updates the status of dependent tasks. Once all dependencies for a task are resolved, it becomes eligible for scheduling in the next cycle.
Iterative Scheduling
Iterative Task Selection: The scheduling process continues iteratively, selecting tasks from the list based on their priority, resolving dependencies, and assigning tasks to nodes as they become available.

Handling Deadline Misses: The algorithm checks if a task’s completion time exceeds its deadline. If so, the task is marked as a missed deadline. The scheduler then attempts to minimize the impact of such deadline misses on subsequent tasks.

Example
Consider the application model described by the DAG in Figure 1, with tasks ordered by their priority and deadlines. The tasks are scheduled as follows:
