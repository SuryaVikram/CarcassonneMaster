from wingedsheep.carcassonne.carcassonne_game import CarcassonneGame


class SpaceSize:

    @classmethod
    def get_state_space(cls, game: CarcassonneGame):
        state_space_x = len(game.state.board)
        state_space_y = len(game.state.board)

        # tile_placed + city_vector + road_vector + river_vector + shield + chapel + flowers + meeple_vectors
        tile_placed = 1
        city_vector = 10
        road_vector = 10
        river_vector = 10
        shield = 1
        chapel = 1
        flowers = 1
        meeple_vector = 9

        state_space_z = tile_placed + \
                        city_vector + \
                        road_vector + \
                        river_vector + \
                        shield + \
                        chapel + \
                        flowers + \
                        meeple_vector * game.players

        return state_space_x, state_space_y, state_space_z

    @classmethod
    def get_action_space(cls, game):
        action_types = 3
        row = len(game.state.board)
        column = len(game.state.board)
        rotation = 4
        meeple_position = 9
        meeple_type = 2
        meeple_remove = 1

        return action_types + row + column + rotation + meeple_position + meeple_type + meeple_remove
