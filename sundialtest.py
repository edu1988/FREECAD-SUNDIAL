#FreeCAD.getDocument('SUNDIAL_MATRIZ_POLAR').getObject('Array_i12').Placement = App.Placement(App.Vector(4.76,-89.94,0.00),App.Rotation(App.Vector(0.00,0.00,1.00),349.84))
import math

def gradosToRadianes(grados):
  return grados * 2 * math.pi / 360

def radianesToGrados(radianes):
   return radianes / (2 * math.pi / 360)

LATITUD = 42
ESPACIOS_ENTRE_HORA = 12
SALTO = 360 / (24 * ESPACIOS_ENTRE_HORA)
name = 'Array_i'
SIN = math.sin(gradosToRadianes(LATITUD))

for x in range(73):
    valorAngulo = x * SALTO
    nameArray = name + str(x)

    valor = SIN * math.tan(gradosToRadianes(valorAngulo))
    angulo = radianesToGrados(math.atan(valor))
    angulo2 = round(360 - angulo, 2)

    a = 0.25 - (0.25 * math.cos(gradosToRadianes(360 - angulo2))) + 4.75
    b = 0.25 * math.sin(gradosToRadianes(360 - angulo2)) - 90

    FreeCAD.getDocument('SUNDIAL_MATRIZ_POLAR___copia').getObject(nameArray).Placement = App.Placement(App.Vector(a,b,0.00),App.Rotation(App.Vector(0.00,0.00,1.00),angulo2))
    print(angulo2)

name = 'Array_i'
for x in range(73):
    nameArray = name + str(x) + '.'
    Gui.Selection.addSelection('SUNDIAL7','Array',nameArray)   
Gui.runCommand('Std_ToggleVisibility',0)


App.activeDocument().addObject("Part::MultiCommon","Common029")
>>> App.activeDocument().Common029.Shapes = [App.activeDocument().Cut003,App.activeDocument().Array_i12,]

items = [36]
nameAro = 'Cut003'
for x in items:
  nameArray = 'Array_i' + str(x) + '.'
  nameArrayS = 'Array_i' + str(x)
  nameLinea = 'LineaHora' + str(x)
  Gui.Selection.addSelection('SUNDIAL7',nameAro)
  Gui.Selection.addSelection('SUNDIAL7','Array',nameArray)
  App.activeDocument().addObject("Part::MultiCommon",nameLinea)
  App.activeDocument().nameLinea.Shapes = [App.activeDocument().nameAro,App.activeDocument().nameArrayS,]

def lineKind(index, stepsHour):
  lineKinds = ['h', 'm', 'd', 'u']
  if index % stepsHour == 0:
    lineKind = lineKinds[0]
  elif index % (stepsHour/2) == 0:
    lineKind = lineKinds[1]
  elif index % (stepsHour/6) == 0:
    lineKind = lineKinds[2]
  else:
    lineKind = lineKinds[3]
  return lineKind


items = range(73)
nameAroHoras = 'Cut003'
nameAroMedias = 'Cut004'
nameAroDieces = 'Cut005'
for x in items:
  nameObject2 = 'Array_i' + str(x)
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
  object1 = App.getDocument("SUNDIAL7").getObject(aroUtilizado)
  object2 = App.getDocument("SUNDIAL7").getObject(nameObject2)
  App.activeDocument().addObject("Part::MultiCommon",nameObjectF)
  objectF = App.getDocument("SUNDIAL7").getObject(nameObjectF)
  objectF.Shapes = [object1,object2]
  objectF.recompute()