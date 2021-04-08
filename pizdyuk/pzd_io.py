import os
import csv
import datetime
import json
from pzd_errors import PizdyukError, PzdNotLoadedError
from pzd_constants import DATE_FORMAT, USER_DATA_PATH
from pzd_utils import create_portfolio_from_data, create_portfolio_member_from_data
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
    data_path = USER_DATA_PATH
    src_dir = os.path.dirname(__file__)
    data_path = os.path.join(src_dir, data_path)


    with open("{0}/{1}.txt".format(data_path, name), "w") as f:
        f.write(data)


def get_user(user_file):
    """ 
    Function to retrieve user data from a file

    Params: 
        user_file (str): path containing the specified user_file

    Returns:
        User object corresponding to data or None if the file is not found
    """

    if not os.path.isfile(user_file):
        return None


    with open(user_file, "r") as f:
        user_dict = f.read()
        user_data = json.loads(user_dict)
        
        if not __validate_user_data(user_data):
            raise PizdyukError("{} is corrupted".format(user_file))

        name = user_data['name']
        user_id = user_data['user_id']
        balance = user_data['balance']
        p = user_data['portfolio']
        portfolio_members = create_portfolio_from_data(p)

    return user.User(name, user_id, balance, portfolio_members)

        


def __validate_user_data(user_data):
    return user_data.get("name", None) and user_data.get("user_id", None) and user_data.get("balance", None) and user_data.get("portfolio")
