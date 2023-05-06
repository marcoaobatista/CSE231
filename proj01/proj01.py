###########################################################
#  Project #1
#
#  Algorithm
#    prompt for rods
#    convert input string to float
#    convert rods to other distances
#    calculate walk time for given distance
#
#    print and round distances and walking time
###########################################################

rods_str = input("Input rods: ") 
rods_float = float(rods_str)
walking_speed = 3.1

meters = rods_float * 5.0292 # rods to meters conversion
feet = meters/0.3048 # meters to feet conversion
miles = meters/1609.34 # meters to miles conversion
furlongs = rods_float/40 # rods to furlongs conversion

walk_time = (miles/walking_speed)*60 # walking time in minutes

# round and output calculations
print("\nYou input",round(rods_float, 3),"rods.\n")
print("Conversions")
print("Meters:",round(meters, 3))
print("Feet:", round(feet, 3))
print("Miles:", round(miles, 3))
print("Furlongs:", round(furlongs, 3))
print("Minutes to walk", round(rods_float, 3), \
      "rods:", round(walk_time, 3))