class Payment():
    def process_payment(self, amt):
        print('Payment Method: ')
        print('1. Cash')
        print('2. Card')
        print('3. UPI')
        try:
            payment_type = int(input("Choose payment method: "))
        except:
            print('Invalid Type')
            payment_type = 1
        
        match payment_type:
            case 1: self.pay_cash(amt)
            case 2: self.pay_through_card(amt)
            case 3: self.pay_through_upi(amt)
    
    def pay_cash(self, amt):
        print(f'Paid {amt} through Cash')
    
    def pay_through_card(self, amt):
        print(f'Paid {amt} through Card')
    
    def pay_through_upi(self, amt):
        print(f'Paid {amt} through UPI')
