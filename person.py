from scipy.stats import bernoulli, uniform
from config import *

class Person():

    def __init__(self):
        self.is_infected = bool(bernoulli.rvs(INITIAL_INFECTION_RATE))
        alpha = uniform.rvs(0, MAX_ALPHA)
        beta = -uniform.rvs(0, MAX_ABSOLUTE_BETA)
        self.safe_sex_threshold = alpha/(alpha-beta) if alpha > beta else 0