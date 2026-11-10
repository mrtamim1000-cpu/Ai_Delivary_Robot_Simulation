
import pygame

from settings import (
    CELL_SIZE,
    ROWS,
    COLS,
    GRAY
)


class Environment:

    def __init__(self):
        self.roadblocks = {
            "building": {
                (3, 3), (3, 4), (3, 5), (3, 6),
                (4, 3), (4, 4), (4, 5), (4, 6),
                (5, 3), (5, 4), (5, 5), (5, 6),
                (9, 15), (9, 16), (10, 15), (10, 16)
            },
            "construction": {
                (5, 9), (5, 10), (5, 11), (5, 12), (5, 13),
                (6, 9), (6, 13), (7, 9), (7, 10), (7, 11), (7, 12), (7, 13)
            },
            "water": {
                (9, 3), (9, 4), (9, 5),
                (10, 3), (10, 4), (10, 5),
                (11, 3), (11, 4), (11, 5)
            },
            "crates": {
                (9, 9), (9, 10), (9, 11),
                (10, 9), (10, 10), (10, 11)
            },
            "barricade": {
                (3, 17), (4, 17), (5, 17), (6, 17), (7, 17),
                (11, 13), (11, 14), (11, 15), (11, 16)
            },
            "roadwork": set()
        }
        self.obstacles = set().union(*self.roadblocks.values())

    def add_roadwork_block(self, position):
        self.roadblocks["roadwork"].add(position)
        self.obstacles.add(position)

    def is_valid(self, position):

        row, col = position

        # Check grid boundaries
        if row < 0 or row >= ROWS:
            return False

        if col < 0 or col >= COLS:
            return False

        # Check obstacles
        if position in self.obstacles:
            return False

        return True

    def get_neighbors(self, position):

        row, col = position

        directions = [
            (-1, 0),  # Up
            (1, 0),   # Down
            (0, -1),  # Left
            (0, 1)    # Right
        ]

        neighbors = []

        for dr, dc in directions:

            new_position = (row + dr, col + dc)

            if self.is_valid(new_position):
                neighbors.append(new_position)

        return neighbors

    def draw(self, screen):

        # Draw grid
        for row in range(ROWS):

            for col in range(COLS):

                rect = pygame.Rect(
                    col * CELL_SIZE,
                    row * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE
                )

                pygame.draw.rect(
                    screen,
                    GRAY,
                    rect,
                    1
                )

        styles = {
            "building": ((75, 83, 91), (145, 153, 158)),
            "construction": ((237, 151, 48), (55, 55, 55)),
            "water": ((40, 151, 190), (178, 232, 241)),
            "crates": ((151, 101, 57), (220, 181, 126)),
            "barricade": ((190, 57, 48), (250, 225, 180)),
            "roadwork": ((210, 57, 91), (255, 242, 222))
        }

        for kind, positions in self.roadblocks.items():
            fill, detail = styles[kind]

            for row, col in positions:
                rect = pygame.Rect(
                    col * CELL_SIZE,
                    row * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE
                )
                pygame.draw.rect(screen, fill, rect)

                if kind == "building":
                    pygame.draw.rect(screen, detail, rect.inflate(-10, -10), 2)
                elif kind == "construction":
                    pygame.draw.line(screen, detail, rect.bottomleft, rect.topright, 4)
                elif kind == "water":
                    pygame.draw.arc(screen, detail, rect.inflate(-8, -16), 0.2, 2.8, 2)
                elif kind == "crates":
                    pygame.draw.line(screen, detail, rect.topleft, rect.bottomright, 2)
                    pygame.draw.line(screen, detail, rect.topright, rect.bottomleft, 2)
                elif kind == "roadwork":
                    pygame.draw.rect(screen, detail, rect.inflate(-10, -10), 3)
                    pygame.draw.line(screen, detail, rect.bottomleft, rect.topright, 4)
                else:
                    pygame.draw.line(screen, detail, rect.bottomleft, rect.topright, 4)
