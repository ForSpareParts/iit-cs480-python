CS480 Project
=============

This is a port of the CS480 project to Python. There are a few differences between the Java and Python versions, the two most noticeable being:

- There is no Bank class in the Python port. The point of the Bank class was to hide the Agent's balance behind a private variable, to prevent tampering. Since Python has no private variables, we might as well make the balance a property of the agent.

- The simulator is not contained within a class -- instead, it's just a module. The simulator isn't really object-oriented, and Python doesn't require us to wrap everything in a class, so there's no use for a class here.

To run the project
------------------

You need to run the simulator as a module for the relative imports in the project to work. To do that, run the following code *from the repository directory*:

    python -m phase1.master.simulator

or, for phase 2,

    python -m phase1.master.simulator path/to/data/file.csv

The simulator will output the performance of all the agents as a tab-separated chart, which you should be able to open in a spreadsheet program. For convenience, you can pipe the output to a file, e.g.:

    python -m phase1.master.simulator >> my_output.csv

To add your own agent
---------------------

Create an agent class in a file in phase1/agents, that imports from Agent. Model it after another agent (like FlipCoinAgent) to get the import syntax right. Once you've implemented your agent, make sure to add an import for it in:

    phase1/agents/__init__.py

Otherwise, the simulator won't be able to see it.

Once you've done that, you can add it to the list of agents in simulator.py -- instantiate it like the other agents in the list.