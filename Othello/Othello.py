# Dieses Pygame-Programm stellt eine grafische Visualisierung für das
# Spiel "Vier Gewinnt" dar. Siehe https://de.wikipedia.org/wiki/Vier_gewinnt.
# Die Spiellogik wurde noch nicht implementiert.

# Import der Pygame-Bibliothek
import pygame, sys, math

# Definition der verwendeten Farben als 3-Tupel von (rot,grün,blau) in [0,255]^3
SCHWARZ = (0,0,0)
ROT   = (255,0,0)
WEISS = (255,255,255)
GELB  = (255,255,0)
BLAU  = (0,80,200)
GRUEN   = (46,139,87)

height = 800
width = 800

# Initialisierung der Pygame-Bibliothek
pygame.init()
# Erzeuge eine Zeichenfläche der festen Größe von 800 x 800 Pixel.
screen = pygame.display.set_mode((height,width),pygame.RESIZABLE)


# Erzeuge eine Uhr, mit der die Geschwindigkeit des sich wiederholenden Bildaufbaus 
# gesteuert werden kann.
clock = pygame.time.Clock()
# Setze die Überschrift des Zeichenfensters.
pygame.display.set_caption("Othello")

# Erzeuge ein 2-dimensionales Spielfeld mit 6 Zeilen und 7 Spalten. Als Feldeinträge
# werden die Werte 0,1,2 verwendet. 0 steht für ein unbelegtes Feld, 1 für einen 
# Spielstein von Spieler 1 und 2 entsprechend für Spieler 2.
feld = [ [ 0 for j in range(8) ] for i in range(8) ]

# Die Startpositionen der Spielsteine.
feld[3][3] = feld[4][4] = 1
feld[3][4] = feld[4][3] = 2

# Spieler 1 beginnt.
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
            
            # -=-=-=- OldVersion  -=-=-=-
            # Durch ganzzahlige Division durch die Gitterlänge 100 erhalten wir die
            # Zeile pi und die Spalte pj der selektierten Spielfeldposition.
            # pi = my // 100
            # pj = mx // 100
            # -=-=-=-   -=-=-=-   -=-=-=-
        
            # Get the current window size
            window_width, window_height = pygame.display.get_surface().get_size()
            
            # Scale the mouse coordinates
            pi = (my * 8) // window_height
            pj = (mx * 8) // window_width
            
            # Check if the indices are within the valid range and the selected tile is empty
            # if 0 <= pi < 8 and 0 <= pj < 8 and feld[pi][pj] == 0:
        
        # Wurde das Fenster geschlossen?
        elif event.type == pygame.QUIT:
            # Wir verlassen die Ereignisschleife und beenden somit das Programm.
            pygame.quit()
            sys.exit()
        
        # Wurde die Fenstergröße verändert?                
        if event.type == pygame.VIDEORESIZE:
            (width,height) = screen.get_size()

    def check_direction(pi, pj, di, dj, player, opponent):
        temp = []
        i = 1
        while 0 <= pi + i*di < len(feld) and 0 <= pj + i*dj < len(feld[0]):
            if feld[pi+i*di][pj+i*dj] == opponent:
                temp.append((pi+i*di, pj+i*dj))
            elif feld[pi+i*di][pj+i*dj] == player:
                return temp
            else:
                return []
            i += 1
        return []

    def valide(pi,pj):
        G = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        if spieler == 1:
            for di, dj in directions:
                G.extend(check_direction(pi, pj, di, dj, 1, 2))
        elif spieler == 2:
            for di, dj in directions:
                G.extend(check_direction(pi, pj, di, dj, 2, 1))
        return G
    '''
    def valide(pi,pj):
        
        G = []
        
        if spieler == 1:
            temp = []
            i = 0
            while i < (len(feld) - pi):
                if feld[pi+i][pj] == 2:
                    temp.append(feld[pi+i][pj])
                elif feld[pi+i][pj] == 0:
                    if feld[pi+i-1][pj] == 1:
                        for i in range(len(temp)):
                            G.append(temp[i])
                        temp = []
                        continue
                    else:
                        G = []
                        continue
                i += 1
            
            i = 0
            while i < (len(feld) - pi):
                if feld[pi-i][pj] == 2:
                    temp.append(feld[pi-i][pj])
                elif feld[pi-i][pj] == 0:
                    if feld[pi-i+1][pj] == 1:
                        for i in range(len(temp)):
                            G.append(temp[i])
                        temp = []
                        continue
                    else:
                        G = []
                        continue
                i += 1
                
            i = 0
            while i < (len(feld[0]) - pj):
                if feld[pi][pj+i] == 2:
                    temp.append(feld[pi][pj+i])
                elif feld[pi][pj+i] == 0:
                    if feld[pi][pj+i-1] == 1:
                        for i in range(len(temp)):
                            G.append(temp[i])
                        temp = []
                        continue
                    else:
                        G = []
                        continue
                i += 1
                
            i = 0
            while i < (len(feld[0]) - pj):
                if feld[pi][pj-i] == 2:
                    temp.append(feld[pi][pj-i])
                elif feld[pi][pj-i] == 0:
                    if feld[pi][pj-i+1] == 1:
                        for i in range(len(temp)):
                            G.append(temp[i])
                        temp = []
                        continue
                    else:
                        G = []
                        continue
                i += 1
                
            i = 0
            while i < (len(feld) - pi) and i < (len(feld[0]) - pj):
                if feld[pi+i][pj+i] == 2:
                    temp.append(feld[pi+i][pj+i])
                elif feld[pi+i][pj+i] == 0:
                    if feld[pi+i-1][pj+i-1] == 1:
                        for i in range(len(temp)):
                            G.append(temp[i])
                        temp = []
                        continue
                    else:
                        G = []
                        continue
                i += 1
            
            i = 0
            while i < (len(feld) - pi) and i < (len(feld[0]) - pj):
                if feld[pi-i][pj-i] == 2:
                    temp.append(feld[pi-i][pj-i])
                elif feld[pi-i][pj-i] == 0:
                    if feld[pi-i+1][pj-i+1] == 1:
                        for i in range(len(temp)):
                            G.append(temp[i])
                        temp = []
                        continue
                    else:
                        G = []
                        continue
                i += 1
            
            i = 0
            while i < (len(feld) - pi) and i < (len(feld[0]) - pj):
                if feld[pi+i][pj-i] == 2:
                    temp.append(feld[pi+i][pj-i])
                elif feld[pi+i][pj-i] == 0:
                    if feld[pi+i-1][pj-i+1] == 1:
                        for i in range(len(temp)):
                            G.append(temp[i])
                        temp = []
                        continue
                    else:
                        G = []
                        continue
                i += 1
            
            i = 0
            while i < (len(feld) - pi) and i < (len(feld[0]) - pj):
                if feld[pi-i][pj+i] == 2:
                    temp.append(feld[pi-i][pj+i])
                elif feld[pi-i][pj+i] == 0:
                    if feld[pi-i+1][pj+i-1] == 1:
                        for i in range(len(temp)):
                            G.append(temp[i])
                        temp = []
                        continue
                    else:
                        G = []
                        continue
                i += 1
            
        if spieler == 2:
            temp = []
            i = 0
            while i < (len(feld) - pi):
                if feld[pi+i][pj] == 1:
                    temp.append(feld[pi+i][pj])
                elif feld[pi+i][pj] == 0:
                    if feld[pi+i-1][pj] == 2:
                        for i in range(len(temp)):
                            G.append(temp[i])
                        temp = []
                        continue
                    else:
                        G = []
                        continue
                i += 1
            
            i = 0
            while i < (len(feld) - pi):
                if feld[pi-i][pj] == 1:
                    temp.append(feld[pi-i][pj])
                elif feld[pi-i][pj] == 0:
                    if feld[pi-i+1][pj] == 2:
                        for i in range(len(temp)):
                            G.append(temp[i])
                        temp = []
                        continue
                    else:
                        G = []
                        continue
                i += 1
                
            i = 0
            while i < (len(feld[0]) - pj):
                if feld[pi][pj+i] == 1:
                    temp.append(feld[pi][pj+i])
                elif feld[pi][pj+i] == 0:
                    if feld[pi][pj+i-1] == 2:
                        for i in range(len(temp)):
                            G.append(temp[i])
                        temp = []
                        continue
                    else:
                        G = []
                        continue
                i += 1
            
            i = 0
            while i < (len(feld[0]) - pj):
                if feld[pi][pj-i] == 1:
                    temp.append(feld[pi][pj-i])
                elif feld[pi][pj-i] == 0:
                    if feld[pi][pj-i+1] == 2:
                        for i in range(len(temp)):
                            G.append(temp[i])
                        temp = []
                        continue
                    else:
                        G = []
                        continue
                i += 1
                
            i = 0
            while i < (len(feld) - pi) and i < (len(feld[0]) - pj):
                if feld[pi+i][pj+i] == 1:
                    temp.append(feld[pi+i][pj+i])
                elif feld[pi+i][pj+i] == 0:
                    if feld[pi+i-1][pj+i-1] == 2:
                        for i in range(len(temp)):
                            G.append(temp[i])
                        temp = []
                        continue
                    else:
                        G = []
                        continue
                i += 1
            
            i = 0
            while i < (len(feld) - pi) and i < (len(feld[0]) - pj):
                if feld[pi-i][pj-i] == 1:
                    temp.append(feld[pi-i][pj-i])
                elif feld[pi-i][pj-i] == 0:
                    if feld[pi-i+1][pj-i+1] == 2:
                        for i in range(len(temp)):
                            G.append(temp[i])
                        temp = []
                        continue
                    else:
                        G = []
                        continue
                i += 1
            
            i = 0
            while i < (len(feld) - pi) and i < (len(feld[0]) - pj):
                if feld[pi+i][pj-i] == 1:
                    temp.append(feld[pi+i][pj-i])
                elif feld[pi+i][pj-i] == 0:
                    if feld[pi+i-1][pj-i+1] == 2:
                        for i in range(len(temp)):
                            G.append(temp[i])
                        temp = []
                        continue
                    else:
                        G = []
                        continue
                i += 1
            
            i = 0
            while i < (len(feld) - pi) and i < (len(feld[0]) - pj):
                if feld[pi-i][pj+i] == 1:
                    temp.append(feld[pi-i][pj+i])
                elif feld[pi-i][pj+i] == 0:
                    if feld[pi-i+1][pj+i-1] == 2:
                        for i in range(len(temp)):
                            G.append(temp[i])
                        temp = []
                        continue
                    else:
                        G = []
                        continue
                i += 1
            
        return G
    '''          
        # if feld[pi+1][pj] == 1 and feld[pi-1][pj] == 1 and feld[pi][pj+1] == 1 and feld[pi][pj-1] == 1 and feld[pi+1][pj+1] == 1 and feld[pi-1][pj-1] == 1 and feld[pi+1][pj-1] == 1 and feld[pi-1][pj+1] == 1:
        #     return False
        # elif feld[pi+1][pj] == 0 and feld[pi-1][pj] == 0 and feld[pi][pj+1] == 0 and feld[pi][pj-1] == 0 and feld[pi+1][pj+1] == 0 and feld[pi-1][pj-1] == 0 and feld[pi+1][pj-1] == 0 and feld[pi-1][pj+1] == 0:
        #     return False
        # elif spieler == 2:
        #     if feld[pi+1][pj] == 2 and feld[pi-1][pj] == 2 and feld[pi][pj+1] == 2 and feld[pi][pj-1] == 2 and feld[pi+1][pj+1] == 2 and feld[pi-1][pj-1] == 2 and feld[pi+1][pj-1] == 2 and feld[pi-1][pj+1] == 2:
        #         return False
        #     elif feld [pi+1][pj] == 0 and feld[pi-1][pj] == 0 and feld[pi][pj+1] == 0 and feld[pi][pj-1] == 0 and feld[pi+1][pj+1] == 0 and feld[pi-1][pj-1] == 0 and feld[pi+1][pj-1] == 0 and feld[pi-1][pj+1] == 0:
        #         return False
        # return True
    
    # Hat ein Spieler eine Spielfeld zum Setzen eines Spielsteines ausgewählt?
    if pi >= 0 and feld[pi][pj] == 0:
        # Abfrage der gültigen Züge
        if valide(pi,pj) != []:
            G = valide(pi,pj)
            # Wir besetzen das selektierte Spielfeld (pi,pj) mit der Nummer des Spielers
            feld[pi][pj] = spieler
            # und wechseln den Spieler.
            if spieler == 1: 
                for i in range (len(G)):
                    feld[G[i][0]][G[i][1]] = 1
                spieler = 2
            else:
                for i in range (len(G)):
                    feld[G[i][0]][G[i][1]] = 2
                spieler = 1
                
        
    # Regelimplementierung
    
    # while feld[i][j] != 0:
    #     rows, cols = len(feld), len(feld[0])
    #     
    #     if i+1 < rows and i-1 >= 0:
    #         if feld[i+1][j] == 1 and feld[i-1][j] == 1:
    #             farbe = ROT
    #         elif feld[i+1][j] == 2 and feld[i-1][j] == 2:
    #             farbe = BLAU
    # 
    #     if j+1 < cols and j-1 >= 0:
    #         if feld[i][j+1] == 1 and feld[i][j-1] == 1:
    #             farbe = ROT
    #         elif feld[i][j+1] == 2 and feld[i][j-1] == 2:
    #             farbe = BLAU
    #             
    #     if i+1 < rows and i-1 >= 0 and j+1 < cols and j-1 >= 0:
    #         if feld[i+1][j+1] == 1 and feld[i-1][j-1] == 1:
    #             farbe = ROT
    #         elif feld[i+1][j+1] == 2 and feld[i-1][j-1] == 2:
    #             farbe = BLAU

    # Das Zeichenfeld wird mit der Farbe Gruen gefüllt.
    screen.fill(GRUEN)
    # Wir durchlaufen das Spielfeld zeilenweise, d.h. grafisch gesehen von oben nach unten.
    for i in range(8):
        # Wir durchlaufen die i-te Zeile spaltenweise, d.h. grafisch gesehen von links nach rechts.
        for j in range(8):
            # Wir schauen uns den Feldeintrag der i-ten Zeile und j-ten Spalte an.
            if feld[i][j] == 0:
                farbe = WEISS
            elif feld[i][j] == 1:
                farbe = ROT
            elif feld[i][j] == 2:
                farbe = BLAU
                
            # Wir zeichnen einen Kreis auf das Zeichenfeld in der entsprechenden Farbe.
            # Die Koordinaten des Kreismittelpunktes (x,y) berechnen sich aus dem 
            # Spaltenindex für die x-Koordinate und dem Zeilenindex für die y-Koordinate.
            
            if height < width:
                circle_radius = height
            else:
                circle_radius = width
            
            
            pygame.draw.circle(screen,farbe,((1/8 * width)*j+(1/16) * width,(1/8 * height)*i+(1/16) * height),(1/20) * (circle_radius))

    # Zum Abschluss der Ereignisschleife sorgen wird dafür, dass die Grafik im Zeichenfenster
    # neu aufgebaut wird.
    pygame.display.update()

