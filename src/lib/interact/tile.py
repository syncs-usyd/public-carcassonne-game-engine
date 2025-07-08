from lib.config.scoring import NO_POINTS
from lib.interact.structure import StructureType

from enum import Enum, auto
from copy import copy
from collections import namedtuple
from dotmap import DotMap

from typing import Callable, final, Self

from lib.models.tile_model import TileModel


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

    @final
    @staticmethod
    def get_bridge_modifier(structure: StructureType) -> "TileModifier | None":
        return {
            StructureType.ROAD: TileModifier.OPP_ROAD_BRIDGE,
            StructureType.CITY: TileModifier.OPP_CITY_BRIDGE,
        }.get(structure, None)

    @final
    @staticmethod
    def apply_point_modifiers(structure: StructureType) -> int:
        def _get_point_modifiers(structure: StructureType) -> list["TileModifier"]:
            return {
                StructureType.CITY: [TileModifier.OPP_CITY_BRIDGE],
            }.get(structure, [])

        def _point_modifier_config(tm: "TileModifier") -> Callable[[int], int]:
            return {
                TileModifier.MONESTERY: lambda x: x + 9,
                TileModifier.SHIELD: lambda x: x + 1,
            }.get(tm, lambda x: x + NO_POINTS)

        points = StructureType.get_points(structure)

        for mod in _get_point_modifiers(structure):
            points = _point_modifier_config(mod)(points)

        return points


class Tile:
    """
    Tile
    Desc: _Stores all Tile Info by internal edges (Structures) and external connections_
    """

    EdgeTuple = namedtuple(
        "EdgeTuple", ["left_edge", "right_edge", "top_edge", "bottom_edge"]
    )

    @final
    @staticmethod
    def get_opposite(edge: str) -> str:
        return {
            "left_edge": "right_edge",
            "right_edge": "left_edge",
            "top_edge": "bottom_edge",
            "bottom_edge": "top_edge",
        }[edge]

    @final
    @staticmethod
    def adjacent_edges(edge: str) -> list[str]:
        return {
            "left_edge": ["top_edge", "bottom_edge"],
            "right_edge": ["top_edge", "bottom_edge"],
            "top_edge": ["left_edge", "right_edge"],
            "bottom_edge": ["left_edge", "right_edge"],
        }[edge]

    @final
    @staticmethod
    def get_external_tile(
        edge, pos: tuple[int, int], grid: list[list["Tile | None"]]
    ) -> "Tile | None":
        match edge:
            case "left_edge":
                return grid[pos[0]][pos[1] - 1]
            case "right_edge":
                return grid[pos[0]][pos[1] + 1]
            case "top_edge":
                return grid[pos[0] - 1][pos[1]]
            case "bottom_edge":
                return grid[pos[0] + 1][pos[1]]

        assert False

    @staticmethod
    def get_starting_tile() -> "Tile":
        return Tile(
            tile_id="R0",
            left_edge=StructureType.GRASS,
            right_edge=StructureType.GRASS,
            top_edge=StructureType.RIVER,
            bottom_edge=StructureType.GRASS,
            modifiers=[TileModifier.RIVER],
        )

    def __init__(
        self,
        tile_id: str,
        left_edge: StructureType,
        right_edge: StructureType,
        top_edge: StructureType,
        bottom_edge: StructureType,
        modifiers: list[TileModifier] = list(),
    ) -> None:
        self.internal_edges = DotMap(
            Tile.EdgeTuple(
                left_edge=left_edge,
                right_edge=right_edge,
                top_edge=top_edge,
                bottom_edge=bottom_edge,
            )._asdict(),
            _dynamic=False,
        )

        self.internal_edge_claims = DotMap(
            Tile.EdgeTuple(
                left_edge=None,
                right_edge=None,
                top_edge=None,
                bottom_edge=None,
            )._asdict(),
            _dynamic=False,
        )

        self.external_edges = DotMap(
            Tile.EdgeTuple(
                left_edge=None,
                right_edge=None,
                top_edge=None,
                bottom_edge=None,
            )._asdict(),
            _dynamic=False,
        )

        self.rotation = 0
        self.modifiers = modifiers
        self.tile_type = tile_id
        self.placed_pos: tuple[int, int] | None = None

        # self.left_tile: "Tile"
        # self.right_tile: "Tile"
        # self.top_tile: "Tile"
        # self.bottom_tile: "Tile"

    def rotate_clockwise(self, number: int) -> None:
        for _ in range(number):
            self.right_edge, self.bottom_edge, self.left_edge, self.top_edge = (
                self.top_edge,
                self.right_edge,
                self.bottom_edge,
                self.left_edge,
            )

    def _claim_edge(self, player_id: int, edge: str):
        self.internal_edge_claims[edge] = player_id

    @final
    def clone_add(self, n: int) -> list[Self]:
        cloned_tiles = [copy(self) for _ in range(n)]
        cloned_tiles.append(self)
        return cloned_tiles

    @final
    def to_model(self, index: int):
        return TileModel(
            player_tile_index=index, tile_type=self.tile_type, rotation=self.rotation
        )


def create_river_tiles() -> list["Tile"]:
    """
    RiverTiles
    _Type A River Tiles_
    """

    tiles: list["Tile"] = []

    tiles.append(
        Tile(
            tile_id="R1",
            left_edge=StructureType.ROAD_START,
            right_edge=StructureType.CITY,
            top_edge=StructureType.RIVER,
            bottom_edge=StructureType.RIVER,
        )
    )

    tiles.extend(
        Tile(
            tile_id="R2",
            left_edge=StructureType.GRASS,
            right_edge=StructureType.GRASS,
            top_edge=StructureType.RIVER,
            bottom_edge=StructureType.RIVER,
        ).clone_add(2)
    )

    tiles.append(
        Tile(
            tile_id="R3",
            left_edge=StructureType.ROAD,
            right_edge=StructureType.RIVER,
            top_edge=StructureType.ROAD,
            bottom_edge=StructureType.RIVER,
        )
    )

    tiles.append(
        Tile(
            tile_id="R4",
            left_edge=StructureType.CITY,
            right_edge=StructureType.CITY,
            top_edge=StructureType.RIVER,
            bottom_edge=StructureType.RIVER,
        )
    )

    tiles.append(
        Tile(
            tile_id="R5",
            left_edge=StructureType.ROAD,
            right_edge=StructureType.ROAD,
            top_edge=StructureType.RIVER,
            bottom_edge=StructureType.RIVER,
            modifiers=[TileModifier.OPP_ROAD_BRIDGE],
        )
    )

    tiles.append(
        Tile(
            tile_id="R6",
            left_edge=StructureType.RIVER,
            right_edge=StructureType.CITY,
            top_edge=StructureType.CITY,
            bottom_edge=StructureType.RIVER,
        )
    )

    tiles.append(
        Tile(
            tile_id="R7",
            left_edge=StructureType.RIVER,
            right_edge=StructureType.RIVER,
            top_edge=StructureType.GRASS,
            bottom_edge=StructureType.GRASS,
            modifiers=[TileModifier.MONESTERY],
        )
    )

    tiles.append(
        Tile(
            tile_id="R8",
            left_edge=StructureType.GRASS,
            right_edge=StructureType.RIVER,
            top_edge=StructureType.RIVER,
            bottom_edge=StructureType.GRASS,
        )
    )

    tiles.append(
        Tile(
            tile_id="R9",
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
            tile_id="A",
            left_edge=StructureType.GRASS,
            right_edge=StructureType.GRASS,
            top_edge=StructureType.GRASS,
            bottom_edge=StructureType.ROAD_START,
        ).clone_add(2)
    )

    # Tile Type B
    tiles.extend(
        Tile(
            tile_id="B",
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
            tile_id="C",
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
            tile_id="D",
            left_edge=StructureType.GRASS,
            right_edge=StructureType.CITY,
            top_edge=StructureType.ROAD,
            bottom_edge=StructureType.ROAD,
        ).clone_add(1)
    )

    # Tile Type E
    tiles.extend(
        Tile(
            tile_id="E",
            left_edge=StructureType.GRASS,
            right_edge=StructureType.GRASS,
            top_edge=StructureType.CITY,
            bottom_edge=StructureType.GRASS,
        ).clone_add(5)
    )

    # Tile Type F
    tiles.extend(
        Tile(
            tile_id="F",
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
            tile_id="G",
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
            tile_id="H",
            left_edge=StructureType.CITY,
            right_edge=StructureType.CITY,
            top_edge=StructureType.GRASS,
            bottom_edge=StructureType.GRASS,
        ).clone_add(3)
    )

    # Tile Type I
    tiles.extend(
        Tile(
            tile_id="I",
            left_edge=StructureType.GRASS,
            right_edge=StructureType.CITY,
            top_edge=StructureType.GRASS,
            bottom_edge=StructureType.CITY,
        ).clone_add(2)
    )

    # Tile Type J
    tiles.extend(
        Tile(
            tile_id="J",
            left_edge=StructureType.GRASS,
            right_edge=StructureType.ROAD,
            top_edge=StructureType.CITY,
            bottom_edge=StructureType.ROAD,
        ).clone_add(3)
    )

    # Tile Type K
    tiles.extend(
        Tile(
            tile_id="K",
            left_edge=StructureType.ROAD,
            right_edge=StructureType.CITY,
            top_edge=StructureType.ROAD,
            bottom_edge=StructureType.GRASS,
        ).clone_add(3)
    )

    # Tile Type L
    tiles.extend(
        Tile(
            tile_id="L",
            left_edge=StructureType.ROAD_START,
            right_edge=StructureType.CITY,
            top_edge=StructureType.ROAD_START,
            bottom_edge=StructureType.ROAD_START,
        ).clone_add(3)
    )

    # Tile Type M
    tiles.extend(
        Tile(
            tile_id="M",
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
            tile_id="N",
            left_edge=StructureType.CITY,
            right_edge=StructureType.GRASS,
            top_edge=StructureType.CITY,
            bottom_edge=StructureType.GRASS,
        ).clone_add(3)
    )

    # Tile Type O
    tiles.extend(
        Tile(
            tile_id="O",
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
            tile_id="P",
            left_edge=StructureType.CITY,
            right_edge=StructureType.ROAD,
            top_edge=StructureType.CITY,
            bottom_edge=StructureType.ROAD,
        ).clone_add(3)
    )

    # Tile Type Q
    tiles.extend(
        Tile(
            tile_id="Q",
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
            tile_id="R",
            left_edge=StructureType.CITY,
            right_edge=StructureType.CITY,
            top_edge=StructureType.CITY,
            bottom_edge=StructureType.GRASS,
        ).clone_add(3)
    )

    # Tile Type S
    tiles.extend(
        Tile(
            tile_id="S",
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
            tile_id="T",
            left_edge=StructureType.CITY,
            right_edge=StructureType.CITY,
            top_edge=StructureType.CITY,
            bottom_edge=StructureType.ROAD,
        ).clone_add(1)
    )

    # Tile Type U
    tiles.extend(
        Tile(
            tile_id="U",
            left_edge=StructureType.GRASS,
            right_edge=StructureType.GRASS,
            top_edge=StructureType.ROAD,
            bottom_edge=StructureType.ROAD,
        ).clone_add(8)
    )

    # Tile Type V
    tiles.extend(
        Tile(
            tile_id="V",
            left_edge=StructureType.ROAD,
            right_edge=StructureType.GRASS,
            top_edge=StructureType.GRASS,
            bottom_edge=StructureType.ROAD,
        ).clone_add(9)
    )

    # Tile Type W
    tiles.extend(
        Tile(
            tile_id="W",
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
            tile_id="X",
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
