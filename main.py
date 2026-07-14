from search import bfs, uniform_cost_search, greedy_best_first_search, a_star, manhattan, euclidean
from mapdisplay import run_menu


# Read map from file and store it in a 2D list
def read_map(filename):
    grid = []

    with open(filename, "r") as file:
        for line in file:
            row = list(line.strip())
            grid.append(row)

    return grid


# Check if map is valid
def validate_map(grid):
    if len(grid) != 40:
        print("Error: map does not have 40 rows.")
        return False

    for row in grid:
        if len(row) != 40:
            print("Error: map does not have 40 columns.")
            return False

    return True


# Find where Start and End are
def find_start_and_end(grid):
    start = None
    end = None

    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == "S":
                start = (row, col)
            elif grid[row][col] == "E":
                end = (row, col)

    return start, end


def main():
    # menu options for running maps and algorithms
    maps = [
        ("Map 1", "map1_stupid.txt", "map1"),
        ("Map 2", "map2_simple.txt", "map2"),
        ("Map 3", "map3_complex.txt", "map3")
    ]

    algorithms = [
        ("BFS", bfs, "bfs"),
        ("Uniform", uniform_cost_search, "ucs"),
        ("Greedy", greedy_best_first_search, "greedy"),
        ("A* M", lambda grid, start, end: a_star(grid, start, end, manhattan), "astar_manhattan"),
        ("A* E", lambda grid, start, end: a_star(grid, start, end, euclidean), "astar_euclidean")
    ]

    run_menu(
        maps,
        algorithms,
        read_map,
        validate_map,
        find_start_and_end
    )


main()