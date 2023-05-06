###########################################################
#  Project #3
#
# Algorithm
# while user wants to continue, loop
#     display welcome message
#     prompt user for inputs
#     if required inputs are not entered, end current loop
#     set price per foot and tax rate to be used according to location input
#     check if apr and down payment are valid, if not set them to 0
#    
#     if there is a Valid sq footage input and Valid monthly payment
#         calculate cost and payables
#         display cost and payables
#         check and display whether user can afford the house based on input
#         prompt user if they want to display amortization table
#             calculate and interest, principal, balance
#             for every month
#                 display and recalculate values
#                 if statement to avoid dividing by 0
#                
#     if there is a Invalid sq footage input and Valid monthly payment
#         calculate cost and house size estimation based on values
#         display calculations results
#        
#     if there is a Valid sq footage input and Invalid monthly payment
#         calculate cost and payables
#         display cost and expected payables
#         prompt user if they want to display amortization table
#             calculate and interest, principal, balance
#             for every month
#                 display and recalculate values
#                 if statement to avoid dividing by 0
#    
#     prompt if user wants to continue
###########################################################

# 30-year fixed rate mortgage, 30 years * 12 monthly payments
NUMBER_OF_PAYMENTS = 360
SEATTLE_PROPERTY_TAX_RATE = 0.0092
SAN_FRANCISCO_PROPERTY_TAX_RATE = 0.0074
AUSTIN_PROPERTY_TAX_RATE = 0.0181
EAST_LANSING_PROPERTY_TAX_RATE = 0.0162
AVERAGE_NATIONAL_PROPERTY_TAX_RATE = 0.011
SEATTLE_PRICE_PER_SQ_FOOT = 499.0
SAN_FRANCISCO_PRICE_PER_SQ_FOOT = 1000.0
AUSTIN_PRICE_PER_SQ_FOOT = 349.0
EAST_LANSING_PRICE_PER_SQ_FOOT = 170.0
AVERAGE_NATIONAL_PRICE_PER_SQ_FOOT = 244.0
APR_2023 = 0.0668


cont = 'y'

while cont.lower() == 'y':
    print("\nMORTGAGE PLANNING CALCULATOR\n============================ ")
    print("\nEnter a value for each of the following items or type 'NA' \
if unknown ")
    
    location = input("\nWhere is the house you are considering \
(Seattle, San Francisco, Austin, East Lansing)? ")

    sq_footage_str = input("\nWhat is the maximum square footage \
you are considering? ")

    max_monthly_payment_str = input("\nWhat is the maximum monthly payment \
you can afford? ")
    
    # If user does not enter both required inputs, warn and restart loop
    if sq_footage_str == 'NA' and max_monthly_payment_str == 'NA':
        print("\nYou must either supply a desired square footage \
or a maximum monthly payment. Please try again.")
        continue
    
    down_payment_str = input("\nHow much money can you put down \
as a down payment? ")

    annual_percentage_rate_str = input("\nWhat is the current annual \
percentage rate? ")
    
    
    # Check if location input is known, set price per foot and 
    # property tax rate accordingly
    price_per_sq_foot = 0
    property_tax_rate = 0
    if location == 'Seattle':
        price_per_sq_foot = SEATTLE_PRICE_PER_SQ_FOOT
        property_tax_rate = SEATTLE_PROPERTY_TAX_RATE
        
    elif location == 'San Francisco':
        price_per_sq_foot = SAN_FRANCISCO_PRICE_PER_SQ_FOOT
        property_tax_rate = SAN_FRANCISCO_PROPERTY_TAX_RATE
    
    elif location == 'Austin':
        price_per_sq_foot = AUSTIN_PRICE_PER_SQ_FOOT
        property_tax_rate = AUSTIN_PROPERTY_TAX_RATE
    
    elif location == 'East Lansing':
        price_per_sq_foot = EAST_LANSING_PRICE_PER_SQ_FOOT
        property_tax_rate = EAST_LANSING_PROPERTY_TAX_RATE
    else:
        print("\nUnknown location. Using national averages for \
price per square foot and tax rate.")

        price_per_sq_foot = AVERAGE_NATIONAL_PRICE_PER_SQ_FOOT
        property_tax_rate = AVERAGE_NATIONAL_PROPERTY_TAX_RATE
        location = 'the average U.S. housing market'
        
        
    # Check if the down payment input is a number
    down_payment = 0
    if down_payment_str.isdigit():
        down_payment = float(down_payment_str)
        
    # Check if the annual percentage rate input is a number
    # otherwise, set it to average national rate
    apr = 0
    if annual_percentage_rate_str != 'NA':
        apr = float(annual_percentage_rate_str)/100
    else:
        apr = APR_2023
        
    # Valid sq footage input, Valid max monthly payment
    if sq_footage_str != 'NA' and max_monthly_payment_str != 'NA':
        sq_footage = float(sq_footage_str)
        max_monthly_payment = float(max_monthly_payment_str)

        cost = sq_footage * price_per_sq_foot
        monthly_taxes = cost * property_tax_rate / 12
        loan_amount = cost - down_payment
        interest_rate = apr/12 # Monthly percentage rate
        
        # mortgage monthly payment formula
        mortgage_monthly_payment = loan_amount* \
            (interest_rate*(1 + interest_rate)**NUMBER_OF_PAYMENTS) \
            /((1 + interest_rate)**NUMBER_OF_PAYMENTS - 1)
        
        total_payable = mortgage_monthly_payment + monthly_taxes
        
        print("\n\nIn {}, an average {:.0f} sq. foot house would cost ${:.0f}.\
\nA 30-year fixed rate mortgage with a down payment of ${:.0f} at {:.1%} APR \
results\n\tin an expected monthly payment of ${:.2f} (taxes) \
+ ${:.2f} (mortgage payment) = ${:.2f}\
".format(location, sq_footage, cost, down_payment, apr, monthly_taxes, \
        mortgage_monthly_payment, total_payable))
        
        # Check and display whether user can afford the house based on input
        if total_payable > max_monthly_payment:
            print("Based on your maximum monthly payment of ${:.2f} \
you cannot afford this house.".format(max_monthly_payment))
        else:
            print("Based on your maximum monthly payment of ${:.2f} \
you can afford this house.".format(max_monthly_payment))
        
        
        display_amortization_table = input("\nWould you like to print \
the monthly payment schedule (Y or N)? ")
        
        if display_amortization_table.lower() == 'y':
            # Setup amortization table
            print("\n{:^7s}|{:^12s}|{:^13s}|{:^14s}"
                  .format('Month', 'Interest', 'Principal', 'Balance'))
            print("="*48)
            
            balance = cost - down_payment
            interest = balance*interest_rate
            mortgage_monthly_payment = balance*\
                (interest_rate*(1 + interest_rate)**NUMBER_OF_PAYMENTS) \
                /((1+interest_rate)**NUMBER_OF_PAYMENTS - 1)
            principal =  mortgage_monthly_payment - interest
            
            for month in range(1,NUMBER_OF_PAYMENTS+1): 
                print("{:^7}| ${:>9.2f} | ${:>10.2f} | ${:>11.2f}"
                      .format(month, interest, principal, balance))
                
                # Update values for current month
                balance = balance - principal
                interest = balance * interest_rate
                
                # Avoid dividing by 0
                if month != 360:
                    mortgage_monthly_payment = balance* \
                        (interest_rate*(1 + interest_rate) \
                             **(NUMBER_OF_PAYMENTS-month)) \
                        /((1 + interest_rate)**(NUMBER_OF_PAYMENTS-month) - 1)
                
                principal =  mortgage_monthly_payment - interest
                
               
    # NO sq footage, Valid max monthly payment
    if sq_footage_str == 'NA' and max_monthly_payment_str != 'NA':
        max_monthly_payment = float(max_monthly_payment_str)
        
        interest_rate = apr/12 # Monthly percentage rate
        
        loan_amount = max_monthly_payment/ \
            ((interest_rate*(1 + interest_rate)**NUMBER_OF_PAYMENTS) \
            /((1 + interest_rate)**NUMBER_OF_PAYMENTS - 1))
        
        cost = down_payment + loan_amount
        sq_footage = cost/price_per_sq_foot
        
        print("\n\nIn {}, a maximum monthly payment of ${:.2f} \
allows the purchase of a house of {:.0f} sq. feet for ${:.0f}\n\t assuming a \
30-year fixed rate mortgage with a ${:.0f} down payment at {:.1%} APR."
.format(location, max_monthly_payment,sq_footage,cost,down_payment,apr))
        

    # Valid sq footage, NO max monthly payment
    if sq_footage_str != 'NA' and max_monthly_payment_str == 'NA':
        sq_footage = float(sq_footage_str)
        
        cost = sq_footage * price_per_sq_foot
        monthly_taxes = cost * property_tax_rate / 12
        
        interest_rate = apr/12 # Monthly percentage rate
        loan_amount = cost - down_payment
        mortgage_monthly_payment = loan_amount* \
            (interest_rate*(1 + interest_rate)**NUMBER_OF_PAYMENTS) \
            /((1 + interest_rate)**NUMBER_OF_PAYMENTS - 1)
        
        total_payable = mortgage_monthly_payment + monthly_taxes
        
        print("\n\nIn {}, an average {:.0f} sq. foot house would cost ${:.0f}.\
\nA 30-year fixed rate mortgage with a down payment of ${:.0f} at {:.1%} APR \
results\n\tin an expected monthly payment of ${:.2f} (taxes) \
+ ${:.2f} (mortgage payment) = ${:.2f}"
        .format(location, sq_footage, cost, down_payment, apr, monthly_taxes, \
                mortgage_monthly_payment, total_payable))
        
        display_amortization_table = input("\nWould you like to print \
the monthly payment schedule (Y or N)? ")
        
        if display_amortization_table.lower() == 'y':
            # Setup amortization table
            print("\n{:^7s}|{:^12s}|{:^13s}|{:^13s} "
                  .format('Month', 'Interest', 'Principal', 'Balance'))
            print("="*48)
            
            balance = cost - down_payment
            interest = balance*interest_rate
           
            mortgage_monthly_payment = balance*\
                (interest_rate*(1 + interest_rate)**NUMBER_OF_PAYMENTS) \
                /((1+interest_rate)**NUMBER_OF_PAYMENTS - 1)
                
            principal =  mortgage_monthly_payment - interest
            
            for month in range(1,NUMBER_OF_PAYMENTS+1): 
                print("{:^7}| ${:>9.2f} | ${:>10.2f} | ${:>11.2f}"
                      .format(month, interest, principal, balance))
                
                # Update values for current month
                balance = balance - principal
                interest = balance * interest_rate
               
                # Avoid dividing by 0
                if month != 360:
                    mortgage_monthly_payment = balance* \
                        (interest_rate*(1 + interest_rate) \
                             **(NUMBER_OF_PAYMENTS-month)) \
                        /((1 + interest_rate)**(NUMBER_OF_PAYMENTS-month) - 1)
                        
                principal =  mortgage_monthly_payment - interest
               
    cont = input("\nWould you like to make another attempt (Y or N)? ")
