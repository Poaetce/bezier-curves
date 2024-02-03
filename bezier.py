import pygame

pygame.init()
pygame.display.set_caption("Bézier curves")
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

holding_right = False
holding_left = False

POINT_SIZE = 5
THICKNESS = 1
CURVE_THICKNESS = 4

T_INCREMENT = 0.005

BACKGROUND_COLOUR = (255, 255, 255)
MAIN_COLOUR = (0, 255, 255)
COLOUR_CHANGE_INDEX = (0, 0, 1)

points = []
t = 0.5


def draw_points(points: list, colour: tuple, point_size: int):
    if len(points) == 1:
        pygame.draw.circle(screen, colour, points[0], point_size * 2)

    else:
        for point in points:
            pygame.draw.circle(screen, colour, point, point_size)


def draw_lines(points: list, colour: tuple, line_thickness: int):
    for index in range(len(points) - 1):
        point_1 = points[index]
        point_2 = points[index + 1]

        pygame.draw.line(screen, colour, point_1, point_2, line_thickness)
        

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


def draw_layers(points: list, t: float, main_colour: tuple, colour_change_index: tuple, point_size: int, line_thickness: int):
    layers = loop_lerp(points, t)
    layer_count = len(layers)
    colour_change = 255 / (layer_count)

    for index in range(layer_count):
        layer = layers[index]
        colour = (
            main_colour[0] - colour_change_index[0] * colour_change * index,
            main_colour[1] - colour_change_index[1] * colour_change * index,
            main_colour[2] - colour_change_index[2] * colour_change * index,
        )

        draw_points(layer, colour, point_size)
        draw_lines(layer, colour, line_thickness)


def curve_point(points: list, t: float):
    layers = loop_lerp(points, t)
    if layers[-1]:
        return layers[-1][0]


def trace_curve(points: list, colour: tuple, curve_thickness: int):
    POINT_COUNT = 100
    previous_point = ()
    for index in range(POINT_COUNT):
        t = index / POINT_COUNT
        point = curve_point(points, t)
        if point:
            if previous_point:
                pygame.draw.line(screen, colour, previous_point, point, curve_thickness)
            previous_point = point


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                points.append(pygame.mouse.get_pos())
                print("new point:", points[-1])

            if event.button == pygame.BUTTON_RIGHT and points:
                print("removed point:", points[-1])
                points.pop()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                holding_right = True
            if event.key == pygame.K_LEFT:
                holding_left = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                holding_right = False
                print("t:", round(t, 2))
            if event.key == pygame.K_LEFT:
                holding_left = False
                print("t:", round(t, 2))

            if event.key == pygame.K_r and points:
                points = []
                print("removed all points")
            
    if holding_right and t <= 1 - T_INCREMENT:
        t = t + T_INCREMENT
    if holding_left and t >= 0 + T_INCREMENT:
        t = t - T_INCREMENT
    
    screen.fill(BACKGROUND_COLOUR)

    draw_layers(points, t, MAIN_COLOUR, COLOUR_CHANGE_INDEX, POINT_SIZE, THICKNESS)
    trace_curve(points, MAIN_COLOUR, CURVE_THICKNESS)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()