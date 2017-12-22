from boa_logic import statistics, crypto_object, scraper, candlesticks
import datetime
import html
import pandas
from datetime import datetime as dt
from matplotlib import pyplot



def main():
    stat_object = statistics.Calculate_Stats()
    now = datetime.datetime.now()
    scrape_obj = scraper.Scraper()
    candle_btc = candlesticks.CandleSticks("BTC-USD")
    candle_eth = candlesticks.CandleSticks("ETH-USD")
    candle_ltc = candlesticks.CandleSticks("LTC-USD")

    try:
        # btc_series = http://api.bitcoincharts.com/v1/csv/coinbaseUSD.csv.gz
        btc_series = stat_object.helper.parse_csv('https://coinmetrics.io/data/btc.csv')
        eth_series = stat_object.helper.parse_csv("https://coinmetrics.io/data/eth.csv")
        dash_series = stat_object.helper.parse_csv("https://coinmetrics.io/data/dash.csv")
        xmr_series = stat_object.helper.parse_csv("https://coinmetrics.io/data/xmr.csv")
        ltc_series = stat_object.helper.parse_csv("https://coinmetrics.io/data/ltc.csv")
        bch_series = stat_object.helper.parse_csv("https://coinmetrics.io/data/bch.csv")
    except:
        btc_series = stat_object.helper.parse_csv('btc.csv')

    btc_series = btc_series.append(pandas.Series([scrape_obj.get_bct_price()],[now.strftime("%Y-%m-%d")]))
    eth_series = eth_series.append(pandas.Series([scrape_obj.get_eth_price()], [now.strftime("%Y-%m-%d")]))
    ltc_series = ltc_series.append(pandas.Series([scrape_obj.get_ltc_price()], [now.strftime("%Y-%m-%d")]))
    bch_series = bch_series.append(pandas.Series([scrape_obj.get_bch_price()], [now.strftime("%Y-%m-%d")]))

    coin = crypto_object.CryptoObject("Bitcoin", btc_series[700:], 4)
    coin2 = crypto_object.CryptoObject("Ethereum", eth_series, 4)
    coin3 = crypto_object.CryptoObject("Litecoin", ltc_series[700:], 3)
    # coin4 = crypto_object.CryptoObject("Bitcoin Cash", bch_series, 3)
    coins = [coin, coin2, coin3, ]#coin4]

    # find_non_stationary(coin, ltc_series)

    # html_report(coins, now)
    print(text_message_report(coins, now))
    # text_report(coins, now)
    # exit_tester(candle_eth)


def exit_tester(candle_ltc):
    df = candle_ltc.fetch(dt(2017, 3, 1), dt(2017, 12, 13), 1440)
    series1 = pandas.Series(df['close'].sub(df['open'], axis=0) / df['open'], index=df.index.values)
    series2 = pandas.Series(df['high'].sub(df['open'], axis=0) / df['open'], index=df.index.values)
    print(series1.describe(), series2.describe())
    reg_val = 1000
    take_val = 1000
    take_exit = []
    reg_exit = []
    count = 0
    for i in range(series1.size - 300, series1.size - 1):

        if series2.values[i] >= (pandas.Series.mean(series2[:i]) + pandas.Series.std(series2[:i]) * 3):
            take_val *= (1 + (pandas.Series.mean(series2[:i]) + pandas.Series.std(series2[:i]) * 3))
            take_exit.append(take_val)
            count += 1
        else:
            take_val *= (1 + series1.values[i])
            take_exit.append(take_val)

        reg_val *= (1 + series1.values[i])
        reg_exit.append(reg_val)
        print(reg_val, take_val)

    print(count, (pandas.Series.mean(series2[:i]) + pandas.Series.std(series2[:i]) * 3))

def text_message_report(coins, now):
    result = "BOA Report "+ now.strftime("%Y-%m-%d %H:%M") + "\n\n"

    for coin in coins:
        result += coin.get_name() + ": " + coin.get_stationarity_as_string() +" and " + coin.get_independence_as_string() + "." + \
              html.unescape(coin.get_most_recent_pattern()) + " " +\
              '%.2f' % coin.get_odds_of_increase(coin.get_most_recent_pattern()) + \
              "% chance of up. " + '%.2f' % coin.get_odds_of_decrease(coin.get_most_recent_pattern()) +\
              "% chance of down.\n Up move: " +\
              '%.2f' % coin.get_magnitude_of_increase(coin.get_most_recent_pattern()) +\
              ". Down move: " +\
              '%.2f' % coin.get_magnitude_of_decrease(coin.get_most_recent_pattern())+ \
              ".\n Today, " + coin.get_prediction_plus(coin.get_most_recent_pattern()) + ".\n"

    from twilio.rest import Client

    # Your Account SID from twilio.com/console
    account_sid = "ACed23e31a89dd21d99d4d6cba4f432ccc"
    # Your Auth Token from twilio.com/console
    auth_token = "6f2c79b6e35553d50d965edab95f6593"

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to="+19106896305",
        from_="+19104461297",
        body=result)

    print(message.sid)

    email_report(coins,now)

    return result

def email_report(coins, now):

    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    s = smtplib.SMTP(host='mail.privateemail.com', port=587)
    s.starttls()
    s.login("admin@cryptoboa.io", "Aesthetics21!P")

    me = "admin@cryptoboa.io"
    you = ["officialemre@gmail.com"]

    for name in you:
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = " BOA Report " + now.strftime("%Y-%m-%d %H:%M")
        msg['From'] = me
        msg['To'] = name

        # Create the body of the message (a plain-text and an HTML version).
        html = '''<html>
                        <head>
                            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
                            <style>body{ margin:0 100; background:whitesmoke; }</style>
                            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
                        </head>
                        <body>
                            <h1>BOA Report ''' + now.strftime("%Y-%m-%d %H:%M") + '''</h1>
                '''

        for coin in coins:
            html += '''
                    
                            <br/>
                            <h2> ''' + coin.get_name() + '''</h2>
  
                                    <h3>
                                    <b> TL;DR: ''' + coin.get_prediction_plus(coin.get_most_recent_pattern()) + '''</b>
                                    </h3>

                            <p> Here's the rundown on <b>''' + coin.get_name() + '''</b> today:
                                <br/>
                                <br/>
                                    Over the last <b>''' + coin.get_time_period() + ''' ''' + coin.get_name() + '''</b> price change 
                                    has been <b>''' + coin.get_stationarity_as_string() + '''</b>, with a Chi-Square sigma of <b>''' + coin.get_stat_sigma() + '''</b> 
                                    and a Chi-Square critical value of <b>''' + coin.get_stat_critical_value() + '''</b> . 
                                    That means that <b>''' + coin.get_name() + ''' ''' + coin.get_likelihood(
                coin.get_stationarity()) + '''</b> 
                                    to keep acting the way it has been acting. 
                                <br/>
                                <br/>
                                    Price change has been <b>''' + coin.get_randomness_as_string() + '''</b>ly distributed, with a Chi-Square sigma of 
                                    <b>''' + coin.get_rand_sigma() + '''</b> and a Chi-Square critical value of <b>''' + coin.get_rand_critical_value() + '''</b>. That means that 
                                    <b>''' + coin.get_name() + '''</b> price  <b>''' + coin.get_likelihood(
                coin.get_randomness()) + '''</b> selected from the
                                    probability distribution. 
                                <br/>
                            <p> 
                                Over the last <b>''' + coin.get_time_period() + ''' ''' + coin.get_name() + '''</b> price change 
                                has been <b>''' + coin.get_independence_as_string() + '''</b>, with a Chi-Square sigma of <b>''' + coin.get_ind_sigma() + '''</b> 
                                and a Chi-Square critical value of <b>''' + coin.get_ind_critical_value() + '''</b>. That means that for
                                    <b>''' + coin.get_name() + '''</b> it <b>''' + coin.get_likelihood(
                not coin.get_independence()) + '''</b> that we can predict
                                    whether the price will go up or down tomorrow.                    

                                After analysing the price history, BOA concluded that there is a <b>''' + '%.2f' % coin.get_odds_of_increase(
                coin.get_most_recent_pattern()) + '''%</b>
                                chance price will go up, and a <b>''' + '%.2f' % coin.get_odds_of_decrease(
                coin.get_most_recent_pattern()) + '''%</b>
                                chance price will go down. The average magnitude of the up move is <b>''' + '%.2f' % coin.get_magnitude_of_increase(
                coin.get_most_recent_pattern()) + '''%</b>
                                and the average magnitude of the down move is <b>''' + '%.2f' % coin.get_magnitude_of_decrease(
                coin.get_most_recent_pattern()) + '''%</b>.
                                Today, you should <b>''' + coin.get_prediction_plus(coin.get_most_recent_pattern()) + '''</b>.
                                <br/>
                                <br/>   
                '''

        html += " See you tomorrow!  "
        msg.attach(MIMEText(html, 'html'))

        s.sendmail(me, you, msg.as_string())
        s.quit()

def text_report(coins, now):
    print("BOA Report ", now.strftime("%Y-%m-%d %H:%M"))
    for coin in coins:
        print("----------", coin.get_name(), "----------", "\n",
              "Most recent price entry:", str(coin.get_most_recent_date()), "\n\n",
              "Over the last", coin.get_time_period(), coin.get_name(), "price change has been ", "\n",
              coin.get_stationarity_as_string(), ": sigma:", coin.get_stat_sigma(), ", critical value:",
              coin.get_stat_critical_value(), "\n",
              coin.get_randomness_as_string(), ": sigma:", coin.get_rand_sigma(), ", critical value:",
              coin.get_rand_critical_value(), "\n",
              coin.get_independence_as_string(), ": sigma:", coin.get_ind_sigma(), ", critical value:",
              coin.get_ind_critical_value(), ", order:", coin.degrees, "\n",
              "\n",

              "The current lead up is", html.unescape(coin.as_arrows(coin.get_predictive_pattern())),
              "which means the possible patterns at midnight and their outcomes are:\n",
              html.unescape(coin.as_arrows(coin.get_predictive_pattern() + "1")), "up:",
              '%.2f' % coin.get_odds_of_increase(coin.get_predictive_pattern() + "1"), "x",
              '%.2f' % coin.get_magnitude_of_increase(coin.get_predictive_pattern() + "1"),"down:",
              '%.2f' % coin.get_odds_of_decrease(coin.get_predictive_pattern() + "1"), "x",
              '%.2f' % coin.get_magnitude_of_decrease(coin.get_predictive_pattern() + "1"),
              coin.get_prediction_plus(coin.get_predictive_pattern() + "1"), "\n",
              html.unescape(coin.as_arrows(coin.get_predictive_pattern() + "2")), "up:",
              '%.2f' % coin.get_odds_of_increase(coin.get_predictive_pattern() + "2"), "x",
              '%.2f' % coin.get_magnitude_of_increase(coin.get_predictive_pattern() + "2"), "down:",
              '%.2f' % coin.get_odds_of_decrease(coin.get_predictive_pattern() + "2"), "x",
              '%.2f' % coin.get_magnitude_of_decrease(coin.get_predictive_pattern() + "2"),
              coin.get_prediction_plus(coin.get_predictive_pattern() + "2"), "\n",

              "Since the most recent sequence of price change was",
              html.unescape(coin.as_arrows(coin.get_most_recent_pattern())), ", there is a",
              '%.2f' % coin.get_odds_of_increase(coin.get_most_recent_pattern()),
              "% chance price will go up, and a", '%.2f' % coin.get_odds_of_decrease(coin.get_most_recent_pattern()),
              "% chance price will go down.\n The average magnitude of the up move is",
              '%.2f' % coin.get_magnitude_of_increase(coin.get_most_recent_pattern()),
              "and the average magnitude of the down move is",
              '%.2f' % coin.get_magnitude_of_decrease(coin.get_most_recent_pattern()),
              ".\n Today, you should", coin.get_prediction_plus(coin.get_most_recent_pattern()),".\n",

              )


def html_report(coins, now):
    for coin in coins:
        html_string = '''
            <html>
                <head>
                    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
                    <style>body{ margin:0 100; background:whitesmoke; }</style>
                    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
                </head>
                <body>
                    <h1>BOA Report ''' + now.strftime("%Y-%m-%d %H:%M") + '''</h1>
                    <br/>
                    <h2> Stationarity and Behavior</h2>
                    <p> Here's the rundown on <b>''' + coin.get_name() + '''</b> today:
                        <br/>
                        <br/>
                            Over the last <b>''' + coin.get_time_period() + ''' ''' + coin.get_name() + '''</b> price change 
                            has been <b>''' + coin.get_stationarity_as_string() + '''</b>, with a Chi-Square sigma of <b>''' + coin.get_stat_sigma() + '''</b> 
                            and a Chi-Square critical value of <b>''' + coin.get_stat_critical_value() + '''</b> . 
                            That means that <b>''' + coin.get_name() + ''' ''' + coin.get_likelihood(
            coin.get_stationarity()) + '''</b> 
                            to keep acting the way it has been acting. 
                        <br/>
                        <br/>
                            Price change has been <b>''' + coin.get_randomness_as_string() + '''</b>ly distributed, with a Chi-Square sigma of 
                            <b>''' + coin.get_rand_sigma() + '''</b> and a Chi-Square critical value of <b>''' + coin.get_rand_critical_value() + '''</b>. That means that 
                            <b>''' + coin.get_name() + '''</b> price  <b>''' + coin.get_likelihood(coin.get_randomness()) + '''</b> selected from the
                            probability distribution. 
                        <br/>
                        <br/>
                            Here's a chart of <b>''' + coin.get_name() + '''</b> daily prices over the last <b>''' + coin.get_time_period() + '''</b>: 
                    </p>
                    <br/>
                    <iframe width="700" height="550" frameborder="0" seamless="seamless" scrolling="no" \
                    src="''' + coin.get_price_chart() + '''">
                    </iframe>
                    
                    <br/>
                    <br/>
                    <h2> Dependence and Prediction</h2>
                    <p> 
                        Over the last <b>''' + coin.get_time_period() + ''' ''' + coin.get_name() + '''</b> price change 
                        has been <b>''' + coin.get_independence_as_string() + '''</b>, with a Chi-Square sigma of <b>''' + coin.get_ind_sigma() + '''</b> 
                        and a Chi-Square critical value of <b>''' + coin.get_ind_critical_value() + '''</b>. That means that for
                            <b>''' + coin.get_name() + '''</b> it <b>''' + coin.get_likelihood(
            not coin.get_independence()) + '''</b> that we can predict
                            whether the price will go up or down tomorrow.                    
                        <br/>
                        <br/>
                        Here's a chart of <b>''' + coin.get_name() + '''</b> dependencies, their odds of occurrence, and the average percent change of those moves
                        <br/>
                        <br/> 
                        <table table class="table table-bordered"> ''' + get_table(coin) + '''
                        </table>
                        <br/>
                        <br/>
                        Since the most recent sequence of price change was <b>''' + coin.as_arrows(coin.get_most_recent_pattern()) + '''</b>, there is a <b>''' + '%.2f' % coin.get_odds_of_increase(coin.get_most_recent_pattern()) + '''%</b>
                        chance price will go up, and a <b>''' + '%.2f' % coin.get_odds_of_decrease(coin.get_most_recent_pattern()) + '''%</b>
                        chance price will go down. The average magnitude of the up move is <b>''' + '%.2f' % coin.get_magnitude_of_increase(coin.get_most_recent_pattern()) + '''%</b>
                        and the average magnitude of the down move is <b>''' + '%.2f' % coin.get_magnitude_of_decrease(coin.get_most_recent_pattern()) + '''%</b>.
                        Today, you should <b>''' + coin.get_prediction_plus(coin.get_most_recent_pattern()) + '''</b>.
                        <br/>
                        <br/>
                        See you tomorrow!     
        '''
        f = open(coin.get_name() + '-report-' + now.strftime("%Y-%m-%d") + '.html', 'w+')
        f.write(html_string)
        f.close()
    # import pdfkit
    # pdfkit.from_url('report-'+now.strftime("%Y-%m-%d")+'.html', 'report-'+now.strftime("%Y-%m-%d")+'.pdf')


def find_non_stationary(coin, ltc_series):
    for i in range(110, ltc_series.size):
        coin = crypto_object.CryptoObject("Litecoin", ltc_series[:i], 4)
        if not coin.get_stationarity():
            print(coin.stat_sigma)
            print("Not stationary at: ", i)


def get_table(coin):
    table_html = '''
        <tr>
            <td>Pattern</td>
            <td>&#x1f856</td>
            <td>Magnitude</td>
            <td>&#x1f855</td>
            <td>Magnitude</td>
            <td>Predicted Gain</td>
        </tr>
    '''
    for i in coin.get_dep_object().get_lead_up_patterns():
        try:
            down_value = float(100.0 * coin.get_dep_object().get_n_gram_matrix_at(i + '1') / (
                coin.get_dep_object().get_n_gram_matrix_at(i + '1') + coin.get_dep_object().get_n_gram_matrix_at(
                    i + '2')))
        except:
            down_value = 0.0
        down_magnitude = float(coin.get_dep_object().get_magnitude_matrix_at(i + '1'))
        try:
            up_value = float(100.0 * coin.get_dep_object().get_n_gram_matrix_at(i + '2') / (
                coin.get_dep_object().get_n_gram_matrix_at(i + '1') + coin.get_dep_object().get_n_gram_matrix_at(
                    i + '2')))
        except:
            up_value = 0.0
        up_magnitude = float(coin.get_dep_object().get_magnitude_matrix_at(i + '2'))

        up = str(coin.get_dep_object().get_n_gram_matrix_at(i + '2'))
        down = str(coin.get_dep_object().get_n_gram_matrix_at(i + '1'))

        table_html += '''        
        <tr>
            <td>''' + coin.get_dep_object().pattern_as_arrows(i) + '''</td>
            <td>''' + '%.2f' % down_value + '''% (''' + down + ''')</td>
            <td>''' + '%.2f' % (down_magnitude) + '''%</td>
            <td>''' + '%.2f' % up_value + '''% (''' + up + ''')</td>
            <td>''' + '%.2f' % (up_magnitude) + '''%</td>
            <td>''' + '%.2f' % (down_value * down_magnitude / 100.0 + up_value * up_magnitude / 100.0) + '''%</td>

        </tr>
        '''
    return table_html


if __name__ == '__main__':
    main()
