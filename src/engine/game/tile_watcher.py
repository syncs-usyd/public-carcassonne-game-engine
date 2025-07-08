from lib.interact.tile import Tile

from abc import ABC, abstractmethod
from typing import final


class TileSubsciber(ABC):
    """
    TileSubsciber
    _For special meeple claim rules. This does impy that the tile must have a meeple for a subsciber to be created_
    """

    @abstractmethod
    def on_tile_changed(self, tile: "Tile", position: tuple[int, int]) -> None:
        pass

    def register_to(self, publisher: "TilePublisherBus") -> None:
        for pos in self._watching():
            publisher.register(pos, self)

    @abstractmethod
    def _watching(self) -> list[tuple[int, int]]:
        pass


class MonataryNeighbourSubsciber(TileSubsciber):
    def __init__(self, center: tuple[int, int]) -> None:
        self.center = center
        self.filled = set()
        self.registered = False
        super().__init__()

    @final
    def on_tile_changed(self, tile: "Tile", position: tuple[int, int]):
        pass

    @final
    def _watching(self) -> list[tuple[int, int]]:
        x, y = self.center

        # May be out of range, but this is okay as Publisher will never notify
        return [
            (x + i, y + j)
            for i in range(-1, 2)
            for j in range(-1, 2)
            if not (i == j == 0)
        ]


class TilePublisherBus:
    _singleton: "TilePublisherBus | None" = None

    def __init__(self):
        self.watchers: dict[tuple[int, int], list[TileSubsciber]] = {}

    def __new__(cls) -> "TilePublisherBus":
        if cls._singleton is None:
            cls._singleton = super().__new__(cls)

        return cls._singleton

    def register(self, position: tuple[int, int], watcher: TileSubsciber):
        self.watchers.setdefault(position, []).append(watcher)

    def check_notify(self, tile: "Tile", position: tuple[int, int]):
        for watcher in self.watchers.get(position, []):
            watcher.on_tile_changed(tile, position)
