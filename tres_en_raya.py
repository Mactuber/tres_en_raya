import PySimpleGUI as sg

# Juego de 3 en raya para 2 jugadores con interfaz gráfica.

# Constantes
BUTTON_SIZE = (7, 3)
PLAYER_ONE = "X"
PLAYER_TWO = "O"
WINNER_PLAYS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
]

# Funciones de lógica
def create_layout():
    board_layout = [
        [sg.Button("", key=f"-{i}-", size=BUTTON_SIZE) for i in range(j, j+3)]
        for j in range(0, 9, 3)
    ]
    return board_layout + [
        [sg.Text("", key="-WINNER-")],
        [sg.Button("Reiniciar", key="-RESET-"), sg.Button("Salir", key="-EXIT-")]
    ]

def check_winner(deck):
    for play in WINNER_PLAYS:
        a, b, c = play
        if deck[a] == deck[b] == deck[c] != 0:
            return deck[a]
    return None

def is_draw(deck):
    return all(cell != 0 for cell in deck)

def switch_player(current):
    return PLAYER_TWO if current == PLAYER_ONE else PLAYER_ONE

def reset_game(window):
    for i in range(9):
        window[f"-{i}-"].update("")
    window["-WINNER-"].update("")
    return [0]*9, PLAYER_ONE, False

# Inicialización
deck = [0] * 9
current_player = PLAYER_ONE
game_end = False

window = sg.Window("3 en Raya", create_layout())

# Bucle principal
while True:
    event, values = window.read()

    if event in (sg.WINDOW_CLOSED, "-EXIT-"):
        break

    if event == "-RESET-":
        deck, current_player, game_end = reset_game(window)
        continue

    if event.startswith("-") and event.endswith("-") and not game_end:
        index = int(event.strip("-"))
        if deck[index] == 0:
            deck[index] = current_player
            window[event].update(current_player)

            winner = check_winner(deck)
            if winner:
                sg.popup(f"¡Jugador '{winner}' ha ganado!")
                window["-WINNER-"].update(f"Ganador: {winner}")
                game_end = True
            elif is_draw(deck):
                sg.popup("¡Empate!")
                window["-WINNER-"].update("Empate")
                game_end = True
            else:
                current_player = switch_player(current_player)

window.close()
