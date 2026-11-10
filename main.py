
import pygame
import sys

from settings import *
from environment import Environment
from pathfinding import astar
from robot import Robot


pygame.init()

screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)

pygame.display.set_caption(SCREEN_TITLE)

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 28)
sidebar_title_font = pygame.font.SysFont(None, 32)
sidebar_font = pygame.font.SysFont(None, 24)

environment = Environment()

goal = None
path = []
roadwork_added = False
notice = ""

robot = Robot(START, path)

mode = "AUTO"


def draw_goal():

    if goal is None:
        return

    rect = pygame.Rect(
        goal[1] * CELL_SIZE,
        goal[0] * CELL_SIZE,
        CELL_SIZE,
        CELL_SIZE
    )

    pygame.draw.rect(screen, GREEN, rect)


def draw_start():

    rect = pygame.Rect(
        START[1] * CELL_SIZE,
        START[0] * CELL_SIZE,
        CELL_SIZE,
        CELL_SIZE
    )

    pygame.draw.rect(screen, YELLOW, rect)


def draw_path():

    for row, col in path:

        rect = pygame.Rect(
            col * CELL_SIZE + 12,
            row * CELL_SIZE + 12,
            CELL_SIZE - 24,
            CELL_SIZE - 24
        )

        pygame.draw.rect(screen, PATH_COLOR, rect)


def draw_sidebar_text(text, y, color=BLACK, text_font=sidebar_font):

    words = text.split()
    lines = []
    line = ""
    max_width = SIDEBAR_WIDTH - 36

    for word in words:
        candidate = f"{line} {word}".strip()

        if line and text_font.size(candidate)[0] > max_width:
            lines.append(line)
            line = word
        else:
            line = candidate

    if line:
        lines.append(line)

    for line in lines:
        rendered = text_font.render(line, True, color)
        screen.blit(rendered, (MAP_WIDTH + 18, y))
        y += rendered.get_height() + 5

    return y


def draw_sidebar():

    sidebar_rect = pygame.Rect(
        MAP_WIDTH,
        0,
        SIDEBAR_WIDTH,
        SCREEN_HEIGHT
    )
    pygame.draw.rect(screen, (244, 247, 249), sidebar_rect)
    pygame.draw.line(screen, (185, 195, 202), (MAP_WIDTH, 0), (MAP_WIDTH, SCREEN_HEIGHT), 2)

    title = sidebar_title_font.render("DELIVERY ROBOT", True, (32, 63, 76))
    screen.blit(title, (MAP_WIDTH + 18, 22))

    y = 72
    if notice:
        y = draw_sidebar_text(notice, y, RED)
    elif goal is None:
        y = draw_sidebar_text("Choose an open tile on the map.", y, BLUE)
    elif robot.is_delivered():
        y = draw_sidebar_text("Delivery completed! Choose another destination on the map.", y, GREEN)
    elif mode == "AUTO":
        y = draw_sidebar_text("AI delivery in progress.", y, BLUE)
    else:
        y = draw_sidebar_text("Manual mode is active.", y, BLUE)

    y += 14
    y = draw_sidebar_text("DESTINATION", y, (91, 109, 119))
    destination_text = "Not selected" if goal is None else f"Row {goal[0] + 1}, column {goal[1] + 1}"
    y = draw_sidebar_text(destination_text, y)

    y += 20
    y = draw_sidebar_text("CONTROLS", y, (91, 109, 119))
    y = draw_sidebar_text("Click the map: choose destination", y)
    y = draw_sidebar_text("M: switch AUTO / MANUAL", y)
    y = draw_sidebar_text("R: reset delivery", y)
    draw_sidebar_text("Arrow keys: move manually", y)


running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if event.pos[0] < MAP_WIDTH and event.pos[1] < SCREEN_HEIGHT:
                destination = (
                    event.pos[1] // CELL_SIZE,
                    event.pos[0] // CELL_SIZE
                )

                if robot.moving:
                    notice = "Wait for the robot to reach its next tile first."
                elif destination == START or not environment.is_valid(destination):
                    notice = "Choose an open tile other than the start."
                else:
                    source = robot.position
                    candidate_path = astar(environment, source, destination)

                    if candidate_path:
                        distance = (
                            abs(source[0] - destination[0])
                            + abs(source[1] - destination[1])
                        )

                        if not roadwork_added and distance < 3:
                            notice = "Choose a destination at least three steps away."
                        else:
                            if not roadwork_added:
                                row_distance = abs(source[0] - destination[0])
                                col_distance = abs(source[1] - destination[1])

                                if col_distance >= row_distance:
                                    barrier_col = (source[1] + destination[1]) // 2
                                    low_row = min(source[0], destination[0])
                                    high_row = max(source[0], destination[0])
                                    gap_row = min(
                                        (
                                            row for row in range(ROWS)
                                            if (row < low_row or row > high_row)
                                            and environment.is_valid((row, barrier_col))
                                        ),
                                        key=lambda row: (
                                            abs(source[0] - row)
                                            + abs(destination[0] - row)
                                        )
                                    )
                                    barrier = {
                                        (row, barrier_col)
                                        for row in range(ROWS)
                                        if row != gap_row
                                    }
                                else:
                                    barrier_row = (source[0] + destination[0]) // 2
                                    low_col = min(source[1], destination[1])
                                    high_col = max(source[1], destination[1])
                                    gap_col = min(
                                        (
                                            col for col in range(COLS)
                                            if (col < low_col or col > high_col)
                                            and environment.is_valid((barrier_row, col))
                                        ),
                                        key=lambda col: (
                                            abs(source[1] - col)
                                            + abs(destination[1] - col)
                                        )
                                    )
                                    barrier = {
                                        (barrier_row, col)
                                        for col in range(COLS)
                                        if col != gap_col
                                    }

                                for blocked_cell in barrier:
                                    environment.add_roadwork_block(blocked_cell)

                                roadwork_added = True

                            goal = destination
                            path = astar(environment, source, goal)
                            robot = Robot(source, path)
                            mode = "AUTO"
                            notice = ""
                    else:
                        notice = "No route to that destination. Choose another tile."

        if event.type == pygame.KEYDOWN:

            # Switch mode
            if event.key == pygame.K_m:

                mode = "MANUAL" if mode == "AUTO" else "AUTO"

            # Restart simulation
            if event.key == pygame.K_r:

                goal = None
                path = []
                robot = Robot(START, path)
                mode = "AUTO"
                notice = ""

            # Manual movement
            if mode == "MANUAL":

                directions = {

                    pygame.K_UP: (-1, 0),
                    pygame.K_DOWN: (1, 0),
                    pygame.K_LEFT: (0, -1),
                    pygame.K_RIGHT: (0, 1)

                }

                if event.key in directions:

                    robot.move_manual(
                        directions[event.key],
                        environment
                    )

    # Robot movement
    if mode == "AUTO":

        if path and not robot.is_delivered():
            robot.move()

    else:

        robot.update()

    # Draw screen
    screen.fill(WHITE)

    environment.draw(screen)

    draw_path()

    draw_start()

    draw_goal()

    robot.draw(screen)

    draw_sidebar()

    pygame.display.flip()


pygame.quit()
sys.exit()
