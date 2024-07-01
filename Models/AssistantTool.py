import math
from Models import NASA

class AssistantTool:

    def __init__(self) -> None:
        self.nasa_power = NASA.SolarInformation()
        return
    
    def execute(self, project:dict, solar_panel:dict, inverter:dict) -> dict:
        sizing = {
            "project_id":project['id'],
            "total_number_of_panels":None,
            "panels_in_parallel":None,
            "panels_in_series":None,
            "panel_reference":solar_panel['id'],
            "inverter_reference":inverter['id'],
            "average_solar_hours":None
        }

        performance_ratio = 0.85

        try:
            #Units per year
            total_energy = project["percentage_of_electrical_energy_supplied"]/project["estimated_power_produced_annually"]*100
            #Units per day
            total_energy_day = total_energy/365 #kWh

            parameters = {
                "start":"20230101",
                "end":"20240101",
                "latitude":project['latitude'],
                "longitude":project['longitude'],
                "community":"re",
                "parameters":"ALLSKY_SFC_SW_DWN",
                "format":"json",
                "header":"true",
                "time-standard":"lst"
            }

            average_solar_hours = self.nasa_power.get_average_solar_hours(parameters)

            peak_power = total_energy_day/average_solar_hours * performance_ratio

            nominal_power = solar_panel['Impo'] * solar_panel['Vmpo']

            sizing["total_number_of_panels"] = math.ceil(peak_power/(nominal_power*1000))
            sizing["panels_in_parallel"]  = math.ceil(inverter['Vdcmax']/solar_panel['Voco'])
            sizing["panels_in_series"] = math.ceil(inverter['Idcmax']/solar_panel['Isco'])
            sizing['average_solar_hours'] = average_solar_hours
        except:
            print("Something was wrong")
        return sizing