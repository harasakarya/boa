from boa_logic import statistics, dependence_object, helper_methods
import plotly as py
import plotly.graph_objs as go


class CryptoObject:
    def __init__(self, name, price_series, degrees):
        self.stat_object = statistics.Calculate_Stats()
        self.helper = helper_methods.HelperMethods()

        # name and data
        self.name = name
        self.price_series = price_series
        self.degrees = degrees

        # price
        self.price_change = self.stat_object.helper.turn_prices_into_changes(self.price_series, permille=True)

        # statistical variables
        self.is_stationary, self.stat_sigma, self.stat_critical_value = self.stat_object.calculate_stationarity(
            self.price_change)
        self.is_random, self.rand_sigma, self.rand_critical_value = self.stat_object.calculate_randomness(
            self.stat_object.helper.remove_outliers(self.price_change))
        self.is_independent, self.ind_sigma, self.ind_critical_value, self.dep_object = \
            self.stat_object.calculate_relative_price_change_independence(
                self.stat_object.helper.remove_outliers(self.price_change), self.degrees)

    def get_time_period(self):
        return "{:,}".format(self.price_series.size) + " days"

    def get_name(self):
        return self.name

    def get_stationarity_as_string(self):
        return "stationary" if self.is_stationary else "not stationary"

    def get_stationarity(self):
        return self.is_stationary

    def get_stat_sigma(self):
        return '%.2f' % self.stat_sigma

    def get_stat_critical_value(self):
        return '%.2f' % self.stat_critical_value

    @staticmethod
    def get_likelihood(boolean):
        return "is likely" if boolean else "is not likely"

    def get_price_chart(self):
        trace = go.Scatter(x=self.price_series.index.values, y=self.price_series.values)
        url = py.offline.plot([trace], image_height=400, image_width=400, auto_open=False,
                              filename=self.name + '-price-chart.html')
        return url

    def get_randomness_as_string(self):
        return "random" if self.is_random else "not random"

    def get_randomness(self):
        return self.is_random

    def get_rand_sigma(self):
        return '%.2f' % self.rand_sigma

    def get_rand_critical_value(self):
        return '%.2f' % self.rand_critical_value

    def get_independence_as_string(self):
        return "independent" if self.is_independent else "dependent"

    def get_independence(self):
        return self.is_independent

    def get_ind_sigma(self):
        return '%.2f' % (self.ind_sigma)

    def get_ind_critical_value(self):
        return '%.2f' % (self.ind_critical_value)

    def get_most_recent_pattern(self):
        pattern = ""
        for i in range(1, self.degrees):
            pattern = str(self.helper.up_down_generator(self.price_change.values[i * -1])) + pattern
        return pattern

    def get_predictive_pattern(self):
        pattern = ""
        for i in range(1, self.degrees - 1):
            pattern = str(self.helper.up_down_generator(self.price_change.values[i * -1])) + pattern
        return pattern

    def as_arrows(self, pattern):
        return self.dep_object.pattern_as_arrows(pattern)

    def get_odds_of_decrease(self, pattern):
        try:
            down_value = float(
                100.0 * self.get_dep_object().get_n_gram_matrix_at(pattern + '1') / (
                    self.get_dep_object().get_n_gram_matrix_at(
                        pattern + '1') + self.get_dep_object().get_n_gram_matrix_at(
                        pattern + '2')))
        except:
            down_value = 0.0
        return down_value

    def get_odds_of_increase(self, pattern):
        try:
            up_value = float(
                100.0 * self.get_dep_object().get_n_gram_matrix_at(pattern + '2') / (
                    self.get_dep_object().get_n_gram_matrix_at(
                        pattern + '1') + self.get_dep_object().get_n_gram_matrix_at(
                        pattern + '2')))
        except:
            up_value = 0.0
        return up_value

    def get_magnitude_of_decrease(self, pattern):
        return float(self.get_dep_object().get_magnitude_matrix_at(pattern + '1'))

    def get_magnitude_of_increase(self, pattern):
        return float(self.get_dep_object().get_magnitude_matrix_at(pattern + '2'))

    def get_numeric_prediction(self, pattern):

        pos_base = (100.0 + self.get_magnitude_of_increase(
            pattern))/100.0
        pos_power = (self.get_odds_of_increase(pattern))
        neg_base = (100.0 + self.get_magnitude_of_decrease(
            pattern)) / 100.0
        neg_power = (self.get_odds_of_decrease(pattern))
        return ((pos_base**pos_power)*(neg_base**neg_power))

    def get_prediction_plus(self, pattern):
        pred = float('%.2f' %  self.get_numeric_prediction(pattern))
        return ("Buy("+ str(pred) + ")") if pred > 1.0 else ("Sell(" + str(pred) + ")")

    def get_prediction(self, pattern):
        pred = float('%.2f' %  self.get_numeric_prediction(pattern))
        return "Buy" if pred > 1.0 else "Sell"

    def get_dep_object(self):
        return self.dep_object

    def get_most_recent_date(self):
        return self.price_series.index.values[-1]
