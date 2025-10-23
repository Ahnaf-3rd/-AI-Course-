tree = {}  # Dictionary to store the children of each non-terminal node
utility = {}  # Dictionary to store the utility value of each terminal node

n = int(input("Enter number of nodes: "))  # Read the total number of nodes in the tree
for i in range(n):  # Loop through each node to collect values
    node = input("Enter node: ")  # Read the name of the current node
    children = input("Enter children of this node (space separated, or '-' if none): ").split()  # Read the children of the current node
    if children[0] != "-":  # Check if the node has children
        tree[node] = children  # Store the children list in the tree dictionary
    else:  # If the node has no children (terminal node)
        val = int(input("Enter utility value of this terminal node (-1, 0, 1): "))  # Read the utility value for the terminal node
        utility[node] = val  # Store the utility value in the utility dictionary

def minimax(node, is_max):  # Define the minimax function with current node and player turn
    if node in utility:  # Check if the current node is a terminal node
        return utility[node]  # Return the stored utility value
    if is_max:  # If it is the maximizer's turn
        best = -999999  # Initialize best value to a very low number
        for child in tree[node]:  # Iterate over each child of the current node
            best = max(best, minimax(child, False))  # Recursively call minimax for the child (minimizer's turn) and update the best value
        return best  # Return the best value found
    else:  # If it is the minimizer's turn
        best = 999999  # Initialize best value to a very high number
        for child in tree[node]:  # Iterate over each child of the current node
            best = min(best, minimax(child, True))  # Recursively call minimax for the child (maximizer's turn) and update the best value
        return best  # Return the best value found

start = input("Enter root node: ")  # Read the root node of the tree
value = minimax(start, True)  # Call minimax starting from the root (maximizer's turn)
print("Min-Max value of root:", value)  # Print the result
