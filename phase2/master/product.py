class Product(object):
    # Stores the value and price of a product
    def __init__(self, value, price):
        self.value = value
        self.price = price

    def __unicode__(self):
        return "Product [value={}, price={}]".format(self.value, self.price)
