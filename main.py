from keyboard import is_pressed, press, release, write
from time import sleep, time

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
    "u": "ǔ",
    "ü": "ǚ"
}

# Mapeo de caracteres para macron (¯)
replacement_map_macron = {
    "a": "ā",
    "o": "ō",
    "e": "ē",
    "i": "ī",
    "u": "ū",
    "ü": "ǖ"
}

ctrl_held = False
awaiting_letter = False
accent_type = None
time_of_first_key = 0  # Para calcular el tiempo entre teclas
###############################


def detect_ctrl_and_accent():
    global ctrl_held, awaiting_letter, accent_type, time_of_first_key

    # Detecta si Ctrl está presionado
    if is_pressed(tecla_activacion):
        if not ctrl_held:
            ctrl_held = True
            time_of_first_key = time()  # Guardar el tiempo de activación

    # Detecta si la segunda tecla fue presionada dentro del intervalo permitido
    if ctrl_held and not awaiting_letter:
        if is_pressed(segunda_tecla_activacion_caron):
            if time() - time_of_first_key <= 2:
                accent_type = "caron"
                awaiting_letter = True

        elif is_pressed(segunda_tecla_activacion_macron):
            if time() - time_of_first_key <= 2:
                accent_type = "macron"
                awaiting_letter = True

    # Si pasaron más de 2 segundos, cancelar la espera
    if awaiting_letter and (time() - time_of_first_key > 2):
        awaiting_letter = False
        ctrl_held = False
        accent_type = None

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
                break


def main():
    while True:
        detect_ctrl_and_accent()
        sleep(0.01)  # Pequeña pausa para reducir uso de CPU


if __name__ == "__main__":
    main()
