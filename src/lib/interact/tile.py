from lib.interact.structure import StructureType
from enum import Enum, auto


# class NodeType(Enum):
#     CENTER = auto()
#     TOP_LEFT = auto()
#     TOP = auto()
#     TOP_RIGHT = auto()
#     RIGHT = auto()
#     BOTTOM_RIGHT = auto()
#     BOTTOM = auto()
#     BOTTOM_LEFT = auto()
#     LEFT = auto()
#
#
# class Node:
#     def __init__(self, tile: "Tile", type: NodeType) -> None:
#         self.parent_tile = tile
#         self.parent_node = self
#         self.type = type
#         self.edges: list[Node] = []


class TileModifier(Enum):
    MONESTERY = auto()
    SHIELD = auto()


class Tile:
    center: StructureType

    def __init__(
        self,
        left: StructureType,
        right: StructureType,
        top: StructureType,
        bottom: StructureType,
        modifiers: list[TileModifier] = list(),
    ) -> None:
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom

        self.roation = 0

        self.modifier = modifiers

    def rotate_clockwise(self, number: int) -> None:
        for _ in range(number):
            self.right, self.bottom, self.left, self.top = (
                self.top,
                self.right,
                self.bottom,
                self.left,
            )

    @staticmethod
    def get_starting_tile() -> "Tile":
        return Tile(
            left=StructureType.GRASS,
            right=StructureType.GRASS,
            top=StructureType.RIVER,
            bottom=StructureType.GRASS,
        )


def create_all_tiles() -> dict[int, Tile]:
    tiles = []

    def create_river_tiles():
        pass

    def create_regular_tiles():
        pass

    def create_expansion_tiles():
        pass

    return dict(tiles)
