graph = {}
nodes = input("Enter nodes (space separated): ").split()
for node in nodes:
    neighbors = input(f"Neighbors of {node}: ").split()
    graph[node] = neighbors

start = input("Start node: ")
goal = input("Goal node: ")

if start == goal:
    print(f"Path: {start}")
    exit()  # Exit if start=goal

def dls(current, goal, depth, path):
    new_path = path + [current]
    
    if current == goal:
        return new_path  # Found path!
        
    if depth <= 0:
        return None  # Depth limit reached
        
    for neighbor in graph.get(current, []):
        if neighbor not in new_path:  # Avoid cycles
            result = dls(neighbor, goal, depth-1, new_path)
            if result is not None:
                return result  # Return first path found
    return None

max_depth = len(graph)
path_found = False  # Track if ANY path was found

# Search deeper and deeper
for depth in range(1, max_depth + 1):
    result = dls(start, goal, depth, [])
    if result:
        print(f"Path at depth {depth}:", " -> ".join(result))
        path_found = True
        # Don't exit here! Just break to stop deepening
        break  # Stop after finding the SHORTEST path

if not path_found:
    print(f"No path between {start} and {goal}")
