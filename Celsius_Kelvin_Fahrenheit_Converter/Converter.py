import time
from colorama import Fore, Style, Back

def kelvin_to_celsius(value):
    return value - 273.15
def kelvin_to_fahrenheit(value):
    return 1.8 * (value - 273.15) + 32

def fahrenheit_to_celsius(value):
    return (value - 32) * 5/9
def fahrenheit_to_kelvin(value):
    return (value + 459.67) * 5/9

def celcius_to_fahrenheit(value):
    return (value * 1.8) + 32
def celcius_to_kelvin(value):
    return value + 273.15

def main():
    while True:
        print(f"\n{Style.BRIGHT}{Fore.BLUE}Tell me what you want to convert{Style.RESET_ALL}\n1. Kelvin to Celcius\n2. Kelvin to Fahrenheit\n3. Fahrenheit to Celcius\n4. Fahrenheit to Kelvin\n5. Celcius to Fahrenheit\n6. Celsius to Kelvin\n0. END OPERATION")
        try: 
            value = int(input("\nGive me the convert format please > "))
            if(value > 6 or value < 0):
                while True:
                    print("Sorry, this is not a valid value, Please try again")
                    value = int(input("Give me the convert format please > "))
                    if(value < 6 and value > 0):
                        break
        except ValueError:
            print("Sorry, this is not a valid value, Please try again")
            while True:   
                try:
                    value = int(input("\nGive me the convert format please > "))
                    if(value <= 6 or value >= 0):
                        break
                except ValueError:
                    print("Do you even try? Again!!")
                
        # Switch Statement
        if(value == 0):
            print(f"\n{Fore.RED}{Style.BRIGHT}Thanks for playing with me{Style.RESET_ALL}")
            break

        # Kelvin to Celcius
        elif(value == 1):
            try:
                give_value = float(input("Give the Kelvin value > "))
            except ValueError:
                while True:
                    print("Sorry, this is not a valid value, Please try again > ")
                    give_value = float(input("Give the Kelvin value > "))

            return_value = kelvin_to_celsius(give_value)
            print(f"\n{Fore.GREEN}{Style.BRIGHT} Celcius: {round(return_value, 2)} C{Style.RESET_ALL}")
            time.sleep(2)

        # Kelvin to Fahrenheit
        elif(value == 2):
            try:
                give_value = float(input("Give the Kelvin value > "))
            except ValueError:
                while True:
                    print("Sorry, this is not a valid value, Please try again > ")
                    give_value = float(input("Give the Kelvin value > "))

            return_value = kelvin_to_fahrenheit(give_value)
            print(f"\n{Fore.GREEN}{Style.BRIGHT} Fahrenheit: {round(return_value, 2)} F{Style.RESET_ALL}")
            time.sleep(2)

        # Farahrenheit to Celsius
        elif(value == 3):
            try:
                give_value = float(input("Give the Farahrenheit value > "))
            except ValueError:
                while True:
                    print("Sorry, this is not a valid value, Please try again > ")
                    give_value = float(input("Give the Farahrenheit value > "))

            return_value = fahrenheit_to_celsius(give_value)
            print(f"\n{Fore.GREEN}{Style.BRIGHT} Celsius: {round(return_value, 2)} C{Style.RESET_ALL}")
            time.sleep(2)

        # Farahrenheit to Kelvin
        elif(value == 4):
            try:
                give_value = float(input("Give the Farahrenheit value > "))
            except ValueError:
                while True:
                    print("Sorry, this is not a valid value, Please try again > ")
                    give_value = float(input("Give the Farahrenheit value > "))

            return_value = fahrenheit_to_kelvin(give_value)
            print(f"\n{Fore.GREEN}{Style.BRIGHT} Kelvin: {round(return_value, 2)} K{Style.RESET_ALL}")
            time.sleep(2)
        
        # Celsius to Farahrenheit
        elif(value == 5):
            try:
                give_value = float(input("Give the Celsius value > "))
            except ValueError:
                while True:
                    print("Sorry, this is not a valid value, Please try again > ")
                    give_value = float(input("Give the Celsius value > "))

            return_value = celcius_to_fahrenheit(give_value)
            print(f"\n{Fore.GREEN}{Style.BRIGHT} Farahrenheit: {round(return_value, 2)} F{Style.RESET_ALL}")
            time.sleep(2)
        
        # Celsius to Kelvin
        elif(value == 6):
            try:
                give_value = float(input("Give the Celsius value > "))
            except ValueError:
                while True:
                    print("Sorry, this is not a valid value, Please try again > ")
                    give_value = float(input("Give the Celsius value > "))

            return_value = celcius_to_kelvin(give_value)
            print(f"\n{Fore.GREEN}{Style.BRIGHT} Kelvin: {round(return_value, 2)} K{Style.RESET_ALL}")
            time.sleep(2)
        

if __name__ == "__main__":
    main()