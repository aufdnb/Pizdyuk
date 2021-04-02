# Pizdyuk
Market Simulator in python

## Running Application
**main.py** is the entry point of the application.

In order to utilize the app, populate the **src/stock_data** with **.csv** files. 


This  csv files represent the Stock data. They must be of format: 
> d.m.Y H:M:S, price

The name of the csv file must be the same as of the ticker of the stock

## Rest API
In order to interact with the server the Rest requests must be sent. The following are the supported functionality.

### POST


#### Create User
To use the server, one needs to create a user in a current session.
```python
{
	{
		"action": "create_user",
		"user_id": "test_user_id",
		"name": "fake_name",
		"balance": 1000
	}
}
```

** Example Response **
```python
{
	"user_id": "test_user_id"
}
```

** NOTE ** user_id must be unique and  is optional and will be generated in case if it was not provided.

#### Buy
This request represents a buy functionality of the stock market. Currently market buy is the only type supported.

```python
{
	{
		"action": "buy",
		"user_id": "test_user_id",
		"symbol": "aapl",
		"num_shares": 3
	}
}
```

#### Sell
This request represents a sell functionality of the stock market. Currently market sell is the only type supported.

```python
{
	{
		"action": "sell",
		"user_id": "test_user_id",
		"symbol": "aapl",
		"num_shares": 1
	}
}
```

#### Add Funds
This requests enables user to add funds to their account.

```python
{
	{
		"action": "add_funds",
		"user_id": "test_user_id",
		"funds": 1000
	}
}
```


### GET


#### Get Stock
This requests returns the stock information.

```python
{
	{
		"action": "get_stock",
		"symbol": "ac"
	}
}
```


#### Get User
This request return the user information. 

```python
{
	{
		"action": "get_user",
		"user_id": "test_user_id"
	}
}
```

** Example Response **

``` python
{
  "name": "fake_name",
  "user_id": "test_user_id",
  "balance": 625.39,
  "portfolio": {
    "aapl": {
      "symbol": "aapl",
      "current_price": 127.36,
      "average_price": 0,
      "performance": 3.7500000000000284,
      "performance_percentage": 3.031282838897442,
      "num_shares": 0,
      "activity": [
        [
          "BUY",
          "01.03.2021 09:00:08",
          124.87,
          3
        ],
        [
          "SELL",
          "01.03.2021 09:00:13",
          123.69,
          1
        ],
        [
          "SELL",
          "01.03.2021 09:00:14",
          123.46,
          1
        ],
        [
          "SELL",
          "01.03.2021 09:00:16",
          123.71,
          1
        ]
      ]
    }
  }
}
```
