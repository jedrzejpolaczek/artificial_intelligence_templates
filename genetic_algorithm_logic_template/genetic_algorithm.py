"""
The module contains functionality needed to run genetic algorithm with calculation of chromosomes in separate threads.
"""
import concurrent.futures
import random

from loguru import logger

import gom.genetic_logic.functions_interface as genetic_interface
from gom.genetic_logic import helper_functions as helper


class GeneticAlgorithm(object):
    def __init__(self, genetics: genetic_interface.GeneticFunctionsInterface):
        """
        Construct object of GeneticAlgorithm.

        :param genetics: implementation of interface GeneticFunctions.

        :return GeneticAlgorithm: instance of class GeneticAlgorithm.
        """
        self.genetics = genetics
        self.initial_population = None
        self.dict_pop = dict()
        self.fitness_and_chromosomes = list()
        self.best_solution = None

    @helper.print_method_run_time
    def run(self) -> list:
        """
        Run computing for genetic algorithm.

        :return list: of most suitable solutions for the issue.

        """
        logger.debug('Creating population.')
        population = self.genetics.generate_initial_population()
        self.initial_population = population
        logger.debug('Start genetic algorithm.')
        population = self._evolve(population)
        logger.debug('Stop genetic algorithm.')
        return population

    @helper.print_method_run_time
    def _evolve(self, population) -> list:
        """
        Perform main loop of calculations for genetic algorithm
        and remember best solution overall till current generation.

        :return list: population with fitness value for each chromosome.

        """
        while True:
            self._fulfill_list_of_chromosomes_with_their_fitness_value(population)
            helper.print_best_five(self.fitness_and_chromosomes)
            if self.genetics.check_stop_conditions(self.fitness_and_chromosomes):
                logger.debug('Stop conditions pass.')
                # helper.print_best_five(self.fitness_and_chromosomes)
                break
            self._remember_best(self.fitness_and_chromosomes)
            population = self._generate_next_population(self.fitness_and_chromosomes)
        return population

    def _remember_best(self, fitness_and_chromosomes: list) -> None:
        """
        Check if best chromosome from current population is the best over all by compering it with previous best one.

        :param fitness_and_chromosomes: list of (fitness_value, chromosome)
        """
        if self.best_solution:
            if fitness_and_chromosomes.sort()[0][0] > self.best_solution[0]:
                self.best_solution = fitness_and_chromosomes.sort()[0][0]

    @helper.print_method_run_time
    def _fulfill_list_of_chromosomes_with_their_fitness_value(self, population):
        """
        Fulfilling list of pairs chromosomes with their fitness value.

        :param population: list of chromosomes in population.
        """
        self.fitness_and_chromosomes = list()

        if self.genetics.number_of_threads < 2:
            for index in range(len(population)):
                logger.debug(f"Start calculations for chromosome number {index+1}.")
                self.fitness_and_chromosomes.append((self.genetics.count_fitness(population[index]), population[index]))
        else:
            last_max_range = 0
            new_max_range = 0
            step = self.genetics.number_of_threads
            for _ in range(0, len(population), step):
                with concurrent.futures.ThreadPoolExecutor(max_workers=self.genetics.number_of_threads) as executor:
                    new_max_range = new_max_range + self.genetics.number_of_threads
                    if new_max_range > len(population):
                        new_max_range = len(population)
                    for index in range(last_max_range, new_max_range):
                        logger.debug(f"Start calculations for chromosome number {last_max_range + index + 1}.")
                        result = executor.submit(self.genetics.count_fitness, population[index])
                        self.fitness_and_chromosomes.append((result.result(), population[index]))
                last_max_range = new_max_range

    @helper.print_method_run_time
    def _generate_next_population(self, fitness_of_chromosomes: list) -> list:
        """
        Generating next generation of population.

        :param fitness_of_chromosomes: list of (fitness_value, chromosome).

        :return list: new population.

        """
        parents_generator = self.genetics.choose_parents(fitness_of_chromosomes)
        size = len(fitness_of_chromosomes)
        next_generation = []
        logger.debug('Start generating next population.')
        while len(next_generation) < size:
            parents = next(parents_generator)
            cross = random.random() < self.genetics.probability_crossover
            children = self.genetics.crossover(parents) if cross else parents
            for chromosome in children:
                mutate = random.random() < self.genetics.probability_mutation
                next_generation.append(self.genetics.mutate(chromosome) if mutate else chromosome)
        return next_generation[0:size]
