import csv
import datetime
import json
from pzd_constants import DATE_FORMAT, SAVED_SESSION
from market import user, stock_manager, portfolio

def get_stock_data(csv_file):
    """ 
        Creates and returns the stock_data from a csv file

        Returns:
        Stock data (list[(date (datetime), price(float))])
    """
    stock_data = [] 

    with open(csv_file, newline='') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if row == []:
                #TODO remove
                continue
            date = datetime.datetime.strptime(row[0], DATE_FORMAT)
            price = float(row[1])
            stock_data.append((date, price))

    return stock_data

def save_user(user):
    data = json.dumps(user.get_object_info())
    name = user.name

    with open("{}.txt".format(name), "w") as f:
        f.write(data)


def get_user(user_file):
    with open(user_file, "r") as f:
        user_dict = f.read()
        user_data = json.loads(user_dict)
        
        if not __validate_user_data(user_data):
            raise RuntimeError("{} is corrupted".format(user_file))

        name = user_data['name']
        user_id = user_data['user_id']
        balance = user_data['balance']
        p = user_data['portfolio']
        portfolio_members = create_portfolio_from_data(p)

    return user.User(name, user_id, balance, portfolio_members)

        
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
        raise RuntimeError("{} is not loaded".format(symbol))

    return  portfolio.PortfolioMember(stock, average_price, performance_percentage, performance, num_shares, activity)       

def __validate_user_data(user_data):
    return user_data.pop("name", None) and user_data.pop("user_id", None) and user_data.pop("balance", None) and user_data.pop("portfolio")
