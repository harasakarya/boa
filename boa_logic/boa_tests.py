from unittest import TestCase
from boa_logic import helper_methods, statistics
import pandas

class Test(TestCase):

    def setUp(self):
        self.helper_methods_object = helper_methods.HelperMethods()
        self.stat_object = statistics.Calculate_Stats()
        self.test_data = self.helper_methods_object.parse_csv("test-data.csv")
        self.test_data_delta = self.helper_methods_object.turn_prices_into_changes(self.test_data, False)
        self.first_half_delta, self.second_half_delta = self.helper_methods_object.split_in_two(self.test_data_delta)

        self.first_half, self.second_half = self.helper_methods_object.split_in_two(self.test_data)
        self.first_freq = self.helper_methods_object.make_frequency_histogram(self.first_half)
        self.second_freq = self.helper_methods_object.make_frequency_histogram(self.second_half)

        self.first_cum = self.helper_methods_object.make_cumulative_probability_density_function(self.first_freq)
        self.second_cum = self.helper_methods_object.make_cumulative_probability_density_function(self.second_freq)
        self.is_stationary, self.stat_sigma, self.stat_critical_value = self.stat_object.calculate_stationarity(self.test_data)
        self.is_diff_independent, self.di_sigma, self.di_critical_value = self.stat_object.calculate_differential_spectrum_independence(
            self.test_data_delta)
        self.is_rel_independent, self.ri_sigma, self.ri_critical_value, self.dep_object= self.stat_object.calculate_relative_price_change_independence(
        self.test_data_delta, 2)
        self.is_rel_independent3, self.ri_sigma3, self.ri_critical_value3, self.dep_object = self.stat_object.calculate_relative_price_change_independence(
            self.test_data_delta, 3)

        self.is_random, self.rand_sigma, self.rand_critical_value = self.stat_object.calculate_randomness(self.test_data)


    def test_a_parse_csv(self):
        self.assertAlmostEqual(self.test_data.count(), 199)
        self.assertAlmostEqual(self.test_data.mean(), 7.924623115577889)
        self.assertAlmostEqual(self.test_data.std(), 4.3968936157646414)

        print("1. PARSING WORKS - Parsing Data to CSV and checking mean, count, and stdev.\n")

    def test_b_split_in_two(self):
        self.assertAlmostEqual(self.first_half.count(), 99)
        self.assertAlmostEqual(self.first_half.mean(), 8.3131313131313131)
        self.assertAlmostEqual(self.first_half.std(), 4.5144811545542876)

        self.assertAlmostEqual(self.second_half.count(), 100)
        self.assertAlmostEqual(self.second_half.mean(), 7.54)
        self.assertAlmostEqual(self.second_half.std(), 4.2650091477396659)

        print("2. SPLITTING DATA WORKS - Splitting Data in two and checking mean, count, and stdev.\n")

    def test_c_make_frequency_histogram(self):
        index = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        values1 = [8,8,3,8,4,6,1,10,9,5,6,10,6,5,10]
        values2 = [10,7,6,4,8,10,4,7,9,5,8,7,5,6,4]

        self.assertEqual(True, self.first_freq.equals(pandas.Series(index=index, data=values1)))
        self.assertEqual(True, self.second_freq.equals(pandas.Series(index=index, data=values2)))

        print("3. FREQUENCY HISTOGRAM WORKS - Constructing Frequency Histograms and checking the values for validity.\n")

    def test_d_make_probability_density_function(self):
        index = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        values1=[8,16,19,27,31,37,38,48,58,63,69,79,85,90,100]
        values2=[10.0,17.0,23.0,27.0,35.0,45.0,49.0,56.0,65.0,70.0,78.0,85.0,90.0,96.0,100.0]

        self.assertEqual(True, self.second_cum.equals(pandas.Series(index=index, data=values2)))

        print("4. CUMULATIVE DENSITY FUNCTION WORKS - Constructing Cumulative Probability Density Functions and checking the values for validity.\n")

    def test_e_calculate_stationarity(self):

        self.assertEqual(True, self.is_stationary)
        self.assertEqual(6.729326789932845, self.stat_sigma)
        self.assertEqual(14.067140449340169, self.stat_critical_value)

        print("5. STATIONARITY WORKS - Using the Cumulative Probability Density Function of Artifical Prices to test stationarity, and checking values for validity.\n")

    def test_f_turn_price_data_into_permille_change(self):
        self.assertAlmostEqual(self.first_half_delta.count(), 99)
        self.assertAlmostEqual(self.first_half_delta.mean(), 0.060606060606060608)
        self.assertAlmostEqual(self.first_half_delta.std(), 6.4615316656097246)

        self.assertAlmostEqual(self.second_half_delta.count(), 99)
        self.assertAlmostEqual(self.second_half_delta.mean(), -0.13131313131313133)
        self.assertAlmostEqual(self.second_half_delta.std(), 6.157203288809276)

        print("6. PRICE CHANGE WORKS - Turning price data into price delta and checking mean, count, and stdev.\n")

    def test_g_calculate_differential_spectrum_independence(self):
        self.assertEqual(False, self.is_diff_independent)
        self.assertAlmostEqual(24.6662878788, self.di_sigma)
        self.assertAlmostEqual(21.0260698175, self.di_critical_value)

        print("7. DI INDEPENDENCE WORKS -  Using the Test Data Delta to check for differential spectrum independence, and checking values for validity.\n")

    def test_h_calculate_relative_price_change_independence(self):
        self.assertEqual(True, self.is_rel_independent)
        self.assertAlmostEqual(0.45408163265306123, self.ri_sigma)
        self.assertAlmostEqual(7.81472790325, self.ri_critical_value)

        print(
            "8. REL INDEPENDENCE WORKS -  Using the Test Data Delta to check for relative price change independence, and checking values for validity.\n")

    def test_i_calculate_relative_price_change_independence3(self):
        self.assertEqual(True, self.is_rel_independent3)
        self.assertAlmostEqual(4.409230769230769, self.ri_sigma3)
        self.assertAlmostEqual(14.067140449340169, self.ri_critical_value3)

        print(
            "9. REL INDEPENDENCE WORKS 2-  Using the Test Data Delta to check for relative price change independence, and checking values for validity.\n")
    def test_j_calculate_randomness(self):

        self.assertEqual(True, self.is_random)
        self.assertAlmostEqual(5.52400692728, self.rand_sigma)
        self.assertAlmostEqual(15.5073130559, self.rand_critical_value)

        print(
            "10. RANDOMNESS WORKS -  Using the Test Data to check for randomness, and checking values for validity.\n")
    pass
