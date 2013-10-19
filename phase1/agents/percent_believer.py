from .agent import Agent


class PercentBeliever(Agent):
    """
    An agent that always believes that a product is worth only a fixed percent
    of its value. The percent is provided initially.
    """
    def __init__(self, id, percent_worth, balance=0):
        self.percent_worth = percent_worth
        super(PercentBeliever, self).__init__(id, balance)

    def will_buy(self, prod, prob_of_good):
        if prod.price <= (prod.value*self.percent_worth)/100:
            return True

        return False

    def learn(self, training_instances):
        pass

    def compute_prob_of_good(self, prod_features):
        return 0
