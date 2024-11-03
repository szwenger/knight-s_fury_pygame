# Import der Pygame-Bibliothek 
import pygame, math

# Definition der beiden Farben schwarz und weiss im RGB-Modell
SCHWARZ = (0,0,0)
WEISS = (255,255,255)

width = 900
height = 900
# Initialisierung der Pygame-Bibliothek
pygame.init()
# Erzeugen einer rechteckigen Zeichenfläche mit width x height Pixeln
screen = pygame.display.set_mode((width,height),pygame.RESIZABLE)
# Erzeugen einer Uhr zur Steuerung der Framerate beim Bildaufbau.
clock = pygame.time.Clock()

# Wir laden eine Bilddatei 
org = pygame.image.load('Games/_images/Muehle.png')
# und skalieren das Bild auf die Größe unseres Zeichenfeldes.
minWH = min(width,height)
image = pygame.transform.scale(org,(minWH,minWH))
BMorg = pygame.image.load('Games/_images/BlackMan.png')
WMorg = pygame.image.load('Games/_images/WhiteMan.png')
radMan = minWH/10
BMimg = pygame.transform.scale(BMorg,(radMan,radMan))
WMimg = pygame.transform.scale(WMorg,(radMan,radMan))
zoom = minWH*0.125
rad = zoom/5

def dist(a,b):
    return(math.sqrt((a[0]-b[0])*(a[0]-b[0])+(a[1]-b[1])*(a[1]-b[1])))

def transformToWorld(p):
    wx = (p[0]-width/2)/zoom
    wy = (height/2-p[1])/zoom
    return((wx,wy))

def transformToScreen(p):
    sx = width/2+p[0]*zoom
    sy = height/2-p[1]*zoom
    return((sx,sy))

def drawShortenedSegment(a,b):
    l = math.sqrt((b[0]-a[0])*(b[0]-a[0])+(b[1]-a[1])*(b[1]-a[1]))
    aa = (a[0]+rad*(b[0]-a[0])/l,a[1]+rad*(b[1]-a[1])/l)
    bb = (b[0]+rad*(a[0]-b[0])/l,b[1]+rad*(a[1]-b[1])/l)
    pygame.draw.line(screen,SCHWARZ,aa,bb,int(zoom/10))

def initMills():
    for r in range(1,4):
        mills.append(((r,0),(r,-r),(r,r)))
        mills.append(((0,r),(r,r),(-r,r)))
        mills.append(((-r,0),(-r,-r),(-r,r)))
        mills.append(((0,-r),(-r,-r),(r,-r)))
    mills.append(((1,0),(2,0),(3,0)))
    mills.append(((-1,0),(-2,0),(-3,0)))
    mills.append(((0,1),(0,2),(0,3)))
    mills.append(((0,-1),(0,-2),(0,-3)))

def hasMill(p):
    col = 0 if p in men[0] else 1
    for m in mills:
        if p in m:
            for q in m:
                if q not in men[col]:
                    break
            else:
                return(True)
    return(False)

def legalMove(p,q):
    if p[0] == q[0]:
        if p[0] == 0:
            return(abs(p[1]-q[1]) == 1)
        else:
            return(abs(p[1]-q[1]) == abs(p[0]))
    if p[1] == q[1]:
        if p[1] == 0:
            return(abs(p[0]-q[0]) == 1)
        else:
            return(abs(p[0]-q[0]) == abs(p[1]))
    return(False)

def drawBoard():
    # Wir löschen die Zeichenfläche, indem wir sie mit der Farbe weiss füllen.
    screen.fill(WEISS)
    screen.blit(image,((width-minWH)/2,(height-minWH)/2))

    P = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
    n = len(P)
    for r in range(1,4):
        for i in range(n):
            a = transformToScreen((r*P[i][0],r*P[i][1]))
            pygame.draw.circle(screen,SCHWARZ,a,math.ceil(rad),int(zoom/20))

            b = transformToScreen((r*P[(i+1)%n][0],r*P[(i+1)%n][1]))
            drawShortenedSegment(a,b)
 
    P = [(1,0),(0,1),(-1,0),(0,-1)]
    for i in range(len(P)):
        for r in range(1,3):
            a = transformToScreen((r*P[i][0],r*P[i][1]))
            b = transformToScreen(((r+1)*P[i][0],(r+1)*P[i][1]))
            drawShortenedSegment(a,b)

men = [[],[]]
count = [0,0]
turn = 0
mills = []
initMills()
removeMan = False
placingPhase = True
movingPhase = False
pickMan = None

# Überschrift des Zeichenfensters
pygame.display.set_caption('Mühle')

# Wir betreten die Ereignisschleife.
running = True
while running:
    # Die Bildwiederholfrequenz wird auf 30 Bilder pro Sekunde gesetzt.
    clock.tick(20)

    # Abarbeitung aller Ereignisse seit dem letzten Durchlauf der Ereignisschleife.
    for event in pygame.event.get():
        # Wurde eine Maustaste gedrückt?
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Ermittele die Position des Mauszeigers.
            mouse = pygame.mouse.get_pos()
            a = transformToWorld(mouse)
            b = (math.floor(a[0]+0.5),math.floor(a[1]+0.5))
            if b[0] == 0 and b[1] == 0:
                continue
            if abs(b[0]) != abs(b[1]) and b[0] != 0 and b[1] != 0: 
                continue
            if dist(a,b) > 2/5:
                continue
            if removeMan:
                if b not in men[(turn+1)%2]:
                    continue
                turn = (turn+1)%2
                men[turn].remove(b)  
                removeMan = False
                pickMan = None
                continue
            if movingPhase:
                if b in men[turn]:
                    pickMan = b
                    pickPos = a
                    print('pickMan = ',pickMan)
            elif placingPhase:
                if b in men[0] or b in men[1]:
                    continue
                if count[turn] < 9:
                    count[turn] += 1
                men[turn].append(b)
                if hasMill(b):
                    print('mill',turn)
                    removeMan = True
                    continue
                turn = (turn+1)%2
                if count[0] == 9 and count[1] == 9:
                    placingPhase = False
                    movingPhase = True
        elif event.type == pygame.MOUSEMOTION:
            mouseNew = pygame.mouse.get_pos()
            if pickMan != None:
                pickPos = transformToWorld(mouseNew)
            mouse = mouseNew
        elif event.type == pygame.MOUSEBUTTONUP:
            if placingPhase or pickMan == None:
                continue
            mouseNew = pygame.mouse.get_pos()
            a = transformToWorld(mouse)
            b = (math.floor(a[0]+0.5),math.floor(a[1]+0.5))
            if b[0] == 0 and b[1] == 0:
                pickMan = None
                continue
            if abs(b[0]) != abs(b[1]) and b[0] != 0 and b[1] != 0:
                pickMan = None
                continue
            if b in men[0] or b in men[1]:
                pickMan = None
                continue
            if len(men[turn]) > 3:
                if not legalMove(pickMan,b):
                    pickMan = None
                    continue
            men[turn].remove(pickMan)
            men[turn].append(b)
            if hasMill(b):
                removeMan = True
            else:
                pickMan = None
                turn = (turn+1)%2
        # Wurde das Fenster geschlossen?
        elif event.type == pygame.QUIT:
            running = False
            break
        # Wurde die Fenstergröße verändert?
        elif event.type == pygame.VIDEORESIZE:
            (width,height) = screen.get_size()
            minWH = min(width,height)
            image = pygame.transform.scale(org,(minWH,minWH))
            radMan = minWH/10
            BMimg = pygame.transform.scale(BMorg,(radMan,radMan))
            WMimg = pygame.transform.scale(WMorg,(radMan,radMan))
            zoom = minWH*0.125
            rad = zoom/5
    
    drawBoard()

    for i in range(2):
        for p in men[i]:
            if p == pickMan:
                a = transformToScreen(pickPos)
            else:
                a = transformToScreen(p)
            aa = (a[0]-radMan/2,a[1]-radMan/2)
            if i == 0:
                screen.blit(WMimg,aa)
            else:
                screen.blit(BMimg,aa)

    # Wir aktualisieren die Zeichenfläche und durchlaufen die Ereignisschleife erneut.
    pygame.display.update()

# Verlasse die Ereignisschleife und das Programm.
pygame.quit()
