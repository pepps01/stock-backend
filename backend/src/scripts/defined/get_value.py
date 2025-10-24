import numpy as np
import time
import os
import pandas as pd
import datetime as datetime
import yahoo_fin.stock_info as si
import yfinance as yf
import requests
from math import floor

from google.colab import drive
drive.mount('/content/drive')


def get_ticker_list(grouped_stocks):
  if grouped_stocks == 'dow':
    ticker_list = si.tickers_dow()

  elif  grouped_stocks == 'sp500':
    ticker_list = si.tickers_sp500()

  elif grouped_stocks == 'nasdaq':
    ticker_list = si.tickers_nasdaq()

  else:
    ticker_list = "Input group of stocks not recognised"
    print(ticker_list)

  return ticker_list

get_ticker_list("sp500")



def get_trading_data(ticker_list, start_date, end_date, index_as_date, interval):
  trading_datas = {}

  for ticker in ticker_list:
    try:
      trading_datas[ticker] = si.get_data(ticker, start_date, end_date, index_as_date, interval)
    except:
      pass

  try:
    trading_datas = pd.concat(trading_datas)
    trading_datas = trading_datas.reset_index(level=[0,1])\
                                .drop(labels='level_0', axis=1)\
                                .rename(columns={'level_1':'date'})\
                                .set_index('date')
  except:
    pass
  return trading_datas


def get_selectionA(trading_datas, mingap, maxgap, numb):


  price = {}
  metric_min = {}
  metric_max = {}
  metric_trend = {}

  metric_bline = {}
  metric_sline = {}
  metric_bsline = {}

  volat_1week = {}
  volat_1day = {}

  df_buy, df_sell, op_buy, op_sell = pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
  df_buy1day, df_buy1week, op_buy1day, op_buy1week  = pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
  df_sell1day, df_sell1week, op_sell1day, op_sell1week = pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
  df_both1day, df_both1week = pd.DataFrame(), pd.DataFrame()
  op_both = pd.DataFrame()
  op_both1day = pd.DataFrame()
  op_both1week = pd.DataFrame()



  trading_datas['prange'] = trading_datas['high'] - trading_datas['low']

  stocks = trading_datas.ticker.unique()
  for stock in stocks:
    dt = trading_datas.loc[(trading_datas.ticker == stock)]
    dt_1week = dt.iloc[-5:]
    dt_1day = dt.iloc[-1:]


    price[stock] = dt_1day.close.iloc[0]
    metric_min[stock] = dt.close.min()
    metric_max[stock] = dt.close.max()

    if len(dt) >= 2:
      metric_trend[stock] = round((dt.close.iloc[-1] - dt.close.iloc[-2]), 2)
    else:
      metric_trend[stock] = 0

    metric_bline[stock] = dt.close.min() + (dt.close.max() - dt.close.min())*mingap
    metric_sline[stock] = dt.close.max() - (dt.close.max() - dt.close.min())*maxgap
    metric_bsline[stock] = dt.close.min() + (dt.close.max() - dt.close.min())*maxgap

    volat_1day[stock] = (dt_1day.high.iloc[0] - dt_1day.low.iloc[0])/dt_1day.close.iloc[0]
    volat_1week[stock] = dt_1week.prange.std()




  price = pd.DataFrame(price, index=[0]).T.rename(columns = {0:'price'})
  metric_min = pd.DataFrame(metric_min, index=[0]).T.rename(columns = {0:'metric_min'})
  metric_max = pd.DataFrame(metric_max, index=[0]).T.rename(columns = {0:'metric_max'})
  metric_trend = pd.DataFrame(metric_trend, index=[0]).T.rename(columns = {0:'metric_trend'})
  metric_bline = pd.DataFrame(metric_bline, index=[0]).T.rename(columns = {0:'metric_bline'})
  metric_sline = pd.DataFrame(metric_sline, index=[0]).T.rename(columns = {0:'metric_sline'})

  volat_1day = pd.DataFrame(volat_1day, index=[0]).T.rename(columns = {0:'volat_1day'})
  volat_1week = pd.DataFrame(volat_1week, index=[0]).T.rename(columns = {0:'volat_1week'})


  df = pd.concat([price, metric_min, metric_max, metric_trend, metric_bline, metric_sline, volat_1day, volat_1week], join = 'inner', axis = 1)

  df_buy = df.loc[(df.metric_trend < 0)]
  df_sell = df.loc[(df.metric_trend > 0)]

  try:
    op_buy = df_buy.loc[(df_buy.price <= df_buy.metric_bline)]
    op_sell = df_sell.loc[(df_sell.price >= df_sell.metric_sline)]
    op_both = df_sell.loc[(df_sell.price <= df_sell.metric_bsline)]
  except:
    pass




  if op_buy.empty:
    try:
      df_buy1day = df_buy.reset_index()\
                         .rename(columns={'index':'ticker'})\
                         .sort_values(by=['volat_1day'], ascending = False)
      df_buy1day = df_buy1day[:numb]['ticker'].reset_index(drop=True)
    except:
      pass

    try:
      df_buy1week = df_buy.reset_index()\
                          .rename(columns={'index':'ticker'})\
                          .sort_values(by=['volat_1week'], ascending = False)
      df_buy1week = df_buy1week[:numb]['ticker'].reset_index(drop=True)
    except:
      pass

  else:
    op_buy1day = op_buy.reset_index()\
                       .rename(columns={'index':'ticker'})\
                       .sort_values(by=['volat_1day'], ascending = False)
    op_buy1day = op_buy1day[:numb]['ticker'].reset_index(drop=True)

    op_buy1week = op_buy.reset_index()\
                        .rename(columns={'index':'ticker'})\
                        .sort_values(by=['volat_1week'], ascending = False)
    op_buy1week = op_buy1week[:numb]['ticker'].reset_index(drop=True)

  if op_sell.empty:
    try:
      df_sell1day = df_sell.reset_index()\
                           .rename(columns={'index':'ticker'})\
                           .sort_values(by=['volat_1day'], ascending = False)
      df_sell1day = df_sell1day[:numb]['ticker'].reset_index(drop=True)
    except:
      pass

    try:
      df_sell1week = df_sell.reset_index()\
                            .rename(columns={'index':'ticker'})\
                            .sort_values(by=['volat_1week'], ascending = False)
      df_sell1week = df_sell1week[:numb]['ticker'].reset_index(drop=True)
    except:
      pass

  else:
    op_sell1day = op_sell.reset_index()\
                         .rename(columns={'index':'ticker'})\
                         .sort_values(by=['volat_1day'], ascending = False)
    op_sell1day = op_sell1day[:numb]['ticker'].reset_index(drop=True)

    op_sell1week = op_sell.reset_index()\
                          .rename(columns={'index':'ticker'})\
                          .sort_values(by=['volat_1week'], ascending = False)
    op_sell1week = op_sell1week[:numb]['ticker'].reset_index(drop=True)

  if op_both.empty:
    try:
      df_both1day = df_buy.reset_index()\
                         .rename(columns={'index':'ticker'})\
                         .sort_values(by=['volat_1day'], ascending = True)
      df_both1day = df_both1day[:numb]['ticker'].reset_index(drop=True)
    except:
      pass

    try:
      df_both1week = df_buy.reset_index()\
                          .rename(columns={'index':'ticker'})\
                          .sort_values(by=['volat_1week'], ascending = True)
      df_both1week = df_both1week[:numb]['ticker'].reset_index(drop=True)
    except:
      pass

  else:
    op_both1day = op_both.reset_index()\
                       .rename(columns={'index':'ticker'})\
                       .sort_values(by=['volat_1day'], ascending = False)
    op_both1day = op_both1day[:numb]['ticker'].reset_index(drop=True)

    op_both1week = op_both.reset_index()\
                        .rename(columns={'index':'ticker'})\
                        .sort_values(by=['volat_1week'], ascending = False)
    op_both1week = op_both1week[:numb]['ticker'].reset_index(drop=True)


  try:
    if op_buy1day.empty:
      op_buy1day = df_buy1day
  except:
    pass

  try:
    if op_buy1week.empty:
      op_buy1week = df_buy1week
  except:
    pass

  try:
    if op_sell1day.empty:
      op_sell1day = df_sell1day
  except:
    pass

  try:
    if op_sell1week.empty:
      op_sell1week = df_sell1week
  except:
    pass

  try:
    if op_both1day.empty:
      op_both1day = df_both1day
  except:
    pass

  try:
    if op_both1week.empty:
      op_both1week = df_both1week
  except:
    pass

  return op_buy1day, op_buy1week, op_sell1day, op_sell1week, op_both1day, op_both1week


def get_selectionB(trading_datas):

  trading_datas = trading_datas.loc[(trading_datas.volume >= 50000)]

  metric_Pstdv = {}
  metric_Rstdv = {}
  metric_Vmean = {}
  metric_Msize = {}

  trading_datas['prange'] = trading_datas['high'] - trading_datas['low']

  stocks = trading_datas.ticker.unique()
  for stock in stocks:
    dt = trading_datas.loc[(trading_datas.ticker == stock)]
    metric_Pstdv[stock] = dt.close.std()
    metric_Rstdv[stock] = dt.prange.std()
    metric_Vmean[stock] = dt.volume.mean()
    metric_Msize[stock] = (dt.volume.mean())*(dt.close.mean())


  metric_Pstdv = pd.DataFrame(metric_Pstdv, index=[0])
  metric_Rstdv = pd.DataFrame(metric_Rstdv, index=[0])
  metric_Vmean = pd.DataFrame(metric_Vmean, index=[0])
  metric_Msize = pd.DataFrame(metric_Msize, index=[0])

  metric_Pstdv = metric_Pstdv.T.reset_index()\
                               .rename(columns={'index':'ticker'})\
                               .rename(columns={0:'Pstdv'})\
                               .sort_values(by=['Pstdv'], ascending = False)


  metric_Rstdv = metric_Rstdv.T.reset_index()\
                               .rename(columns={'index':'ticker'})\
                               .rename(columns={0:'Rstdv'})\
                               .sort_values(by=['Rstdv'], ascending = False)


  metric_Vmean = metric_Vmean.T.reset_index()\
                               .rename(columns={'index':'ticker'})\
                               .rename(columns={0:'Vmean'})\
                               .sort_values(by=['Vmean'], ascending = False)


  metric_Msize = metric_Msize.T.reset_index()\
                               .rename(columns={'index':'ticker'})\
                               .rename(columns={0:'Msize'})\
                               .sort_values(by=['Msize'], ascending = False)


  numb = 5
  metric_Pstdv = metric_Pstdv[:numb]['ticker'].reset_index(drop=True)
  metric_Rstdv = metric_Rstdv[:numb]['ticker'].reset_index(drop=True)
  metric_Vmean = metric_Vmean[:numb]['ticker'].reset_index(drop=True)
  metric_Msize = metric_Msize[:numb]['ticker'].reset_index(drop=True)


  tradin_select = metric_Rstdv[(pd.Series(metric_Rstdv.to_numpy()).isin(metric_Vmean.to_numpy()))]
  invest_select = metric_Pstdv[(pd.Series(metric_Pstdv.to_numpy()).isin(metric_Vmean.to_numpy()))]

  if len(tradin_select) == 0:
    tradin_select = metric_Rstdv

  if len(invest_select) == 0:
    invest_select = metric_Pstdv


  return tradin_select, invest_select


def get_selectionC(trading_datas, intrady_datas, mingap, maxgap, numb):

  price = {}
  metric_min = {}
  metric_max = {}
  metric_trend = {}

  metric_bline = {}
  metric_sline = {}
  metric_bsline = {}

  volat_1week = {}
  volat_1day = {}

  df_buy, df_sell, op_buy, op_sell = pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
  df_buy1day, df_buy1week, op_buy1day, op_buy1week  = pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
  df_sell1day, df_sell1week, op_sell1day, op_sell1week = pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
  df_both1day, df_both1week = pd.DataFrame(), pd.DataFrame()
  op_both = pd.DataFrame()
  op_both1day = pd.DataFrame()
  op_both1week = pd.DataFrame()


  trading_datas['prange'] = trading_datas['high'] - trading_datas['low']
  intrady_datas['prange'] = intrady_datas['close'] - intrady_datas['low']

  stocks = intrady_datas.ticker.unique()
  for stock in stocks:
    dt = trading_datas.loc[(trading_datas.ticker == stock)]
    dt_1week = dt.iloc[-5:]
    dt_1day = intrady_datas.loc[(intrady_datas.ticker == stock)]


    price[stock] = dt_1day.close.iloc[-1]
    metric_min[stock] = dt.close.min()
    metric_max[stock] = dt.close.max()

    if len(dt) >= 2:
      metric_trend[stock] = round((dt.close.iloc[-1] - dt.close.iloc[-2]), 2)
    else:
      metric_trend[stock] = 0

    metric_bline[stock] = dt.close.min() + (dt.close.max() - dt.close.min())*mingap
    metric_sline[stock] = dt.close.max() - (dt.close.max() - dt.close.min())*maxgap
    metric_bsline[stock] = dt.close.min() + (dt.close.max() - dt.close.min())*maxgap


    volat_1day[stock] = dt_1day.prange.std()
    volat_1week[stock] = dt_1week.prange.std()




  price = pd.DataFrame(price, index=[0]).T.rename(columns = {0:'price'})
  metric_min = pd.DataFrame(metric_min, index=[0]).T.rename(columns = {0:'metric_min'})
  metric_max = pd.DataFrame(metric_max, index=[0]).T.rename(columns = {0:'metric_max'})
  metric_trend = pd.DataFrame(metric_trend, index=[0]).T.rename(columns = {0:'metric_trend'})
  metric_bline = pd.DataFrame(metric_bline, index=[0]).T.rename(columns = {0:'metric_bline'})
  metric_sline = pd.DataFrame(metric_sline, index=[0]).T.rename(columns = {0:'metric_sline'})

  volat_1day = pd.DataFrame(volat_1day, index=[0]).T.rename(columns = {0:'volat_1day'})
  volat_1week = pd.DataFrame(volat_1week, index=[0]).T.rename(columns = {0:'volat_1week'})


  df = pd.concat([price, metric_min, metric_max, metric_trend, metric_bline, metric_sline, volat_1day, volat_1week], join = 'inner', axis = 1)

  df_buy = df.loc[(df.metric_trend < 0)]
  df_sell = df.loc[(df.metric_trend > 0)]

  try:
    op_buy = df_buy.loc[(df_buy.price <= df_buy.metric_bline)]
    op_sell = df_sell.loc[(df_sell.price >= df_sell.metric_sline)]
    op_both = df_sell.loc[(df_sell.price <= df_sell.metric_bsline)]
  except:
    pass





  if op_buy.empty:
    try:
      df_buy1day = df_buy.reset_index()\
                         .rename(columns={'index':'ticker'})\
                         .sort_values(by=['volat_1day'], ascending = False)
      df_buy1day = df_buy1day[:numb]['ticker'].reset_index(drop=True)
    except:
      pass

    try:
      df_buy1week = df_buy.reset_index()\
                          .rename(columns={'index':'ticker'})\
                          .sort_values(by=['volat_1week'], ascending = False)
      df_buy1week = df_buy1week[:numb]['ticker'].reset_index(drop=True)
    except:
      pass

  else:
    op_buy1day = op_buy.reset_index()\
                       .rename(columns={'index':'ticker'})\
                       .sort_values(by=['volat_1day'], ascending = False)
    op_buy1day = op_buy1day[:numb]['ticker'].reset_index(drop=True)

    op_buy1week = op_buy.reset_index()\
                        .rename(columns={'index':'ticker'})\
                        .sort_values(by=['volat_1week'], ascending = False)
    op_buy1week = op_buy1week[:numb]['ticker'].reset_index(drop=True)

  if op_sell.empty:
    try:
      df_sell1day = df_sell.reset_index()\
                           .rename(columns={'index':'ticker'})\
                           .sort_values(by=['volat_1day'], ascending = False)
      df_sell1day = df_sell1day[:numb]['ticker'].reset_index(drop=True)
    except:
      pass

    try:
      df_sell1week = df_sell.reset_index()\
                            .rename(columns={'index':'ticker'})\
                            .sort_values(by=['volat_1week'], ascending = False)
      df_sell1week = df_sell1week[:numb]['ticker'].reset_index(drop=True)
    except:
      pass

  else:
    op_sell1day = op_sell.reset_index()\
                         .rename(columns={'index':'ticker'})\
                         .sort_values(by=['volat_1day'], ascending = False)
    op_sell1day = op_sell1day[:numb]['ticker'].reset_index(drop=True)

    op_sell1week = op_sell.reset_index()\
                          .rename(columns={'index':'ticker'})\
                          .sort_values(by=['volat_1week'], ascending = False)
    op_sell1week = op_sell1week[:numb]['ticker'].reset_index(drop=True)

  if op_both.empty:
    try:
      df_both1day = df_buy.reset_index()\
                         .rename(columns={'index':'ticker'})\
                         .sort_values(by=['volat_1day'], ascending = True)
      df_both1day = df_both1day[:numb]['ticker'].reset_index(drop=True)
    except:
      pass

    try:
      df_both1week = df_buy.reset_index()\
                          .rename(columns={'index':'ticker'})\
                          .sort_values(by=['volat_1week'], ascending = True)
      df_both1week = df_both1week[:numb]['ticker'].reset_index(drop=True)
    except:
      pass

  else:
    op_both1day = op_both.reset_index()\
                       .rename(columns={'index':'ticker'})\
                       .sort_values(by=['volat_1day'], ascending = False)
    op_both1day = op_both1day[:numb]['ticker'].reset_index(drop=True)

    op_both1week = op_both.reset_index()\
                        .rename(columns={'index':'ticker'})\
                        .sort_values(by=['volat_1week'], ascending = False)
    op_both1week = op_both1week[:numb]['ticker'].reset_index(drop=True)


  try:
    if op_buy1day.empty:
      op_buy1day = df_buy1day
  except:
    pass

  try:
    if op_buy1week.empty:
      op_buy1week = df_buy1week
  except:
    pass

  try:
    if op_sell1day.empty:
      op_sell1day = df_sell1day
  except:
    pass

  try:
    if op_sell1week.empty:
      op_sell1week = df_sell1week
  except:
    pass

  try:
    if op_both1day.empty:
      op_both1day = df_both1day
  except:
    pass

  try:
    if op_both1week.empty:
      op_both1week = df_both1week
  except:
    pass


  return op_buy1day, op_buy1week, op_sell1day, op_sell1week, op_both1day, op_both1week


basket = ['sp500']

# value
for grouped_stocks in basket:
  input_file = str(grouped_stocks) +  "_summary"
  dt = pd.read_csv('/content/drive/Algizer/{}.csv'.format(input_file))
  watchlist = dt.ticker.loc[dt.Score == 5]
  watchlist = pd.DataFrame(watchlist)
  watchlist = watchlist['ticker'].reset_index(drop=True)

  ticker_list = get_ticker_list(grouped_stocks)
  ticker_list = pd.DataFrame(ticker_list).rename(columns={0:'ticker'})
  ticker_list = ticker_list['ticker'].reset_index(drop=True)
  ticker_list = ticker_list[(pd.Series(ticker_list.to_numpy()).isin(watchlist.to_numpy()))]


  start_date = (datetime.date.today() + datetime.timedelta(days=-366)).strftime("%m/%d/%Y")                                                            #Input format is: month/day/Year
  end_date = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%m/%d/%Y")
  trading_datas = get_trading_data(ticker_list, start_date, end_date, index_as_date = True, interval = "1d")

  ticker_list = trading_datas.ticker.unique()


  select_buy1day, select_buy1week, select_sell1day, select_sell1week, both1day, both1week = get_selectionA(trading_datas, mingap=0.10, maxgap=0.20, numb=10)


  trading_datas.index = pd.to_datetime(trading_datas.index, utc=True)
  trading_datas = trading_datas.reset_index()
  trading_datas.date = trading_datas.date.dt.date
  dateall = pd.Series(trading_datas.date.array)
  date1 = (datetime.date.today() + datetime.timedelta(days=-4))
  date2 = (datetime.date.today() + datetime.timedelta(days=-3))
  date3 = (datetime.date.today() + datetime.timedelta(days=-2))
  date4 = (datetime.date.today() + datetime.timedelta(days=-1))
  date5 = datetime.date.today()

  trading_datas = trading_datas[(dateall == date1) | (dateall == date2) | (dateall == date3) | (dateall == date4) | (dateall == date5)]
  trading_datas = trading_datas.set_index('date')



  volatl_select, _ = get_selectionB(trading_datas)



  output_text = str(grouped_stocks) +  "_buy1day_watchlist.txt"
  with open('/content/drive/Algizer/{}'.format(str(output_text)), "w") as text_file:
    print(select_buy1day, file=text_file)

  output_text = str(grouped_stocks) +  "_sell1day_watchlist.txt"
  with open('/content/drive/Algizer/{}'.format(str(output_text)), "w") as text_file:
    print(select_sell1day, file=text_file)

  output_text = str(grouped_stocks) +  "_both1day_watchlist.txt"
  with open('/content/drive/Algizer/{}'.format(str(output_text)), "w") as text_file:
    print(both1day, file=text_file)

  output_text = str(grouped_stocks) +  "_buysell_watchlist.txt"
  with open('/content/drive/Algizer/{}'.format(str(output_text)), "w") as text_file:
    print(volatl_select, file=text_file)