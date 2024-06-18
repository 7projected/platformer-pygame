import pygame, sys
import entities, sprite_manager, input_manager

pygame.init()

screen = pygame.display.set_mode([1280, 720])
clock = pygame.time.Clock()

sprite = sprite_manager.SpriteManager()
input = input_manager.InputManager([pygame.K_w, pygame.K_a, pygame.K_d, pygame.K_s, pygame.K_SPACE])
surf = pygame.Surface([16, 32])
surf.fill([255,0,0])
sprite.add_sprite("player", surf)
pygame.display.set_caption("Platformer")

gravity :float= 30
entity = entities.Player(0, 0, 32, 64, 4, 7)
player_collision_rect_list = [pygame.Rect(0, 600, 500, 128), pygame.Rect(0, 400, 128, 200), pygame.Rect(400, 600-32, 200, 32), pygame.Rect(400, 600-(32*6), 200, 32)]

while True:
    screen.fill([0, 0, 0])
    pygame.draw.rect(screen, [255,0, 0], entity)    
    
    for rect in player_collision_rect_list:
        pygame.draw.rect(screen, [255,255,255], rect, 2)
    
    pygame.display.update()
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        input.poll(event)
    
    entity.update(player_collision_rect_list, input, gravity)    
    
    entity.move_and_slide(player_collision_rect_list)