from Game.Basics import EntitiesProcessor
from Game.Basics import GameEntity
from Game.Player import Player

class Game:
  player: Player
  def __init__(self):
    self.entities = EntitiesProcessor()
    self.player = None

  def update(self, deltaSeconds):
    self.entities.update(deltaSeconds)

  def draw(self, screen):
    self.entities.draw(screen)

  def add(self, entity: GameEntity):
    self.entities.add(entity)
    entity._enterGame(self)

  def remove(self, entity: GameEntity):
    self.entities.remove(entity)
    entity._leaveGame()
