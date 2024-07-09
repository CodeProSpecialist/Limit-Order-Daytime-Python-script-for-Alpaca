import alpaca_trade_api as tradeapi
import yfinance as yf
import os

# Load environment variables for Alpaca API
APIKEYID = os.getenv('APCA_API_KEY_ID')
APISECRETKEY = os.getenv('APCA_API_SECRET_KEY')
APIBASEURL = os.getenv('APCA_API_BASE_URL')

# Initialize the Alpaca API
api = tradeapi.REST(APIKEYID, APISECRETKEY, APIBASEURL)

def main_menu():
    print("")
    print("Regular Trading Hours: 9:30am - 4:00pm ET Monday thru Friday")
    print("")
    print("1. Print All Owned Stocks")
    print("2. Sell Stock")
    print("3. Buy Stock")
    print("4. Exit")
    print("")

def print_owned_stocks():
    positions = api.list_positions()
    if positions:
        print("Owned Stocks:")
        for i, position in enumerate(positions):
            print(f"{i + 1}. {position.symbol} - Shares: {position.qty}, Avg. Price: ${position.avg_entry_price}")
    else:
        print("You don't own any stocks.")

def sell_stock(symbol):
    position = api.get_position(symbol)
    if position:
        current_quantity = int(position.qty)

        # Fetch the current price using yfinance
        stock_info = yf.Ticker(symbol)
        current_stock_price = stock_info.history(period="1d")["Close"].iloc[0]

        print(f"Symbol: {symbol}")
        print(f"Shares Owned: {current_quantity}")
        print(f"Avg. Price Paid: ${position.avg_entry_price}")
        print(f"Current Market Price: ${current_stock_price}")

        limit_price_number = float(input("Enter the limit price per share: "))
        shares_to_sell = int(input("Enter the number of shares to sell: "))

        if shares_to_sell <= current_quantity:
            order_total = shares_to_sell * limit_price_number
            print(f"Order Total: ${order_total}")
            proceed = input("Proceed to sell? (yes/no): ").lower()
            if proceed == "yes":
                submit_sell_order(symbol, shares_to_sell, limit_price_number)  # Pass all three arguments
            else:
                print("Sell order canceled.")
        else:
            print("You can't sell more shares than you own.")
    else:
        print(f"You don't own any shares of {symbol}.")

def submit_sell_order(symbol, shares_to_sell, limit_price_number):
    # Get current position
    position = api.get_position(symbol)

    if position:
        current_quantity = int(position.qty)  # Convert to an integer

        # Define order parameters
        order = {
            'symbol': symbol,
            'qty': shares_to_sell,
            'side': 'sell',
            'type': 'limit',
            'time_in_force': 'gtc',  # Good 'Til Canceled
            'limit_price': limit_price_number,
        }

        try:
            # Submit the order
            api.submit_order(**order)
            print(f"Sell order for {shares_to_sell} shares of {symbol} submitted successfully at ${limit_price_number} (Limit Price).")
        except Exception as e:
            print(f"Error submitting sell order: {e}")
    else:
        print(f"No position found for {symbol}.")

def buy_stock(symbol):
    # Fetch the current price using yfinance
    stock_info = yf.Ticker(symbol)
    current_stock_price = stock_info.history(period="1d")["Close"].iloc[0]

    print(f"Symbol: {symbol}")
    print(f"Current Market Price: ${current_stock_price}")

    limit_price_number = float(input("Enter the limit price per share: "))
    shares_to_buy = int(input("Enter the number of shares to buy: "))

    # Define order parameters
    order = {
        'symbol': symbol,
        'qty': shares_to_buy,
        'side': 'buy',
        'type': 'limit',
        'time_in_force': 'gtc',  # Good 'Til Canceled
        'limit_price': limit_price_number,
    }

    try:
        # Submit the order
        api.submit_order(**order)
        print(f"Buy order for {shares_to_buy} shares of {symbol} submitted successfully at ${limit_price_number} (Limit Price).")
    except Exception as e:
        print(f"Error submitting buy order: {e}")

while True:
    main_menu()
    choice = input("Enter your choice: ")

    if choice == "1":
        print_owned_stocks()
    elif choice == "2":
        symbol = input("Enter the stock symbol you want to sell: ")
        sell_stock(symbol)
    elif choice == "3":
        symbol = input("Enter the stock symbol you want to buy: ")
        buy_stock(symbol)
    elif choice == "4":
        print("Exiting the program.")
        break
    else:
        print("Invalid choice. Please choose a valid option.")

