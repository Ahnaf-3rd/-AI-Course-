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

def alphabeta(node, alpha, beta, is_max):  # Define the alphabeta function with current node, alpha, beta, and player turn
    if node in utility:  # Check if the current node is a terminal node
        return utility[node]  # Return the stored utility value
    if is_max:  # If it is the maximizer's turn
        value = -999999  # Initialize value to a very low number
        for child in tree[node]:  # Iterate over each child of the current node
            value = max(value, alphabeta(child, alpha, beta, False))  # Recursively call alphabeta for the child (minimizer's turn) and update the value
            alpha = max(alpha, value)  # Update alpha to the maximum of current alpha and value
            if beta <= alpha:  # Check if pruning condition is met
                break 
        return value  
    else:  # If it is the minimizer's turn
        value = 999999  # Initialize value to a very high number
        for child in tree[node]:  # Iterate over each child of the current node
            value = min(value, alphabeta(child, alpha, beta, True))  # Recursively call alphabeta for the child and update the value
            beta = min(beta, value)  # Update beta to the minimum of current beta and value
            if beta <= alpha:  # Check if pruning condition is met
                break  
        return value  

start = input("Enter root node: ")  # Read the root node of the tree
value = alphabeta(start, -999999, 999999, True)  # Call alphabeta starting from the root (maximizer's turn) with initial alpha and beta set to -∞ and +∞
print("Alpha-Beta value of root:", value) 
