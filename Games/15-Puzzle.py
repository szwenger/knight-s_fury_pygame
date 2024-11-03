# Dieses Pygame-Programm demonstriert das Spiel mit einem 15-Puzzle, auch Schiebepuzzle genannt.
# Siehe https://de.wikipedia.org/wiki/15-Puzzle.


# Import der Random- und der Pygame-Bibliothek 
import random, pygame, sys

# Eine Hilfsfunktion zu Tausch von zwei Einträgen eines 2-dimensionalen Feldes
def swap(A,i1,j1,i2,j2):
    tmp = A[i1][j1]
    A[i1][j1] = A[i2][j2]
    A[i2][j2] = tmp

# Definition der beiden Farben schwarz und weiss im RGB-Modell
BLACK = (0,0,0)
WHITE = (255,255,255)

width = 640
height = 640
tileWidth =  min(width,height)//4
# Initialisierung der Pygame-Bibliothek
pygame.init()
# Erzeugen einer quadratischen Zeichenfläche mit 640 x 640 Pixeln
screen = pygame.display.set_mode((width,height),pygame.RESIZABLE)
# Erzeugen einer Uhr zur Steuerung der Framerate beim Bildaufbau.
clock = pygame.time.Clock()
# Überschrift des Zeichenfensters
pygame.display.set_caption("15-Puzzle")
# Auswahl eines Schriftsatzes 
fontname =  pygame.font.get_default_font()
# Die Buchstabengröße des Schriftsatzes wird auf 50 Pixel gesetzt.
font = pygame.font.Font(fontname,tileWidth//4)

# Wir laden eine Bilddatei 
# org = pygame.image.load('Pygame-Demos/Blumen.jpg')
org = pygame.image.load('Games/_images/Blumen.jpg')
# und skalieren das Bild auf die Größe unseres Zeichenfeldes.
image = pygame.transform.scale(org,(width,height))

# Wir stellen uns vor, dass wir das Bild in 4 x 4 Kacheln zerschneiden,
# diese in eine zufällige Reihenfolge bringen, eine Kachel entfernen
# und die frei gewordene Kachel zum Verschieben der übrigen Kacheln
# nutzen, um die korrekte Kachelreihenfolge wiederherzustellen.  

# Das Kachelfeld soll die 4 x 4 Teilbilder des Originalbildes enthalten.
kachel = []

# Wir erzeugen die 16 Teilbilder als quadratische Ausschnitte des Originalbildes.
def createTiles():
    font = pygame.font.Font(fontname,tileWidth//4)
    kachel.clear()
    for i in range(16):
        # Als Hilfe für den Spieler malen wir die Kachelnummer in die linke obere Ecke
        # der Kachel.
        ziffer = font.render(str(i), True, BLACK)
        image.blit(ziffer,(tileWidth*(i%4),tileWidth*(i//4)))
        # Wir extrahieren die Teilbilder von der linken oberen Ecke beginnend von links
        # nach rechts laufend und zeilenweise von oben nach unten. Für die Kachel mit der
        # Nummer i ergibt sich als Spaltenindex (i%4) und als Zeilenindex (i//4).
        R = pygame.Rect(tileWidth*(i%4),tileWidth*(i//4),tileWidth,tileWidth)
        kachel.append(image.subsurface(R))

# Wir permutieren die Kachelnummern zufällig - ohne Rücksicht auf die Lösbarkeit des
# 15-Puzzles zu nehmen.
permutation = [i for i in range(16)]
random.shuffle(permutation)

# Wir nutzen ein 2-dimensionales Feld der Dimension 4 x 4 für die Kachelnummern, um
# die Spielkonfiguration zu speichern.
feld = [[-1 for j in range(4)] for i in range(4)]
k = 0
for i in range(4):
    for j in range(4):
        feld[i][j] = permutation[k]
        k += 1

createTiles()

# Wir betreten die Ereignisschleife.
while True:
    # Die Bildwiederholfrequenz wird auf 30 Bilder pro Sekunde gesetzt.
    clock.tick(30)

    # Die per Maus selektiere Kachel besitzt den Zeilenindex pi und den Spaltenindex pj.
    pi = pj = -1
    # Abarbeitung aller Ereignisse seit dem letzten Durchlauf der Ereignisschleife.
    for event in pygame.event.get():
        # Wurde eine Maustaste gedrückt?
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Ermittele die Position des Mauszeigers.
            (mx,my) = pygame.mouse.get_pos()
            # Berechne Zeilen- und Spaltenindex der selektierten Kachel.
            pi = my // tileWidth
            pj = mx // tileWidth
        # Wurde das Fenster geschlossen?
        elif event.type == pygame.QUIT:
            # Verlasse die Ereignisschleife und das Programm.
            pygame.quit()
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            (width,height) = screen.get_size()
            image = pygame.transform.scale(org,(width,height))
            tileWidth =  min(width,height)//4
            createTiles()

    # Wurde eine Kachel mit der Maus ausgewählt?
    if pi >= 0:
        # Wurde das freie Kachelfeld mit der Nummer 15 angeklickt?
        if feld[pi][pj] == 15: continue
        # Wir tauschen die angeklickte Kachel mit der freien Kachel nur dann, 
        # wenn diese direkt benachbart sind. Wir müssen darauf achten, dass 
        # nicht immer alle 4 Nachbarfelder existieren.
        if pi > 0 and feld[pi-1][pj] == 15:
            swap(feld,pi,pj,pi-1,pj)
        elif pi < 3 and feld[pi+1][pj] == 15:
            swap(feld,pi,pj,pi+1,pj)
        elif pj > 0 and feld[pi][pj-1] == 15:
            swap(feld,pi,pj,pi,pj-1)
        elif pj < 3 and feld[pi][pj+1] == 15:
            swap(feld,pi,pj,pi,pj+1)

    # Wir löschen die Zeichenfläche, indem wir sie mit der Farbe weiss füllen.
    screen.fill(WHITE)
    # Wir zeichnen alle 4 x 4 Kacheln mit Ausnahme der freien Kachel mit der Nummer 15.
    for i in range(4):
        for j in range(4):
            # Wir bestimmen die Kachelnummer k in der i-ten Zeile und der j-ten Spalte.
            k = feld[i][j]
            # Wir überspringen die freie Kachel.
            if k == 15: continue
            # Wir kopieren das Teilbild der Kachel mit der Nummer k an die richtige
            # (x,y)-Position im Zeichenfenster. Die x-Koordinate ergibt sich aus dem
            # Spaltenindex j und die y-Koordinate aus dem Zeilenindex i.
            screen.blit(kachel[k],(tileWidth*j,tileWidth*i))

    # Wir aktualisieren die Zeichenfläche und durchlaufen die Ereignisschleife erneut.
    pygame.display.update()

