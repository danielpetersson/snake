from enum import Enum
from typing import List, Tuple

import datatype


class NavigatorMode(Enum):
	simple = "simple"
	aggressive = "aggressive"


class Navigator:

	me: datatype.Battlesnake
	enemies: datatype.Battlesnake
	obstacles: List[datatype.Point]
	board: datatype.Battlesnake
	distance_food_weights: dict

	def __init__(self, distance_food_weights: dict, mode: NavigatorMode = NavigatorMode.simple):
		self.distance_food_weights = distance_food_weights
		self.mode = mode

	def update(self, my_snake: datatype.Battlesnake, board: datatype.Board) -> None:
		self.me: datatype.Battlesnake = my_snake
		self.board = board
		self.enemies = list(filter(lambda snake: snake.id != self.me.id, self.board.snakes))
		self.obstacles = self.board.hazards

		[self.obstacles.extend([s.head] + s.body) for s in self.board.snakes]

	def attack(self) -> Tuple[bool, datatype.Direction]:
		if self.mode != NavigatorMode.aggressive:
			return False, None

		for enemy in self.enemies:
			x_diff, y_diff = self.me.head.compare_abs(enemy.head)

			if (x_diff == 1 or y_diff == 1) and self.me.length > enemy.length:
				x_diff, y_diff = self.me.head.compare(enemy.head)

				if x_diff > 0:
					return True, datatype.Direction.left
				if x_diff < 0:
					return True, datatype.Direction.right
				if y_diff > 0:
					return True, datatype.Direction.down
				if y_diff < 0:
					return True, datatype.Direction.up

		return False, None

	def go_towards(self, direction_weight: datatype.DirectionWeight) -> datatype.Direction:
		direction_weight = datatype.DirectionWeight()

		self.__find_food(direction_weight)
		self.__avoid_obstacles(direction_weight)
		self.__avoid_walls(direction_weight)

		weight = direction_weight.left
		move = datatype.Direction.left

		if direction_weight.right > weight:
			weight = direction_weight.right
			move = datatype.Direction.right

		if direction_weight.up > weight:
			weight = direction_weight.up
			move = datatype.Direction.up

		if direction_weight.up > weight:
			move = datatype.Direction.down

		return move.value

	def __distance_to_food(self, snake: datatype.Battlesnake) -> List[int]:
		return [abs(snake.head.x - f.x) + abs(snake.head.y - f.y) for f in self.board.food]

	def __is_closer_then_competitors_to_food(self) -> List[bool]:
		my_distance = self.__distance_to_food(self.me)
		is_mine_closest = [True for i in range(0, len(my_distance))]

		for enemy in self.enemies:
			enemy_distance = self.__distance_to_food(enemy)

			# Compare distance with enemies
			for i in range(0, len(enemy_distance)):
				if my_distance[i] > enemy_distance[i]:
					is_mine_closest[i] = False

		return is_mine_closest

	def __find_food(self, direction_weight: datatype.DirectionWeight) -> None:
		is_closest = self.__is_closer_then_competitors_to_food()

		for i in range(0, len(is_closest)):
			if is_closest[i]:
				x_diff, y_diff = self.me.head.compare(self.board.food[i])

				if x_diff < 0:
					direction_weight.right += self.distance_food_weights[abs(x_diff)]
				if x_diff > 0:
					direction_weight.left += self.distance_food_weights[abs(x_diff)]

				if y_diff < 0:
					direction_weight.up += self.distance_food_weights[abs(y_diff)]
				elif y_diff > 0:
					direction_weight.down += self.distance_food_weights[abs(y_diff)]

	def __avoid_obstacles(self, direction_weight: datatype.DirectionWeight) -> None:
		for obstacle in self.obstacles:
			x_diff, y_diff = self.me.head.compare(obstacle)

		if x_diff == 1:
			direction_weight.left = -1
		elif x_diff == - 1:
			direction_weight.right = -1

		if y_diff == 1:
			direction_weight.down = -1
		elif y_diff == -1:
			direction_weight.up = -1

	def __avoid_walls(self, direction_weight: datatype.DirectionWeight) -> None:
		if self.me.head.x == 0:
			direction_weight.left = -1
		elif self.me.head.x == self.board.width - 1:
			direction_weight.right = -1

		if self.me.head.y == 0:
			direction_weight.down = -1
		elif self.me.head.y == self.board.height - 1:
			direction_weight.up = -1
