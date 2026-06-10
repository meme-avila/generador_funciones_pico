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

print("Generando Onda Cuadrada... Presiona Stop en Thonny para detener.")

estado = 0
try:
    while True:
        if estado == 0:
            enviar_dac(4095) # Nivel alto (Aprox 2.048V)
            estado = 1
        else:
            enviar_dac(0)    # Nivel bajo (0V)
            estado = 0
        time.sleep_ms(10)    # Pausa para que el osciloscopio la detecte bien

except KeyboardInterrupt:
    print("Prueba detenida. Apagando DAC.")
    enviar_dac(0)