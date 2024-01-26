import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480))
running = True

POINT_SIZE = 5
LINE_THICKNESS = 1

T_INCREMENT = 0.01

BACKGROUND_COLOUR = (255, 255, 255)
MAIN_COLOUR = (0, 255, 255)
COLOUR_CHANGE_INDEX = (0, 0, 1)

points = []
layers = [points]

t = 0.5

def draw_points(points: list, colour: tuple):
    for point in points:
        pygame.draw.circle(screen, colour, point, POINT_SIZE)


def draw_lines(points: list, colour: tuple):
    for index in range(len(points) - 1):
        point_1 = points[index]
        point_2 = points[index + 1]

        pygame.draw.line(screen, colour, point_1, point_2, LINE_THICKNESS)
        

def lerp_points(points: list, t: float):
    lerps = []

    for index in range(len(points) - 1):
        point_1 = points[index]
        point_2 = points[index + 1]

        x = pygame.math.lerp(point_1[0], point_2[0], t)
        y = pygame.math.lerp(point_1[1], point_2[1], t)

        lerps.append((x, y))
    
    return lerps


def loop_lerp(points: list, t: float):
    layers = [points]
    last_layer = points

    while len(last_layer) > 1:
        layers.append(lerp_points(last_layer, t))
        last_layer = layers[-1]

    return layers


def draw_layers(layers: list):
    layer_count = len(layers)
    colour_change = 255 / (layer_count)
    for index in range(layer_count):
        layer = layers[index]
        colour = (
            MAIN_COLOUR[0] - COLOUR_CHANGE_INDEX[0] * colour_change * index,
            MAIN_COLOUR[1] - COLOUR_CHANGE_INDEX[1] * colour_change * index,
            MAIN_COLOUR[2] - COLOUR_CHANGE_INDEX[2] * colour_change * index,
        )

        draw_points(layer, colour)
        draw_lines(layer, colour)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONUP:
            points.append(pygame.mouse.get_pos())

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and t <= 1 - T_INCREMENT:
                t = t + T_INCREMENT
            
            if event.key == pygame.K_LEFT and t >= 0 + T_INCREMENT:
                t = t - T_INCREMENT
    
    screen.fill(BACKGROUND_COLOUR)

    layers = loop_lerp(points, t)

    draw_layers(layers)

    pygame.display.flip()

pygame.quit()