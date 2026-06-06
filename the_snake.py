"""Игра змейка."""

import sys
from random import randint

import pygame as pg

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
START_POSITION = ((GRID_WIDTH // 2) * GRID_SIZE, (GRID_HEIGHT // 2)
                  * GRID_SIZE)
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
BLACK = (0, 0, 0)
ELECTRIC_BLUE = (93, 216, 228)
RED = (255, 0, 0)
LIME = (0, 255, 0)
BOARD_BACKGROUND_COLOR = BLACK
BORDER_COLOR = ELECTRIC_BLUE
APPLE_COLOR = RED
SNAKE_COLOR = LIME
SPEED = 10

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pg.display.set_caption('Змейка')

clock = pg.time.Clock()


def handle_keys(game_object):
    """Обрабатывает нажатия кнопок пользователем."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                sys.exit()
            elif event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


class GameObject:
    """Родительский класс объектов игры."""

    def __init__(self, position=START_POSITION, body_color=None):
        self.position = position
        self.body_color = body_color

    def draw_rect(self, position, color=None):
        """Отрисовывает квадрат по координатам."""
        if color is None:
            color = self.body_color

        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Абстрактный метод для переопределения в дочерних классах."""
        raise NotImplementedError(
            f'В классе {type(self).__name__} не переопределен метод draw.')


class Apple(GameObject):
    """Объект яблока, определяющий его цвет, позицию, отрисовку."""

    def __init__(self, snake_positions=None):
        super().__init__(body_color=APPLE_COLOR)

        if snake_positions is None:
            snake_positions = []

        self.randomize_position(snake_positions)

    def randomize_position(self, snake_positions):
        """Устанавливает случайное положение яблока на игровом поле."""
        while True:
            position_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            position_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            if (position_x, position_y) not in snake_positions:
                self.position = (position_x, position_y)
                break

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности."""
        self.draw_rect(self.position)


class Snake(GameObject):
    """Объект змейки, описывающий логику и поведение.

    Обеспечивает движение, отрисовку, обработку событий
    и другие аспекты поведения змейки в игре.
    """

    def __init__(self):
        super().__init__(position=START_POSITION, body_color=SNAKE_COLOR)
        self.reset()

    def update_direction(self):
        """Обновляет текущее направление движения."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки на игровом поле.

        Добавляя новую голову в начало списка positions и удаляя
        последний элемент, если длина змейки не увеличилась.
        """
        current_head_x, current_head_y = self.get_head_position()
        direction_x, direction_y = self.direction
        shift_x = direction_x * GRID_SIZE
        shift_y = direction_y * GRID_SIZE
        new_x_position = (current_head_x + shift_x) % SCREEN_WIDTH
        new_y_position = (current_head_y + shift_y) % SCREEN_HEIGHT
        new_head_position = (new_x_position, new_y_position)
        self.positions.insert(0, new_head_position)
        self.last = self.positions[-1]
        if len(self.positions) > self.length:
            del self.positions[-1]

    def draw(self):
        """Отрисовывает змейку на экране, затирая след."""
        for position in self.positions[1:]:
            self.draw_rect(position)

        self.draw_rect(self.get_head_position())

        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Восстанавливает базовые параметры змейки при начале новой игры."""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None


def main():
    """Выполняет основную логику игры."""
    pg.init()
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        if snake.get_head_position() in snake.positions[4:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position(snake.positions)

        apple.draw()
        snake.draw()

        pg.display.update()


if __name__ == '__main__':
    main()
