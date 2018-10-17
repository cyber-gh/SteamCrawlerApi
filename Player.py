

class Player(object):
    
    def __init__(self,steamlink,inventoryValue,hours,level ):
        self.steamlink = steamlink
        self.inventoryValue= inventoryValue
        self.hours = hours
        self.level = level

    def show(self):
        print(self.steamlink +'  '+ str(self.inventoryValue) + '  ' + str(self.hours) + '  ' + str(self.level))

    
    def isGood(self):
        if float(self.inventoryValue) > 30 and float(self.hours) >= 0 and float(self.hours) < 2500 and float(self.level) < 55 :
            return True
        else:
            return False
