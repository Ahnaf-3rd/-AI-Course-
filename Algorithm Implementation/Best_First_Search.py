graph = {}      
heuristic = {}  

# Input graph
n = int(input("Enter number of edges: ")) 
for i in range(n):
    u, v = input("Enter edge (u v): ").split()  
    if u not in graph:
        graph[u] = []  
    if v not in graph:
        graph[v] = []  
    graph[u].append(v) 
    graph[v].append(u) 

# Input heuristic values
m = int(input("Enter number of heuristic values: ")) 
for i in range(m):
    node, h = input("Enter node and heuristic: ").split() 
    heuristic[node] = int(h)  # Store heuristic value for the node

start = input("Enter start node: ")  
goal = input("Enter goal node: ")    

open_list = [start]   # Initialize open list with start node (nodes to be explored)
closed_list = []      # Initialize closed list (nodes already visited)

while open_list:  
    open_list.sort(key=lambda x: heuristic[x])  # Sort open list by heuristic value (lowest first)
    """lambda x: heuristic[x] is an anonymous function that takes one input x and returns heuristic[x].

In this context:

x is a node from next_level.

heuristic[x] is the heuristic value of that node."""
    current = open_list.pop(0)  # Select node with lowest heuristic as current
    print("Visiting:", current)  
    if current == goal: 
        print("Goal reached!")  
        break  
    closed_list.append(current)  # Mark current node as visited by adding it to closed list
    for neighbor in graph[current]:  # Explore all neighbors of current node
        if neighbor not in closed_list and neighbor not in open_list:  
            # If neighbor has not been visited and is not already in open list
            open_list.append(neighbor)  # Add neighbor to open list for future exploration
