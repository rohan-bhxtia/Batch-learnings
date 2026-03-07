class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def info(self):
        print(f"Price of {self.name} is: {self.price}")

p1 = Product("phone", 10000)
p2 = Product("lappy", 100000)

p1.info()
