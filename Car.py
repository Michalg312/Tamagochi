class Car:
    def __init__(self,image,fuel,oil,maxOilCapacity,maxFuelCapacity):
        self.image=image
        self.fuel=fuel
        self.oil=oil
        self.maxOilCapacity=maxOilCapacity
        self.maxFuelCapacity=maxFuelCapacity

    def makeNoise(self):
        print("wrum")

    def addOil(self,num):
        self.oil+=num

    def addFuel(self, num):
        self.fuel += num
