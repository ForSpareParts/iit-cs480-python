from random import Random

from .agent import Agent


class FlipCoinAgent(Agent):
    """
    This agent flips a coin to decide whether to buy a product and increase its
    bid.

    It ignores any other information, whether it be the price, the value, the
    features, or probabilities.
    """

    def __init__(self, id, seed=None, balance=0):
        self.random = Random(seed)
        super(FlipCoinAgent, self).__init__(id, balance)

    def will_buy(self, prod, prob_of_good):
        #flip a coin
        fc = self.random.random()

        if fc > 0.5:
            return True

        return False

    def learn(self, training_instances):
        pass

    def compute_prob_of_good(self, prod_features):
        return 0
