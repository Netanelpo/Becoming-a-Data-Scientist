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


def plot_data(i, data, yticks, color):
    fontsize = 12
    ax = btc['Global Money Supply'].plot(ax=axes[i], color='b')
    ax.set_yticks([80, 100, 120])
    ax.set_ylabel('Global Money Supply', color='b', fontsize=fontsize)
    ax.tick_params(which='both', bottom=False)
    ax.set_xlabel('')
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax2 = ax.twinx()
    data.plot(ax=ax2, color=color)
    ax2.set_yticks(yticks)
    ax2.set_ylabel(data.name, color=color, fontsize=fontsize)
    ax2.tick_params(which='both', bottom=False)
    for spine in ax2.spines.values():
        spine.set_visible(False)

    from matplotlib.lines import Line2D
    custom_lines = [Line2D([0], [0], color='b', lw=2),
                    Line2D([0], [0], color=color, lw=2)]

    ax2.legend(custom_lines, ['Global Money Supply (trillion USD)', data.name + ' price (thousand USD)'])

    (c, pvalue) = sp.pearsonr(data, btc['Global Money Supply'])
    ax.text(0.05, 0.65, 'Pearson coefficient - ' + str(round(c, 3)), transform=ax.transAxes, fontsize=fontsize)


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

    plt.rcParams['figure.figsize'] = [8, 8]
    fig, axes = plt.subplots(nrows=2, ncols=1, sharex='col')

    plot_data(0, btc['BTC'], [0, 20, 40, 60], 'r')
    plot_data(1, nasdaq['NASDAQ'], [5, 10, 15], 'g')

    plt.show()
