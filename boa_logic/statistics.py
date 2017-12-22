#!/usr/bin/python3

import plotly.graph_objs as go
from scipy.stats import chi2
import numpy.polynomial.polynomial as poly
from boa_logic import helper_methods, dependence_object


class Calculate_Stats:

    def __init__(self):
        self.helper = helper_methods.HelperMethods()
        self.dep_object = None

    def calculate_stationarity(self, series):

        first_half, second_half = self.helper.split_in_two(series)

        first_histogram = self.helper.make_frequency_histogram(first_half)
        second_histogram = self.helper.make_frequency_histogram(second_half)

        first_density_function = self.helper.make_cumulative_probability_density_function(first_histogram)
        second_density_function = self.helper.make_cumulative_probability_density_function(second_histogram)

        first_deciles, first_values = self.helper.find_deciles(first_density_function)
        second_deciles = self.helper.find_matching_deciles(second_density_function, first_values)

        critical_value, sigma = self.calculate_chi_squared(self.helper.convert_to_decile_gaps(first_deciles), self.helper.convert_to_decile_gaps(second_deciles))

        return (critical_value>sigma), sigma, critical_value;

    def calculate_differential_spectrum_independence(self, series):

        histogram = self.helper.make_frequency_histogram(series)

        left_half, right_half = self.helper.split_histogram_around_zero(histogram)

        index = []
        for i in range(0,left_half.__sizeof__()):
            index.append(i)

        critical_value, sigma = self.calculate_chi_squared(left_half,right_half)

        return (critical_value > sigma), sigma, critical_value;

    def calculate_relative_price_change_independence(self, series, orders_of_magnitude):
        self.dep_object = self.helper.calculate_transition_matrices(orders_of_magnitude, series)

        critical_value, sigma = self.calculate_chi_squared(self.dep_object.n_gram_matrix_list, self.dep_object.independence_matrix_list)

        return (critical_value > sigma), sigma, critical_value, self.dep_object;

    def calculate_chi_squared(self, list_1, list_2):

        observed_values = list_1
        expected_values = list_2

        sigma = 0
        for observed, expected in zip(observed_values, expected_values):
            next_value = 0 if expected == 0 else ((observed-expected)**2)/expected
            sigma += next_value

        degrees_of_freedom = (len(observed_values)-1)
        probability = .05
        critical_value = chi2.isf(probability,degrees_of_freedom)
        return critical_value, sigma;

    def calculate_randomness(self, series):
        even_half, odd_half = self.helper.divide_even_and_odd(series)

        even_histogram = self.helper.make_frequency_histogram(even_half)
        odd_histogram = self.helper.make_frequency_histogram(odd_half)

        first_density_function = self.helper.make_cumulative_probability_density_function(even_histogram)
        second_density_function = self.helper.make_cumulative_probability_density_function(odd_histogram)

        first_deciles, first_values = self.helper.find_deciles(first_density_function)
        second_deciles = self.helper.find_matching_deciles(second_density_function, first_values)

        critical_value, sigma = self.calculate_chi_squared(first_deciles,second_deciles)

        return (critical_value > sigma), sigma, critical_value;

    def calculate_trend_through_regression(self, series, degree):

        index = []
        for i in range(0,series.size):
            index.append(i)
        coefs = poly.polyfit(index, series.values, degree)
        print(coefs)

        return poly.polyval(index, coefs)
