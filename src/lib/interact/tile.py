from lib.interact.structure import StructureType

from enum import Enum, auto
from copy import copy

from typing import final, Self


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
    """
    TileModifier
    Desc: _A multi-strategy based deisgn modifier for tile_
    Motivated by two reasons
        - My Laziness
        - To allow for larger flexibility of bot algorithms
    """

    RIVER = auto()
    MONESTERY = auto()
    SHIELD = auto()
    BROKEN_ROAD_CENTER = auto()


class Tile:
    """
    Tile
    Desc: _Stores all Tile Info by internal edges (Structures) and external connections_
    """

    left_tile: "Tile"
    right_tile: "Tile"
    top_tile: "Tile"
    bottom_tile: "Tile"

    # Allows for connected componentes for structures within a tile
    # For example: differenctiates between a three edge city and three distinct cities as edges
    structure_edges: list["StructureType"]

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
            modifiers=[TileModifier.RIVER],
        )

    @final
    def clone_add(self, n: int) -> list[Self]:
        cloned_tiles = [copy(self) for i in range(n)]
        cloned_tiles.append(self)
        return cloned_tiles


def create_river_tiles():
    pass


def create_regular_tiles():
    tiles: list["Tile"] = []

    # Tile Type A
    tiles.extend(
        Tile(
            left_edge=StructureType.GRASS,
            right_edge=StructureType.GRASS,
            top_edge=StructureType.GRASS,
            bottom_edge=StructureType.ROAD_START,
        ).clone_add(2)
    )

    # Tile Type B
    tiles.extend(
        Tile(
            left_edge=StructureType.GRASS,
            right_edge=StructureType.GRASS,
            top_edge=StructureType.GRASS,
            bottom_edge=StructureType.GRASS,
            modifiers=[TileModifier.MONESTERY],
        ).clone_add(4)
    )

    # Tile Type C
    tiles.extend(
        Tile(
            left_edge=StructureType.CITY,
            right_edge=StructureType.CITY,
            top_edge=StructureType.CITY,
            bottom_edge=StructureType.CITY,
            modifiers=[TileModifier.SHIELD],
        ).clone_add(1)
    )

    # Tile Type D
    tiles.extend(
        Tile(
            left_edge=StructureType.GRASS,
            right_edge=StructureType.CITY,
            top_edge=StructureType.ROAD,
            bottom_edge=StructureType.ROAD,
        ).clone_add(1)
    )

    # Tile Type E
    tiles.extend(
        Tile(
            left_edge=StructureType.GRASS,
            right_edge=StructureType.GRASS,
            top_edge=StructureType.CITY,
            bottom_edge=StructureType.GRASS,
        ).clone_add(5)
    )

    # Tile Type F
    tiles.extend(
        Tile(
            left_edge=StructureType.CITY,
            right_edge=StructureType.CITY,
            top_edge=StructureType.GRASS,
            bottom_edge=StructureType.GRASS,
            modifiers=[TileModifier.SHIELD],
        ).clone_add(2)
    )

    # Tile Type G
    tiles.extend(
        Tile(
            left_edge=StructureType.GRASS,
            right_edge=StructureType.GRASS,
            top_edge=StructureType.CITY,
            bottom_edge=StructureType.CITY,
        ).clone_add(2)
    )

    # Tile Type H
    tiles.extend(
        Tile(
            left_edge=StructureType.CITY,
            right_edge=StructureType.CITY,
            top_edge=StructureType.GRASS,
            bottom_edge=StructureType.GRASS,
        ).clone_add(3)
    )

    # Tile Type I
    tiles.extend(
        Tile(
            left_edge=StructureType.GRASS,
            right_edge=StructureType.CITY,
            top_edge=StructureType.GRASS,
            bottom_edge=StructureType.CITY,
        ).clone_add(2)
    )

    # Tile Type J
    tiles.extend(
        Tile(
            left_edge=StructureType.GRASS,
            right_edge=StructureType.ROAD,
            top_edge=StructureType.CITY,
            bottom_edge=StructureType.ROAD,
        ).clone_add(3)
    )

    # Tile Type K
    tiles.extend(
        Tile(
            left_edge=StructureType.ROAD,
            right_edge=StructureType.CITY,
            top_edge=StructureType.ROAD,
            bottom_edge=StructureType.GRASS,
        ).clone_add(3)
    )

    # Tile Type L
    tiles.extend(
        Tile(
            left_edge=StructureType.ROAD_START,
            right_edge=StructureType.CITY,
            top_edge=StructureType.ROAD_START,
            bottom_edge=StructureType.ROAD_START,
        ).clone_add(3)
    )

    # Tile Type M
    tiles.extend(
        Tile(
            left_edge=StructureType.CITY,
            right_edge=StructureType.GRASS,
            top_edge=StructureType.CITY,
            bottom_edge=StructureType.GRASS,
            modifiers=[TileModifier.SHIELD],
        ).clone_add(2)
    )

    # Tile Type N
    tiles.extend(
        Tile(
            left_edge=StructureType.CITY,
            right_edge=StructureType.GRASS,
            top_edge=StructureType.CITY,
            bottom_edge=StructureType.GRASS,
        ).clone_add(3)
    )

    # Tile Type O
    tiles.extend(
        Tile(
            left_edge=StructureType.CITY,
            right_edge=StructureType.ROAD,
            top_edge=StructureType.CITY,
            bottom_edge=StructureType.ROAD,
            modifiers=[TileModifier.SHIELD],
        ).clone_add(2)
    )

    # Tile Type P
    tiles.extend(
        Tile(
            left_edge=StructureType.CITY,
            right_edge=StructureType.ROAD,
            top_edge=StructureType.CITY,
            bottom_edge=StructureType.ROAD,
        ).clone_add(3)
    )

    # Tile Type Q
    tiles.extend(
        Tile(
            left_edge=StructureType.CITY,
            right_edge=StructureType.CITY,
            top_edge=StructureType.CITY,
            bottom_edge=StructureType.GRASS,
            modifiers=[TileModifier.SHIELD],
        ).clone_add(1)
    )

    # Tile Type R
    tiles.extend(
        Tile(
            left_edge=StructureType.CITY,
            right_edge=StructureType.CITY,
            top_edge=StructureType.CITY,
            bottom_edge=StructureType.GRASS,
        ).clone_add(3)
    )

    # Tile Type S
    tiles.extend(
        Tile(
            left_edge=StructureType.CITY,
            right_edge=StructureType.CITY,
            top_edge=StructureType.CITY,
            bottom_edge=StructureType.ROAD,
            modifiers=[TileModifier.SHIELD],
        ).clone_add(2)
    )

    # Tile Type T
    tiles.extend(
        Tile(
            left_edge=StructureType.CITY,
            right_edge=StructureType.CITY,
            top_edge=StructureType.CITY,
            bottom_edge=StructureType.ROAD,
        ).clone_add(1)
    )

    # Tile Type U
    tiles.extend(
        Tile(
            left_edge=StructureType.GRASS,
            right_edge=StructureType.GRASS,
            top_edge=StructureType.ROAD,
            bottom_edge=StructureType.ROAD,
        ).clone_add(8)
    )

    # Tile Type V
    tiles.extend(
        Tile(
            left_edge=StructureType.ROAD,
            right_edge=StructureType.GRASS,
            top_edge=StructureType.GRASS,
            bottom_edge=StructureType.ROAD,
        ).clone_add(9)
    )

    # Tile Type W
    tiles.extend(
        Tile(
            left_edge=StructureType.ROAD_START,
            right_edge=StructureType.ROAD_START,
            top_edge=StructureType.GRASS,
            bottom_edge=StructureType.ROAD_START,
            modifiers=[TileModifier.BROKEN_ROAD_CENTER],
        ).clone_add(4)
    )

    # Tile Type X
    tiles.extend(
        Tile(
            left_edge=StructureType.ROAD_START,
            right_edge=StructureType.ROAD_START,
            top_edge=StructureType.ROAD_START,
            bottom_edge=StructureType.ROAD_START,
            modifiers=[TileModifier.BROKEN_ROAD_CENTER],
        ).clone_add(1)
    )


def create_expansion_tiles():
    pass
