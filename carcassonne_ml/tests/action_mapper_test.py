import unittest

from wingedsheep.carcassonne.carcassonne_game_state import CarcassonneGameState
from wingedsheep.carcassonne.objects.actions.tile_action import TileAction
from wingedsheep.carcassonne.objects.coordinate import Coordinate
from wingedsheep.carcassonne.objects.tile import Tile
from wingedsheep.carcassonne.tile_sets.the_river_deck import the_river_tiles

from carcassonne_ml.carcassonne_ml.action_mapper import ActionMapper


class ActionMapperTest(unittest.TestCase):

    def test_reverse_map_tile_action(self):
        # Given
        game_state: CarcassonneGameState = CarcassonneGameState()
        game_state.board = [[None for _ in range(4)] for _ in range(4)]

        tile: Tile = the_river_tiles["river_city_with_road"]
        action: TileAction = TileAction(tile=tile, coordinate=Coordinate(2, 1), tile_rotations=0)

        # When
        action_vector = ActionMapper.map_action(action=action, board_dimensions=(len(game_state.board), len(game_state.board)))
        reversed_action = ActionMapper.reverse_map(action_vector=action_vector, game_state=game_state)

        # Then
        self.assertTrue(isinstance(reversed_action, TileAction))
        self.assertEqual(action.coordinate.row, reversed_action.coordinate.row)
        self.assertEqual(action.coordinate.column, reversed_action.coordinate.column)
        self.assertEqual(action.tile_rotations, reversed_action.tile_rotations)
