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
    df['time'] = pd.to_datetime(df['time']).apply(lambda ts: ts.to_period(freq='M'))
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

    (corr, pv) = sp.pearsonr(btc['close'], btc['Global Money Supply'])
    assert corr == 0.8619596247709039, corr
    assert pv == 5.753006999330866e-31, pv

    (corr, pv) = sp.pearsonr(nasdaq['close'], btc['Global Money Supply'])
    assert corr == 0.9749214514633251, corr
    assert pv == 2.0371240700684105e-66, pv

    btc.rename({'close': 'BTC'}, axis=1, inplace=True)
    btc['BTC'] = btc['BTC'] / 1000
    nasdaq.rename({'close': 'NASDAQ'}, axis=1, inplace=True)
    nasdaq['NASDAQ'] = nasdaq['NASDAQ'] / 1000
    nasdaq.drop('Global Money Supply', axis=1, inplace=True)

    plt.rcParams['figure.figsize'] = [12, 8]
    fig, axes = plt.subplots(nrows=3, ncols=1, sharex='col')

    ax = btc['Global Money Supply'].plot(ax=axes[0], color='b')
    ax.set_yticks([80, 100, 120])
    ax.tick_params(which='both', bottom=False)
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax = btc['BTC'].plot(ax=axes[1], color='r')
    ax.set_yticks([0, 20, 40, 60])
    ax.tick_params(which='both', bottom=False)
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax = nasdaq['NASDAQ'].plot(ax=axes[2], color='g')
    ax.set_yticks([5, 10, 15])
    ax.set_xticks([pd.Period('2015-01') + 12 * y for y in range(9)])
    ax.set_xlabel('')
    ax.tick_params(which='both', bottom=False)
    for spine in ax.spines.values():
        spine.set_visible(False)

    merged = btc.merge(nasdaq, left_index=True, right_index=True)
    plt.show()
    seaborn.pairplot(data=merged)
    plt.show()
