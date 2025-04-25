from qx_settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self,pos,surf = pygame.Surface((tile_size,tile_size)),groups = None, z = Z_layers["main"]):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.old_rect = self.rect.copy()
        self.z = z

class AnimatedSprite(Sprite):
    def __init__ (self, pos, frames, groups, z = Z_layers["main"], animation_speed = animation_speed):
        self.frames, self.frame_index = frames, 0
        super().__init__(pos,self.frames[self.frame_index],groups,z)
        self.animation_speed = animation_speed

    def animate(self,dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]

    def update(self,dt):
        self.animate(dt)

class Node(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups,level,data,paths):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (pos[0] + tile_size/2, pos[1] + tile_size/2))
        self.z = Z_layers["path"]
        self.level = level
        self.data = data
        self.paths = paths
        self.grid_pos = (int(pos[0] /tile_size), int(pos[1] /tile_size))

    def can_move(self,direction):
        if direction in list(self.paths.keys()):
            return True

class Icon(pygame.sprite.Sprite):
    def __init__(self,pos,groups,frames):
        super().__init__(groups)
        self.icon = True
        self.path = None
        self.direction = vector()
        self.speed = 400

        #images
        self.frames, self.frame_index = frames, 0
        self.state = "idle"
        self.image = self.frames[self.state][self.frame_index]
        self.z = Z_layers["main"]

        #rect
        self.rect = self.image.get_frect(center = pos)

    def start_move(self,path):
        self.rect_center = path[0]
        self.path = path[1:]
        self.find_path()

    def find_path(self):
        if self.path:
            if self.rect.centerx == self.path[0][0]: #vertical
                self.direction = vector(0,1 if self.path[0][1] > self.rect.centery else - 1)
            else: #horizontal
                self.direction = vector(1 if self.path[0][0] > self.rect.centerx else - 1, 0)
        else:
            self.direction = vector()

    def point_collision(self):
        if self.direction.y == 1 and self.rect.centery >= self.path [0][1] or \
           self.direction.y == -1 and self.rect.centery <= self.path [0][1]:
            self.rect.centery = self.path[0][1]
            del self.path[0]
            self.find_path()
        
        if self.direction.x == 1 and self.rect.centerx >= self.path[0][0] or \
           self.direction.x == -1 and self.rect.centerx <= self.path[0][0]:
            self.rect.centerx = self.path[0][0]
            del self.path[0]
            self.find_path()

    def animate(self,dt):
        self.frame_index += animation_speed * dt
        self.image = self.frames[self.state][int(self.frame_index % len(self.frames[self.state]))]

    def get_state(self):
        self.state = "idle"
        if self.direction == vector(1,0) : self.state = "right"
        if self.direction == vector(-1,0) : self.state = "left"
        if self.direction == vector(0,1) : self.state = "down"
        if self.direction == vector(0,-1) : self.state = "up"

    def update(self,dt):
        if self.path:
            self.point_collision()
            self.rect.center += self.direction * self.speed * dt
        self.get_state()
        self.animate(dt)