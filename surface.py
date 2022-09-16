from math import pi, cos, sin
import numpy as np
import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

BG_COLOR = BLACK

ROTATE_STEP = 0.02

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

CAMERA_POSITION = [0, 0, -30]
# CAMERA_ORIENTATION = (0, 0, 0)


def init_graph(): 
    global screen, display, clock, font, screen_size, screen_center
    pygame.init()
    # screen = pygame.display.set_mode((1280, 769))
    screen = pygame.display.set_mode((1280, 769), vsync=True)
    # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, vsync=True)
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
        [0, cos(a), -sin(a)],
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


def init_mesh():
    global suraface_mesh, VERTICES, EDGES

    VERTICES = []
    EDGES = []

    cell_size = 1

    cells_x = 50
    cells_y = 50

    for i in range(cells_x):
        for j in range(cells_y):
            x = (i - cells_x / 2) * cell_size
            y = (j - cells_y / 2) * cell_size
            # z = sin(x/2) + cos(y/2)
            z = sin((x ** 2 + y ** 2)/30)
            VERTICES.append((x, y, z))
            if j > 0:
                EDGES.append((j + i * cells_x, (j - 1) + i * cells_x))

    for j in range(cells_y):
        for i in range(cells_x):
            if i > 0:
                EDGES.append((j + i * cells_x, j + (i - 1) * cells_x))


def draw_scene():
    global angle_x, angle_y, angle_z

    camera = np.array(CAMERA_POSITION)
    center = np.array(screen_center)
    verts = np.array(VERTICES)

    verts = rotate_x(verts, angle_x)
    verts = rotate_y(verts, angle_y)
    verts = rotate_z(verts, angle_z)

    # angle_x += -.02
    # angle_y += -.02
    # angle_z += -.02

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

    for v in verts2:
        screen.set_at((int(v[0]), int(v[1])), RED)


if __name__ == '__main__':
    init_graph()
    init_mesh()

    angle_x = 0
    angle_y = 0
    angle_z = 0

    loop = 1
    while loop:
        screen.fill(BG_COLOR)

        display_fps()
        draw_scene()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = 0
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    angle_y -= ROTATE_STEP

        #         if event.key == pygame.K_RIGHT:
        #             angle_y += ROTATE_STEP

        #         if event.key == pygame.K_UP:
        #             angle_x -= ROTATE_STEP

        #         if event.key == pygame.K_DOWN:
        #             angle_x += ROTATE_STEP

        keys = pygame.key.get_pressed()                    
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            angle_y -= ROTATE_STEP
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            angle_y += ROTATE_STEP

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            angle_x -= ROTATE_STEP
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            angle_x += ROTATE_STEP

        if keys[pygame.K_q]:
            angle_z += ROTATE_STEP
        elif keys[pygame.K_e]:
            angle_z -= ROTATE_STEP

        if keys[pygame.K_r] and CAMERA_POSITION[2] < -5:
            CAMERA_POSITION[2] += 1
        elif keys[pygame.K_f]:
            CAMERA_POSITION[2] -= 1


        clock.tick(60)
        pygame.display.flip()
     
    pygame.quit()