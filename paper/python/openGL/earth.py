'''
Created on 2015年12月14日

@author: cdz
'''

import openGL.ball as ball

from math import sin, cos
from PIL import Image
import sys
from OpenGL.GL import glRotate
try:
    from OpenGL.GLUT import *
    from OpenGL.GLU import *
    from OpenGL.GL import *
except Exception as e:
    print(e)
    sys.exit()
    
x = 15
eyex, eyey, eyez = 0, -3, 1.8
width = 0
height = 0
ANGLE_X, ANGLE_Y, ANGLE_Z = 0, 0, 0
CENTER_X ,CENTER_Y ,CENTER_Z = 0, 0, 0
RADIUS = 0.25
LATITUDE_NUM, LONGTITUDE_NUM = 32, 48
LIGHT_X, LIGHT_Y, LIGHT_Z = -0.25, 0.25, 0.75
ball_points = ball.subdivide(RADIUS, LATITUDE_NUM, LONGTITUDE_NUM)
bulb_points = ball.subdivide(0.01, 10, 10)
TEXTURE_ID = 0

def getXYZ(latitude, longtitude):
    global CENTER_X, CENTER_Y, CENTER_Z, RADIUS
    global ball_points
    x = CENTER_X + ball_points[latitude][longtitude][0]
    y = CENTER_Y + ball_points[latitude][longtitude][1]
    z = CENTER_Z + ball_points[latitude][longtitude][2]
    return x, y ,z

def getNormalXYZ(latitude, longtitude):
    global RADIUS
    x, y ,z = getXYZ(latitude, longtitude)
    return x / RADIUS, y / RADIUS, z / RADIUS

def init():
    global eyex, eyey, eyez
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(400, 400)
    glutInitWindowPosition(400, 400)
    glutCreateWindow(bytes('earth', encoding='GBK'))

    glClearColor (0.0, 0.0, 0.0, 0.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(eyex, eyey, eyez, 0,0,1,0,0,1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-2.0, 2.0, -2.0, 2.0, -1.0, 4.0)
    
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    #glEnable(GL_BLEND)
    # 深度测试
    glEnable(GL_DEPTH_TEST)
    # 反走样
    #glEnable(GL_POINT_SMOOTH)
    glEnable(GL_LINE_SMOOTH)
    glEnable(GL_POLYGON_SMOOTH)
    
    #glClearColor ( 0, 0, 0, 0 )
    glShadeModel( GL_SMOOTH )
    glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT )
    glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT )
    glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR )
    glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR )
    w, h, img = load_img()
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, w, h, 0, GL_RGB, GL_UNSIGNED_BYTE, img)
    glEnable( GL_TEXTURE_2D )
    
def load_img(path='d:/a.jpg'):
    _img = Image.open(path)
    img_w, img_h, img = _img.size[0], _img.size[1], _img.tobytes('raw', 'RGB', 0, -1)
    return img_w, img_h, img

def draw_triangle(x1, y1, z1, x2, y2, z2, x3, y3, z3):
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 1.0, 1.0)
    glVertex3f(x1, y1, z1)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(x2, y2, z2)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(x3, y3, z3)
    glEnd()
    
def draw_line(x1, y1, z1, x2, y2, z2):
    glColor3f(1,1,1)
    glBegin(GL_LINES)
    glVertex3f(x1, y1, z1)
    glVertex3f(x2, y2, z2)
    glEnd()
    
def draw_square(x, y, z, a, gray):    
    glBegin(GL_QUADS)
    glColor3f(gray, gray, gray)
    glNormal3f(0,0,1)
    glVertex3f(x, y, z)
    glNormal3f(0,0,1)
    glVertex3f(x + a, y, z)
    glNormal3f(0,0,1)
    glVertex3f(x + a, y + a, z)
    glNormal3f(0,0,1)
    glVertex3f(x, y + a, z)
    glEnd()
    
def draw_bottom():
    gray = 0.5
    a = 0.5
    for x in range(0, 4):
        for y in range(0, 4):
            gray = 0.5 + ((x + y) & 1) * 0.3
            draw_square(x * 0.5 - 1, y * 0.5 - 1, -1, a, gray)

def draw_axis():
    draw_line(0, 0, 0, 2, 0, 0)
    draw_line(0, 0, 0, 0, 2, 0)
    draw_line(0, 0, 0, 0, 0, 2)
    
def draw_light():
    global LIGHT_X, LIGHT_Y, LIGHT_Z
    light_position = [LIGHT_X, LIGHT_Y, LIGHT_Z, 0.0]
    #glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    #light_ambient =  [0.0, 0.0, 0.0, 1.0]
    light_ambient =  [0.65, 0.65, 0.65, 1.0]
    light_diffuse =  [1.0, 1.0, 1.0, 1.0]
    light_specular =  [1.0, 1.0, 1.0, 1.0]
    #  light_position is NOT default value
    #light_position =  [1.0, 1.0, 1.0, 0.0]
    
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)
    
def texture_map():
    global ball_points, CENTER_X, CENTER_Y, CENTER_Z, LIGHT_X, LIGHT_Y, LIGHT_Z
    glColor3f(1,1,1)
    glMatrixMode(GL_TEXTURE)
    # 分三步：1.画北极圈以北； 2.画北极圈和南极圈中间； 3.画南极圈以南    
    #glShadeModel(GL_FLAT)
    glBegin(GL_QUADS)
    for i in range(0, LATITUDE_NUM):
        for j in range(0, LONGTITUDE_NUM):
            glNormal3f(*getNormalXYZ(i, j))
            glTexCoord2f(j / LONGTITUDE_NUM, 1 - (i + 1) / LATITUDE_NUM)
            glVertex3f(*getXYZ(i, j))
            glNormal3f(*getNormalXYZ(i, (j + 1) % LONGTITUDE_NUM))
            glTexCoord2f((j + 1) / LONGTITUDE_NUM, 1 - (i + 1) / LATITUDE_NUM)
            glVertex3f(*getXYZ(i, (j + 1) % LONGTITUDE_NUM))
            glNormal3f(*getNormalXYZ(i + 1, (j + 1) % LONGTITUDE_NUM))
            glTexCoord2f((j + 1) / LONGTITUDE_NUM, 1 - (i + 2) / LATITUDE_NUM)
            glVertex3f(*getXYZ(i + 1, (j + 1) % LONGTITUDE_NUM))
            glNormal3f(*getNormalXYZ(i + 1, j))
            glTexCoord2f(j / LONGTITUDE_NUM, 1 - (i + 2) / LATITUDE_NUM)
            glVertex3f(*getXYZ(i + 1, j))
            pass
    glEnd()

def display():
    global ball_points, bulb_points, LIGHT_X, LIGHT_Y, LIGHT_Z
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(1,1,1)
    draw_axis()
    ball.draw_ball(LIGHT_X, LIGHT_Y, LIGHT_Z, bulb_points)
    
    draw_light()
    draw_bottom()
    texture_map()
    #glFlush()
    glutSwapBuffers()
    
def resize(w, h):
    global width
    width = w
    global height
    height = h
    glViewport(0,0,w,h);
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, w / h, 0.2, 40.0)
    
def onkey(key, x, y):
    global ANGLE_X, ANGLE_Y, ANGLE_Z
    if key == b'j':
#         glMatrixMode(GL_MODELVIEW)
#         glTranslate(0.1, 0, 0)
#         glMatrixMode(GL_PROJECTION)
#         glLoadIdentity()
#         gluPerspective(60, width / height, 0.2, 40.0)
        pass
    elif key == b'k':
#         glMatrixMode(GL_MODELVIEW)
#         glTranslate(-0.1, 0, 0)
#         glMatrixMode(GL_PROJECTION)
#         glLoadIdentity()
#         gluPerspective(60, width / height, 0.2, 40.0)
        pass
    elif key == b'w':
        if ANGLE_X < 80:
            glMatrixMode(GL_MODELVIEW)
            glRotate(-ANGLE_Z, 0, 0, 1)
            glRotate(10, 1, 0, 0)
            glRotate(ANGLE_Z, 0, 0, 1)
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            gluPerspective(60, width / height, 0.2, 40.0)
            ANGLE_X += 10
    elif key == b's':
        if ANGLE_X > -80:
            glMatrixMode(GL_MODELVIEW)
            glRotate(-ANGLE_Z, 0, 0, 1)
            glRotate(10, -1, 0, 0)
            glRotate(ANGLE_Z, 0, 0, 1)
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            gluPerspective(60, width / height, 0.2, 40.0)
            ANGLE_X -= 10
    elif key == b'a':
        glMatrixMode(GL_MODELVIEW)
        glRotate(-ANGLE_X, 1,0,0)
        glRotate(10, 0, 0, 1)
        glRotate(ANGLE_X, 1,0,0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, width / height, 0.2, 40.0)
        ANGLE_Z += 10
    elif key == b'd':
        glMatrixMode(GL_MODELVIEW)
        glRotate(-ANGLE_X, 1,0,0)
        glRotate(-10, 0, 0, 1)
        glRotate(ANGLE_X, 1,0,0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, width / height, 0.2, 40.0)
        ANGLE_Z -= 10
    glutPostRedisplay()
    
if __name__ == '__main__':
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(resize)
    glutKeyboardFunc(onkey)
    glutMainLoop()
    
