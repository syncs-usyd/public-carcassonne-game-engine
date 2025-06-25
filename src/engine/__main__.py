from signal import SIGTERM, signal
import sys

from engine.game_engine import GameEngine


def main():
    engine = GameEngine()

    def kill_handler(a, b):
        # TODO
        assert False
        sys.exit()

    signal(SIGTERM, kill_handler)

    engine.run()


if __name__ == "__main__":
    main()
