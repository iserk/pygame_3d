from math import cos, sin
import numpy as np
import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

BG_COLOR = BLACK

VERTICES = (
    (-10, -10, -10),
    ( 10, -10, -10),
    ( 10,  10, -10),
    (-10,  10, -10),

    (-10, -10,  10),
    ( 10, -10,  10),
    ( 10,  10,  10),
    (-10,  10,  10),
)

EDGES = (
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7),
)

CAMERA_POSITION = (0, 0, -30)
# CAMERA_ORIENTATION = (0, 0, 0)


def init_graph(): 
    global screen, display, clock, font, screen_size, screen_center
    pygame.init()
    # screen = pygame.display.set_mode((1280, 769))
    screen = pygame.display.set_mode((1280, 769), vsync=True)
    # screen = pygame.display.set_mode((0, 0), pygame.DOUBLEBUF | pygame.FULLSCREEN, vsync=True)
    screen_size = pygame.display.get_surface().get_size()

    screen_center = screen_size[0] / 2, screen_size[1] / 2

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18)
  

def display_fps():
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, 1, pygame.Color("lime"))
    screen.blit(fps_text, (10, 0))

    # Shows resolution
    screen.blit(
        font.render(
            "{} x {}".format(*screen_size), 1, pygame.Color("lime")
        ),
        (screen_size[0] - 120, 0)
    )


def rotate_x(verts, a):
    transform_matrix = np.array([
        [1, 0, 0],
        [0, cos(a), sin(a)],
        [0, sin(a), cos(a)],
    ])
    return np.transpose(np.dot(transform_matrix, np.transpose(verts)))


def rotate_y(verts, a):
    transform_matrix = np.array([
        [cos(a), 0, -sin(a)],
        [0, 1, 0],
        [sin(a), 0, cos(a)],
    ])
    return np.transpose(np.dot(transform_matrix, np.transpose(verts)))


def rotate_z(verts, a):
    transform_matrix = np.array([
        [cos(a), sin(a), 0],
        [-sin(a), cos(a), 0],
        [0, 0, 1],
    ])
    return np.transpose(np.dot(transform_matrix, np.transpose(verts)))


def draw_scene():
    global angle_y

    camera = np.array(CAMERA_POSITION)
    center = np.array(screen_center)
    verts = np.array(VERTICES)

    verts = rotate_y(verts, angle_y)

    angle_y += -.02

    verts = np.subtract(verts, camera)

    # Screen size
    sx, sy = screen_size[0], screen_size[1]

    # Recording surface size — rx, ry; rz — distance from the recording surface to the camera center (entrance pupil)
    rx, ry, rz = sx / sy * 1, 1, 2

    verts2 = [[
            v[0] * sx / (v[2] * rx * rz),
            v[1] * sy / (v[2] * ry * rz)
        ] for v in verts
    ]

    verts2 = np.add(verts2, center)

    for edge in EDGES:
        pygame.draw.line(screen, GREEN, (*verts2[edge[0]],), (*verts2[edge[1]], ))



if __name__ == '__main__':
    init_graph()

    angle_y = 0

    loop = 1
    while loop:
        screen.fill(BG_COLOR)

        display_fps()
        draw_scene()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = 0
        clock.tick(60)
        pygame.display.flip()
     
    pygame.quit()