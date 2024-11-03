# Dieses Pygame-Programm stellt eine grafische Visualisierung für das
# Spiel "Vier Gewinnt" dar. Siehe https://de.wikipedia.org/wiki/Vier_gewinnt.
# Die Spiellogik wurde noch nicht implementiert.

# Import der Pygame-Bibliothek
import pygame, sys

# Definition der verwendeten Farben als 3-Tupel von (rot,grün,blau) in [0,255]^3
ROT   = (255,0,0)
WEISS = (255,255,255)
GELB  = (255,255,0)
BLAU  = (0,80,200)

# Initialisierung der Pygame-Bibliothek
pygame.init()
# Erzeuge eine Zeichenfläche der festen Größe von 700 x 600 Pixel.
screen = pygame.display.set_mode((700,600))
# Erzeuge eine Uhr, mit der die Geschwindigkeit des sich wiederholenden Bildaufbaus 
# gesteuert werden kann.
clock = pygame.time.Clock()
# Setze die Überschrift des Zeichenfensters.
pygame.display.set_caption("Vier gewinnt")

# Erzeuge ein 2-dimensionales Spielfeld mit 6 Zeilen und 7 Spalten. Als Feldeinträge
# werden die Werte 0,1,2 verwendet. 0 steht für ein unbelegtes Feld, 1 für einen 
# Spielstein von Spieler 1 und 2 entsprechend für Spieler 2.
feld = [ [ 0 for j in range(7) ] for i in range(6) ]
# Spieler 1 ist am Zug.
spieler = 1

# In der Ereignisschleife werden alle Interaktionen mit den Spielern verarbeitet.
while True:
    # Der Bildaufbau erfolgt 30 mal pro Sekunde.
    clock.tick(30)

    # Die Zeile pi und die Spalte pj des Spielfeldes, das vom Spieler mit der Maus
    # zum Setzen des nächsten Spielsteines ausgewählt wird. 
    pi = pj = -1
    # Wir arbeiten alle Ereignisse des Benutzers seit dem letzten Durchlauf der
    # Ereignisschleife ab.
    for event in pygame.event.get():
        # Wurde eine Maustaste gedrückt?
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Ermittele die Pixelposition (mx,my) des Mauszeigers beim Tastendruck.
            # Der Ursprung des Koordinatensystems ist die linke obere Ecke des Fensters.
            # Die x-Achse zeigt nach rechts, die y-Achse nach unten.
            (mx,my) = pygame.mouse.get_pos()
            # Durch ganzzahlige Division durch die Gitterlänge 100 erhalten wir die
            # Zeile pi und die Spalte pj der selektierten Spielfeldposition.
            pi = my // 100
            pj = mx // 100
        # Wurde das Fenster geschlossen?
        elif event.type == pygame.QUIT:
            # Wir verlassen die Ereignisschleife und beenden somit das Programm.
            pygame.quit()
            sys.exit()

    # Hat ein Spieler eine Spielfeld zum Setzen eines Spielsteines ausgewählt?
    if pi >= 0:
        # Wir besetzen das selektierte Spielfeld (pi,pj) mit der Nummer des Spielers
        feld[pi][pj] = spieler
        # und wechseln den Spieler.
        if spieler == 1: 
            spieler = 2
        else: 
            spieler = 1

    # Das Zeichenfeld wird mit der Farbe blau gefüllt.
    screen.fill(BLAU)
    # Wir durchlaufen das Spielfeld zeilenweise, d.h. grafisch gesehen von oben nach unten.
    for i in range(6):
        # Wir durchlaufen die i-te Zeile spaltenweise, d.h. grafisch gesehen von links nach rechts.
        for j in range(7):
            # Wir schauen uns den Feldeintrag der i-ten Zeile und j-ten Spalte an.
            if feld[i][j] == 0:
                farbe = WEISS
            elif feld[i][j] == 1:
                farbe = ROT
            elif feld[i][j] == 2:
                farbe = GELB
            # Wir zeichnen einen Kreis auf das Zeichenfeld in der entsprechenden Farbe.
            # Die Koordinaten des Kreismittelpunktes (x,y) berechnen sich aus dem 
            # Spaltenindex für die x-Koordinate und dem Zeilenindex für die y-Koordinate.
            pygame.draw.circle(screen,farbe,(100*j+50,100*i+50),40)

    # Zum Abschluss der Ereignisschleife sorgen wird dafür, dass die Grafik im Zeichenfenster
    # neu aufgebaut wird.
    pygame.display.update()

