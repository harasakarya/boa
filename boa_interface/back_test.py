from boa_logic import statistics, scraper, crypto_object
import pandas
import datetime


def back_test(series, name):
    stat_object = statistics.Calculate_Stats()

    current_series = series
    current_name = name
    print(current_series.size)

    price_change = stat_object.helper.turn_prices_into_changes(current_series, permille=True)

    import time
    start_time = time.time()

    days_to_test = 150

    for j in range(2, 8):
        boa_balance = 10000
        inverse_boa_balance = 10000
        likelihood_boa_balance = 10000
        inverse_likelihood_balance = 10000
        hodl_balance = 10000
        boa_accuracy = 0
        inv_boa_accuracy = 0
        likeli_accuracy = 0
        inv_likeli_accuracy = 0
        hodl_accuracy = 0
        order = j
        hodl_result= []
        boa_result = []

        for i in range(1, days_to_test + 1):

            if i % 30 == 0:
                print(i)

            up_to = current_series.size - (days_to_test - i +1)
            coin = crypto_object.CryptoObject(current_name, current_series[:up_to], order)

            # calculate boa values up to current point
            prediction = coin.get_prediction(coin.get_most_recent_pattern())
            num_prediction =coin.get_odds_of_increase(coin.get_most_recent_pattern())
            current_change = (1.0 + price_change.values[(days_to_test - i + 1) * -1] / 1000.0)

            # decide buy or sell
            boa_balance *= current_change if (prediction is "Buy" ) else 1.0
            inverse_boa_balance *= current_change if (prediction is "Sell") else 1.0
            likelihood_boa_balance *= current_change if (num_prediction >= 50.0 ) else 1.0
            inverse_likelihood_balance *= current_change if (num_prediction < 50.0 ) else 1.0
            hodl_balance *= current_change

            # add to the arrays
            hodl_result.append(hodl_balance)
            boa_result.append(boa_balance)

            # record accuracy
            boa_accuracy += 1 if ((coin.get_numeric_prediction(coin.get_most_recent_pattern()) < 1.0 and current_change < 1.0) or (
                 coin.get_numeric_prediction(coin.get_most_recent_pattern()) > 1.0 and current_change > 1.0)) else 0
            inv_boa_accuracy += 1 if (
            (coin.get_numeric_prediction(coin.get_most_recent_pattern()) > 1.0 and current_change < 1.0) or (
                coin.get_numeric_prediction(coin.get_most_recent_pattern()) < 1.0 and current_change > 1.0)) else 0
            likeli_accuracy += 1 if (num_prediction > .5 and current_change > 1.0) or (num_prediction < .5 and current_change < 1.0) else 0
            inv_likeli_accuracy += 1 if (num_prediction < .5 and current_change > 1.0) or (num_prediction > .5 and current_change < 1.0) else 0
            hodl_accuracy += 1 if current_change > 1.0 else 0

            print(prediction, "BOA: ", '%.2f' % boa_balance, "INV BOA: ", '%.2f' % inverse_boa_balance, "Likeli: ", '%.2f' % likelihood_boa_balance, "Inv Likeli: ", '%.2f' % inverse_likelihood_balance,  "Hodl: ", '%.2f' % hodl_balance, coin.get_stationarity_as_string(), coin.get_stat_sigma(), coin.get_stat_critical_value(), " boa accuracy ", boa_accuracy, " inv boa accuracy ", inv_boa_accuracy, " likeli accuracy ", likeli_accuracy, " inv likeli accuracy ", inv_likeli_accuracy," hodl accuracy ", hodl_accuracy)

        # Timer block
        m, s = divmod(time.time() - start_time, 60)
        h, m = divmod(m, 60)

        results = "The " + coin.get_name()+" results for " + str(days_to_test)+ " days and " + str(order) + " degrees are: BOA Final Balance: " + \
        '%.2f' % boa_balance + "INV BOA: " + '%.2f' % inverse_boa_balance + "Likeli: " + '%.2f' % likelihood_boa_balance + "Inv Likeli: " +  '%.2f' % inverse_likelihood_balance + " Hodl Final Balance: " + '%.2f' %(hodl_balance) + \
        " Boa Accuracy: " + str(boa_accuracy) + " inv boa accuracy " + str(inv_boa_accuracy) + " likeli accuracy " + str(likeli_accuracy) + " inv likeli accuracy " + str(inv_likeli_accuracy) + " Hodl accuracy: " + str(hodl_accuracy) + "|| Series Size "+ str(current_series.size) + " Elapsed time: " + str("%d:%02d:%02d" % (h, m, s)) + "\n"

        f = open('backtest.txt', 'a+')
        f.write(results)
        f.close()

        import winsound

        frequency = 2500  # Set Frequency To 2500 Hertz
        duration = 500  # Set Duration To 1000 ms == 1 second
        winsound.Beep(frequency, duration)

        # pyplot.plot(hodl_result)
        # pyplot.plot(boa_result)
        # pyplot.show()

        print(results)

def runner():
    scraper_obj = scraper.Scraper()
    names = ["bitcoin", "litecoin", "ripple", "ethereum", "monero", "stellar", "nav-coin", "nem", "dash"]

    now = datetime.datetime.now()

    f = open('backtest.txt', 'a+')
    f.write("\n=======BACK TEST RESULTS " + now.strftime("%Y-%m-%d") + "=======\n\n")
    f.close()

    for coin in names:
        back_test(scraper_obj.get_price_history(coin), coin)

    # back_test(pandas.Series([21.0,23.0,22.0,30.0,29.0,36.0,37.0,38.0]), "test")

    import winsound

    frequency = 1250
    duration = 3000
    winsound.Beep(frequency, duration)

runner()
