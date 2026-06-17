import rp2
import math
from machine import Pin

# ==========================================
# 1. EL MÚSCULO (Tubería PIO Simple y Universal)
# ==========================================
# Este hardware no cambia NUNCA, sin importar la onda.
@rp2.asm_pio(out_init=(rp2.PIO.OUT_LOW,) * 8, out_shiftdir=rp2.PIO.SHIFT_RIGHT)
def dac_r2r():
    wrap_target()
    pull()          # Espera el dato
    out(pins, 8)    # Dispara a los pines
    wrap()

# ==========================================
# 2. EL CEREBRO (Pre-cálculo de Matemáticas)
# ==========================================
N = 100 # Resolucion: 100 puntos por ciclo

tabla_seno = []
tabla_sierra = []
tabla_cuadrada = []

print("Calculando geometría de las ondas...")

for i in range(N):
    # 1. Matemática de la Onda Seno
    val_seno = int(127.5 + 127.5 * math.sin(2 * math.pi * i / N))
    tabla_seno.append(val_seno)
    
    # 2. Matemática del Diente de Sierra (Proporción lineal)
    val_sierra = int((i / (N - 1)) * 255)
    tabla_sierra.append(val_sierra)
    
    # 3. Matemática de la Onda Cuadrada (Mitad 255, Mitad 0)
    if i < (N / 2):
        tabla_cuadrada.append(255)
    else:
        tabla_cuadrada.append(0)

# ==========================================
# 3. EJECUCIÓN (Hardware + Software)
# ==========================================
# Frecuencia de envío: 100 kHz. 
# Como N=100, la frecuencia final de TODAS las ondas será 1 kHz.
sm = rp2.StateMachine(0, dac_r2r, freq=30000000, out_base=Pin(0))
sm.active(1)

print("¡Hardware activo! Transmitiendo señal al DAC...")

try:
    while True:
        # CAMBIA LA VARIABLE AQUÍ PARA PROBAR EN TU OSCILOSCOPIO
        # Opciones: tabla_seno, tabla_sierra, tabla_cuadrada
        
        onda_actual = tabla_seno   # <--- ¡Cambia esto!
        
        for valor in onda_actual:
            sm.put(valor) 
            
except KeyboardInterrupt:
    sm.put(0)
    print("Generador detenido.")