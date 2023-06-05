import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as sp

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


# def globalMoney(file):
#     gm = pd.read_csv(file)
#     assert gm.shape == (539, 15), gm.shape
#     assert gm.columns.equals(pd.Index(columns)), gm.columns
#     gm = gm[['time', 'Global Money Supply']]
#     gm['time'] = pd.to_datetime(gm['time']).values.astype(dtype='datetime64[D]')
#     gm.set_index('time', inplace=True)
#     return gm
#
#
# def nasdaq(file):
#     n = pd.read_csv(file)
#     assert n.shape == (462, 15), n.shape
#     assert n.columns.equals(pd.Index(columns)), n.columns
#     n = n[['time', 'close']]
#     n['time'] = pd.to_datetime(n['time']).values.astype(dtype='datetime64[D]')
#     n.set_index('time', inplace=True)
#     return n


if __name__ == '__main__':
    btc = read('COINBASE_BTCUSD, 1M.csv')
    assert btc['close'][0] == 340, btc['close'][0]
    assert btc['Global Money Supply'][0] == 74.37004131552007, btc['Global Money Supply'][0]

    nasdaq = read('NASDAQ_DLY_NDX, 1M.csv')
    assert nasdaq['close'][0] == 4236.28, nasdaq['close'][0]

    # gm = gm.filter(items=btc.index, axis=0)
    # btc = btc.filter(items=gm.index, axis=0)
    # nasdaq = nasdaq.filter(items=gm.index, axis=0)

    num_months = 103
    # assert btc.shape[0] == num_months, btc.shape[0]
    # assert gm.shape[0] == num_months, gm.shape[0]
    # assert nasdaq.shape[0] == num_months, nasdaq.shape[0]
    # assert gm.index[0] == pd.Timestamp('2014-10-01'), gm.index[0]
    # assert gm.iloc[0].item() == 75.85531594272636, gm.iloc[0].item()

    (corr, pv) = sp.pearsonr(btc['close'], btc['Global Money Supply'])
    assert corr == 0.8619596247709039, corr
    assert pv == 5.753006999330866e-31, pv

    fig, axes = plt.subplots(nrows=3, ncols=1, sharex='col')
    btc['close'].plot(ax=axes[0])
    btc['Global Money Supply'].plot(ax=axes[1])
    nasdaq['close'].plot(ax=axes[2])
    plt.show()
