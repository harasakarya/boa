from boa_logic import statistics
from matplotlib import pyplot
import plotly as py
import plotly.graph_objs as go
from boa_logic import crypto_object
import datetime
from random import randint
from numpy import max


def backtest_alpha():
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

    # Litecoin setup
    current_series1 = ltc_series[700:]
    current_name1 = "Litecoin"
    price_change1 = stat_object.helper.turn_prices_into_changes(current_series1, permille=True)

    # Bitcoin setup
    current_series2 = btc_series
    current_name2 = "Bitcoin"
    price_change2 = stat_object.helper.turn_prices_into_changes(current_series2, permille=True)

    # Ethereum Setup
    current_series3 = eth_series
    current_name3 = "Ethereum"
    price_change3 = stat_object.helper.turn_prices_into_changes(current_series3, permille=True)

    import time
    start_time = time.time()

    today = datetime.date.today()
    begin = datetime.date(2017, 1, 1)

    days_to_test = (today - begin).days
    print(days_to_test)

    for j in range(4, 5):
        boa_balance = 9999
        boa_1balance = 3333
        boa_2balance = 3333
        boa_3balance = 3333
        hodl_1balance = 3333
        hodl_2balance = 3333
        hodl_3balance = 3333
        random_balance = 9999
        boa_accuracy = 0
        random_accuracy = 0
        order = j
        hodl_result = []
        random_result = []
        boa_result = []
        boa_classic_result = []

        for i in range(1, days_to_test + 1):

            up_to1 = current_series1.size - (days_to_test - i)
            up_to2 = current_series2.size - (days_to_test - i)
            up_to3 = current_series3.size - (days_to_test - i)
            coin1 = crypto_object.CryptoObject(current_name1, current_series1[:up_to1], order - 1)
            coin2 = crypto_object.CryptoObject(current_name2, current_series2[:up_to2], order)
            coin3 = crypto_object.CryptoObject(current_name3, current_series3[:up_to3], order)

            # calculate boa values up to current point
            prediction1 = coin1.get_numeric_prediction(coin1.get_most_recent_pattern())
            prediction2 = coin2.get_numeric_prediction(coin2.get_most_recent_pattern())
            prediction3 = coin3.get_numeric_prediction(coin3.get_most_recent_pattern())
            prediction_array = [prediction1, prediction2, prediction3]

            current_change1 = (
                1.0 + price_change1.values[(days_to_test - i + 1) * -1] / 1000.0)
            current_change2 = (
                1.0 + price_change2.values[(days_to_test - i + 1) * -1] / 1000.0)
            current_change3 = (
                1.0 + price_change3.values[(days_to_test - i + 1) * -1] / 1000.0)

            # decide buy or sell
            boa_pick = current_change1 if max(prediction_array) == prediction1 else current_change2 if max(
                prediction_array) == prediction2 else current_change3
            print(boa_pick)
            boa_balance *= boa_pick if max(prediction_array) > 1.0 else 1.0
            hodl_1balance *= current_change1
            hodl_2balance *= current_change2
            hodl_3balance *= current_change3
            boa_1balance *= current_change1 if (prediction1 > 1.0 ) else 1.0
            boa_2balance *= current_change2 if (prediction2 > 1.0 ) else 1.0
            boa_3balance *= current_change3 if (prediction3 > 1.0 ) else 1.0

            random_pick = randint(1, 3)
            random_value = current_change1 if random_pick is 1 else current_change2 if random_pick is 2 else current_change3
            random_balance *= random_value

            # add to the arrays
            hodl_result.append(hodl_1balance + hodl_2balance + hodl_3balance)
            random_result.append(random_balance)
            boa_result.append(boa_balance)
            boa_classic_result.append(boa_1balance + boa_2balance + boa_3balance)

            # record accuracy
            boa_accuracy += 1 if (
                boa_pick >= current_change1 and boa_pick >= current_change2 and boa_pick >= current_change3) else 0
            random_accuracy += 1 if (
                random_value >= current_change1 and random_value >= current_change2 and random_value >= current_change3) else 0

            print("\n", i, ". \n", '%.2f' % prediction1, "(", current_change1, ")", '%.2f' % prediction2, "(",
                  current_change2, ")", '%.2f' % prediction3, "(", current_change3, ")", "BOA: ", '%.2f' % boa_balance,
                  "BOA Classic: ", '%.2f' % (boa_1balance + boa_2balance + boa_3balance),
                  "Hodl: ",
                  '%.2f' % (hodl_1balance + hodl_2balance + hodl_3balance), "Random: ", '%.2f' % random_balance,
                  coin1.get_name(), ": ",
                  coin1.get_stationarity_as_string(), coin1.get_stat_sigma(), coin1.get_stat_critical_value(),
                  coin2.get_name(), ": ",
                  coin2.get_stationarity_as_string(), coin2.get_stat_sigma(), coin2.get_stat_critical_value(),
                  coin3.get_name(), ": ",
                  coin3.get_stationarity_as_string(), coin3.get_stat_sigma(),
                  coin3.get_stat_critical_value())  # Timer block

        m, s = divmod(time.time() - start_time, 60)
        h, m = divmod(m, 60)

        results = "\n=======BACK TEST RESULTS " + now.strftime("%Y-%m-%d") + "=======\n\n" \
                                                                             "The " + current_name1 + ", " + current_name2 + ", " + current_name3 + " results for " + str(
            days_to_test) + " days and " + str(order) + " degrees are: BOA Final Balance: " + \
                  '%.2f' % boa_balance + " Random Final Balance: " + \
                  '%.2f' % random_balance + " Hodl Final Balance: " + '%.2f' % (
            hodl_1balance + hodl_2balance + hodl_3balance) + \
                  " Boa Accuracy: " + str(boa_accuracy) + " Random accuracy: " + str(
            random_accuracy) + " Elapsed time: " + str(
            "%d:%02d:%02d" % (h, m, s)) + "\n"

        f = open('backtest_alpha.txt', 'a+')
        f.write(results)
        f.close()

        import winsound

        frequency = 2500  # Set Frequency To 2500 Hertz
        duration = 1000  # Set Duration To 1000 ms == 1 second
        winsound.Beep(frequency, duration)

        Hold= go.Scatter(x=btc_series.index.values[btc_series.size-days_to_test:], y=hodl_result, name= "Buy and Hold")
        BOA = go.Scatter(x=btc_series.index.values[btc_series.size-days_to_test:], y=boa_result, name="BOA")

        layout = go.Layout(
            title='BOA Results 2017',
            xaxis=dict(
                title='Time',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=18,
                    color='#7f7f7f'
                )
            ),
            yaxis=dict(
                title='Portfolio Value',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=18,
                    color='#7f7f7f'
                )
            )
        )

        figure = go.Figure(data=[Hold, BOA],layout=layout)
        url = py.offline.plot(figure, image_height=400, image_width=400, auto_open=False,
                              filename='results.html', )

        # pyplot.plot(hodl_result)
        # pyplot.plot(hodl_card_result)
        # pyplot.plot(boa_result)
        # pyplot.show()

        print(results)


backtest_alpha()
