

class EmailCreator():

    def return_contents(self, filename):
        with open(filename, 'r') as myfile:
            return myfile.read().replace('\n', '')

    def make_email(self, coins):

        html = ""
        for coin in coins:

            #email above and below
            email_body = '''<tr>
                        <td bgcolor="#ffffff" align="center" valign="top" style="padding: 10px;">
                            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                                <tr>
                                    <!-- Column : BEGIN -->
                                    <td width="33.33%" class="stack-column-center">
                                        <table role="presentation" cellspacing="0" cellpadding="0" border="0">
                                            <tr>
                                                <td style="padding: 10px; text-align: center">
                                                    <img src="https://files.coinmarketcap.com/static/img/coins/128x128/''' + coin.get_name() +'''.png" width="170" height="170" alt="alt_text" border="0" class="fluid" style="height: auto; background: #dddddd; font-family: sans-serif; font-size: 15px; line-height: 140%; color: #555555;">
                                                </td>
                                            </tr>
                                            <tr>
                                                <td style="font-family: sans-serif; font-size: 15px; line-height: 140%; color: #555555; padding: 0 10px 10px; text-align: left;" class="center-on-narrow">
                                                    <p style="margin: 0;">'''

            email_body2 = '''</td>
                                               </tr>
                                           </table>
                                       </td>
                                       <!-- Column : END -->
                                   </tr>
                               </table>
                           </td>
                       </tr>'''

            #coin analysis

            tldr_val = coin.get_prediction_plus(
                coin.get_most_recent_pattern()) if coin.get_stationarity() else coin.get_stationarity_as_string()
            html += '''
                            <h2> ''' + coin.get_name() + '''</h2>

                                <h4>
                                    <b> TL;DR: ''' + tldr_val + '''</b>
                                </h4>
                                <ul>
                                    <li><b>''' + coin.get_stationarity_as_string() + '''</b>, with a Chi-Square sigma of ''' + coin.get_stat_sigma() + '''
                                    and a Chi-Square critical value of ''' + coin.get_stat_critical_value() + '''</li>
                                    <li><b>''' + coin.get_randomness_as_string() + '''ly</b> distributed, with a Chi-Square sigma of 
                                        ''' + coin.get_rand_sigma() + ''' and a Chi-Square critical value of ''' + coin.get_rand_critical_value() + '''
                                    <li><b>''' + coin.get_independence_as_string() + '''</b>, with a Chi-Square sigma of ''' + coin.get_ind_sigma() + '''
                                    and a Chi-Square critical value of ''' + coin.get_ind_critical_value() + '''</li>
                                </ul>



                                <p>After analysing the price history, BOA concluded that there is a <b>''' + '%.2f' % coin.get_odds_of_increase(
                coin.get_most_recent_pattern()) + '''%</b>
                                chance price will go up, and a <b>''' + '%.2f' % coin.get_odds_of_decrease(
                coin.get_most_recent_pattern()) + '''%</b>
                                chance price will go down. The average magnitude of the up move is <b>''' + '%.2f' % coin.get_magnitude_of_increase(
                coin.get_most_recent_pattern()) + '''%</b>
                                and the average magnitude of the down move is <b>''' + '%.2f' % coin.get_magnitude_of_decrease(
                coin.get_most_recent_pattern()) + '''%</b>.
                                Today, you should <b>''' + coin.get_prediction_plus(coin.get_most_recent_pattern()) + '''</b>.
                                </p>
                                <br/>
                '''

        return self.return_contents('email-a.txt') + html + self.return_contents('email-b.txt')