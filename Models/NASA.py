import requests 

class SolarInformation:
    
    def __init__(self) -> None:
        return

    def get_information(self, parameters:dict = {})->dict:

        #Full URL for path 
        full_path = "&".join(f"{key}={value}" for key, value in parameters.items())
        base_url = "https://power.larc.nasa.gov/api/temporal/daily/point?"+full_path

        payloads = {}
        headers = {}

        response = requests.request("GET", 
                                    base_url, 
                                    headers=headers, 
                                    data=payloads)
        
        return response.json()

    def get_average_solar_hours(self, parameters:dict = {})->dict:
        nasa_answer = self.get_information(parameters)

        solar_hours = nasa_answer['properties']['parameter']['ALLSKY_SFC_SW_DWN']

        total_solar_hours = []
        for time,solar_hour in solar_hours.items():
            total_solar_hours.append(solar_hour)
            
        return sum(total_solar_hours)/len(total_solar_hours)