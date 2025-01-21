import MetaTrader5 as mt5
from dotenv import load_dotenv
import os

load_dotenv()

order_book = [
    {
        "lot_size": 0.01,
        "number_of_trades": 5,
    },
    {
        "lot_size": 0.02,
        "number_of_trades": 2,
    },
    {
        "lot_size": 0.03,
        "number_of_trades": 1,
    },
    {
        "lot_size": 0.04,
        "number_of_trades": 1,
    },
    {
        "lot_size": 0.05,
        "number_of_trades": 2,
    },
    {
        "lot_size": 0.1,
        "number_of_trades": 2,
    }
]


def open_trade(symbol, lot, tp, sl):
    """
        Opens a trade with the given parameters
    """
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY,
        "price": mt5.symbol_info_tick(symbol).ask,
        "sl": sl,
        "tp": tp,
        "magic": 234000,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }
    result = mt5.order_send(request)
    return result

def close_trade(ticket):
    """
        Closes a trade with the given ticket
    """

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "ticket": ticket,
        "magic": 234000,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }
    result = mt5.order_send(request)
    return result


def close_all_trades():
    """
        Closes all active trades
    """
    positions = mt5.positions_get()
    for position in positions:
        close_trade(position.ticket)



def main():
    """
        Main function to run the script
    """
    symbol = "BTCUSDm"

    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()
        return
    
    if not mt5.login(int(os.getenv("MT5_LOGIN")), os.getenv("MT5_PASSWORD"), os.getenv("MT5_SERVER")):
        print("login() failed")
        mt5.shutdown()
        return


    while True:
        response = str(input("Type 'start' to open trades or 'stop' to close all trades: "))
        if response == "start":
            for order in order_book:
                for i in range(order["number_of_trades"]):
                    open_trade(symbol, order["lot_size"], tp, sl)
        elif response == "stop":
            close_all_trades()
            break

    mt5.shutdown()



if __name__ == "__main__":
    main()
