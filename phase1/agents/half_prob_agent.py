from .agent import Agent


class HalfProbAgent(Agent):
    """
    This agent buys a product (or bids as much as it can) when it believes the
    product is in good condition, regardless of the value and the price of the
    product. It believes the product is in good condition when the given or
    computed probability is greater than 0.5.
    """

    def will_buy(self, prod, prob_of_good):
        if prob_of_good > 0.5:
            return True

        return False

    def learn(self, training_instances):
        pass

    def compute_prob_of_good(self, prod_features):
        return 0
