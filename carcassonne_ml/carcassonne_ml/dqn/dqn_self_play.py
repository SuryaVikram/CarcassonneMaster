import numpy as np

from carcassonne_ml.carcassonne_environment import CarcassonneEnvironment
from carcassonne_ml.dqn.dqn_agent import DQNAgent
from carcassonne_ml.state_change import StateChange

def get_final_rewards(scores):
    score1 = scores[0]
    score2 = scores[2]

    if score1 == score2:
        return [0, 0]
    elif score1 > score2:
        return [1, -1]
    else:
        return [-1, 1]

agents: [DQNAgent] = (DQNAgent(), DQNAgent())
env = CarcassonneEnvironment()

for i in range(1000):
    state = env.reset()
    accumulated_reward = [0, 0]
    while not env.finished():
        player = env.current_player()
        agent = agents[player]
        action = agent.pick_action(state, env.allowed_actions())
        observation: StateChange = env.step(action)

        if observation.done:
            final_rewards = get_final_rewards(env.game.state.scores)
            break
        else:

            break
