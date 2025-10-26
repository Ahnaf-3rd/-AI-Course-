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
<img width="1920" height="1078" alt="alphabetaai and 2 more pages - Personal - Microsoft​ Edge 10_26_2025 6_11_20 PM" src="https://github.com/user-attachments/assets/6093ae00-ea26-4dff-850e-794018851448" />


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
<img width="1920" height="1078" alt="alphabetaai and 2 more pages - Personal - Microsoft​ Edge 10_26_2025 6_11_53 PM" src="https://github.com/user-attachments/assets/03a8ffcb-b178-444f-a14f-142caad02dcc" />


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
<img width="1920" height="1078" alt="alphabetaai and 2 more pages - Personal - Microsoft​ Edge 10_26_2025 6_12_25 PM" src="https://github.com/user-attachments/assets/f3711e62-e682-4cef-822e-338ad875f3da" />


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
<img width="1920" height="1078" alt="alphabetaai and 2 more pages - Personal - Microsoft​ Edge 10_26_2025 6_11_37 PM" src="https://github.com/user-attachments/assets/b36fa090-a7d9-4a15-8d17-2dd63a545b0c" />


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


---<img width="1920" height="1078" alt="alphabetaai and 2 more pages - Personal - Microsoft​ Edge 10_26_2025 6_01_35 PM" src="https://github.com/user-attachments/assets/3f9f0f3c-8b20-4dda-aacc-3a4a73bc940e" />


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
<img width="1920" height="1078" alt="alphabetaai and 2 more pages - Personal - Microsoft​ Edge 10_26_2025 6_12_48 PM" src="https://github.com/user-attachments/assets/41dc30a5-69a4-4c21-a7b4-73a35d51518e" />


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
<img width="1920" height="1078" alt="alphabetaai and 2 more pages - Personal - Microsoft​ Edge 10_26_2025 6_12_09 PM" src="https://github.com/user-attachments/assets/95722c38-1313-4d99-9186-9a9ca69f9aaf" />


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

<img width="1920" height="1078" alt="alphabetaai and 2 more pages - Personal - Microsoft​ Edge 10_26_2025 6_10_49 PM" src="https://github.com/user-attachments/assets/27fe5493-3455-4d6c-a741-24b6f524a179" />

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

<img width="1920" height="1078" alt="alphabetaai and 2 more pages - Personal - Microsoft​ Edge 10_26_2025 6_11_20 PM" src="https://github.com/user-attachments/assets/d83cf5c2-d09a-49cf-bba5-c5dc91e30e6e" />

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

<img width="1920" height="1078" alt="alphabetaai and 2 more pages - Personal - Microsoft​ Edge 10_26_2025 6_10_24 PM" src="https://github.com/user-attachments/assets/234caff2-5b75-4f0c-ae35-289dd2462959" />

