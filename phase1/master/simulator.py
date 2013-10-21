from collections import OrderedDict
from random import Random

from ..agents import *
from .product import Product


#: Number of days
NUM_DAYS = 1000

#:The cap on the maximum value of the product
MAXIMUM_VALUE = 50000

#: The initial money the agent has
INITIAL_MONEY = 1000

#: The amount the agent earns daily from other sources
DAILY_EARNINGS = 100

#The markets with the ratio of good vs. bad products

#: An unfavorable market ratio.
UNFAVORABLE = (1, 3)

#: A fair market ratio.
FAIR = (1, 1)

#: A favorable market ratio.
FAVORABLE = (3, 1)

#: Debug mode. When True, shows the full trace.
DEBUG = False


def no_learning_case(agent, market_odds, seed=None):
    """
    Given an agent and a seed, simulates agent.

    You should NOT modify this function, except to print less/more info.

    Args:
        agent: Agent to simulate.
        seed: seed for the random number generator. If None/default, the system time is used.
    """

    rand = Random(seed)

    agent.balance = INITIAL_MONEY
    daily_balance = []

    debug_print("Seed={}".format(seed))

    for d in xrange(0, NUM_DAYS):
        debug_print("Day {}".format(d))
        debug_print("The balance at the beginning of the day is: {}".format(
            agent.balance))

        max_value = min(agent.balance, MAXIMUM_VALUE)
        value = rand.random()*max_value
        price = rand.random()*value

        #probability the product is in working condition
        #use the beta distribution
        prob = rand.betavariate(market_odds[0], market_odds[1])

        #is the product *actually* in working condition?
        draw = rand.random()
        product_working = draw <= prob

        prod = Product(value, price)

        debug_print("Product is {}".format(prod))
        debug_print("The probability of the product being in working condition is {}".format(prob))

        will_buy = agent.will_buy(prod, prob)

        if will_buy:
            debug_print("Agent {} decides to buy it.".format(agent))

            #withdraw the product's price from the agent's account
            agent.balance -= prod.price

            if product_working:
                debug_print("Good call: the product is in working condition.")
                debug_print("The agent's profit is: {}.".format(
                    prod.value - prod.price))

                #deposit the product's value to the agent's account
                agent.balance += prod.value
            else:
                debug_print("Bad call: the product is faulty.")
                debug_print("The agent loses {}.".format(prod.price))

                #no deposit
        else:
            debug_print("Agent {} decides not to buy it.".format(agent))

            if product_working:
                debug_print("Missed opportunity: the product was in working condition.")
            else:
                debug_print("Good call: the product was faulty.")

        #deposit the agent's independent earnings
        agent.balance += DAILY_EARNINGS

        #record the agent's balance
        daily_balance.append(agent.balance)

        debug_print("Day {}:\t{}".format(d+1, agent.balance))

    return daily_balance


def debug_print(text):
    if DEBUG:
        print(text)


def main():
    #TODO: change this to the last four digits of your A#
    last_four_digits = 1234

    seeds = [0, 1, 2, 3, 4, 5, 6, 7, 8, last_four_digits]

    market_odds = FAVORABLE

    #The average value on a given day for a given agent.
    #i.e. averages["FC"][10] to get FC's average on the eleventh day.
    averages = OrderedDict()

    for seed in seeds:
        agents = [
            FlipCoinAgent("FC", seed),
            HalfProbAgent("HP"),
            PercentBeliever("PB0", 0),
            PercentBeliever("PB25", 25),
            PercentBeliever("PB50", 50),
            PercentBeliever("PB75", 75),
            PercentBeliever("PB100", 100),
            #Agent1234("1234")
        ]
        for agent in agents:
            debug_print("Simulating Agent: {}".format(agent))

            #run the simulation
            daily_balance = no_learning_case(agent, market_odds, seed)

            if not agent.id in averages:
                averages[agent.id] = []

            for d in xrange(0, NUM_DAYS):
                if len(averages[agent.id]) < d+1:
                    averages[agent.id].append(0)
                averages[agent.id][d] += daily_balance[d]/len(seeds)

    table_header = "Day"
    for agent_id in averages.keys():
        table_header += "\t{}".format(agent_id)
    print(table_header)

    for d in xrange(0, NUM_DAYS):
        table_row = "{}".format(d+1)
        for agent_id in averages.keys():
            table_row += "\t{}".format(averages[agent_id][d])
        print(table_row)


#invoke the "main" function when this module is run on its own
if __name__ == "__main__":
    main()
