import pygame, input_manager

class Entity(pygame.Rect):
    def __init__(self, pos_x, pos_y, width, height):
        super().__init__(pos_x, pos_y, width, height)
        self.velocity = [0, 0]
        self.move_steps = 20
        self.on_left_wall = False
        self.on_right_wall = False
        self.on_bottom_wall = False
        self.on_top_wall = False
    
    def debug(self, velo:bool, on_walls:bool, pos:bool):
        if velo:
            print(f'v_x:{int(self.velocity[0])} v_y:{int(self.velocity[1])}')
        if on_walls:
            print(f'left_wall:{self.on_left_wall}   right_wall:{self.on_right_wall}   top_wall:{self.on_top_wall}   bottom_wall:{self.on_bottom_wall}')
        if pos:
            print(f'x:{int(self.left)} y:{int(self.top)}')
    
    def apply_gravity(self, gravity:int, weight:int=20):
        if self.on_bottom_wall:
            self.velocity[1] = 1
        else:
            self.velocity[1] += gravity * 0.01 
    
    def move_and_slide(self, rect_list:list[pygame.Rect]):
        last_x = self.left
        last_y = self.top
    
        check_rect = pygame.Rect(self.left, self.top, self.width, self.height)

        x_step_size = self.velocity[0] / self.move_steps
        y_step_size = self.velocity[1] / self.move_steps
        
        if self.velocity[0] != 0:
            for x in range(self.move_steps):
                check_rect.topleft = [self.left + (x_step_size*x), self.top]
                if check_rect.collidelist(rect_list) >= 0:
                    if self.velocity[0] > 0:
                        self.on_right_wall = True
                    if self.velocity[0] < 0:
                        self.on_left_wall = True
                    break
                else:
                    last_x = check_rect.left
                    if x == self.move_steps-1:
                        self.on_right_wall = False
                        self.on_left_wall = False
                    
        
        if self.velocity[1] != 0:
            for y in range(self.move_steps):
                check_rect.topleft = [last_x, self.top + (y_step_size*y)]
                if check_rect.collidelist(rect_list) >= 0:
                    if self.velocity[1] > 0:
                        self.on_bottom_wall = True
                    if self.velocity[1] < 0:
                        self.on_top_wall = True
                    break
                else:
                    last_y = check_rect.top
                    if y == self.move_steps-1:
                        self.on_top_wall = False
                        self.on_bottom_wall = False
        
        self.topleft = [last_x, last_y]

class Player(Entity):
    def __init__(self, pos_x:float, pos_y:float, width:int, height:int, speed:float, jump_force:float):
        super().__init__(pos_x, pos_y, width, height)
        self.speed = speed
        self.jump_force = jump_force
    
    def update(self, rect_list:list[pygame.Rect], input:input_manager.InputManager, gravity:float):
        input_dir_x = int(input.get_key_state(pygame.K_d)) - int(input.get_key_state(pygame.K_a))
        self.velocity[0] = input_dir_x * self.speed
        self.apply_gravity(gravity)
        
        if self.on_bottom_wall and input.get_key_state(pygame.K_SPACE):
            self.velocity[1] = -self.jump_force
        
        if self.velocity[1] < 0 and input.get_key_state(pygame.K_SPACE) == False:
            self.velocity[1] += 2
        
        if self.on_top_wall:
            self.velocity[1] += abs(self.velocity[1])
        
        self.move_and_slide(rect_list)