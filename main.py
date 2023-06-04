import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
    btc = pd.read_csv('BTC-USD.csv')
    assert btc.shape == (3183, 7), btc.shape
    btc_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    assert btc.columns.equals(pd.Index(btc_columns)), btc.columns

    m2_US = pd.read_csv('US_M2.csv')
    assert m2_US.shape == (539, 15), m2_US.shape
    m2_columns = ['time', 'open', 'high', 'low', 'close', 'Global Money Supply', 'Volume',
                  'Volume MA', 'RSI', 'RSI-based MA', 'Upper Bollinger Band',
                  'Lower Bollinger Band', 'Predicted Funding Rate', 'Next Funding Rate', 'Funding Bar']
    assert m2_US.columns.equals(pd.Index(m2_columns)), m2_US.columns

    btc = btc[['Date', 'Close']]
    btc['Date'] = pd.to_datetime(btc['Date'])
    btc.set_index('Date', inplace=True)
    assert btc.index[0] == pd.Timestamp('2014-09-17'), btc.index[0]
    assert btc.iloc[0].item() == 457.334015, btc.iloc[0].item()

    m2_US = m2_US[['time', 'close']]
    m2_US['time'] = pd.to_datetime(m2_US['time']).values.astype(dtype='datetime64[D]')
    m2_US = m2_US[m2_US['time'] >= btc.index[0]]
    m2_US.set_index('time', inplace=True)
    assert m2_US.index[0] == pd.Timestamp('2014-10-01'), m2_US.index[0]
    assert m2_US.iloc[0].item() == 11551400000000, m2_US.iloc[0].item()

    fig, axes = plt.subplots(nrows=2, ncols=1, sharex='col')
    btc.plot(ax = axes[0])
    m2_US.plot(ax= axes[1])
    plt.show()
