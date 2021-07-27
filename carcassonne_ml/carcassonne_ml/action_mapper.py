import numpy as np
from wingedsheep.carcassonne.carcassonne_game_state import CarcassonneGameState
from wingedsheep.carcassonne.objects.actions.action import Action
from wingedsheep.carcassonne.objects.actions.meeple_action import MeepleAction
from wingedsheep.carcassonne.objects.actions.pass_action import PassAction
from wingedsheep.carcassonne.objects.actions.tile_action import TileAction
from wingedsheep.carcassonne.objects.coordinate import Coordinate
from wingedsheep.carcassonne.objects.coordinate_with_side import CoordinateWithSide
from wingedsheep.carcassonne.objects.meeple_type import MeepleType
from wingedsheep.carcassonne.objects.side import Side
from wingedsheep.carcassonne.objects.tile import Tile


class ActionMapper:

    @classmethod
    def map_action(cls, board_dimensions: (int, int), action: Action) -> []:
        vector = []
        vector.extend(cls.map_action_type(action))
        vector.extend(cls.map_row(action, board_dimensions))
        vector.extend(cls.map_column(action, board_dimensions))
        vector.extend(cls.map_rotation(action))
        vector.extend(cls.map_position(action))
        vector.extend(cls.map_meeple_type(action))
        vector.append(cls.map_remove(action))
        return vector

    @classmethod
    def map_action_type(cls, action: Action) -> []:
        if isinstance(action, TileAction):
            return [1, 0, 0]
        elif isinstance(action, MeepleAction):
            return [0, 1, 0]
        else:  # PassAction
            return [0, 0, 1]

    @classmethod
    def map_row(cls, action: Action, board_dimensions: (int, int)):
        vector = np.zeros(board_dimensions[0])
        if isinstance(action, TileAction):
            action: TileAction
            vector[action.coordinate.row] = 1
        elif isinstance(action, MeepleAction):
            action: MeepleAction
            vector[action.coordinate_with_side.coordinate.row] = 1
        return vector

    @classmethod
    def map_column(cls, action: Action, board_dimensions: (int, int)):
        vector = np.zeros(board_dimensions[0])
        if isinstance(action, TileAction):
            action: TileAction
            vector[action.coordinate.column] = 1
        elif isinstance(action, MeepleAction):
            action: MeepleAction
            vector[action.coordinate_with_side.coordinate.column] = 1
        return vector

    @classmethod
    def map_rotation(cls, action: Action):
        vector = np.zeros(4)
        if isinstance(action, TileAction):
            action: TileAction
            vector[action.tile_rotations] = 1
        return vector

    @classmethod
    def map_position(cls, action: Action):
        vector = np.zeros(9)
        if isinstance(action, MeepleAction):
            action: MeepleAction
            if action.coordinate_with_side.side == Side.TOP:
                vector[0] = 1
            elif action.coordinate_with_side.side == Side.RIGHT:
                vector[1] = 1
            elif action.coordinate_with_side.side == Side.BOTTOM:
                vector[2] = 1
            elif action.coordinate_with_side.side == Side.LEFT:
                vector[3] = 1
            elif action.coordinate_with_side.side == Side.TOP_LEFT:
                vector[4] = 1
            elif action.coordinate_with_side.side == Side.TOP_RIGHT:
                vector[5] = 1
            elif action.coordinate_with_side.side == Side.BOTTOM_RIGHT:
                vector[6] = 1
            elif action.coordinate_with_side.side == Side.BOTTOM_LEFT:
                vector[7] = 1
            elif action.coordinate_with_side.side == Side.CENTER:
                vector[8] = 1
        return vector

    @classmethod
    def map_meeple_type(cls, action: Action):
        vector = np.zeros(4)
        if isinstance(action, MeepleAction):
            action: MeepleAction
            if action.meeple_type == MeepleType.NORMAL:
                vector[0] = 1
            elif action.meeple_type == MeepleType.ABBOT:
                vector[1] = 1
        return vector

    @classmethod
    def map_remove(cls, action: Action):
        if isinstance(action, MeepleAction):
            action: MeepleAction
            return 1 if action.remove else 0
        return 0

    @classmethod
    def vector_to_int(cls, vector: []):
        return int(np.argmax(vector))

    @classmethod
    def reverse_map(cls, action_vector: [], game_state: CarcassonneGameState):
        starting_index = 0
        action_type_vector = action_vector[starting_index:starting_index + 3]
        starting_index += 3
        row_vector = action_vector[starting_index:starting_index + len(game_state.board)]
        starting_index += len(game_state.board)
        column_vector = action_vector[starting_index:starting_index + len(game_state.board)]
        starting_index += len(game_state.board)
        rotation_vector = action_vector[starting_index:starting_index + 4]
        starting_index += 4
        position_vector = action_vector[starting_index:starting_index + 9]
        starting_index += 9
        meeple_type_vector = action_vector[starting_index:starting_index + 2]
        starting_index += 2
        remove_meeple = action_vector[len(action_vector) - 1]

        if action_type_vector[0] == 1:
            row = cls.vector_to_int(row_vector)
            column = cls.vector_to_int(column_vector)
            coordinate = Coordinate(row, column)
            rotations = cls.vector_to_int(rotation_vector)
            tile: Tile = game_state.next_tile.turn(rotations)
            return TileAction(tile=tile, coordinate=coordinate, tile_rotations=rotations)
        elif action_type_vector[1] == 1:
            row = cls.vector_to_int(row_vector)
            column = cls.vector_to_int(column_vector)
            coordinate = Coordinate(row, column)
            side = cls.get_position(position_vector)
            coordinate_with_side: CoordinateWithSide = CoordinateWithSide(coordinate, side)
            meeple_type: MeepleType = cls.get_meeple_type(meeple_type_vector)
            remove = True if remove_meeple == 1 else False
            return MeepleAction(coordinate_with_side=coordinate_with_side, meeple_type=meeple_type, remove=remove)
        else:
            return PassAction()

    @classmethod
    def get_position(cls, position_vector):
        if position_vector[0] == 1:
            return Side.TOP
        elif position_vector[1] == 1:
            return Side.RIGHT
        elif position_vector[2] == 1:
            return Side.BOTTOM
        elif position_vector[3] == 1:
            return Side.LEFT
        elif position_vector[4] == 1:
            return Side.TOP_LEFT
        elif position_vector[5] == 1:
            return Side.TOP_RIGHT
        elif position_vector[6] == 1:
            return Side.BOTTOM_RIGHT
        elif position_vector[7] == 1:
            return Side.BOTTOM_LEFT
        elif position_vector[8] == 1:
            return Side.CENTER

    @classmethod
    def get_meeple_type(cls, meeple_type_vector):
        if meeple_type_vector[0] == 1:
            return MeepleType.NORMAL
        elif meeple_type_vector[1] == 1:
            return MeepleType.ABBOT
