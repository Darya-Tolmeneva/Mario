import pygame
import os
import sys


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


pygame.init()
size = width, height = 500, 550
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Марио")
tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mario.png', colorkey=-1)

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.pos = pos_x, pos_y
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def move(self, x, y):
        self.pos = x, y
        self.rect = self.image.get_rect().move(
            tile_width * x + 15, tile_height * y + 5)


player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


def move(player, m):
    if m == "l" and player.pos[0] > 0 and (mapp[player.pos[0] - 1][player.pos[1]] == "." or
                                           mapp[player.pos[0] - 1][player.pos[1]] == "@"):
        player.move(player.pos[0] - 1, player.pos[1])
    elif m == "r" and player.pos[0] < level_x - 1 and (mapp[player.pos[0] + 1][player.pos[1]] == "." or
                                                       mapp[player.pos[0] + 1][player.pos[1]] == "@"):
        player.move(player.pos[0] + 1, player.pos[1])
    elif m == "u" and player.pos[1] > 0 and (mapp[player.pos[0]][player.pos[1] - 1] == "." or
                                             mapp[player.pos[0]][player.pos[1] - 1] == "@"):
        player.move(player.pos[0], player.pos[1] - 1)
    elif m == "d" and player.pos[1] < level_y - 1 and (mapp[player.pos[0]][player.pos[1] + 1] == "." or
                                                       mapp[player.pos[0]][player.pos[1] + 1] == "@"):
        player.move(player.pos[0], player.pos[1] + 1)


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fon = pygame.transform.scale(load_image('fon.jpg'), (500, 550))
    screen.blit(fon, (0, 0))
    intro_text = ["Перемещение героя",
                  "", "Герой двигается", "Карта на месте"]
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


start_screen()
mapp = load_level('map.txt')
player, level_x, level_y = generate_level(mapp)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move(player, 'u')
            if event.key == pygame.K_DOWN:
                move(player, 'd')
            if event.key == pygame.K_RIGHT:
                move(player, 'r')
            if event.key == pygame.K_LEFT:
                move(player, 'l')
    screen.fill(pygame.Color("black"))
    all_sprites.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
pygame.quit()