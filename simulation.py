import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from person import Person
from config import *


class Simulation():

    def __init__(self, number_of_rounds):
        self.number_of_rounds = number_of_rounds
        self.population = [Person() for _ in range(POPULATION_SIZE)]
        self.current_infection_rate = self.calculate_infection_rate()
        print('Infection Rate Growth...')
        print(self.current_infection_rate)
        self.infection_rate_history = [self.current_infection_rate]

    def calculate_infection_rate(self):
        # Count infections to calculate infection rate.
        infected_count = sum(list(map(lambda p: p.is_infected, self.population)))
        infection_rate = infected_count/POPULATION_SIZE
        return infection_rate

    def sexual_encounter(self, partner_one, partner_two):
        # One partner is infected with an STD and the other isn't.
        if ((partner_one.is_infected and not partner_two.is_infected) or 
            (partner_two.is_infected and not partner_one.is_infected)):
            if partner_one.is_infected:
                # Infect partner two if current infection rate is below
                # partner two's safe-sex threshold.
                if self.current_infection_rate < partner_two.safe_sex_threshold:
                    partner_two.is_infected = True
            else:
                # Infect partner one if current infection rate is below
                # partner one's safe-sex threshold.
                if partner_two.is_infected:
                    if self.current_infection_rate < partner_one.safe_sex_threshold:
                        partner_one.is_infected = True


    def simulate_round(self):
        sexual_partners = list(np.random.choice(self.population, 
                                    size=2*NUMBER_OF_SEXUAL_ENCOUNTERS,
                                    replace=False))
        group_one = sexual_partners[:-NUMBER_OF_SEXUAL_ENCOUNTERS]
        group_two = sexual_partners[NUMBER_OF_SEXUAL_ENCOUNTERS:]
        for partner_one, partner_two in zip(group_one, group_two):
            self.sexual_encounter(partner_one, partner_two)
        self.current_infection_rate = self.calculate_infection_rate()
        self.infection_rate_history.append(self.current_infection_rate)
        print(self.current_infection_rate)

    def run_simulation(self):
        for _ in range(self.number_of_rounds):
            self.simulate_round()

    def plot_infection_rate_history(self):
        x = np.array(range(self.number_of_rounds+1))
        y = np.array(self.infection_rate_history)

        def logistic(x, x_0, L, k):
            return L/(1+np.exp(-k*(x-x_0)))

        popt, pcov = curve_fit(logistic, x, y)
        plt.scatter(x, y)
        plt.plot(x, logistic(x, *popt), 'r-')
        plt.axvline(popt[0])
        plt.axhline(popt[1])
        plt.axhline(0)
        plt.show()

if __name__ == '__main__':
    number_of_rounds = 200
    simulation = Simulation(number_of_rounds)
    simulation.run_simulation()
    simulation.plot_infection_rate_history()

    