import pygame
from math import sqrt, pi
from vector import Vector #import the Vector class from vector.py
from object import Object  #import the Object class from object

#CONSTANTS-------------------------------

#-PHYSICS ELEMENT
GRAVITATION_CONSTANT = 6.6743 * 10**-11
G = 100

#-CODING ELEMENT
FPS = 60
WIDTH = 500
HEIGHT = 500
STATE_RUN = 0 #do not care about the values, just need them to be different
STATE_PAUSE = 1
DM = 10

#GLOBAL VARIABLES-----------------------
selected_object = None
state = STATE_RUN
last_mouse_pos = (200, -200)
draging = False
changing_velocity = False
time_scale = 1

def clear_screen(screen):
    screen.fill((0, 0, 0,))

def update(dt, ob_list):
    for ob in ob_list:
        total_acceleration = Vector(0, 0)
        for other_ob in ob_list:
            if other_ob != ob:
                total_acceleration += get_acceleration(ob, other_ob)
                ob.acceleration = total_acceleration
    for ob in ob_list:
        ob.update(dt)

def draw_objects(screen, ob_list):
    for ob in ob_list:
        ob.draw_object(screen)

def get_distance(o1, o2):
    return sqrt((o1.x - o2.x)**2 + (o1.y - o2.y)**2)

def get_acceleration(current_object, other_object):
    distance = get_distance(current_object, other_object)
    g = G * other_object.mass / distance ** 2
    direction = Vector(other_object.x - current_object.x, other_object.y - current_object.y)
    return (direction * (1/distance)) * g

def show_text(screen, object, x, y, size=30, color=(255, 255, 255)):
    font = pygame.font.Font(None, size)
    text_object = f"Mass: {object.mass}, Radius: {object.r:.2f}, Velocity: {object.velocity.x:.2f}, {object.velocity.y:.2f}"
    text_info_game_overall = f"Time scale: {time_scale}, State: {"Running" if state == STATE_RUN else "Paused"}"
    text_surface = font.render(text_object, True, color)
    text_info_surface = font.render(text_info_game_overall, True, color) #if text doesn't change, don't need to render again.
    screen.blit(text_surface, (x, y))
    screen.blit(text_info_surface, (x, y + size + 5))

def show_vector(screen, ob_vector, color=(255, 255, 255)):
    pygame.draw.circle(screen, color, (ob_vector.x, ob_vector.y), 5)
    pygame.draw.line(screen, color, (ob_vector.x, ob_vector.y), (ob_vector.velocity.x + ob_vector.x, ob_vector.velocity.y + ob_vector.y), 3)
    pygame.draw.circle(screen, color, (ob_vector.velocity.x + ob_vector.x, ob_vector.velocity.y + ob_vector.y), 5)
    """
    direction = Vector(vector.velocity.x, vector.velocity.y)

    left_end = Vector()

    line_arrow_left = pygame.draw.line(screen, color, (vector.velocity.x + vector.x, vector.velocity.y + vector.y), ()))

    arrow_length = 5
    arrow_width = 3

    direction = Vector(vector.velocity.x, vector.velocity.y)
"""
  

def handle_event(event, ob_list, screen): 
    global selected_object #need to modify the global variable
    global state
    global last_mouse_pos
    global draging
    global changing_velocity
    global time_scale

    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        state = STATE_RUN if state == STATE_PAUSE else STATE_PAUSE
        print(state)
        if selected_object:
            selected_object.unselect()
            selected_object = None

    if state == STATE_RUN: 
        pass
    else:
        if event.type == pygame.MOUSEBUTTONDOWN:
            generate_new = True
            if event.button == 1:
                draging = False
                for i in range(len(ob_list)):
                    if get_distance(ob_list[i], Object(event.pos[0], event.pos[1], Vector(0,0), 0, 0)) <= ob_list[i].r:
                        generate_new = False
                        temp = selected_object
                        if selected_object:
                            selected_object.unselect()
                            selected_object = None
                            
                        if temp != ob_list[i]:
                            selected_object = ob_list[i]
                            selected_object.select()
                
                if generate_new and selected_object is None:
                    new_object = Object(event.pos[0], event.pos[1], Vector(0,0), 20, 10)
                    ob_list.append(new_object)

                if changing_velocity and selected_object:
                    selected_object.unselect()
                    selected_object = None
                    changing_velocity = False

            elif event.button == 3:
                for i in range(len(ob_list)):
                    if get_distance(ob_list[i], Object(event.pos[0], event.pos[1], Vector(0,0), 0, 0)) <= ob_list[i].r:
                        generate_new = False
                        temp = selected_object
                        if selected_object:
                            selected_object.unselect()
                            selected_object = None
                            
                        if temp != ob_list[i]:
                            selected_object = ob_list[i]
                            selected_object.select()
                draging = True

        elif event.type == pygame.MOUSEMOTION:
            if draging and selected_object:
                selected_object.x, selected_object.y = event.pos

            elif selected_object:
                selected_object.velocity.x = event.pos[0] - selected_object.x
                selected_object.velocity.y = event.pos[1] - selected_object.y
                changing_velocity = True

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_PLUS:
            density = selected_object.mass / (4/3 * pi * selected_object.r**3)
            selected_object.mass += DM
            selected_object.r = ((3 * selected_object.mass)/(4 * pi * density))**(1/3)
        
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_MINUS:
            density = selected_object.mass / (4/3 * pi * selected_object.r**3)
            if selected_object.mass > DM:
                selected_object.mass -= DM
                selected_object.r = ((3 * selected_object.mass)/(4 * pi * density))**(1/3)

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            time_scale *= 2

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            time_scale /= 2

def main():
    global state
    global time_scale

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2D Gravity Simulation")

    clock = pygame.time.Clock()

    running = True

    ob_list = [
        Object(WIDTH/2, HEIGHT/2, Vector(0,0), 100, 20),
        Object(WIDTH/2 - 50, HEIGHT/2, Vector(0,-100), 10, 5),
        Object(WIDTH/2 + 100, HEIGHT/2, Vector(0,50), 20, 7),
        Object(WIDTH/2, HEIGHT/2 + 150, Vector(-50,0), 30, 10),
        Object(WIDTH/2, HEIGHT/2 - 200, Vector(50,0), 40, 12)
    ]

    while running:
        dt = clock.tick(FPS)/1000 #detla time in milliseconds since last frame and convert to seconds
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
            
            handle_event(event, ob_list, screen)

        if state == STATE_RUN: 
            update(dt*time_scale, ob_list)

        clear_screen(screen)
        draw_objects(screen, ob_list)

        if selected_object:
            show_text(screen, selected_object, 10, 10) #shows per frame if an object is selected. Resets with each new event.
            show_vector(screen, selected_object)
        pygame.display.flip()
        

if __name__ == "__main__":
    main()

