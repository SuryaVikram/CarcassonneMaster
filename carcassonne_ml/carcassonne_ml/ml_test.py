import random

from carcassonne_ml.carcassonne_ml.carcassonne_environment import CarcassonneEnvironment

env = CarcassonneEnvironment()
env.reset()

while not env.finished():
    player = env.current_player()
    allowed_actions = env.allowed_actions()
    action = random.choice(allowed_actions)
    state_change = env.step(action)
    print(state_change.rewards)
    env.visualise()
