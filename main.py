import pygame

import geom
from widgets import Label, Button

pygame.init()
screen = pygame.display.set_mode((1200, 900))
pygame.display.set_caption("VisGeom")

b_points = Button(screen, (180, 20, 10), (180, 80, 10), (10, 75, 20), pygame.font.SysFont(None, 30), ".",
                  (183, 183, 183), 200, 830, 20, 20)
b_circles = Button(screen, (180, 20, 10), (180, 80, 10), (10, 75, 20), pygame.font.SysFont(None, 30), "o",
                   (183, 183, 183), 240, 830, 20, 20)
b_lines = Button(screen, (180, 20, 10), (180, 80, 10), (10, 75, 20), pygame.font.SysFont(None, 30), "/",
                 (183, 183, 183), 280, 830, 20, 20)
b_clear = Button(screen, (180, 20, 10), (180, 80, 10), (10, 75, 20), pygame.font.SysFont(None, 30), "Clear",
                 (183, 183, 183), 1000, 820, 70, 50)
undo = Button(screen, (180, 20, 10), (180, 80, 10), (10, 75, 20), pygame.font.SysFont(None, 30), "Undo",
              (183, 183, 183), 1100, 820, 70, 50)

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
            try:
                match render_type:
                    case geom.Shape.POINT:
                        points.pop()
                    case geom.Shape.LINE:
                        lines.pop()
                    case geom.Shape.CIRCLE:
                        circles.pop()
                    case geom.Shape.IDLE:
                        pass
            except IndexError:
                pass
        pressed = pygame.mouse.get_pressed()
        cal_pos = None
        if pos[1] < 800:
            if oc.in_vicinity(pos) is not None:
                cal_pos = oc.in_vicinity(pos)
            elif not (0 < pos[0] % 75 < 20 or 55 < pos[0] < 75) and not (0 < pos[1] % 75 < 20 or 55 < pos[1] < 75):
                cal_pos = (pos[0] - pos[0] % 75 + 50, pos[1] - pos[1] % 75 + 50)
            else:
                cal_pos = pos
        if pressed[0] and cal_pos is not None:
            oc.add_point(cal_pos)
            match render_type:
                case geom.Shape.POINT:
                    points.append(geom.Point(screen, cal_pos, connection=0))
                case geom.Shape.LINE:
                    press_hist_l.append(cal_pos)
                    if len(press_hist_l) % 2 == 0:
                        lines.append(geom.Line(screen, press_hist_l[-1], press_hist_l[-2]))
                    else:
                        points.append(geom.Point(screen, cal_pos, connection=3))
                case geom.Shape.CIRCLE:
                    press_hist_c.append(cal_pos)
                    if len(press_hist_c) % 3 == 0:
                        if press_hist_c[-1] != press_hist_c[-2] and press_hist_c[-3] != press_hist_c[-2] and \
                                press_hist_c[-1] != press_hist_c[-3]:
                            circles.append(
                                geom.Circle(screen, press_hist_c[-1], press_hist_c[-2], press_hist_c[-3]))
                    else:
                        points.append(geom.Point(screen, cal_pos, connection=3))
    screen.fill((50, 50, 50))
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

    if len(lines) >= 2:
        for line1 in lines:
            for line2 in lines:
                try:
                    int_x = (line2.c - line1.c) / (line1.m - line2.m)
                    int_y = line1.m * int_x + line1.c
                    if line1.pos[0][0] <= int_x <= line1.pos[1][0] and line1.pos[0][1] <= int_y <= line1.pos[1][1]\
                            or line1.pos[0][0] >= int_x >= line1.pos[1][0] and line1.pos[0][1] >= int_y >=\
                            line1.pos[1][1]\
                            and line2.pos[0][0] <= int_x <= line2.pos[1][0] and line2.pos[0][1] <= int_y <= line2.pos[1][1]\
                            or line2.pos[0][0] >= int_x >= line2.pos[1][0] and line2.pos[0][1] >= int_y >=\
                            line2.pos[1][1]:
                        oc.add_point((int_x, int_y))
                        points.append(geom.Point(screen, (int_x, int_y), connection=2))
                except ZeroDivisionError:
                    pass
                except AttributeError:
                    pass
            # TODO: Doesnt work
            '''for circ in circles:
                discriminant = (2 * line1.m * (line1.c - circ.c[1]) + 2 * circ.c[0]) ** 2 - 4 * (line1.m ** 2 + 1) * (
                            circ.c[0] ** 2 + (line1.c - circ.c[1]) ** 2 - circ.r ** 2)
                discriminant *= -1
                if discriminant == 0:
                    int_x = (-2 * line1.m * (line1.c - circ.c[1]) - 2 * circ.c[0]) / (2 * circ.c[0])
                    int_y = line1.m * int_x + line1.c
                    oc.add_point((int_x, int_y))
                    points.append(geom.Point(screen, (int_x, int_y), connection=2))
                elif discriminant > 0:
                    int_x1 = (-2 * line1.m * (line1.c - circ.c[1]) - 2 * circ.c[0] + discriminant ** (1 / 2)) / (
                                2 * circ.c[0])
                    int_x2 = (-2 * line1.m * (line1.c - circ.c[1]) - 2 * circ.c[0] - discriminant ** (1 / 2)) / (
                                2 * circ.c[0])
                    int_y1 = line1.m * int_x1 + line1.c
                    int_y2 = line1.m * int_x2 + line1.c
                    oc.add_point((int_x1, int_y1))
                    points.append(geom.Point(screen, (int_x1, int_y1), connection=2))
                    oc.add_point((int_x2, int_y2))
                    points.append(geom.Point(screen, (int_x2, int_y2), connection=2))
                else:
                    print("None")
                    print(discriminant)'''

    b_points.render()
    b_lines.render()
    b_circles.render()
    b_clear.render()
    undo.render()
    if cal_pos is not None and not oc.if_is_occupied(cal_pos):
        pygame.draw.circle(screen, (180, 80, 80), cal_pos, 10)
    pygame.display.update()

pygame.quit()
