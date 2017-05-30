class Item(object):

    def __init__(self, name, price, shop):
        self.name = name
        self.price = price
        self.shop = shop

    def __str__(self):
        return 'Item: {name = %s, price = %s, shop = %s}' % (self.name, self.price, self.shop)
