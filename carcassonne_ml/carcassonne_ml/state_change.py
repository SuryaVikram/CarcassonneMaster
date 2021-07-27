class StateChange:

    def __init__(self, new_state, rewards, done: bool):
        """
        :param new_state: The new state after doing an action.
        :param rewards: Rewards per player.
        :param done: True if the game is finished.
        """
        self.new_state = new_state
        self.rewards = rewards
        self.done = done
