import argparse
import csv
from collections import OrderedDict
from random import Random, shuffle

from ..agents import *
from .product import Product


#: Number of days
NUM_DAYS = 1000

#:The cap on the maximum value of the product
MAXIMUM_VALUE = 100000

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
        agent:  Agent to simulate.
        seed:   Seed for the random number generator. If None/default, the
                system time is used.
    """

    rand = Random(seed)

    agent.balance = INITIAL_MONEY
    daily_balance = []

    debug_print("Seed={}".format(seed))

    for d in range(0, NUM_DAYS):
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


def learning_case(agent, training_instances, test_instances, seed):
    rand = Random(seed)

    agent.balance = INITIAL_MONEY
    daily_balance = []

    debug_print("Seed={}".format(seed))
    debug_print("Agent is learning...")
    agent.learn(training_instances)
    debug_print("Agent has completed the learning process")

    for index, instance in enumerate(test_instances):
        debug_print("Product#: {}".format(index+1))
        debug_print("The balance at the beginning of the day is: {}".format(
            agent.balance))

        max_value = min(agent.balance, MAXIMUM_VALUE)
        value = rand.random()*max_value
        price = rand.random()*value

        prod = Product(value, price)
        debug_print("Product is {}".format(prod))

        #determine the working condition
        working_condition = instance[len(instance) - 1]
        product_working = working_condition == 'G'

        #then create a features list for the agent, omitting the condition
        #(this is a copy of a slice of the instance list, all but the last value)
        features = instance[:len(instance) - 1]

        will_buy = agent.will_buy_given_features(prod, features)

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

        debug_print("Day {}:\t{}".format(index+1, agent.balance))

    return daily_balance


def read_instances(product_data):
    data_reader = csv.reader(product_data)
    instances = []

    #strip out the header line
    data_reader.next()

    for line in data_reader:
        instances.append(line)

    return instances


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


def main():
    #TODO: change this to the last four digits of your A#
    last_four_digits = 1234

    seeds = [0, 1, 2, 3, last_four_digits]

    parser = argparse.ArgumentParser(
        description='Run the agent simulation on a given product input file.')

    parser.add_argument(
        'product_data',
        type=argparse.FileType('r'),
        help='The file to read products from.')

    cmd_args = parser.parse_args()
    all_instances = read_instances(cmd_args.product_data)
    shuffle(all_instances)

    #all_instances contains a randomly ordered list of all training instances
    #each instance is a list -- all features, followed by a 'G' or 'B' to
    #indicate condition

    fold_size = len(all_instances)/len(seeds)

    #The average value on a given day for a given agent.
    #i.e. averages["FC"][10] to get FC's average on the eleventh day.
    averages = OrderedDict()

    for seed_index, seed in enumerate(seeds):
        #divide instances into test and training data
        test_instances = []
        training_instances = []

        for i in range(len(all_instances)):
            if (i >= fold_size * seed_index) and \
                    i < fold_size * (seed_index + 1):
                test_instances.append(all_instances[i])
            else:
                training_instances.append(all_instances[i])

        #initialize the agents we'll be simulating
        agents = [
            RationalBaselineAgent("RB"),
            #Agent1234("1234")
        ]
        for agent in agents:
            debug_print("Simulating Agent: {}".format(agent))

            #run the simulation
            daily_balance = learning_case(
                agent, training_instances, test_instances, seed)

            if not agent.id in averages:
                averages[agent.id] = []

            for d in range(0, len(test_instances)):
                if len(averages[agent.id]) < d+1:
                    averages[agent.id].append(0)
                averages[agent.id][d] += daily_balance[d]/len(test_instances)

    table_header = "Day"
    for agent_id in averages.keys():
        table_header += "\t{}".format(agent_id)
    print(table_header)

    for d in range(0, len(test_instances)):
        table_row = "{}".format(d+1)
        for agent_id in averages.keys():
            table_row += "\t{}".format(averages[agent_id][d])
        print(table_row)


#invoke the "main" function when this module is run on its own
if __name__ == "__main__":
    main()
