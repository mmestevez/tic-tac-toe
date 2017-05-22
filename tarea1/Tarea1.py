from tarea1 import game_file

if __name__ == '__main__':
    GAME_SESSION = game_file.Game()
    GAME_PRINTER = game_file.GamePrinter()
    INPUT_READER = game_file.InputReader()
    GAME_SESSION.run(GAME_PRINTER, INPUT_READER)
