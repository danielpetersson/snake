from datetime import datetime
import json
import os
from typing import List

import cherrypy

import datatype
from navigator import Navigator, NavigatorMode
from quote import get_random_quote

"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md

API: https://docs.battlesnake.com/references/api
"""

DEBUG = False
NAVIGATOR_MODE = NavigatorMode.simple


class Battlesnake(object):

    navigator: Navigator
    stats: List

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        print("INDEX")

        response = datatype.IndexResponse(
            apiversion="1",
            author="chucknorris",
            color="#FF0000",
            head="snowman",
            tail="coffee",
            version="1.0"
        )

        return response.asdict()

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def start(self):
        print("START")

        try:
            if DEBUG:
                self.__dump(
                    json.dumps({'start': cherrypy.request.json}, indent=4),
                    f"{datetime.now().strftime('%H:%M:%S.%f')}_start.json"
                )

            data = datatype.GameRequest(**cherrypy.request.json)

            max_distance = data.board.width + data.board.height
            distance_food_weights = {i: int((0.8 ** i) * 100) for i in range(1, max_distance)}
            self.navigator = Navigator(distance_food_weights, mode=NAVIGATOR_MODE, is_debug=DEBUG)
            self.stats = []
        except Exception as e:
            print(f'Exception: {str(e)}')

        return "ok"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        print("MOVE")

        try:
            if DEBUG:
                self.__dump(
                    json.dumps({'move': cherrypy.request.json}, indent=4),
                    f"{datetime.now().strftime('%H:%M:%S.%f')}_move.json"
                )

            response = datatype.MoveResponse()
            data = datatype.GameRequest(**cherrypy.request.json)
            response.shout = get_random_quote() if (data.turn - 1) % 5 == 0 else ""

            self.navigator.update(data.you, data.board)
            should_me_attack, move = self.navigator.attack()

            if should_me_attack:
                print("ATTACK")

                response.move = move
            else:
                response.move = self.navigator.go_towards()

            for s in data.board.snakes:
                self.stats.append(f"name={s.name},latency={s.latency},health={s.health},length={s.length}")
        except Exception as e:
            print(f'Exception: {str(e)}')

        print(f"MOVE: {response.move} at turn {data.turn} with latency {data.you.latency}")

        return response.asdict()

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        print("END")

        try:
            data = cherrypy.request.json
            data["stats"] = self.stats

            self.__dump(
                json.dumps({'end': data}, indent=4),
                f"{datetime.now().strftime('%H:%M:%S.%f')}_end.json"
            )
        except Exception as e:
            print(f'Exception: {str(e)}')

        return "ok"

    def __dump(self, dump: str, filename: str):
        print(dump)

        with open(filename, 'w') as fp:
            fp.write(dump)


if __name__ == "__main__":
    server = Battlesnake()

    print("Starting Battlesnake Server...")

    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update({"server.socket_port": int(os.environ.get("PORT", "8080"))})

    cherrypy.quickstart(server)
