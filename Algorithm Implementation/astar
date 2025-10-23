graph = {}       # Dictionary to store adjacency list with edge weights for each node
heuristic = {}   # Dictionary to store heuristic values for each node
cost = {}        # Dictionary to store cumulative cost from start to each node

# Input graph with edge weights
n = int(input("Enter number of edges: "))  # Read the number of edges
for i in range(n):
    u, v, w = input("Enter edge (u v w): ").split()  # Read edge from u to v with weight w
    w = int(w)  # Convert weight to integer
    if u not in graph:
        graph[u] = []  
    if v not in graph:
        graph[v] = []  
    graph[u].append((v, w))  
    graph[v].append((u, w))  

# Input heuristic values
m = int(input("Enter number of heuristic values: "))  
for i in range(m):
    node, h = input("Enter node and heuristic: ").split()  
    heuristic[node] = int(h) 

start = input("Enter start node: ")  
goal = input("Enter goal node: ")    

open_list = [start]    # Nodes to explore, initialized with start
closed_list = []       # Nodes already visited
cost[start] = 0 # Cost to reach start node is 0
novisit_list = []
parent = {start: None} # Dictionary to keep track of parent nodes (for path reconstruction)

while open_list: 
    open_list.sort(key=lambda x: cost[x] + heuristic[x])  # Sort by f(n) = g(n) + h(n)
    """lambda x: heuristic[x] is an anonymous function that takes one input x and returns heuristic[x].

In this context:

x is a node from next_level.

heuristic[x] is the heuristic value of that node."""
    current = open_list.pop(0)  # Pick node with lowest f(n)
    if cost [current] < cost[open_list]:
        novisit[current]
    print("Not visiting this:", novisit)
    print("Visiting:", current) 
    if current == goal:  
        print("Goal reached!")
        # Reconstruct the path from goal back to start using parent dictionary
        path = []
        while current is not None:
            path.append(current)
            current = parent[current]
        path.reverse()  # Reverse to get path from start to goal
        print("Path:", " -> ".join(path)) 
        break
    closed_list.append(current)  # Mark current node as visited
    for neighbor, w in graph[current]:  # Explore neighbors of current node
        if neighbor in closed_list:  
            continue
        new_cost = cost[current] + w  # Calculate cost to reach neighbor via current
        if neighbor not in open_list or new_cost < cost.get(neighbor, 999999):  # If neighbor not in open_list or new path is cheaper
            cost[neighbor] = new_cost  # Update cost to neighbor
            parent[neighbor] = current  # Set current as parent of neighbor
            if neighbor not in open_list:  # If neighbor not yet in open_list
                open_list.append(neighbor)  # Add neighbor for future exploration
