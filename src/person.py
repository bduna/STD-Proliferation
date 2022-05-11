from scipy.stats import bernoulli, uniform
from src.config import *

class Person():

    # Initializes both whether the person is infected at the 
    # start of the simulation and their alpha and beta 
    # parameters and then calculates their safe-sex threshold.
    def __init__(self):
        self.is_infected = bool(bernoulli.rvs(INITIAL_INFECTION_RATE))
        alpha = uniform.rvs(0, MAX_ALPHA)
        beta = -uniform.rvs(0, MAX_ABSOLUTE_BETA)
        self.safe_sex_threshold = alpha/(alpha-beta) if alpha > beta else 0