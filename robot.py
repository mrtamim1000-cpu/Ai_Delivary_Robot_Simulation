
import pygame

from settings import CELL_SIZE, BLUE, YELLOW, ROBOT_SPEED


class Robot:

    def __init__(self, start, path):

        self.position = start
        self.path = path

        # Start after the first path cell
        self.path_index = 1

        self.speed = ROBOT_SPEED

        self.x = start[1] * CELL_SIZE
        self.y = start[0] * CELL_SIZE

        self.target_x = self.x
        self.target_y = self.y

        self.target_position = start
        self.moving = False

    def set_target(self, position):

        row, col = position

        self.target_position = position

        self.target_x = col * CELL_SIZE
        self.target_y = row * CELL_SIZE

        self.moving = True

    def update(self):

        if not self.moving:
            return

        # Horizontal movement
        if self.x < self.target_x:
            self.x = min(self.x + self.speed, self.target_x)

        elif self.x > self.target_x:
            self.x = max(self.x - self.speed, self.target_x)

        # Vertical movement
        if self.y < self.target_y:
            self.y = min(self.y + self.speed, self.target_y)

        elif self.y > self.target_y:
            self.y = max(self.y - self.speed, self.target_y)

        # Check movement completion
        if self.x == self.target_x and self.y == self.target_y:

            self.position = self.target_position
            self.moving = False

    def move(self):

        # Automatic AI movement
        if not self.moving and self.path_index < len(self.path):

            next_position = self.path[self.path_index]

            self.set_target(next_position)

            self.path_index += 1

        self.update()

    def move_manual(self, direction, environment):

        if self.moving:
            return

        row, col = self.position

        dr, dc = direction

        new_position = (row + dr, col + dc)

        if environment.is_valid(new_position):

            self.set_target(new_position)

    def draw(self, screen):

        robot_rect = pygame.Rect(
            int(self.x + 5),
            int(self.y + 5),
            CELL_SIZE - 10,
            CELL_SIZE - 10
        )

        pygame.draw.rect(
            screen,
            BLUE,
            robot_rect,
            border_radius=8
        )

        pygame.draw.circle(
            screen,
            YELLOW,
            robot_rect.center,
            5
        )

    def is_delivered(self):

        return (
            bool(self.path)
            and self.position == self.path[-1]
            and not self.moving
        )
