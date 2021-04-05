import csv
import random
from pzd_constants import DATE_FORMAT
from datetime import datetime, timedelta

date = None
price = 0

with open('stock_data/aapl.csv', mode="r") as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        date = datetime.strptime(row[0], DATE_FORMAT)
        price = float(row[1])

with open('stock_data/aapl.csv', mode="w+") as f:
    writer = csv.writer(f, delimiter=",")

    for i in range(1, 360):
        date = date + timedelta(seconds=1)
        price = round(random.uniform(price - 1, price + 1), 2)
        writer.writerow([datetime.strftime(date, DATE_FORMAT), price])