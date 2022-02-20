import requests
from pprint import pprint
import json
from requests.exceptions import ConnectionError


def main():
    while True:
        try:
            city = input("Please enter city or zip code(type 'exit' to exit): ")
            
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
            url = "http://api.openweathermap.org/data/2.5/weather?{}={}&APPID=a9e3d26df0e1654be0ffd5e3cb014926&units=imperial".format(loc,city)
           
            #Prints connection status
            print("Connecting...")
            response = requests.get(url,timeout=5)
            if response.status_code == 200:
                print("Connection successful")
            elif response.status_code == 404:
                print("\nCity not found. Please enter a valid city or zip code.\n")
                main()
                return city
            elif response.status_code == 500-599:
                print("The server encountered an error. Please try again later.")
            else:
                if city == "exit":
                    break
                print("An unknown connection error occurred.")
            
            #Retrieves JSON data from OpenWeather API    
            weather_data = requests.get("http://api.openweathermap.org/data/2.5/weather?{}={}&APPID=a9e3d26df0e1654be0ffd5e3cb014926&units=imperial".format(loc,city)).json()
            
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
            print(status)
            print('Current temperature: {}°F'.format(int(temp)))
            print('Feels like: {}°F'.format(int(feels_like)))
            print('Low: {}°F'.format(int(temp_min)))
            print('High: {}°F'.format(int(temp_max)))
            print('Humidity: {}%'.format(int(humidity)))
            print('Wind speed: {} mph\n'.format(int(wind_speed)))
        
        except ConnectionError:
            print('\nConnection lost. Please connect to the internet and try again or type "exit" to exit. \n')  
        
        except:
            print(city)
            print('An unknown error occurred.')
            input("Press enter to exit.")
            break


if __name__ == "__main__":
    main()

#to do:
#add option to choose between metric and imperial