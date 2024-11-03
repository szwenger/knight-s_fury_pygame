# Dieses Programm demonstriert, wie man das Arcade-Spiel Pong
# mit Hilfe von Pygame umsetzen könnte.
# Siehe https://de.wikipedia.org/wiki/Pong.

# Import der der Mathe-, Random-, und Pygame-Bibliothek
import math, random, pygame, sys

# Initialisierung der Pygame-Bibliothek
pygame.init()
# Erzeugen der Zeichenfläche aus 640 x 480 Pixeln.
screen = pygame.display.set_mode((640, 480))
# Erzeugen einer Uhr zur Kontrolle der Bildwiederholfrequenz
clock = pygame.time.Clock()
# Überschrift des Fensters
pygame.display.set_caption("Pong")

# RGB-Farben
BLACK = (0,0,0)
WHITE = (255,255,255)

# Der Betrag der Ballgeschwindigkeit
speed = 10
# Ein zufälliger Startwinkel für den Ball
winkel = random.randint(-45,45)
# (vx,vy) = Geschwindigkeitsvektor des Balles
vx = speed*math.cos(winkel/180*math.pi)
vy = speed*math.sin(winkel/180*math.pi)
# Der Ball startet in der Fenstermitte.
bx = 320
by = 240
# Der Ballradius
br = 10
# Die y-Position der oberen Rechteckkante der beiden Schläger der
# Spieler, die sich nur in vertikaler Richtung bewegen können.
y1 = y2 = 190

# Damit in der Ereignisschleife möglichst schnell auf das Drücken einer
# Taste reagiert wird, legen wir fest, dass eine dauerhaft gedrückte Taste
# alle 10 Millisekunden das Ereignis eines Tastendrucks generiert.
pygame.key.set_repeat(10)

# Die Ereignisschleife
while True:
    # Bildwiederholfrequenz = 30 Bilder pro Sekunde
    clock.tick(30)
    # Verarbeite alle Ereignisse.
    for event in pygame.event.get():
        # Welche Tasten wurden gedrückt?
        if event.type == pygame.KEYDOWN:
            # Spieler 1 bewegt seinen Schläger mit den Tasten 
            # 'w' und 's' auf und ab.
            if event.key == pygame.K_s:
                y1 += 1
            if event.key == pygame.K_w:
                y1 -= 1
            # Der Schläger darf sich nicht aus dem erlaubten Bereich bewegen.
            if y1 < 0: y1 = 0
            if y1 > 380: y1 = 380
            # Spieler 2 bewegt seinen Schläger mit den Tasten 
            # Pfeiltasten auf und ab.
            if event.key == pygame.K_DOWN:
                y2 += 1
            if event.key == pygame.K_UP:
                y2 -= 1
            # Der Schläger darf sich nicht aus dem erlaubten Bereich bewegen.
            if y2 < 0: y2 = 0
            if y2 > 380: y2 = 380
        # Wurde das Fenster geschlossen?
        elif event.type == pygame.QUIT:
            # Ende der Ereignisschleife und Ende des Programms
            pygame.quit()
            sys.exit()

    # Berechne neue Ballposition anhand der Ballgeschwindigkeit.
    bx += vx
    by += vy

    # Falls der Ball links bzw. rechts das Spielfeld verlässt, wird
    # der Einfachheit halber ein neuer Ball in der Fenstermitte mit
    # zufälligem Startwinkel erzeugt.
    if bx < 0 or bx > 640:
        winkel = random.randint(-45,45)
        vx = speed*math.cos(winkel/180*math.pi)
        vy = speed*math.sin(winkel/180*math.pi)
        bx = 320
        by = 240

    # Kommt der Ball in den Bereich des Schläger 1?
    if bx < 3*br:
        # Trifft der Ball den Schläger 1?
        if by > y1-br and by < y1+100+br:
            # Umkehr der x-Komponente der Ballgeschwindigkeit
            # entspricht einer Reflektion am Schläger.
            vx = -vx

    # Analog für Schläger 2.
    if bx > 640-3*br:
        if by > y2-br and by < y2+100+br:
            vx = -vx

    # Stößt der Ball an die obere bzw. untere Begrenzung des Spielfeldes?
    if by < br or by > 480-br: 
        # Umkehr der y-Komponente der Ballgeschwindigkeit
        # entspricht einer Reflektion an der Bande.
        vy = -vy

    # Löschen der Zeichenfläche in der Farbe schwarz.
    screen.fill(BLACK)
    # Zeichen der beiden Schläger als weiße Rechtecke.
    Player1 = pygame.Rect(0,y1,2*br,100)
    Player2 = pygame.Rect(620,y2,2*br,100)
    pygame.draw.rect(screen,WHITE,Player1)
    pygame.draw.rect(screen,WHITE,Player2)
    # Zeichnen des Balles als weißer Kreis
    pygame.draw.circle(screen,WHITE,(bx,by),br)

    # Aktualisierung der Grafik auf der Zeichenfläche.
    pygame.display.update()

