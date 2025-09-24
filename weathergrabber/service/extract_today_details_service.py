import logging
from pyquery import PyQuery
from weathergrabber.domain.today_details import TodayDetails
from weathergrabber.domain.temperature_hight_low import TemperatureHighLow
from weathergrabber.domain.uv_index import UVIndex
from weathergrabber.domain.moon_phase import MoonPhase
from weathergrabber.domain.moon_phase_enum import MoonPhaseEnum


class ExtractTodayDetailsService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        pass

    def execute(self, weather_data: PyQuery) -> TodayDetails:
        try:
            self.logger.debug("Extracting today's details...")

            today_details_data = weather_data.find("div[class*='TodayDetailsCard--detailsContainer'] div[data-testid='WeatherDetailsListItem']")
            icons = today_details_data.find('svg[class*="WeatherDetailsListItem--icon"]')
            values = today_details_data.find('div[data-testid="wxData"]')

            self.logger.debug(f"Parsing today details values...")
            
            high_low_value = values.eq(0).text() #'--/54°'
            wind = values.eq(1).text()  #''7\xa0mph''
            humidity = values.eq(2).text()  #'100%'
            dew_point = values.eq(3).text()  #'60°'
            pressure = values.eq(4).text()  #'30.31\xa0in'
            uv_index_value = values.eq(5).text()  #'5 of 10'
            visibility = values.eq(6).text()  #'10.0 mi'
            moon_phase_icon = icons.eq(7).attr('name')  #'phase-2'
            moon_phase_value = values.eq(7).text()  #'Waxing Crescent'

            self.logger.debug(f"Creating domain objects for today details...")

            high_low = TemperatureHighLow.from_string(high_low_value)
            uv_index = UVIndex.from_string(uv_index_value)
            moon_phase = MoonPhase(MoonPhaseEnum.from_name(moon_phase_icon), moon_phase_value)

            today_details = TodayDetails(
                high_low=high_low,
                wind=wind,
                humidity=humidity,
                dew_point=dew_point,
                pressure=pressure,
                uv_index=uv_index,
                visibility=visibility,
                moon_phase=moon_phase
            )

            self.logger.debug(f"Extracted today's details: {today_details}")
            return today_details

        except Exception as e:
            self.logger.error(f"Error extracting today's details: {e}")
            raise ValueError("Could not extract today's details.") from e