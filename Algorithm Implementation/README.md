# Algorithm Implementation

This folder contains implementations of fundamental AI search algorithms.

## Algorithms Included:

### 1. Breadth-First Search (BFS)
**How it works:**
- Explores all nodes at the present depth level before moving to nodes at the next depth level
- Uses a queue data structure (FIFO)
- Guarantees finding the shortest path in unweighted graphs

**Applications:**
- Web crawling
- Social networking (finding connections)
- GPS navigation systems
- Finding connected components in graphs

**Complexity:**
- Time: O(V + E) where V = vertices, E = edges
- Space: O(V)

**Input/Output:**
![BFS Example](images/bfs_example.png)

---

### 2. Depth-First Search (DFS)
**How it works:**
- Explores as far as possible along each branch before backtracking
- Uses a stack data structure (LIFO)
- Can be implemented recursively or iteratively

**Applications:**
- Solving mazes
- Topological sorting
- Path finding
- Cycle detection in graphs

**Complexity:**
- Time: O(V + E)
- Space: O(V)

**Input/Output:**
![DFS Example](images/dfs_example.png)

---

### 3. Iterative Deepening Search (IDS)
**How it works:**
- Combines benefits of BFS and DFS
- Performs DFS with increasing depth limits
- Guarantees optimal solution like BFS with DFS memory efficiency

**Applications:**
- Game tree search
- Puzzle solving
- When search space is large and depth unknown

**Complexity:**
- Time: O(b^d) where b = branching factor, d = depth
- Space: O(d)

**Input/Output:**
![IDS Example](images/ids_example.png)

---

### 4. Bidirectional Search
**How it works:**
- Runs two simultaneous searches: forward from start and backward from goal
- Stops when the two searches meet
- Can significantly reduce search space

**Applications:**
- Route planning
- Social network connections
- Database query optimization

**Complexity:**
- Time: O(b^(d/2)) - exponential speedup
- Space: O(b^(d/2))

**Input/Output:**
![Bidirectional Example](images/bidirectional_example.png)

---

### 5. Alpha-Beta Pruning
**How it works:**
- Optimization of minimax algorithm
- Eliminates branches that cannot influence final decision
- Uses alpha (best already explored for max) and beta (best already explored for min) values

**Applications:**
- Game playing AI (chess, checkers)
- Decision making in competitive environments
- Resource allocation games

**Complexity:**
- Time: O(b^(d/2)) - effectively doubles search depth
- Space: O(d)

**Input/Output:**
![Alpha-Beta Example](images/alphabeta_example.png)

---

### 6. Minimax Algorithm
**How it works:**
- Zero-sum game decision algorithm
- Maximizes player's minimum gain (maximizes worst-case scenario)
- Minimizes opponent's maximum gain
- Recursively evaluates game tree

**Applications:**
- Turn-based games (tic-tac-toe, chess)
- Decision theory
- Economics and auction theory

**Complexity:**
- Time: O(b^d)
- Space: O(bd)

**Input/Output:**
![Minimax Example](images/minimax_example.png)

---

### 7. Depth-Limited Search (DLS)
**How it works:**
- DFS with predetermined depth limit
- Prevents infinite loops in infinite graphs
- May not find solution if depth limit is too small

**Applications:**
- Web crawling with depth constraints
- Game playing with time limits
- Exploratory data analysis

**Complexity:**
- Time: O(b^l) where l = depth limit
- Space: O(bl)

**Input/Output:**
![DLS Example](images/dls_example.png)

---

### 8. Beam Search
**How it works:**
- Variation of breadth-first search
- Keeps only the most promising nodes at each level (beam width)
- Memory-efficient but not complete

**Applications:**
- Speech recognition
- Machine translation
- DNA sequence alignment

**Complexity:**
- Time: O(b × w × d) where w = beam width
- Space: O(w)

**Input/Output:**
![Beam Search Example](images/beam_example.png)

---

### 9. Best-First Search
**How it works:**
- Uses heuristic function to determine which node to expand next
- Prioritizes nodes that appear to be closest to goal
- Uses priority queue instead of simple queue/stack

**Applications:**
- Route finding with estimates
- Puzzle solving
- Resource allocation

**Complexity:**
- Time: O(b^d) in worst case
- Space: O(b^d)

**Input/Output:**
![Best-First Example](images/bestfirst_example.png)

---

### 10. A* Search Algorithm
**How it works:**
- Combines uniform cost search and greedy best-first search
- Uses evaluation function f(n) = g(n) + h(n)
- g(n) = cost from start to n, h(n) = heuristic estimate to goal
- Optimal if heuristic is admissible

**Applications:**
- Pathfinding in games
- Robotics navigation
- Natural language processing
- Network routing

**Complexity:**
- Time: O(b^d)
- Space: O(b^d)

**Input/Output:**
![A* Example](images/astar_example.png)

## File Structure
