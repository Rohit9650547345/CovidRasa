# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, AllSlotsReset
import requests
import pandas as pd
import datetime
# pd.options.display.float_format = '{:.2f}'.format

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_covid_tracker_district"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        state = tracker.get_slot('state')
        district = tracker.get_slot('district')
        date_object = tracker.get_slot("date")
        try:
            dt_obj = datetime.datetime.strptime(date_object,'%d-%m-%Y')
        except ValueError:
            dt_obj = datetime.datetime.strptime(date_object,'%d/%m/%Y')
        except TypeError:
            date_object = None

        if district is not None:
            data = pd.read_csv('https://data.covid19india.org/csv/latest/districts.csv')

            if date_object is not None:
                date = datetime.datetime.strftime(dt_obj, "%Y-%m-%d")
            else:
                date = data['Date'].unique()[-1]

            print(district, state, date)

            state_data = data[(data['State'] == state.title()) & (data['Date'] == date)]
            district_data = state_data[state_data['District'] == district.title()]

            if district_data.empty:
                if not state_data[state_data['District']=='Unknown'].empty:
                    district_data = state_data[state_data['District']=='Unknown']
                elif not state_data[state_data['District']=='Other State'].empty:
                    district_data = state_data[state_data['District']=='Other State']
            
            try:
                detail = district_data.iloc[0, 3:].to_string()
            except:
                detail = "Confirmed\t0\nRecovered\t0\nDeceased\t0\nOther\t0\nTested\t0"
        else:
            data = pd.read_csv('https://data.covid19india.org/csv/latest/states.csv')

            if date_object is not None:
                date = datetime.datetime.strftime(dt_obj, "%Y-%m-%d")
            else:
                date = data['Date'].unique()[-1]

            print(state, date)

            cases = data[(data['State'] == state.title()) & (data['Date'] == date)]

            try:
                detail = cases.iloc[0, 2:].to_string()
            except:
                detail = "Confirmed\t0\nRecovered\t0\nDeceased\t0\nOther\t0\nTested\t0"

        print(detail)
        dispatcher.utter_message(text=detail)

        return [SlotSet('date'), None]

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_reset"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [AllSlotsReset()]