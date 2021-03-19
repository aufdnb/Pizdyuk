import csv
import datetime
from pzd_constants import DATE_FORMAT

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
            date = datetime.datetime.strptime(row[0], DATE_FORMAT)
            price = row[1]
            stock_data.append((date, price))

    return stock_data
