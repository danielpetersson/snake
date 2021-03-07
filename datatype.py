from dataclasses import dataclass, asdict
from enum import Enum
import random
from typing import List, Dict


@dataclass
class Point:
    x: int = 0
    y: int = 0

    def compare(self, other):
        return self.x - other.x, self.y - other.y

    def compare_abs(self, other):
        return abs(self.x - other.x), abs(self.y - other.y)


class Direction(Enum):
    right = "right"
    left = "left"
    up = "up"
    down = "down"

    @staticmethod
    def aslist() -> List:
        return [d.value for d in Direction]

    @staticmethod
    def random() -> str:
        return random.choice(Direction.aslist())


@dataclass
class DirectionWeight:
    right: int = 0
    left: int = 0
    up: int = 0
    down: int = 0

    def best_direction(self) -> Direction:
        direction = Direction.right
        value = self.right

        if self.left > value:
            direction = Direction.left
            value = self.west

        if self.up > value:
            direction = Direction.up
            value = self.north

        if self.down > value:
            direction = Direction.down

        return direction


@dataclass
class Ruleset:
    name: str
    version: str


@dataclass
class Game:
    id: str
    ruleset: Dict
    timeout: int


@dataclass
class Battlesnake:
    id: str
    name: dict
    health: int
    body: List[Point]
    latency: int
    head: Point
    length: int
    shout: str
    #squad: str

    def __post_init__(self):
        self.body = [Point(**b) for b in self.body]
        self.head = Point(**self.head)


@dataclass
class Board:
    height: int
    width: int
    food: List[Point]
    hazards: List[Point]
    snakes: List[Battlesnake]

    def __post_init__(self):
        self.food = [Point(**f) for f in self.food]
        self.hazards = [Point(**h) for h in self.hazards]
        self.snakes = [Battlesnake(**s) for s in self.snakes]


@dataclass
class MoveResponse:
    move: str = Direction.random()
    shout: str = ""

    def asdict(self) -> dict:
        return asdict(self)


@dataclass
class IndexResponse:
    apiversion: str
    author: str
    color: str
    head: str
    tail: str
    version: str

    def asdict(self) -> dict:
        return asdict(self)


@dataclass
class GameRequest:
    game: Game
    turn: int
    board: Board
    you: Battlesnake

    def __post_init__(self):
        self.game = Game(**self.game)
        self.board = Board(**self.board)
        self.you = Battlesnake(**self.you)
