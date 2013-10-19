class Agent(object):
    """The base Agent class. All agents should inherit this class.

    In the single agent case, this agent receives a product and decides to
    buy the product or not; a one time decision for a given product.

    In the multi-agent case, it receives the product with the newDay method,
    receives maxBidder's id and bid through currentBidInfo, and when asked,
    it provides a bid through myBidIs function. It learns the result of the
    bidding through endOfDay function."""

    def __init__(this, id, balance=0):
        this.id = id
        this.balance = balance

    #DECISION MAKING:
    def will_buy(self, prod, prob_of_good):
        """
        Given a product prod and the probability of it being in a good
        condition, the agent decides whether to buy the product.

        Args:
           prod: the product
           prob_of_good: probability of the product being in a good condition
        Returns:
           True if the agent decides to buy the product
        """
        raise NotImplementedError

    def will_buy_given_features(self, prod, prod_features):
        """
        Given a product prod and a list of features prod_features, decide
        whether or not to buy it.

        Args:
            prod: the product
            features: a list of the product's features
        Returns:
            True if the agent decides to buy the product
        """
        prob = self.compute_prob_of_good(prod_features)
        return self.will_buy(prod, prob)

    #LEARN AND PREDICT:
    def learn(self, training_instances):
        """
        Learn a function that maps into whether the product is Good or Bad.

        Args:
            training_instances: a list of instances, where each instance is
                                represented by a list of strings, in which each
                                entry represents a categorical feature value.
                                The last feature represents the class (G/B).
        """
        raise NotImplementedError

    def compute_prob_of_good(self, prod_features):
        """
        Given product features, predict whether the product's class is G.

        Args:
            prod_features: A list of features describing the product. These do
                           not include the class information.
        Returns:
            The probability of the product being in a good condition.
        """
        raise NotImplementedError

    def __unicode__(self):
        return "Agent [id={}]".format(self.id)
