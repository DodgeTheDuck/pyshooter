from game_state import GameState
from map_editor_state import MapEditorState
import engine

EXIT_SUCCESS = 0


def main():
    engine.init()
    engine.push_state(GameState())
    engine.run()
    return EXIT_SUCCESS


if __name__ == '__main__':
    main()
