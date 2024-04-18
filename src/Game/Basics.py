import pygame

def blitRotate(surf, image, pos, originPos, angle):
  # offset from pivot to center
  image_rect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
  offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
  
  # roatated offset from pivot to center
  rotated_offset = offset_center_to_pivot.rotate(-angle)

  # roatetd image center
  rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

  # get a rotated image
  rotated_image = pygame.transform.rotate(image, angle)
  rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)

  # rotate and blit the image
  surf.blit(rotated_image, rotated_image_rect)

  # draw rectangle around the image
  # pygame.draw.rect(surf, (255, 0, 0), (*rotxated_image_rect.topleft, *rotated_image.get_size()),2)

class GameEntity:
  game = None
  def __init__(self, parent = None) -> None:
    self.rect = pygame.Rect(0, 0, 0, 0)
    self.parent = parent

  def attachTo(self, entity) -> None:
    self.parent = entity

  def _enterGame(self, game) -> None:
    self.game = game

  def _leaveGame(self) -> None:
    self.game = None

  def _update(self, deltaSeconds: float) -> None:
    if self.parent != None:
      if self.parent.game == None:
        self.game.remove(self)
    self.update(deltaSeconds)

  def _draw(self, screen: pygame.Surface) -> None:
    if self.parent != None:
      original = self.rect.center
      self.rect.x += self.parent.rect.x
      self.rect.y += self.parent.rect.y
      self.draw(screen)
      self.rect.x = original[0]
      self.rect.y = original[1]
    else:
      self.draw(screen)

  def update(self, deltaSeconds: float) -> None: pass
  def draw(self, screen: pygame.Surface) -> None: pass

class EntitiesProcessor(GameEntity):
  def __init__(self):
    self.entities: list[GameEntity] = []

  def add(self, entity):
    self.entities.append(entity)

  def remove(self, entity):
    self.entities.remove(entity)

  def update(self, deltaSeconds):
    for entity in self.entities:
      entity._update(deltaSeconds)

  def draw(self, screen):
    for entity in self.entities:
      entity._draw(screen)

class SpriteAnimated(GameEntity):
  def __init__(self, image, frames, fps, type = 'loop', parent = None):
    super().__init__(parent)
    self.image = image
    self.imageFlipped = pygame.transform.flip(self.image, True, False)
    self.frames = frames
    self.fps = fps
    self.currentFrame = 0
    self.timer = 0
    self.flipped = False
    self.rotation = 0.0
    self.type = type

  def _nextFrame(self):
      self.currentFrame += 1
      if self.type == 'loop':
        if self.currentFrame >= len(self.frames):
          self.currentFrame = 0
      elif self.type == 'once':
        if self.currentFrame >= len(self.frames):
          self.currentFrame = len(self.frames)
          if self.game != None:
            self.game.remove(self)

  def update(self, deltaSeconds):
    self.timer += deltaSeconds
    if self.timer > 1.0 / self.fps:
      self._nextFrame()
      self.timer = 0

  def draw(self, screen):
    position = pygame.Vector2(self.rect.left, self.rect.top)
    if (self.parent != None):
      position += pygame.Vector2(self.parent.rect.left, self.parent.rect.top)

    drawImage = self.image if not self.flipped else self.imageFlipped

    if self.currentFrame >= len(self.frames):
      return

    if self.rotation != 0:
      frameImage = drawImage.subsurface(self.frames[self.currentFrame])
      blitRotate(screen, frameImage, position, (self.rect.w / 2, self.rect.h / 2), self.rotation)
    else:
      screen.blit(drawImage, position, self.frames[self.currentFrame])

  def copy(self, parent):
    return SpriteAnimated(self.image, self.frames, self.fps, self.type, parent)

class SpriteManager(GameEntity):
  def __init__(self, parent):
    super().__init__(parent)
    self.sprites: dict[str, SpriteAnimated] = {}
    self.currentSprite: SpriteAnimated = None
    self.flipped = False
    self.rotation = 0.0

  def copy(self, parent):
    spriteManager = SpriteManager(parent)
    for name in self.sprites:
      spriteManager.add(name, self.sprites[name].copy(parent))
    return spriteManager

  def set(self, name):
    if name in self.sprites:
      self.currentSprite = self.sprites[name]

  def flip(self):
    self.flipped = not self.flipped

  def add(self, name, sprite):
    self.sprites[name] = sprite

  def get(self, name):
    return self.sprites[name].copy()
  
  def remove(self, name):
    del self.sprites[name]

  def update(self, deltaSeconds):
    if self.currentSprite != None:
      self.rect = self.parent.rect.copy()
      self.currentSprite.parent = self
      self.currentSprite.flipped = self.flipped
      self.currentSprite.rotation = self.rotation
      self.currentSprite.update(deltaSeconds)

  def draw(self, screen):
    if self.currentSprite != None:
      self.rect = self.parent.rect.copy()
      self.currentSprite.parent = self
      self.currentSprite.flipped = self.flipped
      self.currentSprite.rotation = self.rotation
      self.currentSprite.draw(screen)

class SpriteStore:
  def __init__(self):
    self.sprites = {}

  def add(self, name, spriteManager):
    self.sprites[name] = spriteManager

  def get(self, name, parent) -> SpriteManager:
    return self.sprites[name].copy(parent)
  
  def remove(self, name):
    del self.sprites[name]

spriteStore = SpriteStore()

class GameCreature(GameEntity):
  def __init__(
      self,
      rect: pygame.Rect,
      moveSpeed: pygame.Vector2,
      health: int,
      max_health: int,
      attack: int,
      defense: int,
      name: str,
      skin: str
    ):
    super().__init__(None)
    self.rect = rect
    self.speed = pygame.Vector2(0, 0)
    self.moveSpeed = moveSpeed
    self.health = health
    self.max_health = max_health
    self.attack = attack
    self.defense = defense
    self.name = name
    self.skin_name = skin
    self.skin = spriteStore.get(self.skin_name, self)

  def update(self, deltaSeconds):
    self.rect.x += self.speed.x * deltaSeconds
    self.rect.y += self.speed.y * deltaSeconds

  def _drawLifeBar(self, screen: pygame.Surface):

    lifePercent = self.health / self.max_health

    rectColor = (0, 255, 0)
    if (lifePercent < 0.2):
      rectColor = (50, 0, 0)
    elif (lifePercent < 0.4):
      rectColor = (240, 0, 0)
    elif (lifePercent < 0.75):
      rectColor = (100, 100, 0)
    elif (lifePercent < 1):
      rectColor = (0, 200, 0)

    lifeBarWidth = 60
    lifeBarHeight = 10
    lifeBar = pygame.Surface((lifeBarWidth, lifeBarHeight))
    lifeBar.fill((0, 0, 0))
    lifeBarX = self.rect.x + self.rect.w / 2 - lifeBarWidth / 2
    lifeBarY = self.rect.y
    pygame.draw.rect(lifeBar, rectColor, (0, 0, lifeBarWidth * self.health / self.max_health, lifeBarHeight))
    screen.blit(lifeBar, (lifeBarX, lifeBarY))

  def draw(self, screen):
    pass
