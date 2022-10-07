class Order:
    def __init__(self, order_dict):
        self.__dict = order_dict
        self.__asset = order_dict["asset"]
        self.__currency = order_dict["currency"]
        self.__cron = order_dict["frequency"]
        self.__quantity = order_dict["quantity"]
        self.__exchange = order_dict["exchange"]
    
    def __repr__(self):
        return str(self.__dict)
    
    @property
    def exchange(self):
        return self.__exchange
    
    @property
    def asset(self):
        return self.__asset

    @property
    def currency(self):
        return self.__currency
    
    @property
    def quantity(self):
        return self.__quantity
    
    @property
    def cron(self):
        return self.__cron