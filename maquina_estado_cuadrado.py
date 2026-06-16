import rp2
from machine import Pin

# ==========================================
# 1. LA MÁQUINA DE ESTADOS PIO (El Músculo)
# ==========================================
@rp2.asm_pio(out_init=(rp2.PIO.OUT_LOW,) * 8)
def r2r_cuadrada_maxima():
    wrap_target()
    # Ejecuta esto en exactamente 8 nanosegundos:
    mov(pins, invert(null))  # Manda 3.3V (255) a los 8 pines
    
    # Ejecuta esto en exactamente otros 8 nanosegundos:
    mov(pins, null)          # Manda 0V (0) a los 8 pines
    wrap()

# ==========================================
# 2. EL NÚMERO EN LA VARIABLE (Frecuencia)
# ==========================================
# Aquí pones exactamente 125000000 (El reloj base de fábrica)
freq=12500
sm = rp2.StateMachine(0, r2r_cuadrada_maxima, freq, out_base=Pin(0))

print("¡Desencadenando el hardware PIO!")
print("Frecuencia esperada: ", freq)

#  Activo
sm.active(1)

# El programa termina aquí, pero la Pico W seguirá generando la onda 
# infinitamente por hardware puro.