import Game.Basics
import pygame
from Game.Attacks import AttackMissile
import random

class EnemyWalkerRandom(Game.Basics.GameEntity):
  def __init__(self, parent):
    super().__init__(parent)

  def update(self, deltaSeconds):
    self.parent.speed.x = 1
    self.parent.speed.y = -1

  def draw(self, screen):
    pass

class Enemy(Game.Basics.GameCreature):
  def __init__(
      self,
      rect: pygame.Rect,
      moveSpeed: pygame.Vector2,
      health: int,
      max_health: int,
      attack: int,
      defense: int,
      name: str,
      skin
    ):
    super().__init__(
      rect, moveSpeed, health, max_health, attack, defense, name, skin
    )
    self.skin.set('idle')
    self.target = None
    self.meleeCooldown = 2
    self.meleeCooldownCount = 0.0

    self.attackCooldown = random.randint(5, 10)
    self.attackCooldownCount = 0.0

  def _enterGame(self, game) -> None:
    super()._enterGame(game)
    self.game.add(self.skin)

  def update(self, deltaSeconds):
    if (self.health <= 0):
      self.game.remove(self)
      return

    super().update(deltaSeconds)

    direction = pygame.Vector2(self.game.player.rect.x - self.rect.x, self.game.player.rect.y - self.rect.y)
    dist = direction.length()

    canAttack = False
    self.meleeCooldownCount += deltaSeconds
    if self.meleeCooldownCount >= self.meleeCooldown:
      self.meleeCooldownCount = 0
      canAttack = True

    self.attackCooldownCount += deltaSeconds
    if self.attackCooldownCount >= self.attackCooldown:
      self.attackCooldownCount = 0
      self.attackCooldown = random.randint(5, 10)
      missile = AttackMissile(self, self.game.player, 20)
      self.game.add(missile)

    if dist >= 60:
      norm = direction.normalize()
      self.speed = norm * 50
    else:
      if canAttack:
        self.game.player.health -= self.attack - self.game.player.defense
      self.speed = pygame.Vector2(0, 0)

  def draw(self, screen: pygame.Surface):
    self._drawLifeBar(screen)