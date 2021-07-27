import numpy as np
from wingedsheep.carcassonne.carcassonne_game_state import CarcassonneGameState
from wingedsheep.carcassonne.objects.connection import Connection
from wingedsheep.carcassonne.objects.meeple_position import MeeplePosition
from wingedsheep.carcassonne.objects.meeple_type import MeepleType
from wingedsheep.carcassonne.objects.side import Side
from wingedsheep.carcassonne.objects.tile import Tile


class StateMapper:
    tile_vector_size = 52

    @classmethod
    def map_state(cls, game_state: CarcassonneGameState) -> []:
        print(game_state.board)
        matrix = np.zeros((len(game_state.board) + 1, len(game_state.board[0]), cls.tile_vector_size))
        for x, row in enumerate(game_state.board):
            for y, tile in enumerate(row):
                for z, value in enumerate(cls.map_tile(game_state, tile, x, y)):
                    matrix[x][y][z] = value

        for z, value in enumerate(cls.map_tile(game_state, game_state.next_tile, -1, -1)):
            matrix[len(game_state.board)][0][z] = value

        return matrix

    @classmethod
    def map_tile(cls, game_state: CarcassonneGameState, tile: Tile, x: int, y: int):
        tile_vector = []

        if tile is None:
            return np.zeros(cls.tile_vector_size)
        else:
            tile_vector.append(1)

        tile_vector.extend(cls.city_vector(tile))
        tile_vector.extend(cls.road_vector(tile))
        tile_vector.extend(cls.river_vector(tile))
        tile_vector.append(1 if tile.shield else 0)
        tile_vector.append(1 if tile.chapel else 0)
        tile_vector.append(1 if tile.flowers else 0)

        if x >= 0:
            tile_vector.extend(cls.meeples(game_state, x, y, game_state.current_player))

            next_player = game_state.current_player + 1
            if next_player >= game_state.players:
                next_player = 0

            tile_vector.extend(cls.meeples(game_state, x, y, next_player))

        return tile_vector

    @staticmethod
    def city_vector(tile: Tile):
        city_vector = np .zeros(10)
        for city_connection in tile.city:
            if Side.TOP in city_connection:
                city_vector[0] = 1
                if Side.RIGHT in city_connection:
                    city_vector[4] = 1
                if Side.BOTTOM in city_connection:
                    city_vector[5] = 1
                if Side.LEFT in city_connection:
                    city_vector[6] = 1
            if Side.RIGHT in city_connection:
                city_vector[1] = 1
                if Side.BOTTOM in city_connection:
                    city_vector[7] = 1
                if Side.LEFT in city_connection:
                    city_vector[8] = 1
            if Side.BOTTOM in city_connection:
                city_vector[2] = 1
                if Side.LEFT in city_connection:
                    city_vector[9] = 1
            if Side.LEFT in city_connection:
                city_vector[3] = 1
        return city_vector

    @classmethod
    def road_vector(cls, tile: Tile):
        return cls.get_connections_vector(tile.road)

    @classmethod
    def river_vector(cls, tile: Tile):
        return cls.get_connections_vector(tile.river)

    @staticmethod
    def get_connections_vector(connections: [Connection]):
        vector = np.zeros(10)
        for connection in connections:
            if Side.TOP in (connection.a, connection.b):
                vector[0] = 1
                if Side.RIGHT in (connection.a, connection.b):
                    vector[4] = 1
                    break
                elif Side.BOTTOM in (connection.a, connection.b):
                    vector[5] = 1
                    break
                elif Side.LEFT in (connection.a, connection.b):
                    vector[6] = 1
                    break
            if Side.RIGHT in (connection.a, connection.b):
                vector[1] = 1
                if Side.BOTTOM in (connection.a, connection.b):
                    vector[7] = 1
                    break
                elif Side.LEFT in (connection.a, connection.b):
                    vector[8] = 1
                    break
            if Side.BOTTOM in (connection.a, connection.b):
                vector[2] = 1
                if Side.LEFT in (connection.a, connection.b):
                    vector[9] = 1
                    break
            if Side.LEFT in (connection.a, connection.b):
                vector[3] = 1
        return vector

    @classmethod
    def meeples(cls, game_state: CarcassonneGameState, x, y, player):
        vector = np.zeros(9)

        meeple: MeeplePosition
        for meeple in game_state.placed_meeples[player]:
            if meeple.coordinate_with_side.coordinate.row == x and meeple.coordinate_with_side.coordinate.column == y:
                if meeple.meeple_type == MeepleType.NORMAL:
                    if meeple.coordinate_with_side.side == Side.TOP:
                        vector[0] = 1
                        break
                    if meeple.coordinate_with_side.side == Side.RIGHT:
                        vector[1] = 1
                        break
                    if meeple.coordinate_with_side.side == Side.BOTTOM:
                        vector[2] = 1
                        break
                    if meeple.coordinate_with_side.side == Side.LEFT:
                        vector[3] = 1
                        break
                    if meeple.coordinate_with_side.side == Side.CENTER:
                        vector[3] = 1
                        break
                elif meeple.meeple_type == MeepleType.ABBOT:
                    if meeple.coordinate_with_side.side == Side.TOP:
                        vector[4] = 1
                        break
                    if meeple.coordinate_with_side.side == Side.RIGHT:
                        vector[5] = 1
                        break
                    if meeple.coordinate_with_side.side == Side.BOTTOM:
                        vector[6] = 1
                        break
                    if meeple.coordinate_with_side.side == Side.LEFT:
                        vector[7] = 1
                        break
                    if meeple.coordinate_with_side.side == Side.CENTER:
                        vector[8] = 1
                        break

        return vector
