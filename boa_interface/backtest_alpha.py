import plotly as py
import plotly.graph_objs as go
from boa_logic import statistics, scraper, crypto_object
import datetime
from random import randint
from numpy import max


def backtest_alpha():
    stat_object = statistics.Calculate_Stats()
    now = datetime.datetime.now()
    scraper_obj = scraper.Scraper()

    current_name = [
        "ripple", "ethereum", "monero", "stellar", "nav-coin", "dash",
        "ethereum-classic", "lisk", "verge", "zcash","stratis", "bitcoin", "litecoin"

    ]

    current_degree = []
    for i in range(current_name.__len__()):
        current_degree.append(4)

    current_series = []
    price_change = []

    for name in current_name:
        new_name = scraper_obj.get_price_history(name)
        current_series.append(new_name)
        price_change.append(stat_object.helper.turn_prices_into_changes(new_name, permille=True))

    import time
    start_time = time.time()

    today = datetime.date.today()
    begin = datetime.date(2017, 1, 1)

    days_to_test = (today - begin).days
    print(days_to_test)

    for j in range(4, 5):
        boa_balance = 9999

        classic_boa_balance = []
        hodl_balance = []
        for i in range(current_name.__len__()):
            classic_boa_balance.append(9999/current_name.__len__())
            hodl_balance.append(9999/current_name.__len__())

        random_balance = 9999
        boa_accuracy = 0
        random_accuracy = 0
        hodl_result = []
        random_result = []
        boa_result = []
        boa_classic_result = []
        fee = 0.001

        for i in range(1, days_to_test + 1-21):

            coins = []

            for k in range(current_name.__len__()):
                up_to = current_series[k].size - (days_to_test - i + 1)
                coin = crypto_object.CryptoObject(current_name[k], current_series[k][:up_to], current_degree[k])
                coins.append(coin)

            # calculate boa values up to current point
            prediction_array = []
            for coin in coins:
                if coin.get_stationarity():
                    prediction_array.append(coin.get_numeric_prediction(coin.get_most_recent_pattern()))
                else:
                    prediction_array.append(0.0)

            current_change = []
            for change in price_change:
                current_change.append((
                1.0 + change.values[(days_to_test - i + 1) * -1] / 1000.0))


            # decide buy or sell
            boa_pick = current_change[prediction_array.index(max(prediction_array))]-fee
            boa_balance *= boa_pick if max(prediction_array) > 1.0 else 1.0

            for k in range(current_name.__len__()):
                hodl_balance[k] *= current_change[k]
                classic_boa_balance[k] *= current_change[k] if prediction_array[k] > 1.0 else 1.0

            random_pick = randint(0, current_name.__len__()-1)
            random_value = current_change[random_pick]
            random_balance *= random_value

            # add to the arrays
            hodl_result.append(sum(hodl_balance))
            boa_classic_result.append(sum(classic_boa_balance))
            random_result.append(random_balance)
            boa_result.append(boa_balance)

            # record accuracy
            boa_accuracy += 1 if (
                boa_pick + fee >= max(current_change)) else 0
            random_accuracy += 1 if (
                random_value >= max(current_change)) else 0

            print_val = str(i) + ". \n"
            print_val2 = ""
            for k in range(current_name.__len__()):
                print_val += '%.2f' % prediction_array[k] +  "(" + str(current_change[k]) + ")"
                print_val2 += coins[k].get_name() + ": " + coins[k].get_stationarity_as_string() + coins[k].get_stat_sigma() + coins[k].get_stat_critical_value()

            print_val += "BOA: " + '%.2f' % boa_balance + "BOA Classic: " + '%.2f' % (sum(classic_boa_balance)) + "Hodl: " + \
                  '%.2f' % (sum(hodl_balance)) + "Random: " + '%.2f' % random_balance + print_val2


            print(print_val)

        # Timer block
        m, s = divmod(time.time() - start_time, 60)
        h, m = divmod(m, 60)

        results = "\n=======BACK TEST RESULTS " + now.strftime("%Y-%m-%d") + "=======\n\n" \
                "The results for a portfolio containing " + str(current_name) + " with degrees " + str(current_degree) + " are" \
                " BOA Final Balance: " + '%.2f' % boa_balance + " Random Final Balance: " + '%.2f' % random_balance + " Hodl Final Balance: " + \
                  '%.2f' % sum(hodl_balance) + " Boa Accuracy: " + str(boa_accuracy) + " Random accuracy: " + str(random_accuracy) + \
                  " Elapsed time: " + str("%d:%02d:%02d" % (h, m, s)) + "\n"

        f = open('backtest_alpha.txt', 'a+')
        f.write(results)
        f.close()

        import winsound

        frequency = 2500  # Set Frequency To 2500 Hertz
        duration = 1000  # Set Duration To 1000 ms == 1 second
        winsound.Beep(frequency, duration)

        Hold= go.Scatter(x=current_series[0].index.values[current_series[0].size-days_to_test:], y=hodl_result, name= "Buy and Hold")
        BOA = go.Scatter(x=current_series[0].index.values[current_series[0].size-days_to_test:], y=boa_result, name="BOA")

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
