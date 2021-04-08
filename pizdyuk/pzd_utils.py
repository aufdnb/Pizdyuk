import uuid
from datetime import datetime 
from pzd_constants import DATE_FORMAT


def get_unique_id():
    return str(uuid.uuid4())

def datetime_to_str(date):
    return datetime.strftime(date, DATE_FORMAT)

def create_portfolio_from_data(portfolio_data):
    portfolio_members = {}
    for symbol, member_data in portfolio_data.items():
        portfolio_members[symbol] = create_portfolio_member_from_data(member_data)

    return portfolio_members
        
def create_portfolio_member_from_data(portfolio_member_data):
    symbol = portfolio_member_data['symbol']
    average_price = portfolio_member_data['average_price']
    performance_percentage = portfolio_member_data['performance_percentage']
    performance = portfolio_member_data['performance']
    num_shares = portfolio_member_data['num_shares']
    activity = portfolio_member_data['activity']

    manager = stock_manager.get_manager()
    stock = manager.get_stock(symbol)

    if not stock:
        raise PzdNotLoadedError("{} is not loaded".format(symbol))

    return  portfolio.PortfolioMember(stock, average_price, performance_percentage, performance, num_shares, activity)       