# Dieses Pygame-Programm demonstriert, wie man das Pacman-Spiel
# grafisch visualisieren kann und wie man die Steuerung des
# Pacman durch die Tasten "wasd" realisieren kann.
# Siehe https://de.wikipedia.org/wiki/Pac-Man.

# Import der Random- und Pygame-Bibliothek
import random, pygame, sys

# Definition von Farben im RGB-Farbraum.
BLACK = (0,0,0)
WHITE = (255,255,255)
YELLOW = (255,255,0)

# Initialisierung der Pygame-Bibliothek
pygame.init()
# Erzeugung einer Zeichenfläche mit 800 x 800 Pixeln.
screen = pygame.display.set_mode((800,800))
# Erzeugung einer Uhr zur Steuerung der Bildwiederholfrequenz in der Ereignisschleife.
clock = pygame.time.Clock()
# Setzen der Fensterüberschrift.
pygame.display.set_caption('Pacman')

# Lade die Bilder für die Pacman-Figuren.
org = pygame.image.load('Games/_images/Pacman.png')
pacman = pygame.transform.scale(org,(40,40))
org = pygame.image.load('Games/_images/Inky.png')
inky = pygame.transform.scale(org,(40,40))
org = pygame.image.load('Games/_images/Blinky.png')
blinky = pygame.transform.scale(org,(40,40))
org = pygame.image.load('Games/_images/Clyde.png')
clyde = pygame.transform.scale(org,(40,40))
org = pygame.image.load('Games/_images/Pinky.png')
pinky = pygame.transform.scale(org,(40,40))

# Das Feld ghost beinhaltet die Bildinformation für die Geister.
ghost = [inky,blinky,clyde,pinky]

# Das folgende Feld aus Zeichenketten dient der einfachen Festlegung
# des Labyrinths. 'x' = Mauer, '.' = Pille, 'P' = Pacman, '0', '1',
# '2' und '3' für die Geister.
org  = ['xxxxxxxxxxxxxxxxxxxx',
        'x....0..xxxx...x...x',
        'x.xx.xx.xxxx.x.x.x.x',
        'x.xx.xx....x.x.x.x.x',
        'x.xx.xx.xx.x.x...x.x',
        'x.......xx...x.x.x.x',
        'xxxx.xxxxxxxxx.x.x.x',
        'x.....P...xxxx.x.x.x',
        'x.xxx.xxx.xxxx.x.x.x',
        'x.xxx.xxx....1.x...x',
        'x.xxx.xxx.xxxx.xx..x',
        'x......xx.xxxx..x.xx',
        'x...xx.xx.xx.......x',
        'x...x..xx....xxxxx.x',
        'x.xxx.xxx.x..2...x.x',
        'x.xxx.xx....xxxx.x.x',
        'x........x..x......x',
        'x.xxx..x.x.xx.xxx..x',
        'x..3..xx...xx.....xx',
        'xxxxxxxxxxxxxxxxxxxx']

# Das Labyrinth besitzt die Dimension n x n. 
n = len(org)

# Um die Belegung der Zellen des Labyrinths einfacher verändern zu können,
# verwenden wir ein 2-dimensionales Feld aus einzelnen Zeichen.
feld = [ [ ' ' for j in range(n)] for i in range(n) ]

for i in range(n):
    for j in range(n):
        feld[i][j] = org[i][j]

# Variablen zur Speicherung der Geister-Positionen
gi = [ -1,-1,-1,-1 ]
gj = [ -1,-1,-1,-1 ]
# und der Pacman-Position.
pi = pj = -1

# Wir schauen im Spielfeld nach, in welcher Zeile und Spalte sich
# die Geister und der Pacman befinden.
for i in range(n):
    for j in range(n):
        if feld[i][j] == 'P':
            pi = i
            pj = j
        elif feld[i][j] == '0':
            gi[0] = i
            gj[0] = j
        elif feld[i][j] == '1':
            gi[1] = i
            gj[1] = j
        elif feld[i][j] == '2':
            gi[2] = i
            gj[2] = j
        elif feld[i][j] == '3':
            gi[3] = i
            gj[3] = j

# Damit in der Ereignisschleife möglichst schnell auf das Drücken einer
# Taste reagiert wird, legen wir fest, dass eine dauerhaft gedrückte Taste
# alle 100 Millisekunden das Ereignis eines Tastendrucks generiert.
pygame.key.set_repeat(100)

# Die Ereignisschleife
while True:
    # Bildwiederholfrequenz = 10 Frames pro Sekunde
    clock.tick(10)

    # Abarbeitung alle aufgetretenen Ereignisse
    for event in pygame.event.get():
        # Wurde eine Taste gedrückt?
        if event.type == pygame.KEYDOWN:
            # Wir benutzen die Pfeiltasten zur Steuerung des Pacman.
            # Wir führen Buch über die Pacman-Position (pi,pj) und
            # sorgen für den entsprechenden 'P'-Eintrag im Spielfeld.
            # Wir achten darauf, dass keine Bewegung durch Mauern 'x'
            # geschieht. Wir fressen Pillen '.', indem wir das betretende
            # Feld durch ' ' ersetzen. Er Einfachheit halber ignorieren wir 
            # jedoch die Geister.
            if event.key == pygame.K_DOWN:
                if pi < n-1 and feld[pi+1][pj] != 'x':
                    feld[pi][pj] = ' '
                    pi += 1
                    feld[pi][pj] = 'P'
            if event.key == pygame.K_UP:
                if pi > 0 and feld[pi-1][pj] != 'x':
                    feld[pi][pj] = ' '
                    pi -= 1
                    feld[pi][pj] = 'P'
            if event.key == pygame.K_RIGHT:
                if pj < n-1 and feld[pi][pj+1] != 'x':
                    feld[pi][pj] = ' '
                    pj += 1
                    feld[pi][pj] = 'P'
            if event.key == pygame.K_LEFT:
                if pj > 0 and feld[pi][pj-1] != 'x':
                    feld[pi][pj] = ' '
                    pj -= 1
                    feld[pi][pj] = 'P'
        # Wurde das Fenster geschlossen?
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Dies ist ein kläglicher Versuch, eine zufällige Geisterbewegung
    # zu realisieren.
    for k in range(4):
        # Zeilenindex i des Geistes mit Nummer k
        i = gi[k]
        # Spaltenindex j des Geistes mit Nummer k
        j = gj[k]

        # Der Geist mit der Nummer k bewegt sich zu einem zufällig
        # ausgewählten Nachbarfeld, das betretbar ist.
        while True:
            si = random.randint(-1,1)
            sj = random.randint(-1,1)
            if abs(si)+abs(sj) != 1:
                continue

            if feld[i+si][j+sj] != 'x':
                feld[i][j] = ' '
                gi[k] = i+si
                gj[k] = j+sj
                feld[i+si][j+sj] = str(k)
                break         

    # Löschen des Zeichenfeldes mit der Farbe schwarz.
    screen.fill(BLACK)
    # Alle Zellen des Spielfeldes der Dimension n x n werden einzeln visualisiert.
    for i in range(n):
        for j in range(n):
            # Mauer?
            if feld[i][j] == 'x':
                # Zeichne ein ausgefülltes weißes Rechteck.
                R = pygame.Rect(40*j,40*i,40,40)
                pygame.draw.rect(screen,WHITE,R)
            # Pille?
            if feld[i][j] == '.':
                # Zeichne einen kleinen gelben Kreis in die Mitte der Zelle.
                pygame.draw.circle(screen,YELLOW,(40*j+20,40*i+20),4)
            # Packman?
            if feld[i][j] == 'P':
                # Zeichne das Bild des Pacman.
                screen.blit(pacman,(40*j,40*i))
            # Ein Geist?
            for k in range(4):
                if feld[i][j] == str(k):
                    # Zeichne das Bild des k-ten Geistes.
                    screen.blit(ghost[k],(40*j,40*i))

    # Aktualisiere die Grafik des Zeichenfeldes.
    pygame.display.update()

