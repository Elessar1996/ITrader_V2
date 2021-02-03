from utils import  buy_hold, rand_p_method, optimize
import xlrd
import pandas_datareader as web_pd
import math
import numpy as np
import xlsxwriter

wb = xlrd.open_workbook('./inp.xls')
sheet = wb.sheet_by_index(0)

list_tickers = []

list_dataset = []

nrows = sheet.nrows
ncols = sheet.ncols

for i in range(1,nrows):
    t = sheet.cell_value(i, 0)
    list_tickers.append(t)

start = sheet.cell_value(1,1)
end = sheet.cell_value(1,2)


for ticker in list_tickers:

    dataset = web_pd.DataReader(ticker,data_source='yahoo', start = start, end = end)
    list_dataset.append(dataset['Close'])

train_set = []
test_set = []

for i in list_dataset:
    train_limit = math.ceil(len(i)*.5)
    train_set.append(i[:train_limit])
    test_set.append(i[train_limit:])

optimized_param = []

for i in train_set:
    fc, fc_param = optimize(i.values)
    m = np.argmax(fc)
    param = fc_param[m]
    optimized_param.append(param)


rand_p_res = []
buy_hold_res = []

for i, j in enumerate(test_set):
    a, b, c, d, e, f, g, h, ff = optimized_param[i]
    res = rand_p_method(j, j.values,k1=a, k2=b,
                        k11=c,k22= d
                        ,k111= e,k222= f,
                        k41= g,k42= h, fc = ff )
    rand_p_res.append(res)
    bh_res = buy_hold(j, j.values)
    buy_hold_res.append(bh_res)


print(buy_hold_res)
print(rand_p_res)

workbook = xlsxwriter.Workbook('./results.xls')
worksheet = workbook.add_worksheet()

for i, j in enumerate(list_tickers):
    worksheet.write('A1', 'tickers')
    worksheet.write(f'A{i+2}', j)
for i, j in enumerate(rand_p_res):
    worksheet.write('B1', 'rp_results')
    worksheet.write(f'B{i+2}', j[0])
for i, j in enumerate(buy_hold_res):
    worksheet.write('C1', 'bh_result')
    worksheet.write(f'C{i+2}', j[0])
for i, j in enumerate(rand_p_res):
    worksheet.write('D1', 'n_days')
    worksheet.write(f'D{i+2}', j[1])


workbook.close()







