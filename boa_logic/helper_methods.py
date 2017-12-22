
import itertools
import math

import pandas
from pandas import Series
from boa_logic import dependence_object


class HelperMethods:

    @staticmethod
    def make_frequency_histogram(series):

        index = []
        values = []
        for x in range(series.min(), series.max() + 1):
            index.append(x)
            values.append(0)

        histogram = Series(data=values, index=index)
        for x in series:
            histogram.at[x] += 1
        return histogram

    @staticmethod
    def turn_prices_into_changes(series, permille):

        price_change_series = Series([])
        if permille:
            for x in range(1, series.size):
                price_change_series[x] = int(1000*((series.values[x]) - (series.values[x - 1]))/series.values[x-1])
            return price_change_series
        else:
            for x in range(1, series.size):
                price_change_series[x] = int(series.values[x] - series.values[x-1])
            return price_change_series

    @staticmethod
    def make_cumulative_probability_density_function(series):

        # sum of all records
        total_records = 0.0
        for x in series:
            total_records += x

        # go through and make cumulative probability density function
        values = []
        prob_sum = 0.0
        for x in series:
            prob_sum += 100*x
            values.append(prob_sum / total_records)
        return Series(values, series.index.values)

    @staticmethod
    def find_deciles(series):

        deciles_observed = [100,100,100,100,100,100,100,100,100]
        values_observed = [0,0,0,0,0,0,0,0,0]

        for x in series:
            for i in range(1,10):
                if abs(i*10-x) < abs(i*10-deciles_observed[i-1]):
                    deciles_observed[i-1] = x
                    values_observed[i-1] = series[series == x].index[0]
        return deciles_observed, values_observed

    @staticmethod
    def find_matching_deciles(series, values):

        counter = 0
        deciles = [100, 100, 100, 100, 100, 100, 100, 100, 100]
        for x in values:
            deciles[counter] = series[x] if x in series else 100 if x > 0.0 else 0
            counter += 1
        return deciles

    @staticmethod
    def convert_to_decile_gaps(list):

        decile_gaps = []
        for x in range(1,len(list)):
            decile_gaps.append(list[x]-list[x-1])
        return decile_gaps

    def split_in_two(self, series):

        half_way_point = int(series.size/2)
        first_half = series.iloc[:half_way_point]
        second_half = series.iloc[half_way_point:]

        return first_half, second_half;

    def divide_even_and_odd(self, series):

        even_half = Series([])
        odd_half = Series([])

        even = True
        for x in range(0,series.size):
            if even:
                even_half[x/2] = series.values[x]
            else:
                odd_half[(x-1)/2] = series.values[x]
            even = not even

        return even_half, odd_half;

    def split_histogram_around_zero(self, series):

        larger_value = series.index.values.max() if abs(series.index.values.max()) > abs(series.index.values.min()) else abs(series.index.values.min())
        left_half = [None] * (larger_value-1)
        right_half = [None] * (larger_value-1)

        for x in range(1,larger_value):
            right_half[x - 1] = 0 if series.get(x) is None else series.get(x)
            left_half[x - 1] = 0 if series.get(x * -1) is None else series.get(x * -1)

        return left_half, right_half;

    def remove_outliers(self, series):
        return series[~((series - series.mean()).abs() > 3 * series.std())]

    def up_down_generator(self, number):
        return 1 if number < 0 else 2

    def calculate_transition_matrices(self, orders_of_magnitude, series):

        n_gram_matrix = {}
        magnitude_matrix = {}
        n_gram_matrix_list = []
        independent_matrix = {}
        independent_matrix_list = []
        final_total_entries = series.size - orders_of_magnitude

        #go through prices
        for x in range(0, final_total_entries):

            #for loop to build 1,2,1 etc pattern
            pattern = ""
            for i in range(orders_of_magnitude):
                pattern += str(self.up_down_generator(series.values[i + x]))

            n_gram_matrix[pattern] = (n_gram_matrix[pattern] + 1) if pattern in n_gram_matrix else 1

            current_val = series.values[orders_of_magnitude-1 + x]
            magnitude_matrix[pattern] = magnitude_matrix[pattern] + current_val if pattern in magnitude_matrix else current_val

        # build all possible permutations
        permutations = []
        for i in list(itertools.product(range(1, 3), repeat=orders_of_magnitude)):
            permutations.append(''.join(tuple(map(str, i))))

        #build all possible permutations - 1
        lead_up_permutations = []
        for i in list(itertools.product(range(1, 3), repeat=orders_of_magnitude-1)):
            lead_up_permutations.append(''.join(tuple(map(str, i))))

        # build independent matrix
        for i in list(itertools.permutations(range(orders_of_magnitude+1))):
            temp_pattern = ""
            for j in range(orders_of_magnitude):
                temp_pattern += str(self.up_down_generator(i[j] - i[j+1]))
            independent_matrix[temp_pattern] = independent_matrix[temp_pattern] + 1 if temp_pattern in independent_matrix else 1

        # convert series values to list
        for i in permutations:
            n_gram_matrix_list.append(n_gram_matrix[i]) if i in n_gram_matrix else n_gram_matrix_list.append(0.0)
            independent_matrix_list.append((independent_matrix[i]/math.factorial(orders_of_magnitude+1))*final_total_entries)
            independent_matrix[i] = ((independent_matrix[i]/math.factorial(orders_of_magnitude+1))*final_total_entries)
            magnitude_matrix[i] = magnitude_matrix[i]/n_gram_matrix[i] if i in magnitude_matrix and i in n_gram_matrix else 0.0

        return dependence_object.DependenceObject(n_gram_matrix, magnitude_matrix, independent_matrix,final_total_entries, n_gram_matrix_list, independent_matrix_list,lead_up_permutations)

    def turn_matrix_into_percent(self, list):

        return_matrix = []
        total = 0

        for item in list:
            total += item

        for item in list:
            return_matrix.append(float('%.2f'%(100*item/total)))

        return return_matrix

    def parse_csv(self, link):
        dataFrame = pandas.read_csv(link, index_col=False)
        return pandas.Series(dataFrame['price(USD)'].values, index=dataFrame['date'])



