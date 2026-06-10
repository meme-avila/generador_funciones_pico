import machine
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

print("Generando Onda Diente de Sierra... Presiona Stop en Thonny para detener.")

escalon = 0
paso = 50 # Que tan rapido sube la rampa

try:
    while True:
        enviar_dac(escalon)
        escalon += paso
        if escalon > 4095:
            escalon = 0 # Caida abrupta al llegar al maximo
            
except KeyboardInterrupt:
    print("Prueba detenida. Apagando DAC.")
    enviar_dac(0)