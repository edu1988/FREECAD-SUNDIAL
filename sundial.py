#SCRIPT FINAL ELABORACIÓN RELOJ DE SOL PARAMÉTRICO
import Draft
import math

# Parámetros principales
LATITUD             = 42
MINUTE_GAP          = 5
TOTAL_HOURS         = 7.75

RADIO               = 180                     #radio reloj en mm
GNOMON_WIDTH        = 10                      #grosor gnomon en mm
GNOMON_LENGTH       = 120                     #largo gnomon en mm
GNOMON_X_POS        = 90                      #distancia del extremo del gnomon al centro del reloj en mm
BORDER_GAP          = 1                       #distancia de las marcas al borde del reloj en mm
HOURS_LINES_LENGTH  = 23                      #longitud de las líneas de las horas
HALF_LINES_LENGTH   = 12                      #longitud de las líneas de las medias
TENTH_LINES_LENGTH  = 6                       #longitud de las líneas de los dieces
FIVE_MIN_PTS_GAP    = 3                       #distancia del borde a los puntos de 5 minutos
FIVE_MIN_PTS_RAD    = 1                       #radio de los puntos de 5 minutos
LINES_WITDH         = 0.5                     #grosor líneas horarias

# Parámetros calculados
posXgnomon          = (GNOMON_WIDTH / 2) * -1
posYgnomon          = GNOMON_X_POS * -1
llineashoras        = RADIO - BORDER_GAP - HOURS_LINES_LENGTH
llineasmedias       = RADIO - BORDER_GAP - HALF_LINES_LENGTH
llineasdieces       = RADIO - BORDER_GAP - TENTH_LINES_LENGTH
posXlineaModelo     = (GNOMON_WIDTH / 2) - (LINES_WITDH / 2)

configHoras = {
  'horas': HOURS_LINES_LENGTH,
  'medias': HALF_LINES_LENGTH,
}

def gradosToRadianes(grados):
  return grados * 2 * math.pi / 360

def radianesToGrados(radianes):
   return radianes / (2 * math.pi / 360)

def lineKind(index, stepsHour):
  lineKinds = ['h', 'm', 'd', 'u']
  default = 'u'
  if index % stepsHour == 0:
    lineKind = lineKinds[0]
  elif index % (stepsHour/2) == 0:
    lineKind = lineKinds[1]
  elif index % (stepsHour/6) == 0:
    lineKind = lineKinds[2]
  elif index % (stepsHour/12):
    lineKind = lineKinds[3]
  else:
    lineKind = default
  return lineKind



# Nombre documento principal
nameDocument = 'SUNDIAL'
App.newDocument(nameDocument)

# Dibujar el círculo principal
pl = FreeCAD.Placement()
pl.Rotation.Q = (0.0, 0.0, 0.0, 1.0)
pl.Base = FreeCAD.Vector(0.0, 0.0, 0.0)
circle = Draft.make_circle(radius=RADIO, placement=pl, face=True, support=None)
circle.Label = 'Perimetro'
Draft.autogroup(circle)

FreeCADGui.getDocument('SUNDIAL').getObject('Circle').Deviation = 0.01
FreeCAD.getDocument('SUNDIAL').getObject('Circle').MakeFace = False

# Dibujar fisura gnomon
pl = FreeCAD.Placement()
pl.Rotation.Q = (0.0, 0.0, 0.0, 1.0)
pl.Base = FreeCAD.Vector(posXgnomon, posYgnomon, 0.0)
rec = Draft.make_rectangle(length=GNOMON_WIDTH, height=GNOMON_LENGTH, placement=pl, face=True, support=None)
rec.Label = 'Gnomon'
FreeCAD.getDocument(nameDocument).getObject('Rectangle').MakeFace = False

# Dibujar rectangulo proyección gnomon mediodia
rec = Draft.make_rectangle(length=GNOMON_WIDTH, height=RADIO*1.6, placement=pl, face=True, support=None)
rec.Label = 'ProyeccionGnomon'
FreeCAD.getDocument(nameDocument).getObject('Rectangle001').MakeFace = True


# Circulo Interno Márgen (Circle001)
offst = Draft.offset(FreeCAD.ActiveDocument.Circle, RADIO - BORDER_GAP, copy=True, occ=False)

# Circulo Interno Puntos 5 min (Circle 002)
offst = Draft.offset(FreeCAD.ActiveDocument.Circle, RADIO - FIVE_MIN_PTS_GAP, copy=True, occ=False)
FreeCAD.getDocument('SUNDIAL').getObject('Circle002').MakeFace = False
FreeCAD.getDocument(nameDocument).getObject('Circle002').Label = 'CirculoCincoMinutos'

# Circulo Horas (Circle003)
offst = Draft.offset(FreeCAD.ActiveDocument.Circle001, llineashoras, copy=True, occ=False)

# Dibujar Aro Horas
App.activeDocument().addObject("Part::Cut","AroHoras")
App.activeDocument().AroHoras.Base = App.activeDocument().Circle001
App.activeDocument().AroHoras.Tool = App.activeDocument().Circle003
FreeCAD.getDocument(nameDocument).getObject('AroHoras').Label = 'AroHoras'
FreeCADGui.getDocument(nameDocument).getObject('AroHoras').Deviation = 0.01

# Circulo Medias (Circle004)
offst = Draft.offset(FreeCAD.ActiveDocument.Circle001, llineasmedias, copy=True, occ=False)

# Dibujar Aro Medias
App.activeDocument().addObject("Part::Cut","AroMedias")
App.activeDocument().AroMedias.Base = App.activeDocument().Circle001
App.activeDocument().AroMedias.Tool = App.activeDocument().Circle004
FreeCAD.getDocument(nameDocument).getObject('AroMedias').Label = 'AroMedias'
FreeCADGui.getDocument(nameDocument).getObject('AroMedias').Deviation = 0.01

# Circulo Dieces (Circle005)
offst = Draft.offset(FreeCAD.ActiveDocument.Circle001, llineasdieces, copy=True, occ=False)

# Dibujar Aro Dieces
App.activeDocument().addObject("Part::Cut","AroDieces")
App.activeDocument().AroDieces.Base = App.activeDocument().Circle001
App.activeDocument().AroDieces.Tool = App.activeDocument().Circle005
FreeCAD.getDocument(nameDocument).getObject('AroDieces').Label = 'AroDieces'
FreeCADGui.getDocument(nameDocument).getObject('AroDieces').Deviation = 0.01


# Dibujar rectángulo modelo
pl = FreeCAD.Placement()
pl.Rotation.Q = (0.0, 0.0, 0.0, 1.0)
pl.Base = FreeCAD.Vector(posXlineaModelo, posYgnomon, 0.0)
rec = Draft.make_rectangle(length=LINES_WITDH, height=RADIO*1.6, placement=pl, face=True, support=None)

TOTAL_LINEAS = int(TOTAL_HOURS * (60 / MINUTE_GAP) + 1)

# Dibujar todos los rectangulos
Draft.make_polar_array(App.ActiveDocument.Rectangle002, number=TOTAL_LINEAS, angle=-90.0, center=FreeCAD.Vector(posXgnomon * -1, posYgnomon, 0.0), use_link=True)


# Draft.autogroup(_obj_)
FreeCAD.getDocument(nameDocument).getObject('Array').ExpandArray = True
FreeCAD.ActiveDocument.recompute()

# Dibujar linea modelo 5 minutos
pl = FreeCAD.Placement()
pl.Rotation.Q = (0.0, 0.0, 0, 1.0)
pl.Base = FreeCAD.Vector(GNOMON_WIDTH/2, posYgnomon, 0.0)
points = [FreeCAD.Vector(GNOMON_WIDTH/2, posYgnomon, 0.0), FreeCAD.Vector(GNOMON_WIDTH/2, RADIO*1.6, 0.0)]
line = Draft.make_wire(points, placement=pl, closed=False, face=True, support=None)

# # Dibujar todas las lineas
Draft.make_polar_array(App.ActiveDocument.Line, number=TOTAL_LINEAS, angle=-90.0, center=FreeCAD.Vector(posXgnomon * -1, posYgnomon, 0.0), use_link=True)
FreeCAD.getDocument(nameDocument).getObject('Array001').ExpandArray = True
FreeCAD.ActiveDocument.recompute()

nameElemsRect = 'Array_i'
nameElemsLine = 'Array001_i'

SALTO = 360 / (24 * (60 / MINUTE_GAP))
SIN = math.sin(gradosToRadianes(LATITUD))
XDEV = LINES_WITDH / 2

for x in range(TOTAL_LINEAS):
    grosor = GNOMON_WIDTH
    valorAngulo = x * SALTO
    nameArrayRect = nameElemsRect + str(x)

    #Array de lineas 5 minutos
    nameArrayLine = nameElemsLine + str(x)

    valor = SIN * math.tan(gradosToRadianes(valorAngulo))
    angulo = radianesToGrados(math.atan(valor))

    anguloPuntosCirculo = round(90 - angulo, 2)

    COEF = 1

    if(angulo < 0):
        angulo += 180
        grosor = GNOMON_WIDTH * -1
        COEF = -1

    anguloFinal = round(360 - angulo, 2)

    

    a = XDEV - (XDEV * math.cos(gradosToRadianes(360 - anguloFinal))) + (grosor / 2 - XDEV)
    b = XDEV * math.sin(gradosToRadianes(360 - anguloFinal)) - GNOMON_X_POS

    #posiciones origen array lineas
    j = GNOMON_WIDTH/2 * COEF
    k = GNOMON_X_POS * -1

    if(x % 2 != 0):
      cosx = math.cos(gradosToRadianes(anguloPuntosCirculo))
      sinx = math.sin(gradosToRadianes(anguloPuntosCirculo))
      posXcircle = cosx * (RADIO + 90 - FIVE_MIN_PTS_GAP) + (GNOMON_WIDTH / 2)
      posYcircle = sinx * (RADIO + 90 - FIVE_MIN_PTS_GAP) - 90
      pl = FreeCAD.Placement()
      pl.Rotation.Q=(0.0, 0.0, 0.0, 1.0)
      pl.Base=FreeCAD.Vector(posXcircle, posYcircle, 0.0)
      circle = Draft.make_circle(radius=0.6, placement=pl, face=True, support=None)

    FreeCAD.getDocument(nameDocument).getObject(nameArrayRect).Placement = App.Placement(App.Vector(a,b,0.00),App.Rotation(App.Vector(0.00,0.00,1.00),anguloFinal))
    FreeCAD.getDocument(nameDocument).getObject(nameArrayLine).Placement = App.Placement(App.Vector(j,k,0.00),App.Rotation(App.Vector(0.00,0.00,1.00),anguloFinal))



# Marca mediodia
App.activeDocument().addObject("Part::MultiCommon","MarcaMediodia")
App.activeDocument().MarcaMediodia.Shapes = [App.activeDocument().Rectangle001,App.activeDocument().AroHoras]
Gui.activeDocument().Rectangle001.Visibility=False
Gui.activeDocument().AroHoras.Visibility=False

# Marcas horas
nameAroHoras  = 'AroHoras'
nameAroMedias = 'AroMedias'
nameAroDieces = 'AroDieces'
for x in range(TOTAL_LINEAS):
  nameObjectR = 'Array_i' + str(x)
  nameObjectF = 'LINEAHORA' + str(x)
  aro = lineKind(x, 12)
  if aro == 'h':
    aroUtilizado = nameAroHoras
  elif aro == 'm':
    aroUtilizado = nameAroMedias
  elif aro == 'd':
    aroUtilizado = nameAroDieces
  else:
    continue

  object1 = App.getDocument(nameDocument).getObject(aroUtilizado)
  object2 = App.getDocument(nameDocument).getObject(nameObjectR)
  App.activeDocument().addObject("Part::MultiCommon",nameObjectF)
  objectF = App.getDocument(nameDocument).getObject(nameObjectF)
  objectF.Shapes = [object1,object2]
  objectF.recompute()






FreeCAD.ActiveDocument.recompute()