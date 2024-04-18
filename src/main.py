import pygame
import Game.Game
from Game.Basics import SpriteAnimated
from Game.Basics import SpriteManager
from Game.Basics import spriteStore
from Game.Enemies import Enemy
from Game.Player import Player, PlayerController
import random

# Pygame setup
pygame.init()
pygame.display.set_caption('Tibia Survival')
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
running = True

# Images
image = pygame.image.load('./Resources/sprites/PinkGirl.png')
IdleImage = SpriteAnimated(
    image,
    [
        pygame.Rect(0, 0, 36, 51)
    ],
    1
)
WalkImage = SpriteAnimated(
    image,
    [
        pygame.Rect(0, 51, 36, 51),
        pygame.Rect(36, 51, 36, 51),
        pygame.Rect(72, 51, 36, 51),
        pygame.Rect(108, 51, 36, 51)
    ],
    8
)
adultGreenDragon = pygame.image.load('./Resources/sprites/AdultGreenDragon.png')
AdultGreenDragonSprite = SpriteAnimated(
    pygame.transform.scale(adultGreenDragon, (48 * 4, 48)),
    [
        pygame.Rect(0, 0, 48, 48),
        pygame.Rect(48, 0, 48, 48),
        pygame.Rect(96,0 , 48, 48),
        pygame.Rect(144, 0, 48, 48),
    ],
    8
)

missileFire = pygame.image.load('./Resources/sprites/MissileFire.png')
MissileFireSprite = SpriteAnimated(
    missileFire,
    [
        pygame.Rect(0, 0, 64, 24)
    ],
    1
)

explosionFire = pygame.image.load('./Resources/sprites/ExplosionFire.png')
ExplosionFireSprite = SpriteAnimated(
    explosionFire,
    [
        pygame.Rect(0, 0, 64, 93),
        pygame.Rect(64, 0, 64, 63),
        pygame.Rect(128, 0, 64, 61),
    ],
    20,
    'once'
)

pink_girl = SpriteManager(None)
pink_girl.add('idle', IdleImage)
pink_girl.add('walk', WalkImage)

dragon = SpriteManager(None)
dragon.add('idle', AdultGreenDragonSprite)

missileFireMngr = SpriteManager(None)
missileFireMngr.add('attack', MissileFireSprite)
missileFireMngr.add('explosion', ExplosionFireSprite)

spriteStore.add('PinkGirl', pink_girl)
spriteStore.add('AdultGreenDragon', dragon)
spriteStore.add('MissileFire', missileFireMngr)

game = Game.Game.Game()
player = Player()
game.add(player)
game.player = player

controller = PlayerController(player)
game.add(controller)

for i in range(0, random.randint(3, 5)):
    game.add(
        Enemy(
            pygame.Rect(random.randint(100, 500), random.randint(100, 300), 48, 48),
            pygame.Vector2(100, 100),
            100,
            100,
            20,
            20,
            'Enemy',
            'AdultGreenDragon'
        )    
    )

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill('#2D882D')

    time = clock.get_time() / 1000
    game.update(time)
    game.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
