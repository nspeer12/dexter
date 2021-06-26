import requests, json

def weather_get (query:str, context):
    API_KEY = "4ba177824d974cc0a3a235847211106"
    #CITY = input("Enter City Name : ")
    #CITY = 'Orlando'
    CITY = context
    # URL to obtain country list as JSON: API key and Zip Code are concatenated with the base URL
    URL = "https://api.weatherapi.com/v1/current.json?key=" + API_KEY + "&q=" + CITY + "&aqi=no";

    # send request to API and get response
    response_data = requests.get(URL)

    # store response in variable
    data = response_data.text

    # parse the json into a JSON object
    json_data = json.loads(data)

    # uncomment following line to see raw json
    # print (data)

    # find individual fields in the JSON data
    location_name = json_data['location']['name']
    region = json_data['location']['region']
    latitude = json_data['location']['lat']
    longitude = json_data['location']['lon']
    temp_c = json_data['current']['temp_c']
    temp_f = json_data['current']['temp_f']
    wind_mph = json_data['current']['wind_mph']
    condition = json_data['current']['condition']['text']

    print("")
    print (f"Location name: {location_name}")
    print (f"Region name: {region}")
    print (f"Longitude: {longitude}")
    print (f"Latitude: {latitude}")
    print (f"Wind (mph): {wind_mph}")
    #print (f"Conditions: {condition}")
    return condition