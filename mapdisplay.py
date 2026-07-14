import os
import pygame

from search import animated_search, manhattan, euclidean


CELL_SIZE = 16
ROWS = 40
COLS = 40
MAP_WIDTH = COLS * CELL_SIZE
MAP_HEIGHT = ROWS * CELL_SIZE
LEGEND_WIDTH = 300

WINDOW_WIDTH = MAP_WIDTH + LEGEND_WIDTH
WINDOW_HEIGHT = MAP_HEIGHT


# Extra: Terrain textures
# Hills intentionally do not have an image.
TILE_IMAGE_FILES = {
    "R": "tiles/road.png",
    "F": "tiles/field.png",
    "O": "tiles/forest.png",
    "M": "tiles/mountain.png",
    "W": "tiles/water.png",
    "S": "tiles/start.png",
    "E": "tiles/end.png"
}


TERRAIN_COLORS = {
    "R": (128, 128, 128),    # gray
    "F": (144, 238, 144),    # light green
    "O": (0, 100, 0),        # dark green
    "H": (120, 110, 70),     # olive-brown green
    "M": (144, 238, 144),    # light green
    "W": (0, 0, 255),        # blue
    "S": (255, 165, 0),      # orange
    "E": (255, 0, 0)         # red
}

CLOSED_COLOR = (200, 150, 200)          # lilac
CLOSED_LEGEND_COLOR = (170, 155, 170)   # muted lilac/gray for legend
OPEN_COLOR = (255, 255, 255)            # white
PATH_COLOR = (0, 0, 0)                  # black


def load_tile_images():
    tile_images = {}

    for terrain, filename in TILE_IMAGE_FILES.items():
        if os.path.exists(filename):
            image = pygame.image.load(filename).convert_alpha()
            image = pygame.transform.scale(image, (CELL_SIZE, CELL_SIZE))
            tile_images[terrain] = image

    return tile_images


def draw_grid(screen, grid, tile_images):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            terrain = grid[row][col]
            color = TERRAIN_COLORS[terrain]

            rect = pygame.Rect(
                col * CELL_SIZE,
                row * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
            pygame.draw.rect(screen, color, rect)

            # Draw sprite on top
            if terrain in tile_images:
                screen.blit(tile_images[terrain], (rect.x, rect.y))

            # pygame.draw.rect(screen, (100, 100, 100), rect, 1)


def draw_overlay_cells(screen, cells, color, alpha):
    overlay = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
    overlay.fill((color[0], color[1], color[2], alpha))

    for row, col in cells:
        x = col * CELL_SIZE
        y = row * CELL_SIZE
        screen.blit(overlay, (x, y))


def redraw_start_end(screen, grid, tile_images):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == "S" or grid[row][col] == "E":
                terrain = grid[row][col]
                color = TERRAIN_COLORS[terrain]

                rect = pygame.Rect(
                    col * CELL_SIZE,
                    row * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE
                )

                pygame.draw.rect(screen, color, rect)

                if terrain in tile_images:
                    screen.blit(tile_images[terrain], (rect.x, rect.y))

                pygame.draw.rect(screen, (0, 0, 0), rect, 1)


def draw_legend_tile(screen, x, y, terrain, color, tile_images):
    color_box = pygame.Rect(x, y, 20, 20)

    pygame.draw.rect(screen, color, color_box)

    if terrain in tile_images:
        small_image = pygame.transform.scale(tile_images[terrain], (20, 20))
        screen.blit(small_image, (x, y))

    pygame.draw.rect(screen, (0, 0, 0), color_box, 1)


def draw_plain_legend_box(screen, x, y, color):
    color_box = pygame.Rect(x, y, 20, 20)
    pygame.draw.rect(screen, color, color_box)
    pygame.draw.rect(screen, (0, 0, 0), color_box, 1)


def draw_menu_panel(
    screen,
    font,
    small_font,
    maps,
    algorithms,
    selected_map_index,
    selected_algorithm_index,
    map_dropdown_open,
    algorithm_dropdown_open,
    title,
    result,
    tile_images
):
    panel_x = MAP_WIDTH
    legend_x = MAP_WIDTH + 15

    # Sidebar background
    pygame.draw.rect(screen, (245, 245, 245), (panel_x, 0, LEGEND_WIDTH, WINDOW_HEIGHT))

    # Compact dropdown positions
    map_label_x = legend_x
    map_dropdown_x = legend_x

    algo_label_x = legend_x + 100
    algo_dropdown_x = legend_x + 100

    y_top = 15

    # Map label
    map_label = small_font.render("Map:", True, (0, 0, 0))
    screen.blit(map_label, (map_label_x, y_top))

    # Algorithm label
    algorithm_label = small_font.render("Algorithm:", True, (0, 0, 0))
    screen.blit(algorithm_label, (algo_label_x, y_top))

    # Map dropdown
    map_dropdown_rect = pygame.Rect(map_dropdown_x, y_top + 20, 80, 28)
    pygame.draw.rect(screen, (255, 255, 255), map_dropdown_rect)
    pygame.draw.rect(screen, (0, 0, 0), map_dropdown_rect, 1)

    selected_map_text = small_font.render(maps[selected_map_index][0], True, (0, 0, 0))
    screen.blit(selected_map_text, (map_dropdown_x + 8, y_top + 26))

    # Algorithm dropdown
    algorithm_dropdown_rect = pygame.Rect(algo_dropdown_x, y_top + 20, 145, 28)
    pygame.draw.rect(screen, (255, 255, 255), algorithm_dropdown_rect)
    pygame.draw.rect(screen, (0, 0, 0), algorithm_dropdown_rect, 1)

    selected_algorithm_text = small_font.render(algorithms[selected_algorithm_index][0], True, (0, 0, 0))
    screen.blit(selected_algorithm_text, (algo_dropdown_x + 8, y_top + 26))

    # Dropdown options
    if map_dropdown_open:
        for i, map_item in enumerate(maps):
            option_rect = pygame.Rect(map_dropdown_x, y_top + 48 + i * 28, 80, 28)
            pygame.draw.rect(screen, (255, 255, 255), option_rect)
            pygame.draw.rect(screen, (0, 0, 0), option_rect, 1)

            option_text = small_font.render(map_item[0], True, (0, 0, 0))
            screen.blit(option_text, (map_dropdown_x + 8, y_top + 54 + i * 28))

    if algorithm_dropdown_open:
        for i, algorithm_item in enumerate(algorithms):
            option_rect = pygame.Rect(algo_dropdown_x, y_top + 48 + i * 28, 145, 28)
            pygame.draw.rect(screen, (255, 255, 255), option_rect)
            pygame.draw.rect(screen, (0, 0, 0), option_rect, 1)

            option_text = small_font.render(algorithm_item[0], True, (0, 0, 0))
            screen.blit(option_text, (algo_dropdown_x + 8, y_top + 54 + i * 28))

    # Result title
    y = 180

    result_title = font.render(title, True, (0, 0, 0))
    screen.blit(result_title, (legend_x, y))
    y += 35

    # Terrain legend
    terrain_legend_items = [
        ("Road", "R", TERRAIN_COLORS["R"]),
        ("Field", "F", TERRAIN_COLORS["F"]),
        ("Forest", "O", TERRAIN_COLORS["O"]),
        ("Hills", "H", TERRAIN_COLORS["H"]),
        ("Mountains", "M", TERRAIN_COLORS["M"]),
        ("Water", "W", TERRAIN_COLORS["W"]),
        ("Start", "S", TERRAIN_COLORS["S"]),
        ("End", "E", TERRAIN_COLORS["E"])
    ]

    for label, terrain, color in terrain_legend_items:
        draw_legend_tile(screen, legend_x, y, terrain, color, tile_images)

        label_text = small_font.render(label, True, (0, 0, 0))
        screen.blit(label_text, (legend_x + 30, y + 2))

        y += 24

    overlay_legend_items = [
        ("Closed / Explored", CLOSED_LEGEND_COLOR),
        ("Open / Frontier", OPEN_COLOR),
        ("Final Path", PATH_COLOR)
    ]

    for label, color in overlay_legend_items:
        draw_plain_legend_box(screen, legend_x, y, color)

        label_text = small_font.render(label, True, (0, 0, 0))
        screen.blit(label_text, (legend_x + 30, y + 2))

        y += 24

    y += 15

    if result is not None:
        stats = [
            f"Path Length: {result.path_length}",
            f"Path Cost: {result.path_cost}",
            f"States Explored: {result.states_explored}",
            f"States Remaining: {result.states_remaining}"
        ]

        for line in stats:
            text = small_font.render(line, True, (0, 0, 0))
            screen.blit(text, (legend_x, y))
            y += 22


def draw_current_state(
    screen,
    grid,
    closed_list,
    open_list,
    path,
    font,
    small_font,
    maps,
    algorithms,
    selected_map_index,
    selected_algorithm_index,
    map_dropdown_open,
    algorithm_dropdown_open,
    title,
    result,
    tile_images
):
    screen.fill((255, 255, 255))

    draw_grid(screen, grid, tile_images)

    draw_overlay_cells(screen, closed_list, CLOSED_COLOR, 90)
    draw_overlay_cells(screen, open_list, OPEN_COLOR, 120)
    draw_overlay_cells(screen, path, PATH_COLOR, 100)

    redraw_start_end(screen, grid, tile_images)

    draw_menu_panel(
        screen,
        font,
        small_font,
        maps,
        algorithms,
        selected_map_index,
        selected_algorithm_index,
        map_dropdown_open,
        algorithm_dropdown_open,
        title,
        result,
        tile_images
    )

    pygame.display.flip()


def run_menu(maps, algorithms, read_map, validate_map, find_start_and_end):
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pathfinding Project Menu")

    font = pygame.font.SysFont("Arial", 18)
    small_font = pygame.font.SysFont("Arial", 14)

    tile_images = load_tile_images()

    selected_map_index = 0
    selected_algorithm_index = 0

    map_dropdown_open = False
    algorithm_dropdown_open = False

    current_grid = None
    current_result = None
    current_title = ""
    current_output_filename = None
    should_save = False

    def run_selected_search():
        nonlocal current_grid
        nonlocal current_result
        nonlocal current_title
        nonlocal current_output_filename
        nonlocal should_save
        nonlocal map_dropdown_open
        nonlocal algorithm_dropdown_open

        map_name, filename, map_file_label = maps[selected_map_index]
        algorithm_name, algorithm_function, algorithm_file_label = algorithms[selected_algorithm_index]

        grid = read_map(filename)

        if not validate_map(grid):
            return

        start, end = find_start_and_end(grid)

        current_title = f"{map_name} - {algorithm_name}"

        algorithm_mode = None
        heuristic = None

        if algorithm_file_label == "bfs":
            algorithm_mode = "bfs"

        elif algorithm_file_label == "ucs":
            algorithm_mode = "ucs"

        elif algorithm_file_label == "greedy":
            algorithm_mode = "greedy"
            heuristic = manhattan

        elif algorithm_file_label == "astar_manhattan":
            algorithm_mode = "astar"
            heuristic = manhattan

        elif algorithm_file_label == "astar_euclidean":
            algorithm_mode = "astar"
            heuristic = euclidean

        def draw_step(closed_list, open_list, path):
            draw_current_state(
                screen,
                grid,
                closed_list,
                open_list,
                path,
                font,
                small_font,
                maps,
                algorithms,
                selected_map_index,
                selected_algorithm_index,
                map_dropdown_open,
                algorithm_dropdown_open,
                current_title,
                None,
                tile_images
            )

            pygame.time.delay(15)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit

        result = animated_search(grid, start, end, algorithm_mode, draw_step, heuristic)

        current_grid = grid
        current_result = result
        current_title = f"{map_name} - {algorithm_name}"
        current_output_filename = f"{map_file_label}_{algorithm_file_label}.png"
        should_save = True

        print()
        print("==============================")
        print(current_title)
        print("Start:", start)
        print("End:", end)
        print("Path length:", result.path_length)
        print("Path cost:", result.path_cost)
        print("States explored:", result.states_explored)
        print("States remaining:", result.states_remaining)

    run_selected_search()

    running = True

    while running:
        if current_grid is not None and current_result is not None:
            draw_current_state(
                screen,
                current_grid,
                current_result.closed_list,
                current_result.open_list,
                current_result.path,
                font,
                small_font,
                maps,
                algorithms,
                selected_map_index,
                selected_algorithm_index,
                map_dropdown_open,
                algorithm_dropdown_open,
                current_title,
                current_result,
                tile_images
            )

        if should_save and current_output_filename is not None:
            pygame.image.save(screen, current_output_filename)
            should_save = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                legend_x = MAP_WIDTH + 15
                y_top = 15

                map_dropdown_rect = pygame.Rect(legend_x, y_top + 20, 80, 28)
                algorithm_dropdown_rect = pygame.Rect(legend_x + 100, y_top + 20, 145, 28)

                if map_dropdown_rect.collidepoint(mouse_x, mouse_y):
                    map_dropdown_open = not map_dropdown_open
                    algorithm_dropdown_open = False

                elif algorithm_dropdown_rect.collidepoint(mouse_x, mouse_y):
                    algorithm_dropdown_open = not algorithm_dropdown_open
                    map_dropdown_open = False

                elif map_dropdown_open:
                    for i in range(len(maps)):
                        option_rect = pygame.Rect(legend_x, y_top + 48 + i * 28, 80, 28)

                        if option_rect.collidepoint(mouse_x, mouse_y):
                            selected_map_index = i
                            map_dropdown_open = False
                            algorithm_dropdown_open = False
                            run_selected_search()

                elif algorithm_dropdown_open:
                    for i in range(len(algorithms)):
                        option_rect = pygame.Rect(legend_x + 100, y_top + 48 + i * 28, 145, 28)

                        if option_rect.collidepoint(mouse_x, mouse_y):
                            selected_algorithm_index = i
                            algorithm_dropdown_open = False
                            map_dropdown_open = False
                            run_selected_search()

                else:
                    map_dropdown_open = False
                    algorithm_dropdown_open = False

    pygame.quit()