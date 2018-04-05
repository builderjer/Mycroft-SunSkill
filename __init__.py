from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
import arrow
import tzlocal
from geopy.geocoders import Nominatim
from solartime import SolarTime

__author__ = 'msev'


class SunSkill(MycroftSkill):
    def __init__(self):
        super(SunSkill, self).__init__(name="SunSkill")
        city = self.config_core.get("location")
        if isinstance(city, str):
            # city is city name
            geolocator = Nominatim()
            location = geolocator.geocode(city)
            self.lat = location.latitude
            self.lon = location.longitude
        else:
            # city is a dict of location information
            self.lat = city['coordinate']['latitude']
            self.lon = city['coordinate']['longitude']

        self.localtz = tzlocal.get_localzone()

    @property
    def schedule(self):
        sun = SolarTime()
        today = arrow.now().date()
        return sun.sun_utc(today, self.lat, self.lon)

    @intent_handler(IntentBuilder("SunRiseIntent"). \
            require("SunRiseKeyword"))
    def handle_sunrise_intent(self, message):
        sunrise = self.schedule['sunrise'].astimezone(self.localtz)
        self.speak_dialog("sunrise", {"sunrise": str(sunrise)[10:16]})

    @intent_handler(IntentBuilder("SunSetIntent"). \
            require("SunSetKeyword"))
    def handle_sunset_intent(self, message):
        sunset = self.schedule['sunset'].astimezone(self.localtz)
        self.speak_dialog("sunset", {"sunset": str(sunset)[10:16]})

    @intent_handler(IntentBuilder("DawnIntent"). \
            require("DawnKeyword"))
    def handle_dawn_intent(self, message):
        dawn = self.schedule['dawn'].astimezone(self.localtz)
        self.speak_dialog("dawn", {"dawn": str(dawn)[10:16]})

    @intent_handler(IntentBuilder("DuskIntent"). \
            require("DuskKeyword"))
    def handle_dusk_intent(self, message):
        dusk = self.schedule['dusk'].astimezone(self.localtz)
        self.speak_dialog("dusk", {"dusk": str(dusk)[10:16]})

    @intent_handler(IntentBuilder("SolarNoonIntent"). \
            require("NoonKeyword"))
    def handle_noon_intent(self, message):
        noon = self.schedule['noon'].astimezone(self.localtz)
        self.speak_dialog("noon", {"noon": str(noon)[10:16]})


def create_skill():
    return SunSkill()
