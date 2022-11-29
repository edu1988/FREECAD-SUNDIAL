#SCRIPT FINAL ELABORACIÓN RELOJ DE SOL PARAMÉTRICO
import Draft
import math

# Parámetros principales
LATITUD             = 41.98
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
HOURS_NUMBERS_GAP   = 20                      #distancia de los números de las horas a las lineas de las horas
FONT_PATH           = "D:/Mis Documentos/FUENTES/goldoni/Goldoni_DEMO.otf"
FONT_SIZE           = 16.0

# Parámetros calculados
posXgnomon          = (GNOMON_WIDTH / 2) * -1
posYgnomon          = GNOMON_X_POS * -1
llineashoras        = RADIO - BORDER_GAP - HOURS_LINES_LENGTH
llineasmedias       = RADIO - BORDER_GAP - HALF_LINES_LENGTH
llineasdieces       = RADIO - BORDER_GAP - TENTH_LINES_LENGTH
posXlineaModelo     = (GNOMON_WIDTH / 2) - (LINES_WITDH / 2)
distanciaHorasBorde = HOURS_LINES_LENGTH + HOURS_NUMBERS_GAP + BORDER_GAP


def gradosToRadianes(grados):
  return grados * math.pi / 180

def radianesToGrados(radianes):
   return radianes * 180 / math.pi

def pos(angulo, margen):
  f = 1 if angulo > 0 and angulo <= 90 else -1
  k = math.cos(gradosToRadianes(angulo))
  h = math.sin(gradosToRadianes(angulo))
  c = radianesToGrados(math.atan(GNOMON_WIDTH / (2 * GNOMON_X_POS))) * f
  l = math.sqrt(pow(GNOMON_WIDTH/2, 2) + pow(GNOMON_X_POS, 2))
  g = math.cos(gradosToRadianes(90 - angulo + c))
  r = RADIO - margen
  i = pow(l, 2) * pow(g, 2) - pow(l, 2) + pow(r, 2)
  s = math.sqrt(i)
  u = (GNOMON_WIDTH / 2) * f
  j = l * g + s 
  x = k * j + u
  y = h * j - GNOMON_X_POS
  return {'x': x, 'y': y}


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
Gui.activeDocument().Circle002.Visibility=False

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


FreeCAD.getDocument(nameDocument).getObject('Array').ExpandArray = True
Gui.activeDocument().Array.Visibility=False
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
Gui.activeDocument().Array001.Visibility=False
FreeCAD.ActiveDocument.recompute()

nameElemsRect = 'Array_i'
nameElemsLine = 'Array001_i'

SALTO = 360 / (24 * (60 / MINUTE_GAP))
SIN = math.sin(gradosToRadianes(LATITUD))
XDEV = LINES_WITDH / 2

# Array de circulos cinco minutos para fusionarlos posteriormente en un solo objeto
arrayCirculos = []
arrayHoras    = []

horas = {
  '0':  ['XII', 'XII'],
  '12': ['I', 'XI'],
  '24': ['II', 'X'],
  '36': ['III', 'IX'],
  '48': ['IV', 'VIII'],
  '60': ['V', 'VI'],
  '72': ['VI', 'VI'],
  '84': ['VII', 'V']
}

for x in range(TOTAL_LINEAS):
    grosor = GNOMON_WIDTH
    valorAngulo = x * SALTO
    nameArrayRect = nameElemsRect + str(x)

    #Array de lineas 5 minutos
    nameArrayLine = nameElemsLine + str(x)

    valor = SIN * math.tan(gradosToRadianes(valorAngulo))
    angulo = radianesToGrados(math.atan(valor))

    COEF = 1

    if(angulo < 0):
        angulo += 180
        grosor = GNOMON_WIDTH * -1
        COEF = -1

    anguloFinal = round(360 - angulo, 2)

    anguloFinalPuntos = round(90 - angulo, 2)

    a = XDEV - (XDEV * math.cos(gradosToRadianes(360 - anguloFinal))) + (grosor / 2 - XDEV)
    b = XDEV * math.sin(gradosToRadianes(360 - anguloFinal)) - GNOMON_X_POS

    #posiciones origen array lineas
    j = GNOMON_WIDTH/2 * COEF
    k = GNOMON_X_POS * -1

    if(x % 2 != 0):

      coords = pos(anguloFinalPuntos, FIVE_MIN_PTS_GAP)
      posXcircle = coords['x']
      posYcircle = coords['y']

      pl = FreeCAD.Placement()
      pl.Rotation.Q=(0.0, 0.0, 0.0, 1.0)
      pl.Base=FreeCAD.Vector(posXcircle, posYcircle, 0.0)
      circle = Draft.make_circle(radius=0.6, placement=pl, face=True, support=None)

      # Añadir circulo a un array para fusionarlos despues en un solo objeto
      arrayCirculos.append(circle)

    if(x % 12 == 0):
      
      coordsNumsD = pos(anguloFinalPuntos, distanciaHorasBorde)
      coordsNumsI = pos(180 - anguloFinalPuntos, distanciaHorasBorde)
      posXnumD = coordsNumsD['x']
      posYnumD = coordsNumsD['y']
      posXnumI = coordsNumsI['x']
      posYnumI = coordsNumsI['y']

      key = str(x)
      hora1 = horas[key][0]
      hora2 = horas[key][1]

      ss = Draft.make_shapestring(String=hora1, FontFile=FONT_PATH, Size=FONT_SIZE, Tracking=0.0)
      
      moveX = (ss.Shape.BoundBox.XLength / 2)
      moveY = (ss.Shape.BoundBox.YLength / 2)
      posXnumD -= moveX
      posYnumD -= moveY

      if(x == 0):
        posXnumD -= (GNOMON_WIDTH / 2)
      
      plm=FreeCAD.Placement()
      plm.Base=FreeCAD.Vector(posXnumD, posYnumD, 0.0)
      plm.Rotation.Q=(0.0, 0.0, 0.0, 1.0)
      ss.Placement=plm
      ss.Support=None

      arrayHoras.append(ss)

      if(x != 0):
        ss = Draft.make_shapestring(String=hora2, FontFile=FONT_PATH, Size=FONT_SIZE, Tracking=0.0)
        
        moveX = (ss.Shape.BoundBox.XLength / 2)
        moveY = (ss.Shape.BoundBox.YLength / 2)
        posXnumI -= moveX
        posYnumI -= moveY
        
        plm=FreeCAD.Placement()
        plm.Base=FreeCAD.Vector(posXnumI, posYnumI, 0.0)
        plm.Rotation.Q=(0.0, 0.0, 0.0, 1.0)
        ss.Placement=plm
        ss.Support=None

        arrayHoras.append(ss)
      

    FreeCAD.getDocument(nameDocument).getObject(nameArrayRect).Placement = App.Placement(App.Vector(a,b,0.00),App.Rotation(App.Vector(0.00,0.00,1.00),anguloFinal))
    FreeCAD.getDocument(nameDocument).getObject(nameArrayLine).Placement = App.Placement(App.Vector(j,k,0.00),App.Rotation(App.Vector(0.00,0.00,1.00),anguloFinal))

App.activeDocument().addObject("Part::MultiFuse","FusionCirculosCinco")
App.activeDocument().FusionCirculosCinco.Shapes = arrayCirculos

App.activeDocument().addObject("Part::MultiFuse","FusionNumerosHoras")
App.activeDocument().FusionNumerosHoras.Shapes = arrayHoras

# Marca mediodia
App.activeDocument().addObject("Part::MultiCommon","MarcaMediodia")
App.activeDocument().MarcaMediodia.Shapes = [App.activeDocument().Rectangle001,App.activeDocument().AroHoras]
Gui.activeDocument().Rectangle001.Visibility=False
Gui.activeDocument().AroHoras.Visibility=False

# Marcas horas
marcasHoras = range(1, TOTAL_LINEAS)


nameAroHoras  = 'AroHoras'
nameAroMedias = 'AroMedias'
nameAroDieces = 'AroDieces'

arrayMarcas = []

for x in marcasHoras:
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

  arrayMarcas.append(objectF)

  objectF.recompute()

  

App.activeDocument().addObject("Part::MultiFuse","FusionLineas")
App.activeDocument().FusionLineas.Shapes = arrayMarcas

App.activeDocument().addObject("Part::MultiFuse","MarcasHorarias")
App.activeDocument().MarcasHorarias.Shapes = [App.activeDocument().FusionCirculosCinco,App.activeDocument().FusionLineas]
Gui.activeDocument().FusionCirculosCinco.Visibility=False
Gui.activeDocument().FusionLineas.Visibility=False

m = Draft.mirror([FreeCAD.ActiveDocument.MarcasHorarias], FreeCAD.Vector(0.0, -1.0, 0.0), FreeCAD.Vector(0.0, 1.0, 0.0))

FreeCAD.ActiveDocument.recompute()