# Build the cave map
graph = {}
nodes = input("Enter rooms (A B C...): ").split()
for node in nodes:
    neighbors = input(f"Where can you go from {node}? (Ex: B C): ").split()
    graph[node] = neighbors

start = input("Start room: ")
goal = input("Treasure room: ")
max_depth = int(input("Flashlight range (max depth): "))

# DLS Exploration Machine
def dls(current, target, depth, path):
    new_path = path + [current]  # Add current room to path
    
    if current == target:
        return new_path  # Found treasure!
    
    if depth >= max_depth:  # Flashlight can't shine further
        return None  # Out of range
    
    # Check connecting tunnels
    for neighbor in graph.get(current, []):
        if neighbor in new_path:  # Skip already visited rooms
            continue
        # Explore deeper (increase depth by 1)
        result = dls(neighbor, target, depth + 1, new_path)
        if result:  # If treasure found in this path
            return result
            
    return None  # Treasure not found this way

# Start the search!
path = dls(start, goal, 0, [])  # Start at depth=0 with empty path

if path:
    print("Path to treasure:", " → ".join(path))
else:
    print(f"Treasure not found within {max_depth} steps")
