import pygame, sys
import entities, sprite_manager, input_manager

pygame.init()

screen = pygame.display.set_mode([1280, 720])
clock = pygame.time.Clock()
delta :float= 0

sprite = sprite_manager.SpriteManager()
input = input_manager.InputManager([pygame.K_w, pygame.K_a, pygame.K_d, pygame.K_s, pygame.K_SPACE])

surf = pygame.Surface([16, 32])
surf.fill([255,0,0])
sprite.add_sprite("player", surf)

pygame.display.set_caption("Platformer")
player = entities.Player([200, 200], [24, 48], sprite)
player_collision_rect_list = [pygame.Rect(0, 600, 500, 128), pygame.Rect(0, 400, 128, 200), pygame.Rect(400, 600-32, 200, 32)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        input.poll(event)
            
    player.update(input, player_collision_rect_list, delta, 8)
    
    screen.fill([0, 0, 0])
    
    player.draw(screen, [0, 0])
    
    for rect in player_collision_rect_list:
        pygame.draw.rect(screen, [255,255,255], rect, 2)
    
    pygame.display.update()
    delta = clock.tick(60) / 1000