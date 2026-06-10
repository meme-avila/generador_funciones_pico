import machine
import math
import time

# Configuracion SPI y Chip Select
spi = machine.SPI(0, baudrate=10000000, polarity=0, phase=0, sck=machine.Pin(18), mosi=machine.Pin(19))
cs = machine.Pin(16, machine.Pin.OUT)
cs.value(1)

def enviar_dac(valor):
    valor = int(valor) & 0x0FFF
    comando = 0x3000 | valor
    cs.value(0)
    spi.write(bytearray([(comando >> 8) & 0xFF, comando & 0xFF]))
    cs.value(1)

# --- CONSTRUCTOR DE ONDA ARBITRARIA (ECG) ---
puntos_ecg = []
linea_base = 1000 # Voltaje de reposo

for i in range(100):
    val = linea_base
    
    # Onda P (Auriculas)
    if 10 <= i < 20:
        val = linea_base + 300 * math.sin(math.pi * (i - 10) / 10)
        
    # Complejo QRS (Ventriculos)
    elif 30 <= i < 35: # Onda Q (pequena caida)
        val = linea_base - 200 * math.sin(math.pi * (i - 30) / 5)
    elif 35 <= i < 40: # Onda R (El pico principal altisimo)
        val = linea_base + 2500 * math.sin(math.pi * (i - 35) / 5)
    elif 40 <= i < 45: # Onda S (Caida profunda)
        val = linea_base - 400 * math.sin(math.pi * (i - 40) / 5)
        
    # Onda T (Recuperacion)
    elif 60 <= i < 75:
        val = linea_base + 500 * math.sin(math.pi * (i - 60) / 15)
        
    puntos_ecg.append(val)

print("Generando senal de Electrocardiograma (ECG)...")

indice = 0
try:
    while True:
        enviar_dac(puntos_ecg[indice])
        indice = (indice + 1) % 100
        # Una pausa de 8ms por punto da aprox 800ms por latido (75 latidos por minuto)
        time.sleep_ms(8) 

except KeyboardInterrupt:
    print("Prueba detenida. Apagando DAC.")
    enviar_dac(0)