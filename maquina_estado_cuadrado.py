import rp2
#from machine import Pin: Es la libreria clasica de MicroPython para manipular los pines fisicos (entradas y salidas) de la tarjeta.
from machine import Pin
#import rp2: Esta es la llave maestra. rp2 es una libreria exclusiva que solo existe para el chip RP2040.
#Es la que te da acceso directo a las entrañas de silicio de los coprocesadores PIO (Programmable I/O).
#Sin ella, la Pico W es un microcontrolador comun y corriente.
# ==========================================
# 1. LA MÁQUINA DE ESTADOS PIO (El Músculo)
# ==========================================
@rp2.asm_pio(out_init=(rp2.PIO.OUT_LOW,) * 8)
#@rp2.asm_pio(...): Esto es un decorador. Le avisa al cerebro principal de Python:
#"Oye, la función que sigue aquí abajo no me la traduzcas como código normal, traducela a micro-ensamblador e inyectala directamente en el hardware PIO"
#out_init=(rp2.PIO.OUT_LOW,) * 8: Antes de arrancar, el hardware necesita saber en que estado inicial deben estar los pines. Aquí le decimos explicitamente que configure 8
#pines y los ponga todos en estado LOW (0V). El * 8 es un truco de Python para no tener que escribir OUT_LOW ocho veces seguidas.
def r2r_cuadrada_maxima():
    wrap_target()
    # Ejecuta esto en exactamente 8 nanosegundos:
    mov(pins, invert(null))  # Manda 3.3V (255) a los 8 pines
    #null: Es un registro fisico interno que esta cableado a tierra; su valor siempre es permanentemente 00000000 (en binario).
    #invert(null): Invierte esos ceros por unos, convirtiéndolo instantáneamente en 11111111 (que es 255 en decimal).
    #mov(pins, ...): La instruccion "Mover". Toma esos 8 unos y los estrella directamente contra los pines de salida. Como los 8 pines
    #tienen un 1 logico, tu escalera R2R recibe 3.3V en todas sus entradas al mismo tiempo. Esto toma exactamente 1 ciclo de reloj (8ns).
    # Ejecuta esto en exactamente otros 8 nanosegundos:
    mov(pins, null)          # Manda 0V (0) a los 8 pines
    #wrap(): Es la pareja de wrap_target(). Le dice al hardware: "rebota de regreso arriba de forma automática y gratuita".
    #No cuesta ciclos de reloj. Asi, la onda completa (subir y bajar) tomo apenas 2 ciclos de reloj en total.
    wrap()

# ==========================================
# 2. EL NÚMERO EN LA VARIABLE (Frecuencia)
# ==========================================
# Aquí pones exactamente 125000000 (El reloj base de fábrica)
freq=12500
sm = rp2.StateMachine(0, r2r_cuadrada_maxima, freq, out_base=Pin(0))
#0: El chip RP2040 tiene 8 Maquinas de Estado fisicas (numeradas del 0 al 7). Aquí le decimos "quiero rentar la maquina numero 0 para este trabajo".
#r2r_cuadrada_maxima: Le entregamos el manual de instrucciones (la función que escribimos arriba).
#freq=125000000: Enchufamos la maquina directamente a la arteria principal del cristal oscilador de la placa (125\MHz). Le estamos quitando los frenos.
#out_base=Pin(0): Este parámetro es crítico para tu circuito R2R. El decorador de arriba sabía que iba a mover 8 pines, pero no sabia cuales. Al decirle que la base es el Pin(0), el hardware cuenta automaticamente 8 posiciones a partir de ahi: GPIO 0, 1, 2, 3, 4, 5, 6 y 7. ---


print("¡Desencadenando el hardware PIO!")
print("Frecuencia esperada: ", freq)

#  Activo
sm.active(1)
#active(1): Es el boton rojo de lanzamiento. En el instante exacto en que Python ejecuta esta linea, la Maquina de Estados 0 se independiza,
#toma control exclusivo de los pines GPIO 0 al 7, y empieza a ejecutar el bucle a 62.5MHz.
# El programa termina aqui, pero la Pico W seguirá generando la onda 
# infinitamente por hardware puro.