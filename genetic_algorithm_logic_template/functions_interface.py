"""The module contains interface for all base functionality for genetic algorithms."""
import abc


class GeneticFunctionsInterface(abc.ABC):
    """Interface for all functions genetic algorithms need to work."""

    def __init__(self):
        self.sequence_run = True

    @abc.abstractmethod
    def probability_crossover(self) -> float:
        """
        Returns rate of occur crossover (0.0-1.0)

        :return float: probability of crossover.
        """

    @abc.abstractmethod
    def probability_mutation(self) -> float:
        """
        Returns rate of occur mutation (0.0-1.0)

        :return float: probability of mutation.
        """

    @abc.abstractmethod
    def generate_initial_population(self) -> list:
        """
        Returns list of initial population.

        :return list: initial population.
        """

    @abc.abstractmethod
    def count_fitness(self, chromosome: list) -> int:
        """
        Returns domain fitness value of chromosome.

        :param chromosome: one individual from the population.

        :return int: fitness value of chromosome.

        """

    @abc.abstractmethod
    def check_stop_conditions(self, fitness_and_chromosomes: list) -> bool:
        """
        Check stop conditions and stop run if returns True.

        :param fitness_and_chromosomes: list of (fitness_value, chromosome).

        :return bool: containing population for genetic algorithm.
        """

    @abc.abstractmethod
    def choose_parents(self, fitness_and_chromosomes: list) -> (list, list):
        """
        Choosing future parents to crossover.

        :param fitness_and_chromosomes: list of (fitness_value, chromosome).

        :return list, list: two chromosome typed to be a parents.
        """

    @abc.abstractmethod
    def crossover(self, parents: (list, list)) -> (list, list):
        """
        Breed children.

        :param parents: two list two crossover.

        :return list, list: two children from crossover parents.
        """

    @abc.abstractmethod
    def mutate(self, chromosome: list) -> list:
        """
        Mutate chromosome.

        :param chromosome: one individual from the population.

        :return list: mutated chromosome.
        """
