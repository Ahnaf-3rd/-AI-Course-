graph = {}
heuristic = {}

# Input graph edges
n = int(input("Enter number of edges: "))
for i in range(n):
    u, v = input("Enter edge (u v): ").split()
    if u not in graph:
        graph[u] = []  
    if v not in graph:
        graph[v] = [] 
    graph[u].append(v)  
    graph[v].append(u) 

# Input heuristic values for nodes
m = int(input("Enter number of heuristic values: "))
for i in range(m):
    node, h = input("Enter node and heuristic: ").split()
    heuristic[node] = int(h)

start = input("Enter start node: ")
goal = input("Enter goal node: ")
beam_width = int(input("Enter beam width: "))  # Max number of nodes to keep at each level

open_list = [start]  # Nodes to explore at current level
closed_list = []     # Already visited nodes

while open_list:
    next_level = []  # Collect nodes for the next level
    for current in open_list:
        print("Visiting:", current)
        if current == goal:
            print("Goal reached!")
            exit()  # Stop search immediately if goal is found

        closed_list.append(current)  # Mark current node as visited
        for neighbor in graph[current]:
            # Add unvisited neighbors to next level
            if neighbor not in closed_list and neighbor not in next_level:
                next_level.append(neighbor)

    # Sort next level by heuristic and keep only top 'beam_width' nodes
    next_level.sort(key=lambda x: heuristic[x])
    """lambda x: heuristic[x] is an anonymous function that takes one input x and returns heuristic[x].

In this context:

x is a node from next_level.

heuristic[x] is the heuristic value of that node."""
    open_list = next_level[:beam_width]  # Update open_list for next iteration
