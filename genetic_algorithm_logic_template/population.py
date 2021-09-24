"""
Module contains functionality for creating, using and maintaining population for population for genetic algorithm.

To create an dictionary of population we need a configuration file for the population.
The configuration file should consist dictionary with the name of the parameter as a key and list of bottom for range,
top for range and step as value.
Explanation:
    Bottom for range - value from which we start counting (inclusive)
    Top for range - value to which we stop counting (inclusive)
    Step - step by which we are moving e.g. for percentages, step 5 gives the results 5, 10, 15, 20, 25, etc.
    Mutation - how big mutation is.

Example:
    Configuration dictionary may look like these
    >>>configuration_dictionary =
    >>>{'param1': [10, 90, 5, 4],  # we start counting percentage from 10% and stop on 90% with step of 5%
    >>> 'param2': [10, 80, 10, 2],  # we start counting degrees from 10 and stop on 80 with step of 10
    >>> 'param3': [1, 3, 1, 1],  # we have three possible geometries, step is 1 to not "jump over" of any of them
    >>> 'param4': [1, 2, 1, 1]}  # we have two possible materials, step is 1 to not "jump over" of any of them

"""

import itertools
import time

from loguru import logger


def generate_population(configuration: dict) -> list:
    """
    Generate population of chromosome for genetic algorithm.

    Based on the configuration for the population from the configuration file.

    :param configuration: Dictionary with configuration consist with the name of the parameter as a key and
                    list of bottom for range, top for range and step as value.

    :return list: containing population for genetic algorithm

    Example: To create population we need to load parameters from configuration file. We can do it in that way:
        >>>from gom.genetic_logic import population
        >>>dummy_configuration_dictionary = {"Parameter": [0, 10, 2, 1]}
        >>>dummy_population = population.generate_population(dummy_configuration_dictionary)
        >>># Population has been created and stored in dummy_population variable!

    """
    validate_configuration_dictionary(configuration)

    algorithm_start = time.perf_counter()
    population = []
    parameter_variation = []

    logger.debug('Creating population.')
    for key in configuration:
        parameter_min = configuration[key][0]
        parameter_max = configuration[key][1]
        parameter_step = configuration[key][2]
        for element in range(parameter_min, parameter_max, parameter_step):
            parameter_variation.append(element)
        population.append(parameter_variation)
        parameter_variation = []

    population = list(itertools.product(*population))
    [logger.debug(elem) for elem in population]
    algorithm_end = time.perf_counter()
    logger.debug(f'Size of population: {len(population)}')
    logger.debug("Time of generating population: {0:02f}s".format(algorithm_end - algorithm_start))

    return population


def validate_configuration_dictionary(configuration: dict) -> None:
    """
    Validate the configuration file and raise an exception when is invalid.

    :param configuration: Dictionary with configuration consist with the name of the parameter as a key and
                    list of bottom for range, top for range and step as value.

    :raise IOError: Raise exception if configuration file is invalid.

    """
    try:
        logger.debug(f"Validate configuration: {configuration}")
        for key in configuration:
            if len(configuration[key]) is not 4:
                raise ValueError(f'For {key} corrupted length.')
            for element in configuration[key]:
                if type(element) is not int:
                    raise ValueError(f'For "{element}" in "{key}" corrupted type.')
        logger.debug("Configuration dictionary is valid.")
    except ValueError as e:
        msg = f'Configuration dictionary is corrupted. {str(e)}'
        logger.error(msg)
        raise ValueError(msg)
