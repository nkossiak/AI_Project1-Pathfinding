from collections import deque #For BFS
import heapq #For Uniform, Greedy and A*
import math # For Euclidean heuristic

TERRAIN_COST = {
    "R": 1,
    "F": 3,
    "O": 5,
    "H": 8,
    "M": 15,
    "S": 0,
    "E": 0
}


#Store results of algorithm: path taken, total cost, stats
class SearchResult:
    def __init__(self, path, path_cost, closed_list, open_list):
        self.path = path
        self.path_cost = path_cost
        self.closed_list = closed_list
        self.open_list = open_list

        self.path_length = max(0, len(path) - 1)
        self.states_explored = len(closed_list)
        self.states_remaining = len(open_list)


#Get neighboring nodes (up, down, left, right)
def get_neighbors(grid, position):
    row, col = position

    possible_neighbors = [
        (row - 1, col),  # up
        (row + 1, col),  # down
        (row, col - 1),  # left
        (row, col + 1)   # right
    ]

    valid_neighbors = []

    for r, c in possible_neighbors:
        if r < 0 or r >= len(grid):
            continue

        if c < 0 or c >= len(grid[0]):
            continue

        if grid[r][c] == "W":
            continue

        valid_neighbors.append((r, c))

    return valid_neighbors


#Calculate total cost
def calculate_path_cost(grid, path):
    if not path:
        return None

    total_cost = 0

    # Skip first cell because we start there.
    for row, col in path[1:]:
        terrain = grid[row][col]
        total_cost += TERRAIN_COST[terrain]

    return total_cost


#Backtrack
def reconstruct_path(came_from, start, end):
    if end not in came_from:
        return []

    path = []
    current = end

    while current is not None:
        path.append(current)
        current = came_from[current]

    path.reverse()
    return path


# HEURISTIC-1: Manhattan
def manhattan(position, end):
    row1, col1 = position
    row2, col2 = end

    return abs(row1 - row2) + abs(col1 - col2)

# HEURISTIC-2: Euclidean
def euclidean(position, end):
    row1, col1 = position
    row2, col2 = end

    return math.sqrt((row1 - row2) ** 2 + (col1 - col2) ** 2)


#ALGORITHM-1:Breadth-First Search (BFS)
def bfs(grid, start, end):
    open_list = deque()
    open_list.append(start)

    closed_list = set()

    came_from = {}
    came_from[start] = None

    while open_list:
        current = open_list.popleft()

        if current in closed_list:
            continue

        closed_list.add(current)

        if current == end:
            break

        for neighbor in get_neighbors(grid, current):
            if neighbor not in closed_list and neighbor not in came_from:
                came_from[neighbor] = current
                open_list.append(neighbor)

    path = reconstruct_path(came_from, start, end)
    path_cost = calculate_path_cost(grid, path)
    remaining_open_list = set(open_list)

    return SearchResult(path, path_cost, closed_list, remaining_open_list)

# ALGORITHM-2: Uniform Cost Search
def uniform_cost_search(grid, start, end):
    open_list = []
    heapq.heappush(open_list, (0, start))

    closed_list = set()

    came_from = {}
    came_from[start] = None

    cost_so_far = {}
    cost_so_far[start] = 0

    while open_list:
        current_cost, current = heapq.heappop(open_list)

        if current in closed_list:
            continue

        closed_list.add(current)

        if current == end:
            break

        for neighbor in get_neighbors(grid, current):
            terrain = grid[neighbor[0]][neighbor[1]]
            new_cost = cost_so_far[current] + TERRAIN_COST[terrain]

            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                came_from[neighbor] = current

                priority = new_cost
                heapq.heappush(open_list, (priority, neighbor))

    path = reconstruct_path(came_from, start, end)
    path_cost = cost_so_far.get(end, None)
    remaining_open_list = {position for priority, position in open_list}

    return SearchResult(path, path_cost, closed_list, remaining_open_list)


# ALGORITHM-3: Greedy Best-First Search
def greedy_best_first_search(grid, start, end):
    open_list = []
    heapq.heappush(open_list, (0, start))

    closed_list = set()

    came_from = {}
    came_from[start] = None

    while open_list:
        priority, current = heapq.heappop(open_list)

        if current in closed_list:
            continue

        closed_list.add(current)

        if current == end:
            break

        for neighbor in get_neighbors(grid, current):
            if neighbor not in closed_list and neighbor not in came_from:
                came_from[neighbor] = current

                priority = manhattan(neighbor, end)
                heapq.heappush(open_list, (priority, neighbor))

    path = reconstruct_path(came_from, start, end)
    path_cost = calculate_path_cost(grid, path)
    remaining_open_list = {position for priority, position in open_list}

    return SearchResult(path, path_cost, closed_list, remaining_open_list)


# ALGORITHM-4/5: A* Search
def a_star(grid, start, end, heuristic):
    open_list = []
    heapq.heappush(open_list, (0, start))

    closed_list = set()

    came_from = {}
    came_from[start] = None

    cost_so_far = {}
    cost_so_far[start] = 0

    while open_list:
        priority, current = heapq.heappop(open_list)

        if current in closed_list:
            continue

        closed_list.add(current)

        if current == end:
            break

        for neighbor in get_neighbors(grid, current):
            terrain = grid[neighbor[0]][neighbor[1]]
            new_cost = cost_so_far[current] + TERRAIN_COST[terrain]

            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                came_from[neighbor] = current

                priority = new_cost + heuristic(neighbor, end)
                heapq.heappush(open_list, (priority, neighbor))

    path = reconstruct_path(came_from, start, end)
    path_cost = cost_so_far.get(end, None)
    remaining_open_list = {position for priority, position in open_list}

    return SearchResult(path, path_cost, closed_list, remaining_open_list)



#Extra: Animation for personal purposes
def animated_search(grid, start, end, algorithm_type, draw_step, heuristic=None):
    if algorithm_type == "bfs":
        open_list = deque()
        open_list.append(start)
    else:
        open_list = []
        heapq.heappush(open_list, (0, start))

    closed_list = set()

    came_from = {}
    came_from[start] = None

    cost_so_far = {}
    cost_so_far[start] = 0

    while open_list:
        if algorithm_type == "bfs":
            current = open_list.popleft()
        else:
            priority, current = heapq.heappop(open_list)

        if current in closed_list:
            continue

        closed_list.add(current)

        if current == end:
            break

        for neighbor in get_neighbors(grid, current):
            terrain = grid[neighbor[0]][neighbor[1]]
            new_cost = cost_so_far[current] + TERRAIN_COST[terrain]

            if algorithm_type == "bfs":
                if neighbor not in closed_list and neighbor not in came_from:
                    came_from[neighbor] = current
                    cost_so_far[neighbor] = new_cost
                    open_list.append(neighbor)

            elif algorithm_type == "ucs":
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    came_from[neighbor] = current
                    heapq.heappush(open_list, (new_cost, neighbor))

            elif algorithm_type == "greedy":
                if neighbor not in closed_list and neighbor not in came_from:
                    came_from[neighbor] = current
                    cost_so_far[neighbor] = new_cost
                    priority = heuristic(neighbor, end)
                    heapq.heappush(open_list, (priority, neighbor))

            elif algorithm_type == "astar":
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    came_from[neighbor] = current
                    priority = new_cost + heuristic(neighbor, end)
                    heapq.heappush(open_list, (priority, neighbor))

        if algorithm_type == "bfs":
            current_open_list = set(open_list)
        else:
            current_open_list = {position for priority, position in open_list if position not in closed_list}

        current_path = reconstruct_path(came_from, start, current)

        draw_step(closed_list, current_open_list, current_path)

    path = reconstruct_path(came_from, start, end)
    path_cost = calculate_path_cost(grid, path)

    if algorithm_type == "bfs":
        remaining_open_list = set(open_list)
    else:
        remaining_open_list = {position for priority, position in open_list if position not in closed_list}

    return SearchResult(path, path_cost, closed_list, remaining_open_list)