from lib.interact.structure import StructureType

from enum import Enum, auto
from copy import copy


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
    RIVER = auto()
    MONESTERY = auto()
    SHIELD = auto()


class Tile:
    left_tile: "Tile"
    right_tile: "Tile"
    top_tile: "Tile"
    bottom_tile: "Tile"

    def __init__(
        self,
        left_edge: StructureType,
        right_edge: StructureType,
        top_edge: StructureType,
        bottom_edge: StructureType,
        modifiers: list[TileModifier] = list(),
    ) -> None:
        self.left_edge = left_edge
        self.right_edge = right_edge
        self.top_edge = top_edge
        self.bottom_edge = bottom_edge

        self.roation = 0

        self.modifier = modifiers

    def rotate_clockwise(self, number: int) -> None:
        for _ in range(number):
            self.right_edge, self.bottom_edge, self.left_edge, self.top_edge = (
                self.top_edge,
                self.right_edge,
                self.bottom_edge,
                self.left_edge,
            )

    @staticmethod
    def get_starting_tile() -> "Tile":
        return Tile(
            left_edge=StructureType.GRASS,
            right_edge=StructureType.GRASS,
            top_edge=StructureType.RIVER,
            bottom_edge=StructureType.GRASS,
            modifiers=[TileModifier.RIVER]
        )

    def clone_add(self, n: int) -> list["Tile"]:
        cloned_tiles = [copy(self) for i in range n]
        cloned_tiles.append(self)
        return cloned_tiles


def create_river_tiles():
    pass

def create_regular_tiles():
    tiles = []

    # Tile Type A
    tiles.extend(Tile(
        left_edge=StructureType.GRASS, 
        right_edge=StructureType.GRASS, 
        top_edge=StructureType.GRASS, 
        bottom_edge=StructureType.ROAD_START).clone_add(2))

    # Tile Type B
    tiles.extend(Tile(
        left_edge=StructureType.GRASS, 
        right_edge=StructureType.GRASS, 
        top_edge=StructureType.GRASS, 
        bottom_edge=StructureType.GRASS,
        modifiers=[TileModifier.MONESTERY]).clone_add(4))

    # Tile Type C
    tiles.extend(Tile(
        left_edge=StructureType.CITY, 
        right_edge=StructureType.CITY, 
        top_edge=StructureType.CITY, 
        bottom_edge=StructureType.CITY,
        modifiers=[TileModifier.SHIELD]).clone_add(1))

    # Tile Type D
    tiles.extend(Tile(
        left_edge=StructureType.GRASS, 
        right_edge=StructureType.CITY, 
        top_edge=StructureType.ROAD, 
        bottom_edge=StructureType.ROAD).clone_add(1))

    # Tile Type E
    tiles.extend(Tile(
        left_edge=StructureType.GRASS, 
        right_edge=StructureType.GRASS, 
        top_edge=StructureType.CITY, 
        bottom_edge=StructureType.GRASS).clone_add(5))

    # Tile Type F
    tiles.extend(Tile(
        left_edge=StructureType.CITY, 
        right_edge=StructureType.CITY, 
        top_edge=StructureType.GRASS, 
        bottom_edge=StructureType.GRASS,
        modifiers=[TileModifier.SHIELD]).clone_add(2))

    # Tile Type G
    tiles.extend(Tile(
        left_edge=StructureType.GRASS, 
        right_edge=StructureType.GRASS, 
        top_edge=StructureType.CITY, 
        bottom_edge=StructureType.CITY).clone_add(2))

    # Tile Type H
    tiles.extend(Tile(
        left_edge=StructureType.GRASS, 
        right_edge=StructureType.GRASS, 
        top_edge=StructureType.CITY, 
        bottom_edge=StructureType.CITY).clone_add(3))

def create_expansion_tiles():
    pass
