

class DependenceObject:

    def __init__(self, n_gram_matrix, magnitude_matrix, independence_matrix, final_total_entries, n_gram_matrix_list, independence_matrix_list, lead_up_patterns):
        self.n_gram_matrix = n_gram_matrix
        self.magnitude_matrix = magnitude_matrix
        self.independence_matrix = independence_matrix
        self.final_total_entries = final_total_entries
        self.n_gram_matrix_list = n_gram_matrix_list
        self.independence_matrix_list = independence_matrix_list
        self.lead_up_patterns = lead_up_patterns


    def get_n_gram_matrix(self):
        return self.n_gram_matrix

    def get_magnitude_matrix(self):
        return self.magnitude_matrix

    def get_independence_matrix(self):
        return self.independence_matrix

    def get_n_gram_matrix_at(self, pattern):
        return self.n_gram_matrix[pattern] if pattern in self.n_gram_matrix else 0.0

    def get_magnitude_matrix_at(self, pattern):
        return float('%.2f' % (float(self.magnitude_matrix[pattern])/10.0)) if pattern in self.magnitude_matrix else 0.0

    def get_independence_matrix_at(self, pattern):
        return float('%.2f' % self.independence_matrix[pattern]) if pattern in self.independence_matrix else 0.0

    def get_n_gram_matrix_percent_at(self, pattern):
        return float('%.2f' % (100.0 * self.n_gram_matrix[pattern]/self.final_total_entries)) if pattern in self.n_gram_matrix else 0.0

    def get_independence_matrix_percent_at(self, pattern):
        return float('%.2f' % (100.0 * self.independence_matrix[pattern]/self.final_total_entries)) if pattern in self.independence_matrix else 0.0

    def get_n_gram_matrix_list(self):
        return self.n_gram_matrix_list

    def get_independence_matrix_list(self):
        return self.independence_matrix_list

    def get_lead_up_patterns(self):
        return self.lead_up_patterns

    @staticmethod
    def pattern_as_arrows(pattern):
        html_return = ""
        for i in pattern:
            html_return += "&#x1f856" if i is "1" else "&#x1f855"
        return html_return



