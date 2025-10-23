from collections import deque

# Get graph from user
graph = {}
nodes = input("Enter all nodes (separated by spaces): ").split()
for node in nodes:
    neighbors = input(f"Enter neighbors of {node} (separated by spaces, or press Enter if none): ").split()
    graph[node] = neighbors

start_node = input("Enter starting node: ")

# BFS Algorithm
def bfs(graph, start):
    visited = []
    queue = deque([start])
    
    while queue:
        current_node = queue.popleft()
        if current_node not in visited:
            visited.append(current_node)
            # Add unvisited neighbors to the queue
            for neighbor in graph.get(current_node, []):
                if neighbor not in visited:
                    queue.append(neighbor)
    return visited

# Run BFS and show result
result = bfs(graph, start_node)
print("BFS traversal order:", " -> ".join(result))
