import requests
from pprint import pprint
import json
from requests.exceptions import ConnectionError
from requests.exceptions import Timeout
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


def main():
    while True:
        val = URLValidator()
        try:
            
            #Choose metric or imperial
            unit = input("Type 'm' for metric or 'i' for imperial ('exit' to exit): ")
            if unit == "m":
                unit = "metric"
                print("Metric selected.\n")
            elif unit == "i":
                unit = "imperial"
                print("Imperial selected.\n")
            elif unit == "exit":
                break
            else:
                unit = "imperial"
                print("Invalid input. Defaulting to imperial.\n")
            city = input("Please enter city or zip code or type 'exit' to exit: ")

            #Process user input    
            if city == "exit":
                break
            elif city.isalpha():
                loc = "q"
            elif city.isdigit():
                loc = "zip"
            else:
                print("\nInvalid input. Please enter a valid city or zip code.\n")
                main()
                return city
            url = "http://api.openweathermap.org/data/2.5/weather?{}={}&APPID=a9e3d26df0e1654be0ffd5e3cb014926&units={}".format(loc,city,unit)

            #Prints connection status
            try:
                print("Connecting...")
                response = requests.get(url,timeout=5)
                val(url)
                if response.status_code == 404:
                    print("\nCity not found. Please enter a valid city or zip code.\n")
                    main()
                    return city
                elif response.status_code == 500-599:
                    print("\nThe server encountered an error. Please try again later.\n")
                else:
                    if city == "exit":
                        break
                print("Connection successful")
            except Timeout:
                print('\nConnection timeout. Please try again or type "exit" to exit.\n')
                main()
            except ConnectionError:
                print('\nConnection lost. Please connect to the internet and try again or type "exit" to exit. \n')
                main()
            except ValidationError:
                print('\nInvalid URL. Please try again or type "exit" to exit.\n')
                main()
            except:
                print("An unknown connection error occurred.")
                input("Press enter to exit.")
                break

            #Retrieves JSON data from OpenWeather API
            weather_data = requests.get("http://api.openweathermap.org/data/2.5/weather?{}={}&APPID=a9e3d26df0e1654be0ffd5e3cb014926&units={}".format(loc,city,unit)).json()
            
            #JSON data variables
            status = weather_data ['weather'][0]['main']
            temp = weather_data['main']['temp']
            feels_like = weather_data['main']['feels_like']
            temp_min = weather_data['main']['temp_min']
            temp_max = weather_data['main']['temp_max']
            humidity = weather_data['main']['humidity']
            wind_speed = weather_data['wind']['speed']
            country = weather_data['sys']['country']
            name = weather_data['name']
            
            #Prints city and country
            print("\n", '   ', name + ", " + country, "\n")
        
            #Prints JSON data in readable format
            if unit == "metric":
                print(status)
                print('\nCurrent temperature: {}°C'.format(int(temp)))
                print('\nFeels like: {}°C'.format(int(feels_like)))
                print('\nLow: {}°C'.format(int(temp_min)))
                print('\nHigh: {}°C'.format(int(temp_max)))
                print('\nHumidity: {}%'.format(int(humidity)))
                print('\nWind speed: {} kmph\n'.format(int(wind_speed)))
            if unit == "imperial":
                print(status)
                print('\nCurrent temperature: {}°F'.format(int(temp)))
                print('\nFeels like: {}°F'.format(int(feels_like)))
                print('\nLow: {}°F'.format(int(temp_min)))
                print('\nHigh: {}°F'.format(int(temp_max)))
                print('\nHumidity: {}%'.format(int(humidity)))
                print('\nWind speed: {} mph\n'.format(int(wind_speed)))
        
        except:
            print(city)
            print('An unknown error occurred.')
            input("Press enter to exit.")
            break

if __name__ == "__main__":
    main()
