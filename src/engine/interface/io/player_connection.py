from engine.config.io_config import CORE_DIRECTORY, PIPE_DELIM


class InvalidMoveError(ValueError):
    def __init__(self, message: str, move: None):
        super().__init__(message)
        self.invalid_move = move


class PlayerConnection:
    def __init__(self, player_id: int) -> None:
        self.player_id = player_id
        self.from_pipe = None
        self.to_pipe = None

        self.cummalative_time = 0
        self._init_pipes()

    def _init_pipes(self) -> None:
        self._to_engine_pipe = open(f"{CORE_DIRECTORY}/submission{self.player_id}/io/to_engine.pipe", "r")
        self._from_engine_pipe = open(f"{CORE_DIRECTORY}/submission{self.player_id}/io/from_engine.pipe", "w")

    def query_move(self) -> None:
        pass

    def _send(self, data: str) -> None:
        self._from_engine_pipe.write(str(len(data)) + PIPE_DELIM)
        self._from_engine_pipe.write(data)
        self._from_engine_pipe.flush()


    def _recieve(self) -> None:

