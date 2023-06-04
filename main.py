import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
    df = pd.read_csv('BTC-USD.csv')
    assert df.shape == (3183,7), df.shape
    columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    assert df.columns.equals(pd.Index(columns)), df.columns

    btc = df[['Date', 'Close']]
    btc.plot()
    plt.show()
