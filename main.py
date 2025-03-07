import pygame

import geom
from widgets import Label, Button

pygame.init()
screen = pygame.display.set_mode((1200, 900))
pygame.display.set_caption("VisGeom")

b_points = Button(screen, (180, 20, 10), (180, 80, 10), (10, 75, 20), pygame.font.SysFont(None, 50), ".",
                  (183, 183, 183), 160, 830, 40, 40)
b_circles = Button(screen, (180, 20, 10), (180, 80, 10), (10, 75, 20), pygame.font.SysFont(None, 50), "o",
                   (183, 183, 183), 220, 830, 40, 40)
b_lines = Button(screen, (180, 20, 10), (180, 80, 10), (10, 75, 20), pygame.font.SysFont(None, 50), "/",
                 (183, 183, 183), 280, 830, 40, 40)
b_protractor = Button(screen, (180, 20, 10), (180, 80, 10), (10, 75, 20), pygame.font.SysFont(None, 20), "Protractor",
                 (183, 183, 183), 400, 820, 70, 50)
b_save = Button(screen, (180, 20, 10), (180, 80, 10), (10, 75, 20), pygame.font.SysFont(None, 30), "Capture",
                 (183, 183, 183), 880, 820, 90, 50)
b_clear = Button(screen, (180, 20, 10), (180, 80, 10), (10, 75, 20), pygame.font.SysFont(None, 30), "Clear",
                 (183, 183, 183), 1000, 820, 70, 50)
undo = Button(screen, (180, 20, 10), (180, 80, 10), (10, 75, 20), pygame.font.SysFont(None, 30), "Undo",
              (183, 183, 183), 1100, 820, 70, 50)

render_type = geom.Shape.IDLE
render_type_hist = list()
screenshot_count = 0

points = list()
lines = list()
circles = list()
cal_pos = (-2, -2)
oc = geom.Occupied()
grid = geom.Occupied()
press_hist_l = list()
press_hist_c = list()
clicked = list()

protractor = pygame.image.load("protractor.png")
protractor_flipped = pygame.transform.flip(protractor, False, True)
toggle_protractor = False
toggle_flip = False
protractor_positions = geom.Occupied()
protractor_flip_positions = geom.Occupied()

for i in range(16):
    for j in range(12):
        grid.add_point((50+i*75, 50+j*75))


running = True
while running:
    b_save.clicked = False
    undo.cliced = False
    b_clear.clicked = False
    if render_type == geom.Shape.IDLE:
        b_circles.clicked = False
        b_lines.clicked = False
        b_points.clicked = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        pos = pygame.mouse.get_pos()
        if b_points.handle_event(event, pos):
            render_type_hist.append(render_type)
            render_type = geom.Shape.POINT
            b_points.clicked = True
            b_circles.clicked = False
            b_lines.clicked = False
        if b_circles.handle_event(event, pos):
            render_type_hist.append(render_type)
            render_type = geom.Shape.CIRCLE
            b_circles.clicked = True
            b_lines.clicked = False
            b_points.clicked = False
        if b_lines.handle_event(event, pos):
            render_type_hist.append(render_type)
            render_type = geom.Shape.LINE
            b_lines.clicked = True
            b_circles.clicked = False
            b_points.clicked = False
        if b_save.handle_event(event, pos):
            screenshot_count += 1
            pygame.image.save(screen, f"screenshot_{screenshot_count}.jpg")
        if b_clear.handle_event(event, pos):
            points = []
            lines = []
            circles = []
            press_hist_l = []
            press_hist_c = []
            oc = geom.Occupied()
            protractor_positions = geom.Occupied()
            protractor_flip_positions = geom.Occupied()
        if b_protractor.handle_event(event, pos):
            render_type_hist.append(render_type)
            if toggle_flip:
                render_type = geom.Misc.FLIP_PROTRACTOR
            else:
                render_type = geom.Misc.PROTRACTOR
            toggle_protractor = not toggle_protractor
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
                    case geom.Misc.PROTRACTOR:
                        protractor_positions.occ_pts.pop()
                    case geom.Misc.FLIP_PROTRACTOR:
                        protractor_flip_positions.occ_pts.pop()
                render_type_hist.pop()
                render_type = render_type_hist[-1]
            except IndexError:
                pass
            undo.clicked = False
        pressed = pygame.mouse.get_pressed()
        cal_pos = None
        if pos[1] < 800:
            if oc.in_vicinity(pos) is not None:
                cal_pos = oc.in_vicinity(pos)
            elif grid.in_vicinity(pos) is not None:
                cal_pos = grid.in_vicinity(pos)
            else:
                cal_pos = pos
        if not toggle_protractor:
            if (pressed[0] or pressed[2]) and cal_pos is not None:
                if pressed[2]: cal_pos = pos
                oc.add_point(cal_pos)
                match render_type:
                    case geom.Shape.POINT:
                        render_type_hist.append(render_type)
                        points.append(geom.Point(screen, cal_pos, connection=0))
                    case geom.Shape.LINE:
                        press_hist_l.append(cal_pos)
                        if len(press_hist_l) % 2 == 0:
                            render_type_hist.append(render_type)
                            lines.append(geom.Line(screen, press_hist_l[-1], press_hist_l[-2]))
                            clicked = list()
                        else:
                            clicked.append(geom.Point(screen, cal_pos, connection=3))
                    case geom.Shape.CIRCLE:
                        press_hist_c.append(cal_pos)
                        if len(press_hist_c) % 3 == 0:
                            render_type_hist.append(render_type)
                            if press_hist_c[-1] != press_hist_c[-2] and press_hist_c[-3] != press_hist_c[-2] and \
                                    press_hist_c[-1] != press_hist_c[-3]:
                                _circ = geom.Circle(screen, press_hist_c[-1], press_hist_c[-2], press_hist_c[-3])
                                circles.append(_circ)
                                oc.add_point(_circ.c)
                                clicked = list()
                        else:
                            clicked.append(geom.Point(screen, cal_pos, connection=3))
        elif toggle_protractor:
            if pressed[0] and pos[1] < 800:
                if toggle_flip:
                    render_type = geom.Misc.FLIP_PROTRACTOR
                    render_type_hist.append(render_type)
                    protractor_flip_positions.add_point(cal_pos)
                else:
                    render_type = geom.Misc.PROTRACTOR
                    render_type_hist.append(render_type)
                    protractor_positions.add_point(cal_pos)
            elif pressed[2]:
                toggle_flip = not toggle_flip

    screen.fill((250, 250, 250))
    if toggle_protractor:
        if toggle_flip:
            screen.blit(protractor_flipped, (pos[0]-360, pos[1]-300))
        else:
            screen.blit(protractor, (pos[0]-360, pos[1]-300))
    for i in protractor_positions.occ_pts:
        screen.blit(protractor, (i[0]-360, i[1]-300))
    for i in protractor_flip_positions.occ_pts:
        screen.blit(protractor_flipped, (i[0]-360, i[1]-300))
    for i in range(16):
        pygame.draw.line(screen, (200, 200, 250), (50 + 75 * i, 0), (50 + 75 * i, 800))
    for j in range(12):
        pygame.draw.line(screen, (200, 200, 250), (0, 50 + 75 * j), (1200, 50 + 75 * j))
    for point in points:
        point.draw()
    for line in lines:
        line.draw()
    for circle in circles:
        try:
            circle.draw()
        except TypeError:
            pass
    for clicks in clicked:
        clicks.draw()

    if len(lines) >= 1:
        for line1 in lines:
            for line2 in lines:
                if line1.m == 0 and line2.m != 0:
                    if line2.pos[0][0] <= line1.pos[0][0] <= line2.pos[1][0]:
                        int_x = line1.pos[0][0]
                        int_y = line2.m * int_x + line2.c
                        oc.add_point((int_x, int_y))
                        points.append(geom.Point(screen, (int_x, int_y), connection=2))
                elif line2.m == 0 and line1.m != 0:
                    if line1.pos[0][0] <= line2.pos[0][0] <= line1.pos[1][0]:
                        int_x = line2.pos[0][0]
                        int_y = line1.m * int_x + line1.c
                        oc.add_point((int_x, int_y))
                        points.append(geom.Point(screen, (int_x, int_y), connection=2))
                elif line1.m != 0 and line2.m != 0:
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

    b_circles.render()
    b_lines.render()
    b_points.render()
    b_protractor.render()
    b_save.render()
    b_clear.render()
    undo.render()
    if not toggle_protractor and cal_pos is not None and not oc.if_is_occupied(cal_pos):
        pygame.draw.circle(screen, (180, 80, 80), cal_pos, 7)
    pygame.display.update()

pygame.quit()
