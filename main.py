from keyboard import is_pressed, press, release, write
from time import sleep
#Creado por 2b2 :3
####################################
tecla_activacion = "ctrl"
segunda_tecla_activacion = "'"

# Mapeo de caracteres a reemplazar
replacement_map = {
    "a": "ǎ",
    "o": "ǒ",
    "e": "ě",
    "i": "ǐ",
    "u": "ǔ",
    "ü": "ǚ"
}

ctrl_held = False
awaiting_letter = False
is_comma_pressed = False
####################################

def detect_ctrl_and_comma():
    global ctrl_held, awaiting_letter, is_comma_pressed

    # Detecta si Ctrl está presionado
    if is_pressed(tecla_activacion):
        if not ctrl_held:
            ctrl_held = True
            #print("[DEBUG] Ctrl presionado")

    # Detecta si se presiona la comilla simple después de Ctrl
    if is_pressed(segunda_tecla_activacion) and ctrl_held and not is_comma_pressed:
        is_comma_pressed = True
        #print("[DEBUG] Comilla simple detectada después de Ctrl")
    
    # Si ambas teclas están presionadas al mismo tiempo
    if is_pressed(tecla_activacion) and is_pressed(segunda_tecla_activacion):
        awaiting_letter = True
        #print("[DEBUG] Ambas teclas presionadas simultáneamente")

    # Si estamos esperando una letra después de Ctrl + '
    if awaiting_letter:
        # Detectar la tecla presionada
        for char in "abcdefghijklmnopqrstuvwxyz":
            if is_pressed(char):
                #print(f"[DEBUG] Tecla presionada después de Ctrl + ': {char}")

                if char in replacement_map:
                    #print(f"[DEBUG] Reemplazando {char} con {replacement_map[char]}")
                    
                    # Borrar los dos últimos caracteres antes de escribir la nueva letra
                    for _ in range(1):
                        press('backspace')
                        release('backspace')
                    
                    # Escribir la letra con el diacrítico
                    write(replacement_map[char])
                else:
                    #print("[DEBUG] Tecla no está en el mapeo, no se reemplaza nada")
                    pass
                
                awaiting_letter = False  # Reiniciar estado
                ctrl_held = False  # Liberar Ctrl
                break

    # Detecta cuando se libera la comilla simple para poder usarla nuevamente
    if not is_pressed("'") and is_comma_pressed:
        is_comma_pressed = False  # Resetear flag cuando la comilla se ha soltado

def main():
    #print("[DEBUG] Escuchando teclado...")

    while True:
        detect_ctrl_and_comma()
        sleep(0.01)  # Pausar ligeramente para reducir uso de CPU

if __name__ == "__main__":
    main()
