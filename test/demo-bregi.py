#!/usr/bin/python
import serial
import time

import serial
import time
#import sys
import numpy
import binascii
from copy import copy, deepcopy

#TAMANO DE CADA MODULO EN LEDS
ALTOM=4
ANCHOM=8

#MODULOS HORIZ Y VERT DEL CARTEL
MODULOSH = 7
MODULOSV = 3

#Tiempos de demora entre comandos
TIMEZG=0.01
TIMEZS=0.01
TIMEZM=0.01

DEBUG=1

DEVICE="/dev/ttyS0"


offy=-1
sube=1


##########LERTAS##########################################
font = numpy.array([
[0x00, 0x00, 0x00, 0x00, 0x00], # (spacja)
[0x00, 0x00, 0x5F, 0x00, 0x00], # !
[0x00, 0x07, 0x00, 0x07, 0x00], # "
[0x14, 0x7F, 0x14, 0x7F, 0x14], # #
[0x24, 0x2A, 0x7F, 0x2A, 0x12], # $
[0x23, 0x13, 0x08, 0x64, 0x62], # %
[0x36, 0x49, 0x55, 0x22, 0x50], # &
[0x00, 0x05, 0x03, 0x00, 0x00], # '
[0x00, 0x1C, 0x22, 0x41, 0x00], # (
[0x00, 0x41, 0x22, 0x1C, 0x00], # )
[0x08, 0x2A, 0x1C, 0x2A, 0x08], # *
[0x08, 0x08, 0x3E, 0x08, 0x08], # +
[0x00, 0x50, 0x30, 0x00, 0x00], # ,
[0x08, 0x08, 0x08, 0x08, 0x08], # -
[0x00, 0x30, 0x30, 0x00, 0x00], # .
[0x20, 0x10, 0x08, 0x04, 0x02], # /
[0x3E, 0x51, 0x49, 0x45, 0x3E], # 0
[0x00, 0x42, 0x7F, 0x40, 0x00], # 1
[0x42, 0x61, 0x51, 0x49, 0x46], # 2
[0x21, 0x41, 0x45, 0x4B, 0x31], # 3
[0x18, 0x14, 0x12, 0x7F, 0x10], # 4
[0x27, 0x45, 0x45, 0x45, 0x39], # 5
[0x3C, 0x4A, 0x49, 0x49, 0x30], # 6
[0x01, 0x71, 0x09, 0x05, 0x03], # 7
[0x36, 0x49, 0x49, 0x49, 0x36], # 8
[0x06, 0x49, 0x49, 0x29, 0x1E], # 9
[0x00, 0x36, 0x36, 0x00, 0x00], # :
[0x00, 0x56, 0x36, 0x00, 0x00], # ;
[0x00, 0x08, 0x14, 0x22, 0x41], # <
[0x14, 0x14, 0x14, 0x14, 0x14], # =
[0x41, 0x22, 0x14, 0x08, 0x00], # >
[0x02, 0x01, 0x51, 0x09, 0x06], # ?
[0x32, 0x49, 0x79, 0x41, 0x3E], # @
[0x7E, 0x11, 0x11, 0x11, 0x7E], # A
[0x7F, 0x49, 0x49, 0x49, 0x36], # B
[0x3E, 0x41, 0x41, 0x41, 0x22], # C
[0x7F, 0x41, 0x41, 0x22, 0x1C], # D
[0x7F, 0x49, 0x49, 0x49, 0x41], # E
[0x7F, 0x09, 0x09, 0x01, 0x01], # F
[0x3E, 0x41, 0x41, 0x51, 0x32], # G
[0x7F, 0x08, 0x08, 0x08, 0x7F], # H
[0x00, 0x41, 0x7F, 0x41, 0x00], # I
[0x20, 0x40, 0x41, 0x3F, 0x01], # J
[0x7F, 0x08, 0x14, 0x22, 0x41], # K
[0x7F, 0x40, 0x40, 0x40, 0x40], # L
[0x7F, 0x02, 0x04, 0x02, 0x7F], # M
[0x7F, 0x04, 0x08, 0x10, 0x7F], # N
[0x3E, 0x41, 0x41, 0x41, 0x3E], # O
[0x7F, 0x09, 0x09, 0x09, 0x06], # P
[0x3E, 0x41, 0x51, 0x21, 0x5E], # Q
[0x7F, 0x09, 0x19, 0x29, 0x46], # R
[0x46, 0x49, 0x49, 0x49, 0x31], # S
[0x01, 0x01, 0x7F, 0x01, 0x01], # T
[0x3F, 0x40, 0x40, 0x40, 0x3F], # U
[0x1F, 0x20, 0x40, 0x20, 0x1F], # V
[0x7F, 0x20, 0x18, 0x20, 0x7F], # W
[0x63, 0x14, 0x08, 0x14, 0x63], # X
[0x03, 0x04, 0x78, 0x04, 0x03], # Y
[0x61, 0x51, 0x49, 0x45, 0x43], # Z
[0x00, 0x00, 0x7F, 0x41, 0x41], # [
[0x02, 0x04, 0x08, 0x10, 0x20], # "\"
[0x41, 0x41, 0x7F, 0x00, 0x00], # ]
[0x04, 0x02, 0x01, 0x02, 0x04], # ^
[0x40, 0x40, 0x40, 0x40, 0x40], # _
[0x00, 0x01, 0x02, 0x04, 0x00], # `
[0x20, 0x54, 0x54, 0x54, 0x78], # a
[0x7F, 0x48, 0x44, 0x44, 0x38], # b
[0x38, 0x44, 0x44, 0x44, 0x20], # c
[0x38, 0x44, 0x44, 0x48, 0x7F], # d
[0x38, 0x54, 0x54, 0x54, 0x18], # e
[0x08, 0x7E, 0x09, 0x01, 0x02], # f
[0x08, 0x14, 0x54, 0x54, 0x3C], # g
[0x7F, 0x08, 0x04, 0x04, 0x78], # h
[0x00, 0x44, 0x7D, 0x40, 0x00], # i
[0x20, 0x40, 0x44, 0x3D, 0x00], # j
[0x00, 0x7F, 0x10, 0x28, 0x44], # k
[0x00, 0x41, 0x7F, 0x40, 0x00], # l
[0x7C, 0x04, 0x18, 0x04, 0x78], # m
[0x7C, 0x08, 0x04, 0x04, 0x78], # n
[0x38, 0x44, 0x44, 0x44, 0x38], # o
[0x7C, 0x14, 0x14, 0x14, 0x08], # p
[0x08, 0x14, 0x14, 0x18, 0x7C], # q
[0x7C, 0x08, 0x04, 0x04, 0x08], # r
[0x48, 0x54, 0x54, 0x54, 0x20], # s
[0x04, 0x3F, 0x44, 0x40, 0x20], # t
[0x3C, 0x40, 0x40, 0x20, 0x7C], # u
[0x1C, 0x20, 0x40, 0x20, 0x1C], # v
[0x3C, 0x40, 0x30, 0x40, 0x3C], # w
[0x44, 0x28, 0x10, 0x28, 0x44], # x
[0x0C, 0x50, 0x50, 0x50, 0x3C], # y
[0x44, 0x64, 0x54, 0x4C, 0x44], # z
[0x00, 0x08, 0x36, 0x41, 0x00], # {
[0x00, 0x00, 0x7F, 0x00, 0x00], # |
[0x00, 0x41, 0x36, 0x08, 0x00], # }
[0x08, 0x08, 0x2A, 0x1C, 0x08], # ->
[0x08, 0x1C, 0x2A, 0x08, 0x08]], dtype=numpy.uint8) # <-

ser = serial.Serial('/dev/ttyS0', baudrate=19200)
#ser = serial.Serial("/dev/ttyS0", baudrate=19200)
print "Inicializando puerto serial"


#Imprime en binario un numero##############################
def pbin(x, digits=0):
 oct2bin = ['000','001','010','011','100','101','110','111']
 binstring = [oct2bin[int(n)] for n in oct(x)]
 return ''.join(binstring).lstrip('0').zfill(digits)

#Imrpime el array en binario#############################################
def printbin (matt):
 for ml in range (MODULOSV):
   for y in range (ALTOM):
     fila=(ml*ALTOM)+y
     for x in range (MODULOSH):
       print  pbin(matt[fila][x],8),
     print " "
     #print (" fila %d"  %fila)
 print ("---------------------------")
 return

#Swap una matriz para acomodar a la salida #################################3
def swapmatrix(inmat):

 swapn=deepcopy(inmat)
 for x in range (MODULOSH):
   for y in range (MODULOSV*ALTOM):
      #swapn = ((inmat[y][x] >> 4) & 0x0f) | ((inmat[y][x] << 4) & 0xf0);
      swapn[y][x]=0x00
      if (inmat[y][x] & 0x01):
        swapn[y][x]|=0x80
      if (inmat[y][x] & 0x02):
        swapn[y][x]|=0x40
      if (inmat[y][x] & 0x04):
        swapn[y][x]|=0x20
      if (inmat[y][x] & 0x08):
        swapn[y][x]|=0x10
      if (inmat[y][x] & 0x10):
        swapn[y][x]|=0x08
      if (inmat[y][x] & 0x20):
        swapn[y][x]|=0x04
      if (inmat[y][x] & 0x40):
        swapn[y][x]|=0x02
      if (inmat[y][x] & 0x80):
        swapn[y][x]|=0x01
 
# tempm = numpy.zeros( 4, dtype=numpy.uint8 )
#  for x in range (MODULOSH):
#   for y in range (MODULOSV):
 
 return swapn
      
#Imrpime el array#############################################
def serialled (origin):
 #cambia el orden de todos los bits
 zzz=swapmatrix(origin)
 for x in range (MODULOSH):
  #for y in range (MODULOSV):
   fila=0
   s1 = 'zg' + binascii.hexlify(zzz[fila+3][x]) + binascii.hexlify(zzz[fila+2][x]) + "\r"
   s2 = 'zG' + binascii.hexlify(zzz[fila+1][x]) + binascii.hexlify(zzz[fila+0][x]) + "\r"
   s3 = 'zh' + binascii.hexlify(zzz[fila+7][x]) + binascii.hexlify(zzz[fila+6][x]) + "\r"
   s4 = 'zH' + binascii.hexlify(zzz[fila+5][x]) + binascii.hexlify(zzz[fila+4][x]) + "\r"
   s5 = 'zi' + binascii.hexlify(zzz[fila+11][x]) + binascii.hexlify(zzz[fila+10][x]) + "\r"
   s6 = 'zI' + binascii.hexlify(zzz[fila+9][x]) + binascii.hexlify(zzz[fila+8][x]) + "\r"
   #print ("zg", zzz[fila][x],  zzz[fila+1][x] )
   if (DEBUG==1):
     print s1
     print s2
     print s3
     print s4
     print s5
     print s6
   ser.write(s1)
   time.sleep(TIMEZG)
   ser.write(s2)
   time.sleep(TIMEZG)
   ser.write(s3)
   time.sleep(TIMEZG)
   ser.write(s4)
   time.sleep(TIMEZG)
   ser.write(s5)
   time.sleep(TIMEZG)
   ser.write(s6)
   time.sleep(TIMEZG)
   ser.write("zS\r")

   if (DEBUG==1):
     print ("zS-------------------------------------")
   time.sleep(TIMEZS)
 ser.write("zm\r")
 print ("zm-------------------------------------")
 time.sleep(TIMEZM)
 return

#Llena modulos con cuatro bytes########################################
def llenamatriz (matt, b1, b2, b3, b4):
 for y in range (MODULOSV):
   for x in range (MODULOSH):
     fila=y*4
     matt[fila+0][x]=b1
     matt[fila+1][x]=b2
     matt[fila+2][x]=b3
     matt[fila+3][x]=b4
 return

#Rota el cartel a la derecha##########################################
def rotamatriz_der (tmatt,nro=1):

    for t in range (nro):
        for y in range (MODULOSV*ALTOM):
          for x in range (MODULOSH-1, -1,-1):
            #print "IT:", x , " "
            tmatt[y][x]=tmatt[y][x]>>1
            if x!=0 and (tmatt[y][x-1]&0x01!=0):
             tmatt[y][x]|=0x80
    return

#Rota el cartel a la izquierda##########################################
def rotamatriz_izq (tmatt,nro=1):

     for t in range (nro):
        for y in range (MODULOSV*ALTOM):
          for x in range (0,MODULOSH):
            #print "IT:", x , " "
            tmatt[y][x]=tmatt[y][x]<<1
            if x<MODULOSH-1 and (tmatt[y][x+1]&0x80!=0):
             tmatt[y][x]|=0x01
     return

#Rota el cartel a la derecha insertando de una matriz auxiliar##########
def arotamatriz_der (mattizq, tmatt, nro=1):
  for v in range(0,nro):
    rotamatriz_der (tmatt)                       #Rota la matriz
    for y in range (MODULOSV*ALTOM):         #Se fija si la matriz auxiliar termina con 1 y los pasa
      if (mattizq[y][MODULOSH-1]&0x01)!=0:
         tmatt[y][0]|=0x80
    rotamatriz_der (mattizq)                     #Rota la matriz auziliar
  return

#Rota el cartel a la izquierda insertando de una matriz auxiliar##########
def arotamatriz_izq (mattder, tmatt, nro=1):
  for v in range(0,nro):
    rotamatriz_izq (tmatt)                       #Rota la matriz hacia la izq
    for y in range (MODULOSV*ALTOM):         #Se fija si la matriz auxiliar termina con 1 y los pasa
      if (mattder[y][0]&0x80)!=0:
         tmatt[y][MODULOSH-1]|=0x01
    rotamatriz_izq (mattder)                     #Rota la matriz auxiliar
  return

####Imprime letra en buffer#############################################
def printfont (mtrx, caracter,offsety=0, offsetx=MODULOSH-1):
  nfont=caracter - 0x20

  letrarot = numpy.zeros( 7, dtype=numpy.uint8 )
  #letraorig= numpy.zeros( 5, dtype=numpy.uint8 )
  #for t in range(5):
  #  letraorig[t]=font[nfont][t]
  letraorig=font[nfont][:]
  #for idx in range (0,7):
  idx=0
  for msk in  [0x01, 0x02, 0x04, 0x8, 0x10, 0x20, 0x40]:
     if (letraorig[0]&msk!=0):
      letrarot[idx]|=0x10
      
     if (letraorig[1]&msk!=0):
      letrarot[idx]|=0x08

     if (letraorig[2]&msk!=0):
      letrarot[idx]|=0x04

     if (letraorig[3]&msk!=0):
      letrarot[idx]|=0x02

     if (letraorig[4]&msk!=0):
      letrarot[idx]|=0x01
     mtrx[idx+offsety][offsetx]|=letrarot[idx]
     idx+=1
  #print letraorig
  #print  letrarot
  return
###Calcula offset loco en y de la letra###############################
def cambia_offset ():

  global offy
  global sube

  if offy>4:
    sube=0
  if offy<1:
   sube=1

  if sube!=0:
    offy+=1
  if sube==0:
    offy-=1

  return offy

#####MAIN################################################################

buffer = numpy.zeros( (MODULOSV*4, MODULOSH), dtype=numpy.uint8 )
cartel = numpy.zeros( (MODULOSV*4, MODULOSH), dtype=numpy.uint8 )
encender = numpy.ones( (MODULOSV*4, MODULOSH), dtype=numpy.uint8 )
apagar = numpy.zeros( (MODULOSV*4, MODULOSH), dtype=numpy.uint8 )

#Encendido
#serialled(encender)
#serialled(encender)
#time.sleep(5)

#Efectoflechitas
#llenamatriz(buffer,0x41,0x22,0x14,0x08)
#for lop in range (0,MODULOSH*ANCHOM):
#    serialled(cartel)
#    arotamatriz(buffer,cartel)
#    printbin(cartel)
#serialled(apagar)
#serialled(apagar)

texto="UNLAM 2012 - TALLER DE ELECTRONICA - LACIE - EXPOPROYECTO - ROBOLUCHA 2012 #?![]{}+\/<>@678 1234 "
texto2="1 2 3 4 5 6 7 8 9 0"

#printfont(buffer,ord('H'))
#printbin(buffer)
#rotamatriz_izq(buffer,43)
#printbin(buffer)

ON_TIME=0.5
OFF_TIME=0.2
PARPADEOS=5





offsety=cambia_offset()
#print "testint"
#ser.write("zv\r")
#time.sleep(10)
#print "testcont"
for tiempo in range (10):


  for cnt in range(0,len(texto)):
    printfont(buffer,ord(texto[cnt]),offsety,0)
    if  texto[cnt]==' ':
       offsety=cambia_offset()

    for t in range (6):
      arotamatriz_izq(buffer,cartel,1)
      #printbin(cartel)
      serialled(cartel)


for i in ['FFFF', '00FF', 'AA55', '55AA', 'F0F0', 'FF00']:
    for j in range(PARPADEOS):
        for n in range(MODULOSH*2):
            ser.write("zg0000\r")
            ser.write("zh0000\r")
            ser.write("zi0000\r")
            # ser.write("zj0000\r")
            ser.write("zs\r")
            time.sleep(TIMEZS)
        ser.write("zm\r")
        time.sleep(OFF_TIME)

        for n in range(MODULOSH*2):
            ser.write("zg%s\r" % i.rjust(4, '0'))
            ser.write("zh%s\r" % i.rjust(4, '0'))
            ser.write("zi%s\r" % i)
            # ser.write("zj%s\r" % i)
            ser.write("zs\r")
            time.sleep(TIMEZS)
        ser.write("zm\r")
        time.sleep(ON_TIME)

#for t in range (MODULOSH*ANCHOM):
#  rotamatriz_izq(cartel,1)
#  printbin(cartel)

#printbin(cartel)
#printbin(buffer)

#printfont(apagar,ord('H'))
#printbin (apagar)
#rotamatriz_izq(apagar)
#rotamatriz_izq(apagar)
#printbin (apagar)

ser.write("zv\r")
ser.close()




