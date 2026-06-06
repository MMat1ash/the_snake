"""Игра змейка."""

from random import randint

import pygame


SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
START_POSITION = ((GRID_WIDTH // 2) * GRID_SIZE, (GRID_HEIGHT // 2) * GRID_SIZE)
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
SPEED = 10

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()


def handle_keys(game_object):
    """Обрабатывает нажатия кнопок пользователем."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


class GameObject:
    """Родительский класс объектов игры."""

    def __init__(self):
        self.position = START_POSITION
        self.body_color = None

    def draw(self):
        """Абстрактный метод для переопределения в дочерних классах."""
        pass


class Apple(GameObject):
    """Объект яблока, определяющий его цвет, позицию, отрисовку."""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле."""
        position_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        position_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (position_x, position_y)

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Объект змейки, описывающий логику и поведение.
    
    Обеспечивает движение, отрисовку, обработку событий 
    и другие аспекты поведения змейки в игре.
    """

    def __init__(self):
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

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
        new_x_position = (current_head_x + direction_x * GRID_SIZE) % SCREEN_WIDTH
        new_y_position = (current_head_y + direction_y * GRID_SIZE) % SCREEN_HEIGHT
        new_head_position = (new_x_position, new_y_position)
        self.positions.insert(0, new_head_position)
        self.last = self.positions[-1]
        if len(self.positions) > self.length:
            del self.positions[-1]

    def draw(self):
        """Отрисовывает змейку на экране, затирая след."""
        for position in self.positions[1:]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки (первый элемент в списке positions)."""
        return self.positions[0] 

    def reset(self):
        """Восстанавливает базовые параметры змейки при начале новой игры."""
        self.length = 1
        self.positions = [self.position] # Возвращаем на старт
        self.direction = RIGHT            # Сбрасываем направление
        self.next_direction = None
        self.last = None


def main():
    """Выполняет основную логику игры."""
    pygame.init()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position()

        apple.draw()
        snake.draw()
        
        pygame.display.update()

if __name__ == '__main__':
    main()