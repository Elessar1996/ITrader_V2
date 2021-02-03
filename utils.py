def firstD(arr, i, k):
    x = arr[i]

    y = arr[i - k]

    diff = x - y

    diff /= max(x, y)

    return diff


def secondD(arr, i, k1, k2):
    x = arr[i]

    y = arr[i - min(k1, k2)]

    z = arr[i - max(k1, k2)]

    diff1 = x - y

    diff2 = y - z

    second_diff = diff1 - diff2

    return second_diff


def optimize(train_df_close):
    import numpy as np
    import math

    fc = []
    fc_param = []

    for i in range(100):

        real_stock_price = train_df_close
        initial_capital = 10000
        total_shares = 0
        our_property = 0
        total_property = [initial_capital]
        phase_delay = 1
        acc_thresh = 0

        k1 = np.random.randint(1, 100)
        k2 = np.random.randint(1, 100)

        k11 = np.random.randint(1, 100)
        k22 = np.random.randint(1, 100)

        k111 = np.random.randint(1, 100)
        k222 = np.random.randint(1, 100)

        k41 = np.random.randint(1, 100)
        k42 = np.random.randint(1, 100)

        num_buys = 0
        num_sells = 0

        def buy(n):
            nonlocal initial_capital
            nonlocal total_shares
            nonlocal real_stock_price
            nonlocal our_property
            nonlocal num_buys
            # p = real_stock_price[n + phase_delay] * 0.05
            bought_shares = math.floor(initial_capital / (real_stock_price[n + phase_delay]))
            change = initial_capital - bought_shares * real_stock_price[n]
            total_shares += bought_shares
            initial_capital = 0
            our_property = (initial_capital > 0) * initial_capital + (total_shares > 0) * total_shares * \
                           real_stock_price[n + phase_delay]
            total_property.append(our_property)
            num_buys += 1

        #         print(f"we buy today: date: {train_df.index[n]")
        #         print(f"real stock price is {real_stock_price[n]}")
        #         print(f'our_property in day {train_df.index[n]}: {our_property}')
        #         print("------------------------------------------------")
        def sell(n):
            nonlocal initial_capital
            nonlocal total_shares
            nonlocal real_stock_price
            nonlocal our_property
            nonlocal num_sells
            gained_money = total_shares * (real_stock_price[n + phase_delay])
            initial_capital += gained_money
            total_shares = 0
            our_property = (initial_capital > 0) * initial_capital + (total_shares > 0) * total_shares * \
                           real_stock_price[n + phase_delay]
            total_property.append(our_property)
            num_sells += 1

        #         print(f"we sell today: date: {train_df.index[n]}")
        #         print(f"real stock price is {real_stock_price[n]}")
        #         print(f'our_property in day {train_df.index[n]}: {our_property}')
        #         print("------------------------------------------------")

        def doNothing(n):
            nonlocal our_property
            nonlocal total_property
            #         print(f'we do nothing today: date: {train_df.index[n]}')
            #         print(f"real stock price is {real_stock_price[n]}")
            our_property = (initial_capital > 0) * initial_capital + (total_shares > 0) * total_shares * \
                           real_stock_price[n]
            # padding removal

        #         total_property.append(our_property)
        #         print(f'our_property in day {n}: {our_property}')
        #         print("------------------------------------------------")

        for i, j in enumerate(real_stock_price):
            if i + 1 > len(real_stock_price) - 1:
                break
            else:

                #         signal = 1
                #         acc = 1
                signal1 = firstD(real_stock_price, i, k1)
                acc1 = secondD(real_stock_price, i, k1, k2)

                signal2 = firstD(real_stock_price, i, k11)
                acc2 = secondD(real_stock_price, i, k11, k22)

                signal3 = firstD(real_stock_price, i, k111)
                acc3 = secondD(real_stock_price, i, k111, k222)

                signal4 = firstD(real_stock_price, i, k41)
                acc4 = secondD(real_stock_price, i, k41, k42)

                #                                 signal4 = firstD(real_stock_price, i, k41)
                #                                 acc4 = secondD(real_stock_price, i, k41, k42)

                #                                 signal5 = firstD(real_stock_price, i, k51)
                #                                 acc5 = secondD(real_stock_price,i , k51, k52)

                #                                 signal6 = firstD(real_stock_price, i, k61)
                #                                 acc6 = secondD(real_stock_price, i, k61, k62)

                signal = 1 if (signal1 > 0 and signal2 > 0 and signal3 > 0 and signal4 > 0) else -1
                acc = 1 if (acc1 > 0 or acc2 > 0 or acc3 > 0 or acc4 > 0) else -1
                #                                 signal = (signal1+signal2+signal3+signal4+signal5+signal6)/6
                #                                 acc = (acc1+acc2+acc3+acc4+acc5+acc6)/6

                #         signal = XOR((signal1>0),(signal2>0))
                #         acc = XOR((acc1>0),(acc2>0))

                if signal > 0 and initial_capital > 0 and acc > acc_thresh:
                    buy(i)
                elif signal > 0 and initial_capital > 0 and acc < acc_thresh:
                    doNothing(i)
                elif signal > 0 and initial_capital == 0 and acc > acc_thresh:
                    doNothing(i)
                elif signal > 0 and initial_capital == 0 and acc < acc_thresh:
                    sell(i)
                elif signal < 0 and total_shares > 0 and acc < acc_thresh:
                    sell(i)
                elif signal < 0 and total_shares > 0 and acc > acc_thresh:
                    doNothing(i)
                elif signal < 0 and total_shares == 0 and acc < acc_thresh:
                    doNothing(i)
                elif signal < 0 and total_shares == 0 and acc > acc_thresh:
                    buy(i)
                else:
                    doNothing(i)

            fc.append(total_property[-1])
            fc_param.append((k1, k2, k11, k22, k111, k222, k41, k42, total_property[-1]))

    return fc, fc_param


def ret_ith_max(i, arr):
    import numpy as np
    for j in range(i):
        m = np.argmax(arr)
        arr[m] = 0

    mm = np.argmax(arr)

    return mm


def rand_p_method(test_df, test_df_close, **kwargs):
    real_stock_price = test_df_close
    test_df_date = test_df
    capital = 10000
    total_shares = 0
    our_property = 0
    our_property = capital
    phase_delay = 1
    acc_thresh = 0
    change = 0
    num_buys = 0
    num_sells = 0

    k1, k2, k11, k22, k111, k222, k41, k42, fc = kwargs.values()

    # k41 = fourth_max[0]
    # k42 = fourth_max[1]

    # k51 = fifth_max[0]
    # k52 = fifth_max[1]

    def buy(n):
        nonlocal num_buys
        nonlocal our_property
        nonlocal real_stock_price
        nonlocal total_shares
        nonlocal test_df_date
        nonlocal change
        nonlocal capital
        num_buys += 1
        p = real_stock_price[n + phase_delay] * 0.05
        total_shares = (our_property > 0) * int(our_property / real_stock_price[n])
        change = our_property - real_stock_price[n] * total_shares
        capital = 0
        # print(f'we buy today {test_df_date.index[n]}')
        # print(f"real stock price is {real_stock_price[n]}")
        # print(f'total shares: {total_shares}. Change: {change}')
        # print(f'our_property in day {n} - {test_df_date.index[n]}: {our_property}')
        # print("------------------------------------------------")

    def sell(n):
        nonlocal num_sells
        nonlocal our_property
        nonlocal real_stock_price
        nonlocal test_df_date
        nonlocal total_shares
        nonlocal change
        nonlocal capital
        num_sells += 1
        our_property = change + (total_shares > 0) * (total_shares * real_stock_price[n])
        change = 0
        capital = our_property
        total_shares = 0
        # print(f'we sell today {test_df_date.index[n]}')
        # print(f"real stock price is {real_stock_price[n]}")
        # print(f'total shares: {total_shares}')
        # print(f'our_property in day {n} - {test_df_date.index[n]}: {our_property}')
        # print("------------------------------------------------")

    def doNothing(n):
        nonlocal our_property
        # print(f'we do nothing today {test_df_date.index[n]}')
        # print(f'Current position quantity {total_shares}. Change {change}')
        # print(f"real stock price is {real_stock_price[n]}")
        our_property = ((capital > 0) * capital) + (total_shares > 0) * (total_shares * real_stock_price[n] + change)
        # Ben Edits - This line is incorrect.
        # total_property.append(our_property)

    #     print(f'our_property in day {n} - {test_df_date.index[n]}: {our_property}')
    #     print("------------------------------------------------")
    #
    # print(f'Property at the begining {our_property}')
    # print("------------------------------------------------")
    for i, j in enumerate(real_stock_price):
        if i + 1 > len(real_stock_price) - 1:
            break
        else:

            signal1 = firstD(real_stock_price, i, k1)
            acc1 = secondD(real_stock_price, i, k1, k2)

            signal2 = firstD(real_stock_price, i, k11)
            acc2 = secondD(real_stock_price, i, k11, k22)

            signal3 = firstD(real_stock_price, i, k111)
            acc3 = secondD(real_stock_price, i, k111, k222)

            signal4 = firstD(real_stock_price, i, k41)
            acc4 = secondD(real_stock_price, i, k41, k42)

            #         signal5 = firstD(real_stock_price, i, k51)
            #         acc5 = secondD(real_stock_price,i , k51, k52)

            # Testing three sets of params first

            signal = 1 if (signal1 > 0 and signal2 > 0 and signal3 > 0 and signal4) else -1
            acc = 1 if (acc1 > 0 or acc2 > 0 or acc3 > 0 or acc4 > 0) else -1
            #         signal = 1
            #         acc = 1

            if signal > 0 and capital > 0 and acc > acc_thresh:
                buy(i)
            elif signal > 0 and capital > 0 and acc < acc_thresh:
                doNothing(i)
            elif signal > 0 and capital == 0 and acc > acc_thresh:
                doNothing(i)
            elif signal > 0 and capital == 0 and acc < acc_thresh:
                sell(i)
            elif signal < 0 and total_shares > 0 and acc < acc_thresh:
                sell(i)
            elif signal < 0 and total_shares > 0 and acc > acc_thresh:
                doNothing(i)
            elif signal < 0 and total_shares == 0 and acc < acc_thresh:
                doNothing(i)
            elif signal < 0 and total_shares == 0 and acc > acc_thresh:
                buy(i)
            else:
                doNothing(i)

    # print(f'number of buys: {num_buys}')
    # print(f'number of sells: {num_sells}')

    return our_property, len(test_df_close)


def buy_hold(test_df_close, test_df):
    real_stock_price = test_df_close
    test_df_date = test_df
    capital = 10000
    total_shares = 0
    our_property = 0
    our_property = capital
    phase_delay = 1
    acc_thresh = 0
    change = 0
    num_buys = 0
    num_sells = 0

    # k41 = fourth_max[0]
    # k42 = fourth_max[1]

    # k51 = fifth_max[0]
    # k52 = fifth_max[1]

    def buy(n):
        nonlocal num_buys
        nonlocal our_property
        nonlocal real_stock_price
        nonlocal total_shares
        nonlocal test_df_date
        nonlocal change
        nonlocal capital
        num_buys += 1
        p = real_stock_price[n + phase_delay] * 0.05
        total_shares = (our_property > 0) * int(our_property / real_stock_price[n])
        change = our_property - real_stock_price[n] * total_shares
        capital = 0
        # our_property = total_shares*real_stock_price[n] + change
        # print(f'we buy today {test_df_date.index[n]}')
        # print(f"real stock price is {real_stock_price[n]}")
        # print(f'total shares: {total_shares}. Change: {change}')
        # print(f'our_property in day {n} - {test_df_date.index[n]}: {our_property}')
        # print("------------------------------------------------")

    def sell(n):
        nonlocal num_sells
        nonlocal our_property
        nonlocal real_stock_price
        nonlocal test_df_date
        nonlocal total_shares
        nonlocal change
        nonlocal capital
        num_sells += 1
        our_property = change + (total_shares > 0) * (total_shares * real_stock_price[n])
        change = 0
        capital = our_property
        total_shares = 0
        # print(f'we sell today {test_df_date.index[n]}')
        # print(f"real stock price is {real_stock_price[n]}")
        # print(f'total shares: {total_shares}')
        # print(f'our_property in day {n} - {test_df_date.index[n]}: {our_property}')
        # print("------------------------------------------------")

    def doNothing(n):
        nonlocal our_property
        # print(f'we do nothing today {test_df_date.index[n]}')
        # print(f'Current position quantity {total_shares}. Change {change}')
        # print(f"real stock price is {real_stock_price[n]}")
        our_property = ((capital > 0) * capital) + (total_shares > 0) * (total_shares * real_stock_price[n] + change)
        # Ben Edits - This line is incorrect.
        # total_property.append(our_property)

    #     print(f'our_property in day {n} - {test_df_date.index[n]}: {our_property}')
    #     print("------------------------------------------------")
    #
    # print(f'Property at the begining {our_property}')
    # print("------------------------------------------------")
    for i, j in enumerate(real_stock_price):
        if i + 1 > len(real_stock_price) - 1:
            break
        else:

            signal = 1
            acc = 1

            if signal > 0 and capital > 0 and acc > acc_thresh:
                buy(i)
            elif signal > 0 and capital > 0 and acc < acc_thresh:
                doNothing(i)
            elif signal > 0 and capital == 0 and acc > acc_thresh:
                doNothing(i)
            elif signal > 0 and capital == 0 and acc < acc_thresh:
                sell(i)
            elif signal < 0 and total_shares > 0 and acc < acc_thresh:
                sell(i)
            elif signal < 0 and total_shares > 0 and acc > acc_thresh:
                doNothing(i)
            elif signal < 0 and total_shares == 0 and acc < acc_thresh:
                doNothing(i)
            elif signal < 0 and total_shares == 0 and acc > acc_thresh:
                buy(i)
            else:
                doNothing(i)

    # print(f'number of buys: {num_buys}')
    # print(f'number of sells: {num_sells}')

    return our_property, len(test_df_close)

