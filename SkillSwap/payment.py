# For payment 

class Payment:
    def __init__(self, user_id):
        self.user_id = user_id
        self.subscribed = False

    def process_payment(self):
        self.subscribed = True
        return "Payment successful! You are now a Premium Member."
    
    def check_subscription(self):
        return self.subscribed