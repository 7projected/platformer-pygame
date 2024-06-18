import input_manager, pygame, math_functions

class Camera:
    def __init__(self, coords:list):
        self.position = coords
    
    def clamp(self, left:int, right:int, top:int, bottom:int):
        self.position[0] = math_functions.clamp(self.position[0], left, right)
        self.position[1] = math_functions.clamp(self.position[1], top, bottom)
    
    def debug(self, inputManager:input_manager.InputManager, dt:float, speed:int=500):
        dir = inputManager.getVector(pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s)
        self.position = [dir[0] * speed * dt, dir[1] * speed * dt]
    
    def get_offset(self) -> list:
        return [-self.position[0], -self.position[1]]

    def lerp_to(self, coords:list, dt:float, speed):
        dist = [coords[0] - self.position[0], coords[1] - self.position[1]]
        move = [dist[0] * 0.01 * speed * dt, dist[1] * 0.01 * speed * dt]
        self.position = [self.position[0] + move[0], self.position[1] + move[1]]