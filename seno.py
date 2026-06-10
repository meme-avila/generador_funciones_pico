import machine
import math
import time

# Configuracion SPI y Chip Select
spi = machine.SPI(0, baudrate=10000000, polarity=0, phase=0, sck=machine.Pin(18), mosi=machine.Pin(19))
cs = machine.Pin(16, machine.Pin.OUT)
cs.value(1)

def enviar_dac(valor):
    valor = valor & 0x0FFF
    comando = 0x3000 | valor
    cs.value(0)
    spi.write(bytearray([(comando >> 8) & 0xFF, comando & 0xFF]))
    cs.value(1)

# Pre-calcular 100 puntos de la onda senoidal
puntos_seno = []
for i in range(100):
    valor = int(2047 + 2047 * math.sin(2 * math.pi * i / 100))
    puntos_seno.append(valor)

print("Generando Onda Senoidal... Presiona Stop en Thonny para detener.")

indice = 0
try:
    while True:
        enviar_dac(puntos_seno[indice])
        indice = (indice + 1) % 100
        time.sleep_us(500) # Micro-pausa para ajustar la frecuencia visual

except KeyboardInterrupt:
    print("Prueba detenida. Apagando DAC.")
    enviar_dac(0)