from lib.interact.structure import StructureType

from enum import Enum, auto
from copy import copy
from collections import namedtuple
from dotmap import DotMap

from typing import final, Self


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
    OPP_ROAD_BRIDGE = auto()
    OPP_CITY_BRIDGE = auto()


class Tile:
    """
    Tile
    Desc: _Stores all Tile Info by internal edges (Structures) and external connections_
    """

    InternalEdges = namedtuple(
        "InternalEdges", ["left_edge", "right_edge", "top_edge", "bottom_edge"]
    )

    def __init__(
        self,
        left_edge: StructureType,
        right_edge: StructureType,
        top_edge: StructureType,
        bottom_edge: StructureType,
        modifiers: list[TileModifier] = list(),
    ) -> None:
        self.internal_edges = DotMap(
            Tile.InternalEdges(
                left_edge=left_edge,
                right_edge=right_edge,
                top_edge=top_edge,
                bottom_edge=bottom_edge,
            )._asdict(),
            _dynamic=False,
        )

        self.internal_edge_claims = DotMap(
            Tile.InternalEdges(
                left_edge=None,
                right_edge=None,
                top_edge=None,
                bottom_edge=None,
            )._asdict(),
            _dynamic=False,
        )

        self.roation = 0
        self.modifier = modifiers

        self.left_tile: "Tile"
        self.right_tile: "Tile"
        self.top_tile: "Tile"
        self.bottom_tile: "Tile"

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


def create_river_tiles() -> list["Tile"]:
    """
    RiverTiles
    _Type A River Tiles_
    """

    tiles: list["Tile"] = []

    tiles.append(
        Tile(
            left_edge=StructureType.ROAD_START,
            right_edge=StructureType.CITY,
            top_edge=StructureType.RIVER,
            bottom_edge=StructureType.RIVER,
        )
    )

    tiles.extend(
        Tile(
            left_edge=StructureType.GRASS,
            right_edge=StructureType.GRASS,
            top_edge=StructureType.RIVER,
            bottom_edge=StructureType.RIVER,
        ).clone_add(2)
    )

    tiles.append(
        Tile(
            left_edge=StructureType.ROAD,
            right_edge=StructureType.RIVER,
            top_edge=StructureType.ROAD,
            bottom_edge=StructureType.RIVER,
        )
    )

    tiles.append(
        Tile(
            left_edge=StructureType.CITY,
            right_edge=StructureType.CITY,
            top_edge=StructureType.RIVER,
            bottom_edge=StructureType.RIVER,
        )
    )

    tiles.append(
        Tile(
            left_edge=StructureType.ROAD,
            right_edge=StructureType.ROAD,
            top_edge=StructureType.RIVER,
            bottom_edge=StructureType.RIVER,
            modifiers=[TileModifier.OPP_ROAD_BRIDGE],
        )
    )

    tiles.append(
        Tile(
            left_edge=StructureType.RIVER,
            right_edge=StructureType.CITY,
            top_edge=StructureType.CITY,
            bottom_edge=StructureType.RIVER,
        )
    )

    tiles.append(
        Tile(
            left_edge=StructureType.RIVER,
            right_edge=StructureType.RIVER,
            top_edge=StructureType.GRASS,
            bottom_edge=StructureType.GRASS,
            modifiers=[TileModifier.MONESTERY],
        )
    )

    tiles.append(
        Tile(
            left_edge=StructureType.GRASS,
            right_edge=StructureType.RIVER,
            top_edge=StructureType.RIVER,
            bottom_edge=StructureType.GRASS,
        )
    )

    tiles.append(
        Tile(
            left_edge=StructureType.GRASS,
            right_edge=StructureType.GRASS,
            top_edge=StructureType.GRASS,
            bottom_edge=StructureType.RIVER,
        )
    )

    return tiles


def create_base_tiles() -> list["Tile"]:
    """
    BaseTiles
    """

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
            modifiers=[TileModifier.SHIELD, TileModifier.OPP_CITY_BRIDGE],
        ).clone_add(2)
    )

    # Tile Type G
    tiles.extend(
        Tile(
            left_edge=StructureType.GRASS,
            right_edge=StructureType.GRASS,
            top_edge=StructureType.CITY,
            bottom_edge=StructureType.CITY,
            modifiers=[TileModifier.OPP_CITY_BRIDGE],
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

    return tiles


def create_expansion_tiles():
    """
    ExpansionTiles
    """
    pass
