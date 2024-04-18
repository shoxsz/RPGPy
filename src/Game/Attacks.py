from Game.Basics import GameEntity, GameCreature, spriteStore
import pygame
from math import atan2, degrees, pi

class AttackMissile(GameEntity):
  def __init__(self, shooter: GameEntity, target: GameCreature, damage: int):
    super().__init__(None)
    self.shooter = shooter
    self.rect = pygame.Rect(shooter.rect.center[0], shooter.rect.center[1], 3, 3)
    self.target = target
    self.damage = damage
    self.speed = 1000
    self.skin = spriteStore.get('MissileFire', self)
    self.skin.set('attack')
    self.explodeTime = -1

  def _enterGame(self, game) -> None:
    super()._enterGame(game)
    self.game.add(self.skin)

  def update(self, deltaSeconds):
    if self.explodeTime > 0:
      self.explodeTime -= deltaSeconds
      if self.explodeTime <= 0:
        self.game.remove(self)
      return

    direction = pygame.Vector2(self.target.rect.center) - pygame.Vector2(self.rect.center)

    d = direction.normalize() * self.speed * deltaSeconds
    self.rect.x += d.x
    self.rect.y += d.y

    dx = self.rect.x - self.target.rect.x
    dy = self.rect.y - self.target.rect.y
    rads = atan2(-dy,dx)
    rads %= 2*pi
    degs = degrees(rads)
    self.skin.rotation = degs

    direction = pygame.Vector2(self.target.rect.center) - pygame.Vector2(self.rect.center)
    if self.target.rect.colliderect(self.rect):
      self.target.health -= self.damage
      self.explodeTime = 0.5
      self.skin.set('explosion')
      self.skin.rotation = 0

      self.rect.y = self.target.rect.y
      self.rect.x = self.target.rect.x + 16

  def draw(self, screen):
    pass
