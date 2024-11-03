import math,pygame

SCHWARZ = (0,0,0)
BLAU    = (17,69,126)
ROT     = (255,0,0)
ROT2    = (215,20,26)
ROT3    = (238,0,0)
WEISS   = (255,255,255)
GRUEN   = (46,139,87)
GELB    = (255,215,0)
GOLD    = (255,206,0)

SKY_BLUE = (117, 170, 219)
GREECE_BLUE = (0, 20, 137)

def pentagramm(cx,cy,cr):
    punkte = []
    r = math.sqrt((25-11*math.sqrt(5))/10)
    R = math.sqrt((5-math.sqrt(5))/10)
    for i in range(5):
        x1 = cx+cr*R*math.sin(2*i*math.pi/5)
        y1 = cy-cr*R*math.cos(2*i*math.pi/5)
        punkte.append((x1,y1))
        x2 = cx+cr*r*math.sin((2*i+1)*math.pi/5)
        y2 = cy-cr*r*math.cos((2*i+1)*math.pi/5)
        punkte.append((x2,y2))
    return(punkte)

width = 900
height = 600
pygame.init()
screen = pygame.display.set_mode((width,height),pygame.RESIZABLE)
pygame.display.set_caption("Flaggen")
clock = pygame.time.Clock()

P = pentagramm(3*height/10,3*height/10,height/3)
F = ['Japan','Tschechien','Deutschland','Togo','Argentina','Greece','Mazedonien','Great Britain']
flagge = 0

def draw_rectangle(x, y, width, height, color, rotation=0):
    points = []

    radius = math.sqrt((height / 2) ** 2 + (width / 2) ** 2)
    angle = math.atan2(height / 2, width / 2)
    angles = [angle, -angle + math.pi, angle + math.pi, -angle]
    rot_radians = (math.pi / 180) * rotation

    for angle in angles:
        y_offset = -1 * radius * math.sin(angle + rot_radians)
        x_offset = radius * math.cos(angle + rot_radians)
        points.append((x + x_offset, y + y_offset))

    pygame.draw.polygon(screen, color, points)

running = True
while running:
    for event in pygame.event.get():
        # Wurde das Fenster geschlossen?
        if event.type == pygame.QUIT:
            running = False
            break

        # Wurde das eine Pfeiltaste gedrückt?
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                flagge = (flagge+1)%len(F)
            if event.key == pygame.K_UP:
                flagge = (flagge+len(F)-1)%len(F)

        # Wurde die Fenstergröße verändert?                
        if event.type == pygame.VIDEORESIZE:
            (width,height) = screen.get_size()
            P = pentagramm(3*height/10,3*height/10,height/3)


    if F[flagge] == 'Japan':
        screen.fill(WEISS)
        pygame.draw.circle(screen,ROT,(width/2,height/2),width/5)

    if F[flagge] == 'Deutschland':
        R = pygame.Rect(0,0,width,height/3)
        pygame.draw.rect(screen,SCHWARZ,R)
        R = pygame.Rect(0,height/3,width,height/3)
        pygame.draw.rect(screen,ROT,R)
        R = pygame.Rect(0,2*height/3,width,height/3)
        pygame.draw.rect(screen,GOLD,R)

    if F[flagge] == 'Tschechien':
        pygame.draw.polygon(screen,BLAU,[(0,0),(width/2,height/2),(0,height)])
        pygame.draw.polygon(screen,WEISS,[(0,0),(width,0),(width,height/2),(width/2,height/2)])
        pygame.draw.polygon(screen,ROT2,[(width/2,height/2),(width,height/2),(width,height),(0,height)])

    if F[flagge] == 'Togo':
        for i in range(3):
            R = pygame.Rect(0,2*i*height/5,width,height/5)
            pygame.draw.rect(screen,GRUEN,R)
        for i in range(2):
            R = pygame.Rect(0,(2*i+1)*height/5,width,height/5)
            pygame.draw.rect(screen,GELB,R)

        R = pygame.Rect(0,0,3*height/5,3*height/5)
        pygame.draw.rect(screen,ROT3,R)

        pygame.draw.polygon(screen,WEISS,P)

    if F[flagge] == 'Argentina':
        screen.fill(SKY_BLUE)
        pygame.draw.rect(screen, WEISS, (0,height/3,width,height/3)) 
        star = pygame.image.load("Flaggen/_images/star_arg.png")
        star = pygame.transform.scale(star, (height/3, height/3))
        screen.blit(star, (width/2 - height/6, height/2 - height/6))
    
    if F[flagge] == 'Greece':
        screen.fill(GREECE_BLUE)
        for i in range (1, 9, 2):
            pygame.draw.rect(screen, WEISS, (0,i * (height/9),width,height/9))
        pygame.draw.rect(screen, GREECE_BLUE, (0,0,width * (10/27), height * (5/9)))
        pygame.draw.rect(screen, WEISS, ((4/27) * width, 0, width * (2/27), height * (5/9)))
        pygame.draw.rect(screen, WEISS, (0, (2/9) * height, width * (10/27), height * (1/9)))
    
    if F[flagge] == 'Great Britain':
        screen.fill(BLAU)
        
        # draw_rectangle((1/2) * width, (1/2) * height, (1/5) * height, math.sqrt(width ** 2 + height ** 2), WEISS, 59.04)
        # draw_rectangle((1/2) * width, (1/2) * height, (1/5) * height, math.sqrt(width ** 2 + height ** 2), WEISS, -59.04)
        
        # draw_rectangle((1/4) * width, (1/4) * height + (1/30) * width, (1/15) * height, height, ROT, 59.04)
        # draw_rectangle((3/4) * width, (1/4) * height, (1/15) * height, height, ROT, -59.04)
        # draw_rectangle((1/4) * width, (3/4) * height, (1/15) * height, height, ROT, -59.04)
        # draw_rectangle((3/4) * width, (3/4) * height, (1/15) * height, height, ROT, 59.04)
        
        pygame.draw.polygon(screen, WEISS, [(0, (3.393/30) * height), (0,0), ((1/10) * width, 0), (width, (5/6) * height), (width, height), ((5/6) * width, height)])
        pygame.draw.polygon(screen, WEISS, [((1 - 3.393/30) * width, 0), (width,0), (width, (1/6) * height), ((1/6) * width, height), (0, height), (0,(5/6) * height)])
    
        pygame.draw.polygon(screen, ROT, [(0, 0), ((1/2) * width, (1/2) * height), ((1/2 - 4/50) * width, (1/2) * height), (0, ((1.5/18.5)) * height)])
        pygame.draw.polygon(screen, ROT, [((1 - 4/45) * width, 0), (width, 0), ((1/2) * width, (1/2) * height), ((1/2 - 4/45) * width, (1/2) * height)])
        
        pygame.draw.polygon(screen, ROT, [(0, height), ((1/2) * width, (1/2) * height), ((1/2 - 4/50) * width, (1/2) * height), (0, height - ((1.5/18.5)) * height)])
        pygame.draw.polygon(screen, ROT, [((1 - 4/45) * width, height), (width, height), ((1/2) * width, (1/2) * height), ((1/2 - 4/45) * width, (1/2) * height)])
        
        pygame.draw.rect(screen, WEISS, (0,(1/3) * height, width, (1/3) * height))
        pygame.draw.rect(screen, WEISS, ((2/5) * width, 0, (1/5) * width, height))
        
        pygame.draw.rect(screen, ROT, (0, (12/30) * height, width, (1/5) * height))
        pygame.draw.rect(screen, ROT, ((11/25) * width, 0, (3/25) * width, height))
        
    
    if F[flagge]=='Mazedonien':
        screen.fill(ROT)
        diag=height*2/7
        radius=height/7
        diag2=diag-2*(diag/8)
        radius2=diag2/2
        halfheightsqaure=math.sqrt((height*6 /28)**2-(0.2*height)**2)

        pygame.draw.polygon(screen,GELB,(((width/2),(height*0.5-radius2)),((width*0.45),0),((width*0.55),0)))
        pygame.draw.polygon(screen,GELB,(((width/2),(height*0.5+radius2)),((width*0.45),height),((width*0.55),height)))

        pygame.draw.polygon(screen,GELB,(((0.45*width),(0.5*height+halfheightsqaure)),((width-0.3*height),0),(width,0)))
        pygame.draw.polygon(screen,GELB,(((0.55*width),(0.5*height+halfheightsqaure)),((height*0.3),0),(0,0)))

        pygame.draw.polygon(screen,GELB,(((0.45*width),(0.5*height-halfheightsqaure)),((width-0.3*height),height),(width,height)))
        pygame.draw.polygon(screen,GELB,(((0.55*width),(0.5*height-halfheightsqaure)),((height*0.3),height),(0,height)))


        pygame.draw.polygon(screen,GELB,(((width/2),(height/2)),(width,(height*0.4)),(width,(height*0.6))))
        pygame.draw.polygon(screen,GELB,(((width/2),(height/2)),(0,(height*0.4)),(0,(height*0.6))))

        pygame.draw.circle(screen,ROT,((width/2),(height/2)), ((radius)+(radius/8)))
        pygame.draw.circle(screen,GELB,((width/2),(height/2)), (radius))
        
    pygame.display.update()

    # Die Bildwiederholfrequenz wird auf 20 Bilder pro Sekunde gesetzt.
    clock.tick(20)

pygame.quit()