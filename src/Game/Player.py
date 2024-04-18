from Game.Basics import GameCreature
from Game.Attacks import AttackMissile
from Game.Basics import GameEntity
import pygame

class Player(GameCreature):
  target: GameCreature = None
  def __init__(self):
    super().__init__(
      pygame.Rect(0, 0, 48, 48),
      pygame.Vector2(150, 150),
      100,
      100,
      10,
      10,
      'Player',
      'PinkGirl'
    )
    self.skin.set('walk')

  def _enterGame(self, game) -> None:
    super()._enterGame(game)
    self.game.add(self.skin)

  def update(self, deltaSeconds):
    super().update(deltaSeconds)

  def draw(self, screen):
    self._drawLifeBar(screen)
    if (self.target != None):
      if (self.target.game == None):
        self.target = None
        return
      pygame.draw.rect(screen, (255, 0, 0), self.target.rect.inflate(4, 4), 2)

class PlayerController(GameEntity):
  def __init__(self, player: GameEntity):
    super().__init__(player)
    self.player = player
    self.cooldown = 0.3
    self.cooldownCount = 0.3

  def update(self, deltaSeconds):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
      self.player.speed.y = -self.player.moveSpeed.y
    elif keys[pygame.K_s]:
      self.player.speed.y = self.player.moveSpeed.y
    else:
      self.player.speed.y = 0

    if keys[pygame.K_d]:
      self.player.speed.x = self.player.moveSpeed.x
    elif keys[pygame.K_a]:
      self.player.speed.x = -self.player.moveSpeed.x
    else:
      self.player.speed.x = 0

    if self.player.speed.x == 0 and self.player.speed.y == 0:
      self.player.skin.set('idle')
    else:
      self.player.skin.set('walk')

    if (self.player.speed.x > 0):
      self.player.skin.flipped = True
    else:
      self.player.skin.flipped = False

    self.cooldownCount += deltaSeconds
    if self.cooldownCount >= self.cooldown and keys[pygame.K_SPACE] and self.player.target != None:
      self.cooldownCount = 0
      missile = AttackMissile(self.player, self.player.target, 5)
      self.player.game.add(missile)

    if pygame.mouse.get_pressed()[0]:
      pos = pygame.mouse.get_pos()
      for entity in self.game.entities.entities:
        if entity.rect.collidepoint(pos) and type(entity).__name__ == 'Enemy':
          self.player.target = entity
          return

  def draw(self, screen):
    pass
