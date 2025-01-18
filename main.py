import pygame
import os
import time

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Уровни игры")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Размеры тайлов
tile_width = tile_height = 50


# Загрузка изображений
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mario.png')
splash_image = load_image('fon.jpg')  # Загружаем изображение для заставки


# Классы спрайтов
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, *groups):
        super().__init__(*groups)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, *groups):
        super().__init__(*groups)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

        self.pos_x = pos_x
        self.pos_y = pos_y

    def move(self, dx, dy):
        self.pos_x += dx
        self.pos_y += dy
        self.rect.x = tile_width * self.pos_x + 15
        self.rect.y = tile_height * self.pos_y + 5


# Функции загрузки и генерации уровня
def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


# основной персонаж
player = None
level = None  # Добавляем объявление глобальной переменной level

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def generate_level(level_data):
    global level  # Делаем level глобальной
    level = level_data
    new_player, level_x, level_y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y, tiles_group, all_sprites)
            elif level[y][x] == '#':
                Tile('wall', x, y, tiles_group, all_sprites)
            elif level[y][x] == '@':
                Tile('empty', x, y, tiles_group, all_sprites)
                new_player = Player(x, y, player_group, all_sprites)
    return new_player, x, y


# --- ЗАСТАВКА ---
screen.fill(BLACK)
# Уменьшаем размер заставки
scaled_splash_image = pygame.transform.scale(splash_image, (400, 300))  # Изменяем размеры по вашему вкусу
splash_rect = scaled_splash_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
screen.blit(scaled_splash_image, splash_rect)
pygame.display.flip()
time.sleep(3)  # Задержка в 3 секунды
# --- КОНЕЦ ЗАСТАВКИ ---

# Получаем имя файла из стандартного ввода
level_filename = input("Введите имя файла уровня (например, map.txt): ")

# Проверяем существование файла
if not os.path.exists(os.path.join("data", level_filename)):
    print(f"Ошибка: файл '{level_filename}' не найден в папке 'data'.")
    pygame.quit()
    exit()

# Загрузка и отрисовка уровня
player, level_x, level_y = generate_level(load_level(level_filename))

# Игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # проверяем возможность перемещения
                if player.pos_x > 0 and level[player.pos_y][player.pos_x - 1] != '#':
                    player.move(-1, 0)
            if event.key == pygame.K_RIGHT:
                if player.pos_x < len(level[0]) - 1 and level[player.pos_y][player.pos_x + 1] != '#':
                    player.move(1, 0)
            if event.key == pygame.K_UP:
                if player.pos_y > 0 and level[player.pos_y - 1][player.pos_x] != '#':
                    player.move(0, -1)
            if event.key == pygame.K_DOWN:
                if player.pos_y < len(level) - 1 and level[player.pos_y + 1][player.pos_x] != '#':
                    player.move(0, 1)

    screen.fill(BLACK)
    tiles_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()

pygame.quit()