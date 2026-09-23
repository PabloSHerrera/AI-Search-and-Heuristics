# AI Search and Heuristics

Maze-solving with classical AI search algorithms. Three 128×128 mazes are parsed from text files into graphs, and four search strategies are compared in terms of optimality, nodes explored, and execution time, using two different heuristics.

## Problem Setup

- **Mazes:** 128×128 grids (`1` = wall, `0` = free cell, `2` = start, `3` = goal)
- **Graph model:** each free cell is a node; edges connect 4-directional neighbors with unit cost
- **Experiments:** each algorithm runs from the maze's defined start and from a random start (fixed seed for reproducibility)

## Algorithms

| Algorithm | Type | Frontier |
|---|---|---|
| Breadth-First Search (BFS) | Uninformed | FIFO queue |
| Depth-First Search (DFS) | Uninformed | LIFO stack |
| Greedy Best-First Search (GBFS) | Informed | Priority queue on h(n) |
| A* | Informed | Priority queue on g(n) + h(n) |

**Heuristics:** Manhattan distance and Euclidean distance to the goal.

All data structures (FIFO/LIFO queues, priority queue, search nodes, and path reconstruction) are implemented from scratch.

## Results (defined start state)

| Algorithm | Maze 1 — nodes / path | Maze 2 — nodes / path | Maze 3 — nodes / path |
|---|---|---|---|
| BFS | 15,876 / **250** | 15,507 / **250** | 14,804 / **124** |
| DFS* | 251 / 249 | 367 / 365 | 125 / 123 |
| GBFS (Manhattan) | 250 / 250 | 354 / 276 | 124 / 124 |
| GBFS (Euclidean) | 250 / 250 | 435 / 280 | 151 / 136 |
| A* (Manhattan) | 3,123 / **250** | 3,416 / **250** | 785 / **124** |
| A* (Euclidean) | 15,653 / **250** | 13,557 / **250** | 2,850 / **124** |

*For DFS, the reported value is the maximum search depth reached.
Bold = optimal path.

## Key Findings

- **A* with Manhattan distance is the best trade-off:** it always finds the optimal path while exploring 78–95% fewer nodes than BFS.
- **The choice of heuristic matters:** on a 4-connected grid, Manhattan distance is a tighter admissible heuristic than Euclidean distance. As a result, A* with Euclidean distance explores 3.6–5× more nodes to reach the same optimal solution.
- **Greedy search is fast but not optimal:** GBFS explores very few nodes, but in Maze 2 its path is 10–12% longer than the optimum (276–280 vs. 250 steps).
- **DFS is cheap but unreliable:** it explores few nodes, but in Maze 2 it goes more than 100 steps deeper than the optimal solution.

## Repository Structure

| File | Description |
|---|---|
| `Proyecto_1_Codigo.ipynb` | Notebook with implementation and results |
| `Proyecto 1 codigo.py` | Standalone Python script version |
| `Laberinto1.txt` – `Laberinto3.txt` | Test mazes |

## Tech Stack

Python · pandas · heapq · Jupyter Notebook

## How to Run

```bash
git clone https://github.com/PabloSHerrera/AI-Search-and-Heuristics.git
cd AI-Search-and-Heuristics
python "Proyecto 1 codigo.py"
```

---

*Developed as part of the Artificial Intelligence course at Universidad del Valle de Guatemala.*
