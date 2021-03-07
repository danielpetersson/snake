from datetime import datetime
import json
import os

import cherrypy

import datatype
from navigator import Navigator
from quote import get_random_quote

"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md

API: https://docs.battlesnake.com/references/api
"""

DEBUG = False


class Battlesnake(object):

    navigator: Navigator

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

        data = datatype.GameRequest(**cherrypy.request.json)

        distance_food_weights = {i: int((0.8 ** i) * 100) for i in range(1, max(data.board.width, data.board.height))}
        self.navigator = Navigator(distance_food_weights)

        return "ok"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        print("MOVE")

        data = datatype.GameRequest(**cherrypy.request.json)
        response = datatype.MoveResponse()
        response.shout = get_random_quote() if data.turn % 5 == 0 else ""

        try:
            self.navigator.update(data.you, data.board)
            should_me_attack, move = self.navigator.attack()

            if should_me_attack:
                print("ATTACK")

                response.move = move
            else:
                response.move = self.navigator.go_towards(datatype.DirectionWeight())

        except Exception as e:
            print(f'Exception: {str(e)}')

        print(f"MOVE: {response.move}")

        if DEBUG:
            self.__dump_to_file(
                json.dumps(cherrypy.request.json, indent=4),
                f"{datetime.now().strftime('%H:%M:%S.%f')}_{data.turn}.json"
            )

        return response.asdict()

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        print("END")

        self.__dump_to_file(
            json.dumps(cherrypy.request.json, indent=4),
            f"{datetime.now().strftime('%H:%M:%S.%f')}_END.json"
        )

        return "ok"

    def __dump_to_file(self, dump: str, filename: str):
        with open(filename, 'w') as fp:
            fp.write(dump)


if __name__ == "__main__":
    server = Battlesnake()

    print("Starting Battlesnake Server...")

    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update({"server.socket_port": int(os.environ.get("PORT", "8080"))})

    cherrypy.quickstart(server)
