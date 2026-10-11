class Wallet :
    def __init__ (self , name , balance , pin ) :
        self.name = name
        self.__pin = pin
        self.__balance = balance

    def showbalance (self) :
        print (f"The Balance is {self.__balance}" )

    def checkpin (self ) :
            pin = int(input("Enter The Pin"))

            if pin == self.__pin  :
                
                return f"CORRECT!"  
            
            return "INCORRECT"

    def change_pin (self) :
         old_pin  = int(input("Enter Your Old PIN : "))
         if old_pin ==self.__pin :
              new_pin = int(input("Enter Your New PIN : "))
              self.__pin = new_pin
              return "PIN Changed Successfully!"

         return "INCORRECT PIN"

    def withdraw (self , money) :
         if money <=0  :
              return("ERROR")

         if money > self.__balance:
            return "INSUFFICIENT BALANCE"     
         self.__balance = self.__balance - money
         return f'after the withdraw { self.__balance } '
    
    def deposit (self , money) :
             if money <= 0 :
                  return ("CANNOT BE -ve Numbers or zeros")
            
             self.__balance = self.__balance + money
             return f'after the deposit { self.__balance } '
         


    
    
    

p1 = Wallet("MUHAMMAD" , 5000 , 124) 

