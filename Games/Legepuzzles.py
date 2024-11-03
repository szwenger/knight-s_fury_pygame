# Dieses Pygame-Programm demonstriert das Tangram-Spiel
# Siehe https://de.wikipedia.org/wiki/Tangram
# https://en.wikipedia.org/wiki/Ostomachion
# https://en.wikipedia.org/wiki/Egg_of_Columbus_(tangram_shape)
# https://en.wikipedia.org/wiki/T_puzzle
# https://de.wikipedia.org/wiki/Drei-Dreiecke-Tangram

# Import der Random- und der Pygame-Bibliothek 
import random, pygame, sys, math

def rightOfLine(p,a,b):
    pa = (p[0]-a[0],p[1]-a[1])
    ba = (b[0]-a[0],b[1]-a[1])
    return(pa[0]*ba[1]-pa[1]*ba[0] > 0.0)

def dist2(a,b):
    return((a[0]-b[0])*(a[0]-b[0])+(a[1]-b[1])*(a[1]-b[1]))

def angle(u,v):
    return(math.atan2(u[0]*v[1]-u[1]*v[0],u[0]*v[0]+u[1]*v[1]))

def createCircularArc(c,a,b):
    p = []
    phi = math.atan2(b[1]-c[1],b[0]-c[0])-math.atan2(a[1]-c[1],a[0]-c[0])
    if phi < 0.0: 
        phi += 2*math.pi

    n = math.floor(phi/math.pi*40+0.5)
    cdp = math.cos(phi/n)
    sdp = math.sin(phi/n)

    cp1 = a[0]-c[0]
    sp1 = a[1]-c[1]
    p.append((c[0] + cp1,c[1] + sp1))
    for i in range(n):
        cp2 = cp1 * cdp - sp1 * sdp
        sp2 = cp1 * sdp + sp1 * cdp
        p.append((c[0] + cp2,c[1] + sp2))
        cp1 = cp2
        sp1 = sp2
    return(p)

class GeoForm:
    def __init__(self,pos,angle,center,color):
        self.pos = pos
        self.angle = angle
        self.center = center
        self.color = color

    def translate(self,t):
        px = self.pos[0] + t[0]
        py = self.pos[1] + t[1]
        self.pos = (px,py)

    def rotate(self,phi):
        self.angle += phi
        if self.angle > 2*math.pi:
            self.angle -= 2*math.pi

    def transform(self,p):
        cp = math.cos(self.angle)
        sp = math.sin(self.angle)
        cx = self.center[0]
        cy = self.center[1]
        x  = cp*(p[0]-cx)-sp*(p[1]-cy)+cx+self.pos[0]
        y  = sp*(p[0]-cx)+cp*(p[1]-cy)+cy+self.pos[1]
        return((x,y))

    def inverseTransform(self,p):
        tx = self.pos[0]
        ty = self.pos[1]
        cx = self.center[0]
        cy = self.center[1]
        cp = math.cos(self.angle)
        sp = math.sin(self.angle)
        x  =  cp*(p[0]-cx-tx)+sp*(p[1]-cy-ty)+cx
        y  = -sp*(p[0]-cx-tx)+cp*(p[1]-cy-ty)+cy
        return((x,y))

class Polygon(GeoForm):
    def __init__(self,points,color):
        self.points = points
        super().__init__((0.0,0.0),0.0,self.detCenter(),color)

    def detCenter(self):
        cx = cy = 0.0
        for p in self.points:
            cx += p[0]
            cy += p[1]
        n = len(self.points)
        cx /= n
        cy /= n
        return((cx,cy))

    def __contains__(self,p):
        n = len(self.points)
        phi = 0.0
        for i in range(n):
            a = self.points[i]
            b = self.points[(i+1)%n]
            phi += angle((a[0]-p[0],a[1]-p[1]),(b[0]-p[0],b[1]-p[1]))
        return(phi > math.pi)

    def draw(self):
        P = []
        for p in self.points:
            (x,y) = self.transform(p)
            P.append((x*zoom+width/2,-y*zoom+height/2))
        pygame.draw.polygon(screen,self.color,P)
        pygame.draw.aalines(screen,SCHWARZ,True,P)

class ConvexPolygon(Polygon):
    def __contains__(self,p):
        n = len(self.points)
        for i in range(n):
            if rightOfLine(p,self.points[i],self.points[(i+1)%n]):
                return(False)
        return(True)

class MixedPolygon(GeoForm):
    def __init__(self,arcCenter,vertices,color):
        self.arcCenter = arcCenter
        self.vertices = vertices
        super().__init__((0.0,0.0),0.0,self.detCenter(),color)
        
        self.points = createCircularArc(arcCenter,vertices[0],vertices[1])
        for i in range(2,len(vertices)):
            self.points.append(vertices[i])

    def detCenter(self):
        cx = cy = 0.0
        for p in self.vertices:
            cx += p[0]
            cy += p[1]
        n = len(self.vertices)
        cx /= n
        cy /= n
        return((cx,cy))

    def __contains__(self,p):
        n = len(self.vertices)

        if dist2(self.arcCenter,p) > dist2(self.arcCenter,self.vertices[0]):
            return(False)

        for i in range(1,n):
            if rightOfLine(p,self.vertices[i],self.vertices[(i+1)%n]):
                return(False)
        return(True)

    def draw(self):
        P = []
        for p in self.points:
            (x,y) = self.transform(p)
            P.append((x*zoom+width/2,-y*zoom+height/2))
        pygame.draw.polygon(screen,self.color,P)
        # pygame.draw.lines(screen,SCHWARZ,True,P,2)
        pygame.draw.aalines(screen,SCHWARZ,True,P)

class Puzzle:
    def __init__(self,parts):
        self.parts = parts

    def pick(self,x,y):
        u = (x-width/2)/zoom
        v = (height/2-y)/zoom
        for poly in self.parts:
            (px,py) = poly.inverseTransform((u,v))
            if (px,py) in poly:
                return(poly)
        return(None)       

    def snap(self,aPoly):
        d2min = float('inf')
        for aPoint in aPoly.points:
            a = aPoly.transform(aPoint)
            for bPoly in self.parts:
                if aPoly == bPoly: continue
                for bPoint in bPoly.points:
                    b = bPoly.transform(bPoint)   
                    d2 = dist2(a,b)
                    if d2 < d2min:
                        d2min = d2
                        d = (b[0]-a[0],b[1]-a[1])
                n = len(bPoly.points)
                for i in range(n):
                    b1 = bPoly.transform(bPoly.points[i])   
                    b2 = bPoly.transform(bPoly.points[(i+1)%n])   
                    b  = ((b1[0]+b2[0])/2,(b1[1]+b2[1])/2)
                    d2 = dist2(a,b)
                    if d2 < d2min:
                        d2min = d2
                        d = (b[0]-a[0],b[1]-a[1])
        if d2min > 0.01: return
        aPoly.translate(d)

    def snapOrientation(self,aPoly):
        d2min = phi = float('inf')
        na = len(aPoly.points)
        for i in range(na):
            aPoint = aPoly.points[i]
            a = aPoly.transform(aPoint)
            a0 = aPoly.transform(aPoly.points[(i+na-1)%na])
            a1 = aPoly.transform(aPoly.points[(i+1)%na])
            for bPoly in self.parts:
                if aPoly == bPoly: continue
                nb = len(bPoly.points)
                for j in range(nb):
                    bPoint = bPoly.points[j]
                    b = bPoly.transform(bPoint)   
                    d2 = dist2(a,b)
                    b0 = bPoly.transform(bPoly.points[(j+nb-1)%nb])
                    b1 = bPoly.transform(bPoly.points[(j+1)%nb])
                    phi1 = angle((a1[0]-a[0],a1[1]-a[1]),(b0[0]-b[0],b0[1]-b[1]))
                    phi2 = angle((a0[0]-a[0],a0[1]-a[1]),(b1[0]-b[0],b1[1]-b[1]))
                    if d2 <= 0.01 and (abs(phi1) < 0.1 or abs(phi2) < 0.1):
                        d2min = d2
                        d = (b[0]-a[0],b[1]-a[1])
                        if abs(phi1) < abs(phi2):
                            phi = phi1
                        else:
                            phi = phi2
        if abs(phi) > 0.1: return
        aPoly.rotate(phi)

    def aabb(self):
        xmin = ymin = float('inf')
        xmax = ymax = float('-inf')
        for poly in self.parts:
            for point in poly.points:
                p = poly.transform(point)
                if p[0] < xmin: xmin = p[0]
                if p[0] > xmax: xmax = p[0]
                if p[1] < ymin: ymin = p[1]
                if p[1] > ymax: ymax = p[1]
        return((xmin,xmax,ymin,ymax))

    def save(self):
        (xmin,xmax,ymin,ymax) = self.aabb()
        cx = (xmax+xmin)/2
        cy = (ymax+ymin)/2
        d2min = float('inf')
        for poly in self.parts:
            for point in poly.points:
                p = poly.transform(point)
                d2 = dist2(p,(cx,cy))
                if d2 < d2min:
                    d2min = d2
                    dx = p[0]
                    dy = p[1]
    
        #for i in range(len(self.parts)):
        #    poly = self.parts[i]
        #    print(i,poly.pos,poly.angle)
    
        for poly in self.parts:
            poly.translate((-dx,-dy))
        
        for i in range(len(self.parts)):
            poly = self.parts[i]
            phi = round(poly.angle*180.0/math.pi,8)
            tx = round(poly.pos[0],8)
            ty = round(poly.pos[1],8)
            print(i,tx,ty,phi)

    def draw(self):
        for poly in self.parts:
            poly.draw()

        if len(self.shape) == 0:
            return
        for i in range(len(self.parts)):
            poly = self.parts[i]
            tx = self.shape[self.shapeCnt][i][0]
            ty = self.shape[self.shapeCnt][i][1]
            phi = self.shape[self.shapeCnt][i][2]*math.pi/180.0
            cx = poly.center[0]
            cy = poly.center[1]
            cp = math.cos(phi)
            sp = math.sin(phi)
            P = []
            for point in poly.points:
                x = cp*(point[0]-cx)-sp*(point[1]-cy)+cx+tx
                y = sp*(point[0]-cx)+cp*(point[1]-cy)+cy+ty
                P.append((x*zoom/3+width*5/6,-y*zoom/3+height/6))
            pygame.draw.polygon(screen,SCHWARZ,P)
            if solutionOn: 
                pygame.draw.lines(screen,WEISS,True,P,2)

class Tangram(Puzzle):
    def __init__(self):
        parts = [ConvexPolygon([(0.0,0.0),(1.0,1.0),(-1.0,1.0)],(95,201,43)),
                 ConvexPolygon([(0.0,0.0),(-1.0,1.0),(-1.0,-1.0)],(255,153,51)),
                 ConvexPolygon([(0.0,0.0),(-0.5,-0.5),(0.0,-1.0),(0.5,-0.5)],(255,0,0)),
                 ConvexPolygon([(-0.5,-0.5),(-1.0,-1.0),(0.0,-1.0)], (255,255,0)),
                 ConvexPolygon([(0.0,0.0),(0.5,-0.5),(0.5,0.5)],(102,153,255)),
                 ConvexPolygon([(1.0,0.0),(1.0,1.0),(0.5,0.5),(0.5,-0.5)],(255,0,255)),
                 ConvexPolygon([(1.0,0.0),(0.0,-1.0),(1.0,-1.0)],(102,51,153))]
        super().__init__(parts)

        self.shape = [[(-0.47140452,0.27614237,135.0),(1.13807119,0.94280904,135.0),
                       ( -0.5,0.5,0.0), (0.0,0.0,0.0),( 0.33333333, 0.0,180.0),
                       ( -0.5,-1.0,90.0), ( -0.5,0.5,0.0)],
                      [( -0.0,-1.33333333,180.0),( 0.83333333,0.5,180.0),( -0.5,0.5,0.0),
                       ( 1.16666667,0.83333333,270.0), ( -0.83333333,0.83333333,90.0), 
                       ( -1.5,1.0,90.0), ( 0.16666667,1.83333333,180.0)],
                      [( -0.47140452,0.27614237,135.0),( 1.13807119,0.94280904,135.0),
                       ( -0.5,0.5,0.0), ( 1.0,0.66666667,180.0), ( 0.16666667,0.16666667,270.0), 
                       ( -1.105,-0.95355339,135.0),( -0.31455989,-0.15473785,135.0)],
                      [(-0.33333333,-1.66666667,270.0),(0.0,0.0,0.0),(-1.0,1.85355339,45.0),
                       (0.66666667,0.33333333,270.0),(-1.34375,1.87230339,270.0), 
                       (-0.5,0.0,90.0),(-1.33333333,-1.0,270.0)],
                      [(-0.51070226,-0.63986893,315.0),(0.15596441,-0.9160113,135.0),
                       (-0.98210678,1.82316017,45.0),(0.25359548,-1.49689153,135.0),
                       (-1.33864237,1.84456469,270.0),(-0.5,-0.0,90.0), 
                       (-0.98210678,-0.85882034,0.0)]]

        self.shapeCnt = 0
        self.delta = math.pi/4
        self.snapOrientationOn = False
        self.name = 'Tangram'

class AsymmetricT(Puzzle):
    def __init__(self):
        s2 = math.sqrt(2.0)
        parts = [Polygon([(0.25,0.0),(0.25,0.5),(s2/2-0.25,0.5),(-0.75+s2/2,1.0),(-0.75,1.0)],(95,201,43)),
                 ConvexPolygon([(s2/2-0.25,0.5),(s2-0.75,0.5),(s2-0.75,1.0),(s2/2-0.75,1.0)],(255,153,51)),
                 ConvexPolygon([(-0.75,1.0),(-0.75,0.5),(-0.25,0.5)],(255,0,0)),
                 ConvexPolygon([(-0.25,0.5),(-0.25,-s2+0.5),(0.25,-s2+0.5),(0.25,0)],(255,255,0))]
        super().__init__(parts)

        self.shape = [[(0.19644661,-0.2636039,135.0),(-0.27404852,0.14904852,315.0),
                       (0.91666667,0.58088023,180.0),(0.25,-0.5,0.0)],
                      [(-0.30355339,-0.67781746,135.0), (-0.77404852,-0.26516504,315.0),
                       (0.75,-0.5,-0.0),(0.25,-0.25,180.0)],
                      [(0.19644661,-0.2636039,135.0),(0.22595148,-1.05805826,-45.0),
                       (0.20118446,-0.10600649,135.0),(-0.41161165,0.27404852,-45.0)]]

        self.shapeCnt = 0
        self.delta = math.pi/4
        self.snapOrientationOn = False
        self.name = 'AsymmetricT'

class Ostomachion(Puzzle):
    def __init__(self):
        parts = [ConvexPolygon([(0.0,0.0),(0.4,-0.4),(0.6,0.0),(0.0,1.2)],(255,0,0)),
                 ConvexPolygon([(0.6,0.0),(1.2, 0.0),(1.2,0.4)],(255,127,0)),
                 ConvexPolygon([(0.6,0.0),(1.2, 0.4),(1.2,1.2),(0.0,1.2)],(255,0,127)),
                 ConvexPolygon([(0.0,1.2),(-0.4, 0.4),(0.0,0.0)],(255,127,127)),
                 ConvexPolygon([(0.0,1.2),(-1.2, 1.2),(-0.4,0.4)],(0,255,0)),
                 ConvexPolygon([(-1.2,1.2),(-1.2,-1.2),(-0.8,0.8)],(127,255,0)),
                 ConvexPolygon([(-0.8,0.8),(-1.2,-1.2),(-0.4,0.4)],(0,255,127)),
                 ConvexPolygon([(-1.2,-1.2),(-0.6,-1.2),(-0.8,-0.4)],(127,255,127)),
                 ConvexPolygon([(-0.8,-0.4),(-0.6,-1.2),(-0.6, 0.0)],(0,0,255)),
                 ConvexPolygon([(-0.6, 0.0),(-0.6,-1.2),( 0.0,-1.2),(0.0,0.0),(-0.4,0.4)],(0,127,255)),
                 ConvexPolygon([( 0.0, 0.0),( 0.0,-1.2),( 0.4,-0.4)],(127,0,255)),
                 ConvexPolygon([( 0.0,-1.2),( 1.2,-1.2),( 0.4,-0.4)],(127,127,255)),
                 ConvexPolygon([( 0.4,-0.4),( 1.2,-1.2),( 0.6, 0.0)],(255,0,255)),
                 ConvexPolygon([( 0.6, 0.0),( 1.2,-1.2),( 1.2, 0.0)],(255,255,0))]

        super().__init__(parts)

        self.shape = [[(-0.1,-0.8,180.0),(0.33333333,0.06666667,-90.0), (-0.25,0.05,90.0),
                       (0.17556246,-1.71593398,26.56505118),(-0.6,0.13333333,90.0),
                       (2.49532689,0.23071308,33.69006753),
                       (-0.34701779,-0.35894664,18.43494882),
                       (2.72819206,-0.27980411,5.61758059),
                       (2.6275367,-0.18286664,199.65382406),(0.04,0.8,-180.0),
                       (0.53333333,0.4,-90.0),(-1.4,1.46666667,90.0),
                       (-2.48464346,0.85937331,213.69006753),(-0.2,0.6,-90.0)],
                      [(0.55,-0.45,-90.0),(0.63196578,-1.05907301,-108.43494882),
                       (-0.3,-0.2,180.0),(0.2,-0.66666667,90.0),(0.2,-1.46666667,90.0),
                       (2.09149643,-0.80332298,-63.43494882),
                       (1.70557281,-0.89442719,-63.43494882),
                       (-0.0,1.2,-0.0),(-0.0,1.2,0.0),(0.0,1.2,0.0),
                       (-0.86666667,-0.13333333,180.0), (-1.66666667,0.66666667,180.0),
                       (-0.66666667,-0.2,-90.0),(0.4,0.8,-180.0)],
                      [(1.48033009,-0.51611652,135.0),(0.24714045,0.12802068,135.0),
                       (0.2732233,-1.01611652,135.0),(0.26666667,-1.06666667,180.0),
                       (-0.93333333,-0.4,270.0),(-0.0,0.0,0.0),(-0.0,0.0,0.0),
                       (-0.0,0.0,0.0),(-0.0,0.0,0.0),(-0.0,0.0,-0.0),
                       (-2.0,0.66666667,90.0),(-0.0,0.0,0.0), 
                       (1.17377345,1.07753006,135.0),(0.62426407,1.03847763,135.0)],
                      [(-0.4,0.4,-0.0), (-0.4,0.4,-0.0), (-0.4,0.4,0.0), (-0.4,-0.8,0.0),
                       (-0.4,-0.8,0.0), (0.8,-0.8,0.0), (0.8,-0.8,0.0), (0.8,-0.8,0.0),
                       (0.8,-0.8,0.0), (0.8,-0.8,0.0), (1.33333333,0.8,-90.0),
                       (0.53333333,0.8,-90.0), (-0.4,0.4,0.0),(-0.4,0.4,-360.0)]]

        self.shapeCnt = 0
        self.delta = math.pi/72
        self.snapOrientationOn = True
        self.name = 'Ostomachion'

class MagicEgg(Puzzle):
    def __init__(self):
        s2 = math.sqrt(2.0)
        parts = [MixedPolygon((0.0,0.0),[(1.0,0.0),(0.0,1.0),(0.0,s2-1.0),(s2-1.0,0.0)],(255,0,0)),
                 MixedPolygon((0.0,-1.0),[(0.0,1.0),(-s2,s2-1.0),(-1.0,0.0)],(0,255,0)),
                 MixedPolygon((-1.0,0.0),[(-s2,s2-1.0),(-3.0+s2,0.0),(-1.0,0.0)],(0,0,255)),
                 ConvexPolygon([(0.0,0.0),(s2-1.0,0.0),(0.0,s2-1.0)],(0,255,255)),
                 ConvexPolygon([(0.0,0.0),(0.0,1.0),(-1.0,0.0)],(255,255,0)),
                 MixedPolygon((0.0,0.0),[(0.0,-1.0),(1.0,0.0),(s2-1.0,0.0),(0.0,1.0-s2)],(255,0,255)),
                 MixedPolygon((0.0,1.0),[(-s2,1.0-s2),(0.0,-1.0),(-1.0,0.0)],(255,127,127)),
                 MixedPolygon((-1.0,0.0),[(-3.0+s2,0.0),(-s2,1.0-s2),(-1.0,0.0)],(127,255,127)),
                 ConvexPolygon([(0.0,0.0),(0.0,1.0-s2),(s2-1.0,0.0)],(127,127,255)),
                 ConvexPolygon([(0.0,0.0),(-1.0,0.0),(0.0,-1.0)],(0,255,255))]

        super().__init__(parts)

        self.shape = [[(0.5857864376269052,0.14558844416339467,315.0),
                       (0.06556638036696438,-0.4841073213452754,90.0),
                       (1.9846861513272023,-0.4841073213452759,180.0),
                       (0.7322330470336313,-0.20796494642987912,0.0),
                       (0.34502167936045186,-1.718093251254129,135.0),
                       (-0.32842712474619007,-0.06151833702315282,315.0),
                       (1.47977994274006,1.482390990858613,270.0),
                       (0.22732683844648754,1.068177428485518,180.0),
                       (-1.129695765508671,0.792035053570121,270.0),
                       (0.7322330470336313,0.45870172023678746,270.0)],
        	      [(-0.35355339059327373,-0.6465962805257706,225.0),
                       (1.7071067811865475,-0.5001496711190445,0.0),
                       (1.1785113019775793,1.1093260371296858,270.0),
                       (-0.33333333333333337,0.0688859226098048,135.0),
                       (0.2928932188134524,0.24739722458738406,90.0),
                       (-0.8535533905932734,0.5605105006607769,225.0),
                       (0.04044011451988069,1.5807305579207178,225.0),
                       (1.3737734478532144,1.190206266169448,180.0),
                       (-0.13807118745769842,0.14976615164956644,315.0),
                       (0.27134597597636434,-0.930814735152107,45.0)],
        	      [(-1.0,0.0021587256790454035,90.0),
                       (0.9832491561019436,0.1402299131367436,315.0),
                       (0.26968289577256843,-0.687711645863755,225.0),
                       (0.43096440627115074,0.1402299131367436,180.0),
                       (0.39756921904077436,-1.0997897986168632,135.0),
                       (-0.35355339059327384,0.5628188974588666,315.0),
                       (2.121320343559643,0.4163722880521401,0.0),
                       (-0.5118446353109127,-0.11222319115682769,270.0),
                       (0.7071067811865472,0.4163722880521402,0.0),
                       (-1.040440114519881,0.0021587256790455145,90.0)]]

        self.shapeCnt = 0
        self.delta = math.pi/4
        self.snapOrientationOn = False
        self.name = 'Magic Egg'

# Definition der beiden Farben schwarz und weiss im RGB-Modell
SCHWARZ = (0,0,0)
WEISS = (255,255,255)

width = 1200
height = 900
# Initialisierung der Pygame-Bibliothek
pygame.init()
# Erzeugen einer quadratischen Zeichenfläche mit width x height Pixeln
screen = pygame.display.set_mode((width,height),pygame.RESIZABLE)
# Erzeugen einer Uhr zur Steuerung der Framerate beim Bildaufbau.
clock = pygame.time.Clock()
# Überschrift des Zeichenfensters
fontname =  pygame.font.get_default_font()
font = pygame.font.Font(fontname,10)
pygame.key.set_repeat(100)

zoom = min(width,height)/5
pickPart = None
solutionOn = False

puzzles = [Tangram(),Ostomachion(),AsymmetricT(),MagicEgg()]
puzzleIndex = 0
puzzle = puzzles[0]
pygame.display.set_caption(puzzle.name)

# Wir betreten die Ereignisschleife.
while True:
    # Die Bildwiederholfrequenz wird auf 30 Bilder pro Sekunde gesetzt.
    clock.tick(30)

    # Abarbeitung aller Ereignisse seit dem letzten Durchlauf der Ereignisschleife.
    for event in pygame.event.get():
        # Wurde eine Maustaste gedrückt?
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Ermittele die Position des Mauszeigers.
            (mx,my) = pygame.mouse.get_pos()
            pickPart = puzzle.pick(mx,my)
        elif event.type == pygame.MOUSEBUTTONUP:
            if pickPart != None:
                if puzzle.snapOrientationOn:
                    puzzle.snapOrientation(pickPart)
                puzzle.snap(pickPart)
                pickPart = None
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                puzzleIndex = (puzzleIndex+1)%len(puzzles)
                puzzle = puzzles[puzzleIndex]
                pygame.display.set_caption(puzzle.name)
            elif event.key == pygame.K_PAGEDOWN:
                puzzleIndex = (puzzleIndex+len(puzzles)-1)%len(puzzles)
                puzzle = puzzles[puzzleIndex]
                pygame.display.set_caption(puzzle.name)
            elif pickPart != None and event.key == pygame.K_LSHIFT:
                pickPart.rotate(puzzle.delta)
            elif pickPart != None and event.key == pygame.K_RSHIFT:
                pickPart.rotate(-puzzle.delta)
            elif event.key == pygame.K_l:
                solutionOn = not solutionOn
            elif event.key == pygame.K_s:
                puzzle.save()
            elif event.key == pygame.K_UP:
                puzzle.shapeCnt = (puzzle.shapeCnt+len(puzzle.shape)-1)%len(puzzle.shape)
            elif event.key == pygame.K_DOWN:
                puzzle.shapeCnt = (puzzle.shapeCnt+1)%len(puzzle.shape)
        # Wurde das Fenster geschlossen?
        elif event.type == pygame.MOUSEMOTION:
            if pickPart != None:
                (x,y) = pygame.mouse.get_pos()
                pickPart.translate(((x-mx)/zoom,(my-y)/zoom))
                mx = x
                my = y
        elif event.type == pygame.MOUSEWHEEL:
            if event.y < 0:
                zoom /= 1.05
            else:
                zoom *= 1.05
        elif event.type == pygame.QUIT:
            # Verlasse die Ereignisschleife und das Programm.
            pygame.quit()
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            (width,height) = screen.get_size()
            zoom = min(width,height)/5

    # Wir löschen die Zeichenfläche, indem wir sie mit der Farbe weiss füllen.
    screen.fill(WEISS)

    puzzle.draw()

    # Wir aktualisieren die Zeichenfläche und durchlaufen die Ereignisschleife erneut.
    pygame.display.update()

