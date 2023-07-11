# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from .features import productionTable,regionalTable,querySearcher,question_formatter,location_coder,extraction_info,openFunction
from .features import normpeopleTable,ansShows,columnTable,castTable,authorTable,Bot
            


            
        
class contextAction(Action):

    def name(self) -> Text:
        return "action_context_set"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            print("$$$$$$$$$$$$$$$$$$$$$$","action_context_set")

            full_message = tracker.latest_message['text']
            both_info = extraction_info(full_message)
            broadway_show = both_info[0]
            pre_broadway_show = tracker.get_slot("broadway_name")
            preCity = tracker.get_slot("place")
            preCityCode = tracker.get_slot("cityCode")
            city = both_info[1]
            cityCode = location_coder(city)

            if broadway_show==None and city==None:
                print("###############  first condition worked")
                if pre_broadway_show==None and preCity==None:
                    reply = openFunction(f"you are an exception handler of a chatbot function that tells about broadway shows timing,vanues and other details so if users question doesn't have location or broadway then ask for it and if these are not required like user is asking for suggetions or something then answer the question, now user's question is: {full_message}")
                    dispatcher.utter_message(text=reply)
                elif pre_broadway_show!=None and preCity==None:
                    #example : show runtime
                    try:
                        reply = regionalTable(full_message,pre_broadway_show,preCity)
                        if len(reply)>1:
                            dispatcher.utter_message(text=reply)
                        else:
                            dispatcher.utter_message(text="for which city")
                    except:
                        try:
                            reply = productionTable(full_message,pre_broadway_show,preCityCode,preCity)
                            if len(reply)>1:
                                dispatcher.utter_message(text=reply)
                            else:
                                dispatcher.utter_message(text="for which city")
                        except:
                            dispatcher.utter_message(text="for which city")
                elif pre_broadway_show==None and preCity!=None:
                    if preCityCode == "('LN','WE')" or preCityCode =="('NY','OF','FF','BR')" or preCityCode in ["('LN')", "('WE')", "('BR')", "('NY')", "('OF')", "('FF')", "('LA')"]:
                       reply = productionTable(full_message,pre_broadway_show,preCityCode,preCity)
                       if len(reply)>1:
                        dispatcher.utter_message(text=reply)
                        
                       else:
                        try:
                            new_reply = regionalTable(full_message,pre_broadway_show,preCity)
                            dispatcher.utter_message(text=new_reply)
                            
                        except:
                            dispatcher.utter_message(text="sorry I don't have any data about this")
                    else:
                        reply = regionalTable(full_message,broadway_show,preCity)
                        if len(reply)>1:
                            dispatcher.utter_message(text=reply)
                        else:
                            try:
                                new_reply = productionTable(full_message,broadway_show,preCityCode,preCity)
                                dispatcher.utter_message(text=new_reply)
            
                            except:
                                dispatcher.utter_message(text="sorry I don't have any data about this")
            
                else:
                    # when both are predefined
                    
                    if preCityCode == "('LN','WE')" or preCityCode =="('NY','OF','FF','BR')" or preCityCode in ["('LN')", "('WE')", "('BR')", "('NY')", "('OF')", "('FF')", "('LA')"]:
                       reply = productionTable(full_message,pre_broadway_show,preCityCode,preCity)
                       if len(reply)>1:
                        dispatcher.utter_message(text=reply)
                        
                       else:
                        try:
                            new_reply = regionalTable(full_message,pre_broadway_show,preCity)
                            dispatcher.utter_message(text=new_reply)
                            
                        except:
                            dispatcher.utter_message(text="sorry I don't have any data about this")
                    else:
                        reply = regionalTable(full_message,pre_broadway_show,preCity)
                        if len(reply)>1:
                            dispatcher.utter_message(text=reply)
                            
                        else:
                            try:
                                new_reply = productionTable(full_message,pre_broadway_show,preCityCode,preCity)
                                dispatcher.utter_message(text=new_reply)
            
                            except:
                                dispatcher.utter_message(text="sorry I don't have any data about this")
                if Bot.broadway != None:
                    return[SlotSet("broadway_name",Bot.broadway)]
                elif Bot.city !=None:
                    return[SlotSet("place",Bot.city)]
                else:
                    return []
                       
            elif broadway_show!=None and city==None:
                print("############################  second condition worked")
                if preCity==None:
                    try:
                        reply = regionalTable(full_message,broadway_show,preCity)
                        dispatcher.utter_message(text=reply)
                    except:
                        try:
                            reply = productionTable(full_message,broadway_show,preCityCode,city)
                            dispatcher.utter_message(text=reply)
                        except:
                            dispatcher.utter_message(text="for which city")
                else:
                    if preCityCode == "('LN','WE')" or preCityCode =="('NY','OF','FF','BR')" or preCityCode in ["('LN')", "('WE')", "('BR')", "('NY')", "('OF')", "('FF')", "('LA')"]:
                       reply = productionTable(full_message,broadway_show,preCityCode,preCity)
                       if len(reply)>1:
                        dispatcher.utter_message(text=reply)
                        
                       else:
                        try:
                            new_reply = regionalTable(full_message,broadway_show,preCity)
                            dispatcher.utter_message(text=new_reply)
                            
                        except:
                            dispatcher.utter_message(text="sorry I don't have any data about this")
                    else:
                        reply = regionalTable(full_message,broadway_show,preCity)
                        if len(reply)>1:
                            dispatcher.utter_message(text=reply)
                            
                        else:
                            try:
                                new_reply = productionTable(full_message,broadway_show,preCityCode,preCity)
                                dispatcher.utter_message(text=new_reply)
            
                            except:
                                dispatcher.utter_message(text="sorry I don't have any data about this")
                if Bot.city !=None:
                    return[SlotSet("broadway_name", broadway_show),SlotSet("place", Bot.city),SlotSet("cityCode", Bot.code)]
                return [SlotSet("broadway_name", broadway_show)]

            elif broadway_show==None and city!=None:
                print("######################## third condition worked")
                if pre_broadway_show==None:
                    if cityCode == "('LN','WE')" or cityCode =="('NY','OF','FF','BR')" or cityCode in ["('LN')", "('WE')", "('BR')", "('NY')", "('OF')", "('FF')", "('LA')"]:
                        reply = productionTable(full_message,broadway_show,cityCode,city)
                        if len(reply)>1:
                            dispatcher.utter_message(text=reply)
                            
                        else:
                            try:
                                new_reply = regionalTable(full_message,broadway_show,city)
                                dispatcher.utter_message(text=new_reply)
                                
                            except:
                                dispatcher.utter_message(text="for which show")
                                
                    else:
                        reply = regionalTable(full_message,broadway_show,city)
                        print(reply)
                        if len(reply)>1:
                            dispatcher.utter_message(text=reply)
                            
                        else:
                            print("conditon")
                            try:
                                new_reply = productionTable(full_message,broadway_show,cityCode,city)
                                dispatcher.utter_message(text=new_reply)
            
                            except:
                                dispatcher.utter_message(text="for which show")
                else:
                    if cityCode == "('LN','WE')" or cityCode =="('NY','OF','FF','BR')" or cityCode in ["('LN')", "('WE')", "('BR')", "('NY')", "('OF')", "('FF')", "('LA')"]:
                        reply = productionTable(full_message,pre_broadway_show,cityCode,city)
                        if len(reply)>1:
                            dispatcher.utter_message(text=reply)
                            
                        else:
                            try:
                                new_reply = regionalTable(full_message,pre_broadway_show,city)
                                dispatcher.utter_message(text=new_reply)
                                
                            except:
                                dispatcher.utter_message(text="for which show")
                                
                    else:
                        reply = regionalTable(full_message,pre_broadway_show,city)
                        if len(reply)>1:
                            dispatcher.utter_message(text=reply)
                            
                        else:
                            try:
                                new_reply = productionTable(full_message,pre_broadway_show,cityCode,city)
                                dispatcher.utter_message(text=new_reply)
            
                            except:
                                dispatcher.utter_message(text="for which show")
                
                if Bot.broadway != None:
                    return [SlotSet("place", city),SlotSet("cityCode", cityCode),SlotSet("broadway_name",Bot.broadway)]
                return [SlotSet("place", city),SlotSet("cityCode", cityCode)]
                
            else:
                print("last condition worked")
                if cityCode == "('LN','WE')" or cityCode =="('NY','OF','FF','BR')" or cityCode in ["('LN')", "('WE')", "('BR')", "('NY')", "('OF')", "('FF')", "('LA')"]:
                    reply = productionTable(full_message,broadway_show,cityCode,city)
                    if len(reply)>1:
                        dispatcher.utter_message(text=reply)
                        
                    else:
                        try:
                            new_reply = regionalTable(full_message,broadway_show,city)
                            dispatcher.utter_message(text=new_reply)
                            
                        except:
                            dispatcher.utter_message(text="sorry I don't have any data about this")
                            
                else:
                    reply = regionalTable(full_message,broadway_show,city)
                    if len(reply)>1:
                        dispatcher.utter_message(text=reply)
                        
                    else:
                        try:
                            new_reply = productionTable(full_message,broadway_show,cityCode,city)
                            dispatcher.utter_message(text=new_reply)
        
                        except:
                            dispatcher.utter_message(text="sorry I don't have any data about this")
                return [SlotSet("broadway_name", broadway_show),SlotSet("place", city),SlotSet("cityCode", cityCode)]



        
        
class actionFacts(Action):
    def name(self) -> Text:
        return "action_about_facts"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("$$$$$$$$$$$$$$$$$$$$$$","action_about_facts")
        try:
            full_message = tracker.latest_message['text']
            last_people = tracker.get_slot("people")
            formated = question_formatter(full_message)
            print(formated)

            query = f'''SELECT answer FROM faq WHERE question = "{formated.strip()}";'''
            data = querySearcher(query)
            print(data)

            if len(data) == 0:
                try:
                    query_people = normpeopleTable(full_message,last_people)
                    query = query_people['ans']
                    print(query)
                    people = query_people['new_people']
                    data = querySearcher(query)
                    final_que = full_message + f",{data}"
                    response = ansShows(final_que,"broadway show","city")
                    print(response)

                except:
                    response = "Sorry I don't have data about it"
            else:
                # Format show timings as a string
                response = ", ".join(str(result[0]) for result in data)
            
            dispatcher.utter_message(text=response)
            
            return []

        except:
            prompt = f"you are an exception handler of chatbot of https://www.broadwayworld.com/, chatbot got an error while answering {full_message}\nNow handle it with grace like a gentle man and say sorry for not having it's answer"
            reply = openFunction(prompt)
            dispatcher.utter_message(text=reply)
            
            return []
        

class actionNorm(Action):
    def name(self) -> Text:
        return "action_about_normpeople"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("$$$$$$$$$$$$$$$$$$$$$$","action_about_normpeople")
        try:
            full_message = tracker.latest_message['text']
            print(full_message)
            last_people = tracker.get_slot("people")

            query_people = normpeopleTable(full_message,last_people)
            query = query_people['ans']
            print(query)
            people = query_people['new_people']
            data = querySearcher(query)
            final_que = full_message + f",{data}"
            response = ansShows(final_que,"broadway show","city")
            print(response)

                
            dispatcher.utter_message(text=response)
            
            return [SlotSet("people",people)]

        except:
            prompt = f"you are an exception handler of chatbot of https://www.broadwayworld.com/, chatbot got an error while answering {full_message}\nNow handle it with grace like a gentle man and say sorry for not having it's answer"
            reply = openFunction(prompt)
            dispatcher.utter_message(text=reply)
            
            return []



class ActionSetCityName(Action):
    def name(self) -> Text:
        return "action_city"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Dict[Text, Any]]:
        print("$$$$$$$$$$$$$$$$$$$$$$","action_city")
        full_message = tracker.latest_message['text']
        broadway_show = tracker.get_slot("broadway_name")
        city = extraction_info(full_message)[1]
        print(city)
        cityCode = location_coder(city)
        if city == None:
            dispatcher.utter_message(text="sorry I didn't got city can you ask again with show name and city name")
            return []
        elif cityCode == "('LN','WE')" or cityCode =="('NY','OF','FF','BR')" or cityCode in ["('LN')", "('WE')", "('BR')", "('NY')", "('OF')", "('FF')", "('LA')"]:
            reply = productionTable(full_message,broadway_show,cityCode,city)
            dispatcher.utter_message(text=reply)
            return [SlotSet("place", city),SlotSet("cityCode", cityCode)]
        else:
            reply = regionalTable(full_message,broadway_show,city)
            dispatcher.utter_message(text=reply)
            return [SlotSet("place", city),SlotSet("cityCode", cityCode)]
        

    
class ActionSetName(Action):
    def name(self) -> Text:
        return "action_my_name"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Dict[Text, Any]]:
        print("$$$$$$$$$$$$$$$$$$$$$$","action_my_name")
        full_message = tracker.latest_message['text']
        prompt = f"just return person's name from text\ntext: {full_message}"
        name = openFunction(prompt)
        
        dispatcher.utter_message(text=f"Hello {name}")

        return [SlotSet("username", name)]
    
class ActionColumn(Action):
    def name(self) -> Text:
        return "action_columntable"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Dict[Text, Any]]:
        print("$$$$$$$$$$$$$$$$$$$$$$","action_columntable")
        try:
            context = tracker.get_slot("context")
            print(context)
            full_message = tracker.latest_message['text']
            # try:
            query_New_context = columnTable(full_message,context)
            query = query_New_context['ans']
            print(query)
            new_context = query_New_context['new_context']
            print(query)
            data = querySearcher(query)
            formated = full_message + f",{data}"
            answer = ansShows(formated)
            print(answer)

            dispatcher.utter_message(text=answer)

            return [SlotSet("context", new_context)]
        except:
            prompt = f"you are an exception handler of chatbot of https://www.broadwayworld.com/, chatbot got an error while answering {full_message}\nNow handle it with grace like a gentle man and say sorry for not having it's answer"
            reply = openFunction(prompt)
            dispatcher.utter_message(text=reply)
            
            return []
    
class ActionAuthors(Action):
    def name(self) -> Text:
        return "action_authors"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Dict[Text, Any]]:
        print("$$$$$$$$$$$$$$$$$$$$$$","action_authors")
        # try:
        broadway = tracker.get_slot("broadway_name")
        # print(context)
        full_message = tracker.latest_message['text']
        try:
            query_New_context = authorTable(full_message,broadway)
            query = query_New_context['ans']
            print(query)
            new_broadway = query_New_context['broadway']
            data = querySearcher(query)
            print(data)
            formated = full_message + f",{data}"
            answer = ansShows(formated,broadway_show=broadway)
            print(answer)

            dispatcher.utter_message(text=answer)

            return [SlotSet("broadway_name",new_broadway)]
        except:
            prompt = f"you are an exception handler of chatbot of https://www.broadwayworld.com/, chatbot got an error while answering {full_message}\nNow handle it with grace like a gentle man and say sorry for not having it's answer"
            reply = openFunction(prompt)
            dispatcher.utter_message(text=reply)
            
            return []

class ActionCast(Action):
    def name(self) -> Text:
        return "action_cast"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Dict[Text, Any]]:
        print("$$$$$$$$$$$$$$$$$$$$$$","action_cast")
        try:
            full_message = tracker.latest_message['text']
            broadway = tracker.get_slot("broadway_name")
            query_broadway = castTable(full_message,broadway)
            print(query_broadway)
            query = query_broadway['ans']
            new_broadway = query_broadway['broadway']
            # production_id = querySearcher(f"SELECT id FROM productions WHERE prodtitle LIKE '%{broadway}%' AND market_type_code = 'BR' LIMIT 1;")
            data = querySearcher(query)
            print(data)
            final_que = full_message + f",{data}"
            format_reply = ansShows(final_que,broadway,"city")

            dispatcher.utter_message(text=format_reply)

            return [SlotSet("broadway_name", new_broadway)]
    
        except:
            prompt = f"you are an exception handler of chatbot of https://www.broadwayworld.com/, chatbot got an error while answering {full_message}\nNow handle it with grace like a gentle man and say sorry for not having it's answer"
            reply = openFunction(prompt)
            dispatcher.utter_message(text=reply)
            
            return []

class ActionFallback(Action):
    def name(self) -> Text:
        return "action_fallback"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Dict[Text, Any]]:
        print("$$$$$$$$$$$$$$$$$$$$$$","action_fallback")

        # pre_broadway_show = tracker.get_slot("broadway_name")
        # preCity = tracker.get_slot("place")
        full_message = tracker.latest_message['text']
        print("exception worked")
        prompt = f"you are fallback handler of chatbot of https://www.broadwayworld.com/ , you are responsible to answer questions which are not related to database or any specific data, do not give any specific information, answer like a professional person,now answer this: {full_message}"
        answer = openFunction(prompt)
        
        dispatcher.utter_message(text=answer)

        return []






