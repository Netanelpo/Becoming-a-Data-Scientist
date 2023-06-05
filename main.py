import datetime

import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as sp
import seaborn as seaborn

columns = ['time', 'open', 'high', 'low', 'close', 'Global Money Supply', 'Volume',
           'Volume MA', 'RSI', 'RSI-based MA', 'Upper Bollinger Band',
           'Lower Bollinger Band', 'Predicted Funding Rate', 'Next Funding Rate', 'Funding Bar']

num_months = 101


def read(file):
    df = pd.read_csv(file)
    assert df.columns.equals(pd.Index(columns)), df.columns
    assert df.shape[1] == 15, df.shape
    df = df[['time', 'close', 'Global Money Supply']]
    df['time'] = pd.to_datetime(df['time']).apply(lambda ts: (ts + datetime.timedelta(days=20)).to_period(freq='M'))
    df = df[df['time'] < pd.Period('2023-05')].tail(num_months)
    df.set_index('time', inplace=True)
    assert df.shape == (num_months, 2), df.shape
    assert df.index[-1] == pd.Period('2023-04'), df.index[-1]
    assert df.index[0] == pd.Period('2014-12'), df.index[0]
    return df


if __name__ == '__main__':
    btc = read('COINBASE_BTCUSD, 1M.csv')
    assert btc['close'][0] == 340, btc['close'][0]
    assert btc['Global Money Supply'][0] == 74.37004131552007, btc['Global Money Supply'][0]

    nasdaq = read('NASDAQ_DLY_NDX, 1M.csv')
    assert nasdaq['close'][0] == 4236.28, nasdaq['close'][0]

    dxy = read('TVC_DXY, 1M.csv')
    assert dxy['close'][0] == 90.276, dxy['close'][0]

    (corr, pv) = sp.pearsonr(btc['close'], btc['Global Money Supply'])
    assert corr == 0.8619596247709039, corr
    assert pv == 5.753006999330866e-31, pv

    (corr, pv) = sp.pearsonr(nasdaq['close'], btc['Global Money Supply'])
    assert corr == 0.9749214514633251, corr
    assert pv == 2.0371240700684105e-66, pv

    (corr, pv) = sp.pearsonr(dxy['close'], btc['Global Money Supply'])
    assert corr == 0.11979692345114668, corr
    assert pv == 0.23276713887275874, pv

    fig, axes = plt.subplots(nrows=4, ncols=1, sharex='col')
    btc['close'].plot(ax=axes[0])
    btc['Global Money Supply'].plot(ax=axes[1])
    nasdaq['close'].plot(ax=axes[2])
    dxy['close'].plot(ax=axes[3])

    btc.rename({'close': 'btc'}, axis=1, inplace=True)
    nasdaq.rename({'close': 'nasdaq'}, axis=1, inplace=True)
    dxy.rename({'close': 'dxy'}, axis=1, inplace=True)
    merged = btc.merge(nasdaq, left_index=True, right_index=True)
    merged = merged.merge(dxy, left_index=True, right_index=True)
    merged.drop(['Global Money Supply_y', 'Global Money Supply_x'], axis=1, inplace=True)
    print(merged.columns)
    plt.show()
    seaborn.pairplot(data=merged)
    plt.show()
