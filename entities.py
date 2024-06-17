import pygame, input_manager, sprite_manager

class Entity(pygame.Rect):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.velocity = [0, 0]
        self.collision_check_steps = 5
        self.is_on_floor = False
        self.is_on_roof = False
        self.is_on_left_wall = False
        self.is_on_right_wall = False
    
    def move_and_slide(self, rect_list:list[pygame.Rect]):
        self.is_on_floor = False
        self.is_on_roof = False
        self.is_on_left_wall = False
        self.is_on_right_wall = False
        
        for i in range(self.collision_check_steps):
            x_rect = pygame.Rect(self.left, self.top, self.width, self.height)
            x_rect.left += self.velocity[0] / (i+1)
            x_coll = x_rect.collidelist(rect_list)
            
            if x_coll == -1:
                self.left = x_rect.left
                break
            else:
                if self.velocity[0] > 0:
                    self.is_on_right_wall = True
                if self.velocity[0] < 0:
                    self.is_on_left_wall = True
    
        for i in range(self.collision_check_steps):
            y_rect = pygame.Rect(self.left, self.top, self.width, self.height)
            y_rect.top += self.velocity[1] / (i+1)
            y_coll = y_rect.collidelist(rect_list)
            
            if y_coll == -1:
                self.top = y_rect.top
                break
            else:
                if self.velocity[1] > 0:
                    self.is_on_floor = True
                if self.velocity[1] < 0:
                    self.is_on_roof = True

class Player(Entity):
    def __init__(self, position:list, size:list, spriteHandler:sprite_manager.SpriteManager):
        Entity.__init__(self, position[0], position[1], size[0], size[1])
        self.speed = 250
        self.jump_force = 320
        self.collision_check_steps = self.speed // 25
        self.sprite = spriteHandler.get_sprite('player')
        self.sprite = pygame.transform.scale(self.sprite, [size[0], size[1]])
        self.jumping = True
    
    def update(self, input:input_manager.InputManager, rect_list:list[pygame.Rect], delta:float, gravity:float):
        input_dir_x = 0
        if input.get_key_state(pygame.K_a): input_dir_x -= 1
        if input.get_key_state(pygame.K_d): input_dir_x += 1
        
        self.velocity = [input_dir_x * delta * self.speed, self.velocity[1]]
        self.velocity[1] += gravity * delta
        self.move_and_slide(rect_list)

        if self.is_on_floor:
            self.velocity[1] = 1
            self.jumping = False
            
            if input.get_key_state(pygame.K_SPACE):
                self.velocity[1] = -self.jump_force * 0.01
                self.jumping = True
        #else:
        #    if self.velocity[1] < 0 and input.get_key_state(pygame.K_SPACE) == False and self.jumping:
        #        self.velocity[1] += (self.jump_force/4) * delta

        if self.is_on_roof:
            self.velocity[1] += abs(self.velocity[1]) * delta * 100
    
    def draw(self, surf:pygame.Surface, offset:list):
        surf.blit(self.sprite, [self.left + offset[0], self.top + offset[1]])
