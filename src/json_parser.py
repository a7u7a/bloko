def parse_stocks_data(json_data: list) -> dict:
    """ Transforms a list of stock data into a dictionary keyed by symbol. """

    required_fields = {"current_price", "regular_market_volume", "regular_market_change_percent"}
    result = {}
    for stock in json_data:
        symbol = stock.get("symbol")
        if not symbol:
            continue
            
        # Extract only the required fields
        stock_data = {
            field: stock.get(field)
            for field in required_fields
            if field in stock
        }
        
        # Only add if all required fields are present
        if len(stock_data) == len(required_fields):
            result[symbol] = stock_data
            
    return result