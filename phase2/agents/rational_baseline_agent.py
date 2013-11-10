from .agent import Agent


class RationalBaselineAgent(Agent):
    """
    A learning agent that only calculates the overall market condition.
    """
    def __init__(self, id, balance=0):
        self.market_condition = 0.5
        super(RationalBaselineAgent, self).__init__(id, balance)

    def will_buy(self, prod, prob_of_good):
        return prob_of_good*prod.value > prod.price

    def learn(self, training_instances):
        """
        Computer the market condition based on the number of good products.
        """

        num_good_products = 0

        for product in training_instances:
            condition = product[len(product)-1]

            if condition == 'G':
                num_good_products += 1

        self.market_condition = (num_good_products*1.0)/len(training_instances)

    def compute_prob_of_good(self, prod_features):
        # Ignore features; simply return the market condition
        return self.market_condition
