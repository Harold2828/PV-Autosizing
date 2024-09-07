import math
import numpy as np
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
            "number_of_inverters":None,
            "panel_reference":solar_panel['id'],
            "inverter_reference":inverter['id']
        }

        performance_ratio = 0.85

        try:

            #Data validation of inverters
            if(np.isnan(inverter['Vdcmax'])):
                raise Exception("The Maximum Voltage in DC should be a number not a Nan")
            
            if(np.isnan(inverter['Idcmax'])):
                raise Exception("The Maximum Current in DC should be a number not a Nan")

            #Data validation of solar panels
            if(np.isnan(solar_panel['Impo'])):
                raise Exception("The maximum current solar panel should be a number ")
            if(np.isnan(solar_panel['Vmpo'])):
                raise Exception("The maximum voltage solar panel should be a number ")
            if(np.isnan(solar_panel['Voco'])):
                raise Exception("The Voltage in open circuit should be a number")
            if(np.isnan(solar_panel['Isco'])):
                raise Exception("The Current in short circuit should be a number")


            #Units per year
            total_energy = project["estimated_power_produced_annually"] / (project["percentage_of_electrical_energy_supplied"]/100)
            #Units per hour
            total_energy_day = total_energy/8760 #kWh

            peak_power = total_energy_day/(project['average_solar_hours'] * performance_ratio * 1000) #w

            nominal_inverter_power = inverter['Vdcmax'] * inverter['Idcmax']
            number_of_inverters = peak_power/nominal_inverter_power
            sizing["number_of_inverters"] = number_of_inverters
            if(number_of_inverters <1):
                raise Exception("The inverter have more capacity than the necessary")


            nominal_power = solar_panel['Isco'] * solar_panel['Voco']

            sizing["total_number_of_panels"] = math.ceil(peak_power/nominal_power)
            sizing["panels_in_parallel"]  = math.ceil(inverter['Vdcmax']/solar_panel['Voco'])
            sizing["panels_in_series"] = math.ceil(inverter['Idcmax']/solar_panel['Isco'])

            if(sizing["panels_in_parallel"] * sizing["panels_in_series"] > sizing["total_number_of_panels"]):
                raise Exception("The number can't be more than the limit")
            
            if(sizing["panels_in_parallel"] * sizing["panels_in_series"] * solar_panel['Module Area [m^2]'] > project['area']):
                raise Exception("No is possible")

        except:
            sizing["total_number_of_panels"] = None
            sizing["panels_in_parallel"]  = None
            sizing["panels_in_series"] = None
            sizing["total_number_of_panels"] = None

        return sizing
   
