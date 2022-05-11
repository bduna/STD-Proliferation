import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from person import Person
from config import *


class Simulation():

    def __init__(self, num_rounds):
        self.num_rounds = num_rounds
        self.population = [Person() for _ in range(POP_SIZE)]
        self.curr_infect_rate = self.calc_infect_rate()
        self.infect_rate_hist = [self.curr_infect_rate]
        print('Infection Rate Growth Over Time...')
        print('Initial Infection Rate: {:.2%}'.format(self.curr_infect_rate))

    def calc_infect_rate(self):
        # Count infections to calculate infection rate.
        infect_cnt = sum(map(lambda p: p.is_infected, self.population))
        infect_rate = infect_cnt/POP_SIZE
        return infect_rate

    def sexual_encounter(self, partner_1, partner_2):
        # One partner is infected with an STD and the other isn't.
        if ((partner_1.is_infected and not partner_2.is_infected) or 
            (partner_2.is_infected and not partner_1.is_infected)):
            if partner_1.is_infected:
                # Infect partner two if current infection rate is below
                # partner two's safe-sex threshold.
                if self.curr_infect_rate < partner_2.ss_thresh:
                    partner_2.is_infected = True
            else:
                # Infect partner one if current infection rate is below
                # partner one's safe-sex threshold.
                if partner_2.is_infected:
                    if self.curr_infect_rate < partner_1.ss_thresh:
                        partner_1.is_infected = True


    def simulate_round(self, round_num):
        sexual_partners = list(np.random.choice(self.population, 
                                    size=2*NUM_SEXUAL_ENCOUNTERS,
                                    replace=False))
        group_1 = sexual_partners[:-NUM_SEXUAL_ENCOUNTERS]
        group_2 = sexual_partners[NUM_SEXUAL_ENCOUNTERS:]
        for partner_1, partner_2 in zip(group_1, group_2):
            self.sexual_encounter(partner_1, partner_2)
        self.curr_infect_rate = self.calc_infect_rate()
        self.infect_rate_hist.append(self.curr_infect_rate)
        print('Round #{}: {:.2%}'.format(round_num, self.curr_infect_rate))

    def run_simulation(self):
        for i in range(self.num_rounds):
            self.simulate_round(i+1)

    def plot_infect_rate_hist(self):
        x = np.arange(self.num_rounds+1)
        y = np.array(self.infect_rate_hist)

        def logistic(x, x_0, L, k):
            return L/(1+np.exp(-k*(x-x_0)))

        popt, pcov = curve_fit(logistic, x, y)
        inflection_round = int(popt[0])
        infect_rate_asymptote = popt[1]
        plt.title('Population STD Proliferation')
        plt.text(90, 0.25, f'Inflection Point: Round #{inflection_round}')
        plt.text(90, 0.2, 'Infection Rate Asymptote: {:.1%}'.format(infect_rate_asymptote))
        plt.scatter(x, y)
        plt.plot(x, logistic(x, *popt), 'r-')
        plt.xlabel('Round #')
        plt.ylabel('% Population Infected')
        plt.xlim(left=0)
        plt.ylim(bottom=0)
        plt.axvline(inflection_round)
        plt.axhline(infect_rate_asymptote)
        plt.savefig('plots/infection_rate_plot.jpg')
        plt.show()

if __name__ == '__main__':
    num_rounds = 200
    simulation = Simulation(num_rounds)
    simulation.run_simulation()
    simulation.plot_infect_rate_hist()

    