from tardis_dev import datasets
import pandas as pd
import numpy as np
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')
import nest_asyncio



nest_asyncio.apply()
datasets.download(
    exchange="binance-futures",
    data_types=[
        "incremental_book_L2",
        #"trades",
        #"quotes",
        #"derivative_ticker",
        #"book_snapshot_25",
        #"liquidations"
    ],
    from_date=f"2023-02-01T00:00:00Z",
    to_date=f"2023-02-01T23:59:59Z",
    symbols=['BTCUSDT'],
    api_key='',
)

nest_asyncio.apply()
datasets.download(
    exchange="binance",
    data_types=[
        "incremental_book_L2",
        #"trades",
        #"quotes",
        #"derivative_ticker",
        #"book_snapshot_25",
        #"liquidations"
    ],
    from_date=f"2023-02-01T00:00:00Z",
    to_date=f"2023-02-01T23:59:59Z",
    symbols=['BTCUSDT'],
    api_key='',
)

nest_asyncio.apply()
datasets.download(
    exchange="binance-futures",
    data_types=[
        #"incremental_book_L2",
        #"trades",
        "quotes",
        #"derivative_ticker",
        #"book_snapshot_25",
        #"liquidations"
    ],
    from_date=f"2023-02-01T00:00:00Z",
    to_date=f"2023-02-01T23:59:59Z",
    symbols=['BTCUSDT'],
    api_key='',
)

nest_asyncio.apply()
datasets.download(
    exchange="binance",
    data_types=[
        #"incremental_book_L2",
        #"trades",
        "quotes",
        #"derivative_ticker",
        #"book_snapshot_25",
        #"liquidations"
    ],
    from_date=f"2023-02-01T00:00:00Z",
    to_date=f"2023-02-01T23:59:59Z",
    symbols=['BTCUSDT'],
    api_key='',
)

fname_spotquotes = 'binance_quotes_2023-02-01_BTCUSDT.csv.gz'
fname_perpquotes = 'binance-futures_quotes_2023-02-01_BTCUSDT.csv.gz'
fname_perp = 'binance-futures_incremental_book_L2_2023-02-01_BTCUSDT.csv.gz'
fname_spot = 'binance_incremental_book_L2_2023-02-01_BTCUSDT.csv.gz'

perpbook = pd.read_csv(f'datasets/{fname_perp}', compression='gzip')
spotbook = pd.read_csv(f'datasets/{fname_spot}', compression='gzip')
    
perpquotes = pd.read_csv(f'datasets/{fname_perpquotes}', compression='gzip')
spotquotes = pd.read_csv(f'datasets/{fname_spotquotes}', compression='gzip')


def bookstate(book, snaptime):
    book = book[book['timestamp'] == 1675227824977135]
    ##################################################
    return book

def bookpressure(quotes):
    ##################################################
    return quotes
    
bookpressure(perpquotes)

def Latency():
    
    bpspot = bookpressure(spotquotes).set_index('timestamp')
    bpperp = bookpressure(perpquotes).set_index('timestamp')
    combinedbp = bpperp.join(bpspot, lsuffix='_perp', rsuffix='_spot')
    combinedbp[['ask_amount_spot', 'ask_price_spot', 'bid_price_spot', 'bid_amount_spot', 'bookpressure_spot']] = combinedbp[['ask_amount_spot', 'ask_price_spot', 'bid_price_spot', 'bid_amount_spot', 'bookpressure_spot']].ffill()
    combinedbp[['ask_amount_spot', 'ask_price_spot', 'bid_price_spot', 'bid_amount_spot', 'bookpressure_spot']] = combinedbp[['ask_amount_spot', 'ask_price_spot', 'bid_price_spot', 'bid_amount_spot', 'bookpressure_spot']].bfill()
    combinedbp['bookpressure_spot'].ffill(inplace=True)
    combinedbp['bookpressure_spot'].bfill(inplace=True)
    combinedbp['bookpressure_perp'].ffill(inplace=True)
    
def main():
    bookstate(spotbook, 1675227824977135)

main()