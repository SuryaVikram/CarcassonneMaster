class DQNAgent:

    def __init__(self, network):
        self.network = network
        self.experience_replay_memory = []