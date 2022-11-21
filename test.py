import math

def gradosToRadianes(grados):
  return grados * 2 * math.pi / 360

def radianesToGrados(radianes):
   return radianes / (2 * math.pi / 360)

CADA_CUANTOS_MINUTOS = 5
LATITUD = 42
grosor_lineas = 0.5
HORAS = 7
TOTAL_LINEAS = int(HORAS * (60 / CADA_CUANTOS_MINUTOS) + 1)

ancho_gnomon        = 10                      #grosor gnomon en mm
largo_gnomon        = 120                     #largo gnomon en mm
posicion_gnomon     = 90 

SALTO = 360 / (24 * (60 / CADA_CUANTOS_MINUTOS))
SIN = math.sin(gradosToRadianes(LATITUD))
XDEV = grosor_lineas / 2

for x in range(TOTAL_LINEAS):
    valorAngulo = x * SALTO
    valor = SIN * math.tan(gradosToRadianes(valorAngulo))
    angulo = radianesToGrados(math.atan(valor))

    if(angulo < 0):
        angulo += 180
    
    anguloF = round(360 - angulo, 2)

    print(anguloF)
    # a = XDEV - (XDEV * math.cos(gradosToRadianes(360 - anguloF))) + (ancho_gnomon / 2 - XDEV)
    # b = XDEV * math.sin(gradosToRadianes(360 - anguloF)) - posicion_gnomon