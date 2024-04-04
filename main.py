import pygame

import geom
from widgets import Label, Button

pygame.init()

screen = pygame.display.set_mode((1200, 900))

b_points = Button(screen, (180, 20, 10), (180, 80, 10), (10, 75, 20), pygame.font.SysFont(None, 30), "Points",
                  (183, 183, 183), 200, 800, 100, 50)
b_circles = Button(screen, (180, 20, 10), (180, 80, 10), (10, 75, 20), pygame.font.SysFont(None, 30), "Circles",
                   (183, 183, 183), 400, 800, 100, 50)
b_lines = Button(screen, (180, 20, 10), (180, 80, 10), (10, 75, 20), pygame.font.SysFont(None, 30), "Lines",
                 (183, 183, 183), 600, 800, 100, 50)
b_clear = Button(screen, (180, 20, 10), (180, 80, 10), (10, 75, 20), pygame.font.SysFont(None, 30), "Clear",
                 (183, 183, 183), 800, 800, 100, 50)
undo = Button(screen, (180, 20, 10), (180, 80, 10), (10, 75, 20), pygame.font.SysFont(None, 30), "Undo",
              (183, 183, 183), 1000, 800, 100, 50)

render_type = geom.Shape.IDLE

points = list()
lines = list()
circles = list()
cal_pos = (-2, -2)
oc = geom.Occupied()
press_hist_l = list()
press_hist_c = list()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        pos = pygame.mouse.get_pos()
        if b_points.handle_event(event, pos):
            render_type = geom.Shape.POINT
        if b_circles.handle_event(event, pos):
            render_type = geom.Shape.CIRCLE
        if b_lines.handle_event(event, pos):
            render_type = geom.Shape.LINE
        if b_clear.handle_event(event, pos):
            points = []
            lines = []
            circles = []
            press_hist_l = []
            press_hist_c = []
            oc = geom.Occupied()
        if undo.handle_event(event, pos):
            match render_type:
                case geom.Shape.POINT:
                    points.pop()
                case geom.Shape.LINE:
                    lines.pop()
                case geom.Shape.CIRCLE:
                    circles.pop()
                case geom.Shape.IDLE:
                    pass
        pressed = pygame.mouse.get_pressed()
        cal_pos = None
        if pos[1] < 800:
            cal_pos = pos
            if not 20 < pos[0] % 75 < 50 and not 20 < pos[1] % 75 < 50:
                cal_pos = (pos[0] - pos[0] % 75 + 50, pos[1] - pos[1] % 75 + 50)
        if pressed[0] and cal_pos is not None:
            oc.add_point(cal_pos)
            match render_type:
                case geom.Shape.POINT:
                    points.append(geom.Point(screen, cal_pos, connection=False))
                case geom.Shape.LINE:
                    press_hist_l.append(cal_pos)
                    if len(press_hist_l) % 2 == 0:
                        lines.append(geom.Line(screen, press_hist_l[-1], press_hist_l[-2]))
                case geom.Shape.CIRCLE:
                    press_hist_c.append(cal_pos)
                    if len(press_hist_c) % 3 == 0:
                        if press_hist_c[-1] != press_hist_c[-2] and press_hist_c[-3] != press_hist_c[-2] and \
                                press_hist_c[-1] != press_hist_c[-3]:
                            circles.append(
                                geom.Circle(screen, press_hist_c[-1], press_hist_c[-2], press_hist_c[-3]))
    screen.fill((0, 0, 0))
    for i in range(16):
        pygame.draw.line(screen, (200, 200, 200), (50 + 75 * i, 0), (50 + 75 * i, 800))
    for j in range(12):
        pygame.draw.line(screen, (200, 200, 200), (0, 50 + 75 * j), (1200, 50 + 75 * j))
    for point in points:
        point.draw()
    for line in lines:
        line.draw()
    for circle in circles:
        try:
            circle.draw()
        except TypeError:
            pass

    b_points.render()
    b_lines.render()
    b_circles.render()
    b_clear.render()
    undo.render()
    if cal_pos is not None and not oc.if_is_occupied(cal_pos):
        pygame.draw.circle(screen, (80, 80, 80), cal_pos, 10)
    pygame.display.update()

pygame.quit()
