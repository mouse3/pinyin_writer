from keyboard import is_pressed, press, release, write
from time import sleep

###############################
# Teclas de activación
tecla_activacion = "ctrl"
segunda_tecla_activacion_caron = "`"
segunda_tecla_activacion_macron = "´"

# Mapeo de caracteres para caron (ˇ)
replacement_map_caron = {
    "a": "ǎ",
    "o": "ǒ",
    "e": "ě",
    "i": "ǐ",
    "u": "ǔ"
}

# Mapeo de caracteres para macron (¯)
replacement_map_macron = {
    "a": "ā",
    "o": "ō",
    "e": "ē",
    "i": "ī",
    "u": "ū"
}

ctrl_held = False
awaiting_letter = False
accent_type = None  # 'caron' o 'macron'
###############################


def detect_ctrl_and_accent():
    global ctrl_held, awaiting_letter, accent_type

    # Detecta si Ctrl está presionado
    if is_pressed(tecla_activacion):
        ctrl_held = True

    # Detecta si se presionó el acento y asigna el tipo correcto
    if ctrl_held:
        if is_pressed(segunda_tecla_activacion_caron) and accent_type is None:
            accent_type = "caron"
            awaiting_letter = True
            sleep(0.1)  # Evita detectar múltiples pulsaciones seguidas

        if is_pressed(segunda_tecla_activacion_macron) and accent_type is None:
            accent_type = "macron"
            awaiting_letter = True
            sleep(0.1)

    # Si estamos esperando una letra después de Ctrl + acento
    if awaiting_letter:
        for char in "abcdefghijklmnopqrstuvwxyz":
            if is_pressed(char):
                replacement_map = replacement_map_caron if accent_type == "caron" else replacement_map_macron
                
                if char in replacement_map:
                    press('backspace')
                    release('backspace')
                    write(replacement_map[char])

                # Reiniciar estados después de escribir la letra
                awaiting_letter = False
                ctrl_held = False
                accent_type = None
                return
        
        # Si se presiona una tecla que no es una vocal válida, cancelar el estado de espera
        if any(is_pressed(key) for key in "1234567890-=[];',./\\"):
            awaiting_letter = False
            ctrl_held = False
            accent_type = None


def main():
    while True:
        detect_ctrl_and_accent()
        sleep(0.01)  # Pequeña pausa para reducir uso de CPU

if __name__ == "__main__":
    main()
