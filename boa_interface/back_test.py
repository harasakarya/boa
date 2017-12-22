from boa_logic import statistics
from matplotlib import pyplot
import plotly as py
import plotly.graph_objs as go
from boa_logic import crypto_object
import datetime


def back_test():
    stat_object = statistics.Calculate_Stats()
    now = datetime.datetime.now()
    try:
        btc_series = stat_object.helper.parse_csv('https://coinmetrics.io/data/btc.csv')
        eth_series = stat_object.helper.parse_csv("https://coinmetrics.io/data/eth.csv")
        dash_series = stat_object.helper.parse_csv("https://coinmetrics.io/data/dash.csv")
        xmr_series = stat_object.helper.parse_csv("https://coinmetrics.io/data/xmr.csv")
        ltc_series = stat_object.helper.parse_csv("https://coinmetrics.io/data/ltc.csv")
    except:
        btc_series = stat_object.helper.parse_csv('btc.csv')

    current_series = xmr_series
    current_name = "Litecoin"
    print(current_series.size)

    price_change = stat_object.helper.turn_prices_into_changes(current_series, permille=True)

    import time
    start_time = time.time()

    days_to_test = 300

    for j in range(3, 4):
        boa_balance = 1000
        hodl_balance = 1000
        hodl_card_balance = 1000
        boa_accuracy = 0
        hodl_accuracy = 0
        order = j
        hodl_result= []
        hodl_card_result = []
        boa_result = []

        for i in range(1, days_to_test + 1):

            if i % 30 == 0:
                print(i)
                boa_balance += 500
                hodl_balance += 500
            if (i + 7) % 30 == 0:
                hodl_card_balance += 500*.9601

            up_to = current_series.size - (days_to_test - i)
            coin = crypto_object.CryptoObject(current_name, current_series[:up_to], order)

            # calculate boa values up to current point
            prediction = coin.get_prediction(coin.get_most_recent_pattern())
            current_change = (1.0 + price_change.values[(days_to_test - i + 1) * -1] / 1000.0)

            # decide buy or sell
            boa_balance *= current_change if (prediction is "Buy" and (coin.get_stationarity())) else 1.0
            # boa_balance *= current_change if (coin.get_odds_of_increase(coin.get_most_recent_pattern()) > 50.0 and (coin.get_stationarity())) else 1.0
            hodl_balance *= current_change
            hodl_card_balance *= current_change

            # add to the arrays
            hodl_result.append(hodl_balance)
            hodl_card_result.append(hodl_card_balance)
            boa_result.append(boa_balance)

            # record accuracy
            boa_accuracy += 1 if ((coin.get_numeric_prediction(coin.get_most_recent_pattern()) < 1.0 and current_change < 1.0) or (
                 coin.get_numeric_prediction(coin.get_most_recent_pattern()) > 1.0 and current_change > 1.0)) else 0
            hodl_accuracy += 1 if current_change > 1.0 else 0

            print(prediction, "BOA: ", '%.2f' % boa_balance, "Hodl: ", '%.2f' % hodl_balance, "Hodl C: ", '%.2f' % hodl_card_balance, coin.get_stationarity_as_string(), coin.get_stat_sigma(), coin.get_stat_critical_value())

        # Timer block
        m, s = divmod(time.time() - start_time, 60)
        h, m = divmod(m, 60)

        results = "\n=======BACK TEST RESULTS " + now.strftime("%Y-%m-%d") +"=======\n\n"\
            "The " + coin.get_name()+" results for " + str(days_to_test)+ " days and " + str(order) + " degrees are: BOA Final Balance: " + \
        '%.2f' % boa_balance + " Hodl Final Balance: " + '%.2f' %(hodl_balance) + \
        " Boa Accuracy: " + str(boa_accuracy) + " Hodl accuracy: " + str(hodl_accuracy) + " Elapsed time: " + str(
            "%d:%02d:%02d" % (h, m, s)) + "\n"

        f = open('backtest.txt', 'a+')
        f.write(results)
        f.close()

        import winsound

        frequency = 2500  # Set Frequency To 2500 Hertz
        duration = 1000  # Set Duration To 1000 ms == 1 second
        winsound.Beep(frequency, duration)

        pyplot.plot(hodl_result)
        pyplot.plot(hodl_card_result)
        pyplot.plot(boa_result)
        pyplot.show()

        print(results)

back_test()
