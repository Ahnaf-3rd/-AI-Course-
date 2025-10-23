# Get graph from user
graph = {}
nodes = input("Enter all nodes (separated by spaces): ").split()
for node in nodes:
    neighbors = input(f"Enter neighbors of {node} (separated by spaces, or press Enter if none): ").split()
    graph[node] = neighbors

start_node = input("Enter starting node: ")

# DFS Algorithm (iterative version)
def dfs(graph, start):
    visited = []
    stack = [start]  # Use a stack instead of a queue
    
    while stack:
        current_node = stack.pop()  # Take last node added
        if current_node not in visited:
            visited.append(current_node)
            # Add unvisited neighbors to the stack in reverse order
            for neighbor in reversed(graph.get(current_node, [])):
                if neighbor not in visited:
                    stack.append(neighbor)
    return visited

# Run DFS and show result
result = dfs_rec(graph, start_node)
print("DFS traversal order:", " -> ".join(result))
