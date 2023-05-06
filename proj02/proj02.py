
###########################################################
# Project #2
#  
# Forza car rental price 
#     display welcome message with intructions
#     loop while user wants to continue
#         prompt for classification code
#         loop for a valid code input
#         prompt for rental period, final and initial odometer value
#         check if odometer reset and calculate mileage accordingly
#         calculate rental price according to classification
#         display customer summary
#         prompt for continue
#     display closing message
###########################################################

import math

print("\nWelcome to Horizons car rentals. \
\n\nAt the prompts, please enter the following: \
\n\tCustomer's classification code (a character: BD, D, W) \
\n\tNumber of days the vehicle was rented (int)\
\n\tOdometer reading at the start of the rental period (int)\
\n\tOdometer reading at the end of the rental period (int)")

answer = input('\nWould you like to continue (A/B)? ')

# run loop if player wants to continue
while answer == 'A':
    code = input("\nCustomer code (BD, D, W): ")
    
    # continue prompting until user enters valid code
    while not(code == 'BD' or code == 'D' or code == 'W'):
        print("\n\t*** Invalid customer code. Try again. ***")
        code = input("\nCustomer code (BD, D, W): ")
    
    rent_days = int(input("\nNumber of days: "))
    odometer_initial = int(input("\nOdometer reading at the start: "))
    odometer_final = int(input("\nOdometer reading at the end:   "))
    
    amount_due = 0
    
    # check if odometer reset and calculate miles driven
    if odometer_final < odometer_initial: 
        miles_driven = (1000000 - abs(odometer_final - odometer_initial )) / 10
    else:
        miles_driven = (odometer_final - odometer_initial) / 10
        
    # calculate rental price according to code input
    if code == 'BD':
        amount_due = 40.0 * rent_days # daily base charge
        amount_due += 0.25 * miles_driven # mileage charge
        
    elif code == 'D':
        amount_due = 60.0 * rent_days # daily base charge
        miles_per_day = miles_driven/rent_days
        if (miles_per_day > 100):
            # mileage charge for exceeding 100
            amount_due += 0.25 * (miles_driven - (100 * rent_days))
            
    elif code == 'W':
        rent_weeks = math.ceil(rent_days/7) # weeks rented rounded up
        amount_due = 190.0 * rent_weeks # weekly base charge
        miles_per_week = miles_driven / rent_weeks
        if (1500 >= miles_per_week > 900):
            amount_due += rent_weeks * 100.0
        elif (miles_per_week > 1500):
            amount_due += rent_weeks * 200.0 # extra charge per week
            # mileage charge for exceeding 1500
            amount_due += 0.25 * (miles_driven - (1500 * rent_weeks))
        
    
    # print summary
    print("\n\nCustomer summary:")
    print("\tclassification code:", code)
    print("\trental period (days):", rent_days)
    print("\todometer reading at start:", odometer_initial)
    print("\todometer reading at end:  ", odometer_final)
    print("\tnumber of miles driven: ", miles_driven)
    print("\tamount due: $",round(amount_due,2))
    
    
    answer = input('\nWould you like to continue (A/B)? ')

print("\nThank you for your loyalty.")