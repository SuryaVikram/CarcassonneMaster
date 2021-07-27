import numpy as np
from wingedsheep.carcassonne.carcassonne_game import CarcassonneGame
from wingedsheep.carcassonne.tile_sets.supplementary_rules import SupplementaryRule
from wingedsheep.carcassonne.tile_sets.tile_sets import TileSet

from carcassonne_ml.carcassonne_ml.action_mapper import ActionMapper
from carcassonne_ml.carcassonne_ml.space_size import SpaceSize
from carcassonne_ml.carcassonne_ml.state_change import StateChange
from carcassonne_ml.carcassonne_ml.state_mapper import StateMapper


class CarcassonneEnvironment:
    state_space: []
    action_space: []
    game: CarcassonneGame

    def __init__(self):
        pass

    def reset(self) -> []:
        self.game = CarcassonneGame(tile_sets=[TileSet.BASE, TileSet.THE_RIVER],
                                    supplementary_rules=[SupplementaryRule.ABBOTS])
        self.state_space = SpaceSize.get_state_space(self.game)
        self.action_space = SpaceSize.get_action_space(self.game)
        return StateMapper.map_state(self.game.state)

    def step(self, action_vector: []) -> StateChange:
        action = ActionMapper.reverse_map(action_vector=action_vector, game_state=self.game.state)
        prev_scores = self.game.state.scores
        self.game.step(player=self.game.get_current_player(), action=action)
        new_scores = self.game.state.scores
        rewards = np.subtract(new_scores, prev_scores)
        return StateChange(
            new_state=StateMapper.map_state(self.game.state),
            rewards=rewards,
            done=self.game.is_finished()
        )

    def allowed_actions(self):
        return list(map(lambda action: ActionMapper.map_action(action=action, board_dimensions=(len(self.game.state.board), len(self.game.state.board))), self.game.get_possible_actions()))

    def current_player(self) -> int:
        return self.game.get_current_player()

    def finished(self) -> bool:
        return self.game.is_finished()

    def visualise(self):
        return self.game.render()
