import cherrypy
import urllib2
import xml.etree.ElementTree as ET
import json

class Index(object):

    def api(self,query="10027"):

        now = self.weather_now(query)
        fahr = self.get_f_now(now)
        cels = self.get_c_now(now)
        lst = self.weather_forecast(query)

        days = self.forecast_today_low(lst) + " " + self.forecast_today_high(lst)
        return str(days)
    api.exposed = True


    def weather_now(self,query):
        req = urllib2.urlopen("http://www.google.com/ig/api?weather=" + query)
        tree = ET.ElementTree()
        elt = tree.parse(req) #returns an Element object
        cur_weather = elt.find("weather").find("current_conditions")
        return cur_weather

    def weather_forecast(self,query):
        req = urllib2.urlopen("http://www.google.com/ig/api?weather=" + query)
        tree = ET.ElementTree()
        elt = tree.parse(req) #returns an Element object
        cur_weather = elt.find("weather").findall("forecast_conditions")
        return cur_weather

    def forecast_today_rich(self,forecast):
        elt = lst[0]
        return (elt.find("day_of_week").get("data"),elt.find("low").get("data"),elt.find("high").get("data"),elt.find("condition").get("data"))

    def forecast_today_day(self,forecast):
        elt = forecast[0]
        return elt.find("day_of_week").get("data")

    def forecast_today_low(self,forecast):
        elt = forecast[0]
        return elt.find("low").get("data")

    def forecast_today_high(self,forecast):
        elt = forecast[0]
        return elt.find("high").get("data")

    def forecast_today_condition(self,forecast):
        elt = forecast[0]
        return elt.find("condition").get("data")

    def forecast_rich(self,forecast):
        return [(elt.find("day_of_week").get("data"),elt.find("low").get("data"),elt.find("high").get("data"),elt.find("condition").get("data")) for elt in forecast]

    def forecast_low(self,forecast):
        return [elt.find("low").get("data") for elt in forecast]

    def forecast_high(self,forecast):
        return [elt.find("high").get("data") for elt in forecast]

    def forecast_day(self,forecast):
        return [elt.find("day_of_week").get("data") for elt in forecast]

    def forecast_condition(self,forecast):
        return [elt.find("condition").get("data") for elt in forecast]

    def get_f_now(self,weather):
        return weather.find("temp_f").get("data")

    def get_c_now(self,weather):
        return weather.find("temp_c").get("data")
    

cherrypy.quickstart(Index())
