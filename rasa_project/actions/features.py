
import re
import mysql.connector
import openai
from .gpt import GPT,Example

class bot_memory:
    broadway = None
    city = None
    code = None

    def slotsetter(self,query,data):
        try:
            if ("SELECT showname" in query or "SELECT prodtitle" in query) and len(data)==1 and data[0][0] != '':            
                Bot.broadway = data[0][0]
                Bot.city = None
                Bot.code = None
            elif "SELECT city" in query and len(data)==1 and data[0][0] != '':           
                Bot.city = data[0][0]
                Bot.code = location_coder(Bot.city)
                Bot.broadway = None
            elif "SELECT market_type_code" in query and len(data)==1 and data[0][0] != '':
                Bot.city = querySearcher(f'''SELECT meaning FROM Code WHERE type = 'MarketType' and code = '{data[0][0]}';''')[0][0]
                Bot.code = data[0]
                Bot.broadway = None
            else:
                Bot.broadway = None
                Bot.broadway = None
                Bot.code = None
        except:
            Bot.broadway = None
            Bot.broadway = None
            Bot.code = None

Bot = bot_memory()

# database connection
dydb = mysql.connector.connect(
            user = "root",
            password = "shashikant420",
            database="chatbot1",
            host = "chatbot1.cyxgntsmiing.eu-north-1.rds.amazonaws.com",
            port = 3306
        )
cursor = dydb.cursor()

# function to use openai search
def openFunction(crust):

    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=crust,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return completions["choices"][0]["text"]


# function to run query, fetch data and return formatted reply for production show table 
def productionTable(full_message,broadway_show,cityCode,city): 
    query = productionShows(full_message,broadway_show,cityCode)
    try:
        data = querySearcher(query)
        if len(data)==0 and broadway_show==None:
            return "For which show"
        elif len(data)==0 and city==None:
            return "For which City"
        else:
            final_que = full_message + f",{data}"
            format_reply = ansShows(final_que,broadway_show,city)
            Bot.slotsetter(query,data)
            return format_reply
    except:
        prompt = f"you are an exception handler of chatbot of https://www.broadwayworld.com/, chatbot got an error while answering '{full_message}', conversation was going on {broadway_show} in {city}\nif current question is not from previous context then handle it with grace\n Now answer users question"
        ans = openFunction(prompt)
        return ans

# function to run query, fetch data and return formatted reply for regional show table
def regionalTable(full_message,broadway_show,city): 
    query = regionalShows(full_message,broadway_show,city)
    try:
        data = querySearcher(query)
        if len(data)==0:
            query = productionShows(full_message,broadway_show,city)
            data = querySearcher(query)
    except:
        prompt = f"you are an exception handler of chatbot of https://www.broadwayworld.com/, chatbot got an error while answering '{full_message}', conversation was going on {broadway_show} in {city}\nif current question is not from previous context then handle it with grace\n Now answer users question"
        ans = openFunction(prompt)
        return ans
    # else:
    final_que = full_message + f",{data}"
    format_reply = ansShows(final_que,broadway_show,city)
    Bot.slotsetter(query,data)
    return format_reply
    
###########openai function###########
# openai.api_key = ""






# function to find code of city from code table
def location_coder(city):
    if city ==None:
        return None
    elif city.lower() == "london":
        data = ["('LN','WE')"]

        return data[0]
    elif city.lower() == "new york":
        data = ["('NY','OF','FF','BR')"]

        return data[0]
    else:
        query = f'''SELECT code FROM Code WHERE meaning = "{city}" AND type = 'MarketType';'''
        data = querySearcher(query)
        if len(data)==0:
    
            return f"('US')"

        return f"('{data[0][0]}')"

# connects database and run the query to fetch data
def querySearcher(query):
    cursor.execute(query)
    data = cursor.fetchall()
    return data


    


# function to format users questions to be matched with faq table
def question_formatter(prompt,people):

    # model to generate the answer
    gpt = GPT(engine="text-davinci-003",
            temperature=0.2,
            max_tokens=100)


    gpt.add_example(Example("does the book of mormon won any of tony awards","What Tony Awards has The Book of Mormon won?"))
    gpt.add_example(Example("what awards does the book of mormon nominated for",'What other awards has The Book of Mormon been nominated for?'))
    gpt.add_example(Example('is there any theatre playing the book of mormon on broadway','What theatre is The Book of Mormon playing on Broadway?'))
    gpt.add_example(Example("in how many broadway shows rosie O'donnell been","How many Broadway shows has Rosie O'Donnell been in?"))
    gpt.add_example(Example("did rosie O'donnell won any awards","What awards has Rosie O'Donnell won?"))
    gpt.add_example(Example("awards that rosid o'donnell won","What awards has Rosie O'Donnell won?"))
    gpt.add_example(Example('list the awards that mandy gozalez nominated for','What awards has Mandy Gonzalez been nominated for?'))
    gpt.add_example(Example('how many west end show kirsten aimee did','How many West End shows has Kirsten Aimee been in'))
    gpt.add_example(Example("broadway shows of jean anderson","How many Broadway shows has Jean Anderson been in?"))
    gpt.add_example(Example("marie andrews west end shows","How many West End shows has Marie Andrews been in?"))
    gpt.add_example(Example("How many shows has Andrew Rannells been in on Broadway?","How many Broadway shows has Andrew Rannells been in?"))
    gpt.add_example(Example("In how many West End productions has Andrew Rannells appeared?" or "Can you tell me the number of West End shows that Andrew Rannells has been a part of?" or "How many times has Andrew Rannells been cast in West End shows?" or "What is the total number of West End productions that Andrew Rannells has been involved in?" or "Has Andrew Rannells been in many West End shows, and if so, how many?", "How many West End shows has Andrew Rannells been in?"))
    gpt.add_example(Example("What accolades has Andrew Rannells been recognized for?" or "Which awards has Andrew Rannells been nominated for?" or "Which specific honors and prizes has Andrew Rannells been up for?" or "How many award nominations has Andrew Rannells received during his career?" or "Has Andrew Rannells been nominated for any awards in his career", "What awards has Andrew Rannells been nominated for?"))
    gpt.add_example(Example("Besides the Tony Awards, what other awards has The Book of Mormon won?","What other awards has The Book of Mormon won?"))
    gpt.add_example(Example("Which of the Broadway shows has Rosie O'Donnell been in?","What Broadway shows has Rosie O'Donnell been in?"))
    gpt.add_example(Example("in which broadway shows has Laura Benanti been","What Broadway shows has Rosie O'Donnell been in?"))
    gpt.add_example(Example("what award has she won",f"What awards has {people} Won"))
    gpt.add_example(Example("In how many West End productions has he appeared?",f"How many West End shows has {people} been in?"))
    gpt.add_example(Example("did he won any awards",f"What awards has {people} won?"))
    p = gpt.submit_request(prompt)

    return p['choices'][0]['text'][8:]

# function to generate sql queries for production show table
def productionShows(prompt,broadway_show,cityCode):

    # model to generate the answer
    prod = GPT(engine="text-davinci-003",
            temperature=0.2,
            max_tokens=250)


    prod.add_example(Example("What time is the show Kimberly Akimbo tonight?" or "What time is Kimberly Akimbo showing this evening?" or "What are the show timings for Kimberly akimbo this weekend?" or "Is there a kimberly akimbo show tonight" or "is there any shows of kimberly akimbo on sunday",f'''SELECT schedule_text FROM productions WHERE prodtitle LIKE "%Kimberly Akimbo%" AND market_type_code IN {cityCode} AND production_status_code NOT IN ('CA', 'CL') AND schedule_text is not NULL AND schedule_text <> '' LIMIT 1;'''))
    prod.add_example(Example("What time is The Lion King showing tonight in West End?" or "What are the show timings for The Lion King in West End?" or "What time is The Lion King showing this evening in West End?" or "Is there a The Lion King show tonight in West End?",f'''SELECT schedule_text FROM productions WHERE prodtitle LIKE "%Lion King%" AND market_type_code IN ('LN','WE') AND production_status_code NOT IN ('CA', 'CL') AND schedule_text is not NULL AND schedule_text <> '' LIMIT 1;'''))
    prod.add_example(Example("What are the show timings for The Belles of the Kitchen in New York?" or "What are the show timings for The Belles of the Kitchen this weekend in New york?" or "When can I catch a performance of The Belles of the Kitchen this week in new york?" or "What time does The Belles of the Kitchen start on Friday evening in new york?",f'''SELECT schedule_text FROM productions WHERE prodtitle LIKE "%Belles of the Kitchen%" AND market_type_code IN ('NY','OF','FF','BR') AND production_status_code NOT IN ('CA', 'CL') AND schedule_text is not NULL AND schedule_text <> '' LIMIT 1;'''))
    prod.add_example(Example("What are the show timings for The Belles of the Kitchen in off-broadway?" or "What are the show timings for The Belles of the Kitchen this weekend in off-broadway?" or "When can I catch a performance of The Belles of the Kitchen this week in off-broadway?" or "What time does The Belles of the Kitchen start on Friday evening in off-broadway?",f'''SELECT schedule_text FROM productions WHERE prodtitle LIKE "%Belles of the Kitchen%" AND market_type_code IN ('NY','OF','FF','BR') AND production_status_code NOT IN ('CA', 'CL') AND schedule_text is not NULL AND schedule_text <> '' LIMIT 1;'''))
    prod.add_example(Example("What are the show timings for The Belles of the Kitchen in London?" or "What are the show timings for The Belles of the Kitchen this weekend in London?" or "When can I catch a performance of The Belles of the Kitchen this week in London?" or "What time does The Belles of the Kitchen start on Friday evening in London?",f'''SELECT schedule_text FROM productions WHERE prodtitle LIKE "%Belles of the Kitchen%" AND market_type_code IN ('LN','WE') AND production_status_code NOT IN ('CA', 'CL') AND schedule_text is not NULL AND schedule_text <> '' LIMIT 1;'''))
    prod.add_example(Example("Can you give me an overview of the plot for this show?" or "can you tell me more about the show" or "What is the theme of the production" or "What is the central message or lesson of the show?",f'''SELECT tagline,meta_desc FROM productions WHERE prodtitle LIKE "%{broadway_show}%" AND production_status_code NOT IN ('CA', 'CL') AND tagline is not NULL AND tagline <> '' LIMIT 1;'''))
    prod.add_example(Example("How long does the performance last, roughly?" or "Can you give me an estimate of the show's running time?" or "What is the average duration of the performance?" or "Do you know the approximate length of the show?",f'''SELECT running_time FROM productions WHERE prodtitle LIKE "%{broadway_show}%" AND production_status_code NOT IN ('CA', 'CL') AND schedule_text is not NULL AND schedule_text <> '' LIMIT 1;'''))
    prod.add_example(Example("How long is the runtime of 'Harry Potter and the Cursed Child'?" or "Can you tell me how many hours I should expect to be in the theater for Harry Potter and the Cursed Child?" or "Can you give me an estimate of the total run time, including any intermissions, for Harry Potter and the Cursed Child?",f'''SELECT running_time FROM productions WHERE prodtitle LIKE "%Harry Potter and the Cursed Child%" AND production_status_code NOT IN ('CA', 'CL') AND running_time is not NULL AND running_time <> '' LIMIT 1;'''))
    prod.add_example(Example("Can you provide me with a link to book tickets for the show" or "Can you give me a link to the box office or ticket sales page for the performance" or "Where can I find more information on booking tickets for the show you just talked about?" or "Can you send me a link to the online ticket sales page for the play/musical",f'''SELECT tickets FROM productions WHERE prodtitle LIKE "%{broadway_show}%" AND market_type_code IN {cityCode} AND production_status_code NOT IN ('CA', 'CL') AND schedule_text is not NULL AND schedule_text <> '' LIMIT 1;'''))
    prod.add_example(Example("What is the price range for tickets to the show" or "Can you provide me with information on ticket prices for the show?" or "Do you have any insights on the cost of tickets for the show in the West End?" or "What is the typical price range for tickets to see the show",f'''SELECT ticket_price FROM productions WHERE prodtitle LIKE "%{broadway_show}%" AND market_type_code IN {cityCode} AND production_status_code NOT IN ('CA', 'CL') AND schedule_text is not NULL AND schedule_text <> '' LIMIT 1;'''))
    prod.add_example(Example("Can you provide me with more details about the show and where I can learn more?" or "Where can I find more information on the plot of the show?" or "Can you recommend any resources to learn more about the show, such as articles or interviews?",f'''SELECT URL FROM productions WHERE prodtitle LIKE "%{broadway_show}%" AND market_type_code IN {cityCode} AND production_status_code NOT IN ('CA', 'CL') AND schedule_text is not NULL AND schedule_text <> '' LIMIT 1;'''))
    prod.add_example(Example("can you tell me some description about the show" or "what is show about",f'''SELECT tagline FROM productions WHERE prodtitle LIKE "%{broadway_show}%" AND production_status_code NOT IN ('CA', 'CL') AND tagline is not NULL AND tagline <> '' LIMIT 1;'''))
    prod.add_example(Example("can you tell me about Jersey Boys" or "can you tell me more about Jersey Boys show", f'''SELECT tagline FROM productions WHERE prodtitle LIKE "%{broadway_show}%" AND production_status_code NOT IN ('CA', 'CL') AND tagline is not NULL AND tagline <> '' LIMIT 1;'''))
    prod.add_example(Example("ok what's the show timing on Sunday" or "what are the show timings on monday" or "show timings of Friday",f'''SELECT schedule_text FROM productions WHERE prodtitle LIKE "%{broadway_show}%" AND market_type_code IN {cityCode} AND production_status_code NOT IN ('CA', 'CL') AND schedule_text is not NULL AND schedule_text <> '' LIMIT 1;'''))
    prod.add_example(Example("What shows are showing in the West End right now?" or "Can you give me a list of West End shows?",f'''SELECT prodtitle FROM productions WHERE market_type_code IN ('WE') AND production_status_code NOT IN ('CA', 'CL') AND schedule_text is not NULL AND schedule_text <> '';'''))
    prod.add_example(Example("Is there any musical going on in Paris",f'''SELECT prodtitle FROM productions WHERE showgenre IN ('MU') AND market_type_code IN ('PA') AND production_status_code NOT IN ('CA', 'CL') AND schedule_text is not NULL AND schedule_text <> '';'''))
    prod.add_example(Example("is there any intermission in the show",f'''SELECT intermission FROM productions WHERE prodtitle LIKE "%{broadway_show}%" AND production_status_code NOT IN ('CA', 'CL') AND intermission is not NULL AND intermission <> '';'''))
    prod.add_example(Example("can you show me any picture of the show" or "do you have any photo or poster of show" or "I want to see the first look of show",f'''SELECT vid_image_medium FROM productions WHERE prodtitle LIKE "%{broadway_show}%" AND production_status_code NOT IN ('CA', 'CL');'''))
    prod.add_example(Example("Can you show me the poster of 'The Lion King' show?" or "I'm interested in seeing the poster for 'The Lion King' show. Can you provide it?",f'''SELECT vid_image_medium FROM productions WHERE prodtitle LIKE "%Lion King%" AND production_status_code NOT IN ('CA', 'CL');'''))
    prod.add_example(Example("where can I watch the show",f'''SELECT market_type_code FROM productions WHERE prodtitle LIKE "%{broadway_show}%" AND production_status_code NOT IN ('CA', 'CL') AND schedule_text is not NULL AND schedule_text <> '';'''))
    prod.add_example(Example("where can I watch the Funny Girl" or "in which city Funny Girl is playing" or "Where is Funny girl going on",f'''SELECT market_type_code FROM productions WHERE prodtitle LIKE "%{broadway_show}%" AND production_status_code NOT IN ('CA', 'CL') AND schedule_text is not NULL AND schedule_text <> '';'''))
    prod.add_example(Example("I'm searching for the timings of Lion King show in London before 05 may",f'''SELECT schedule_text FROM productions WHERE prodtitle LIKE "%Lion King%" AND market_type_code IN ('LN','WE') AND production_status_code NOT IN ('CA', 'CL') AND schedule_text is not NULL AND schedule_text <> '' LIMIT 1;'''))
    prod.add_example(Example("isn't the show playing in London",f'''SELECT market_type_code FROM productions WHERE prodtitle LIKE "%{broadway_show}%" AND production_status_code NOT IN ('CA', 'CL') AND schedule_text is not NULL AND schedule_text <> '' LIMIT 1;'''))
    prod.add_example(Example("Are there any comedy shows in Paris",f'''SELECT prodtitle FROM productions WHERE showgenre IN ('MU','OT','PM','UN') AND market_type_code IN ('PA') AND production_status_code NOT IN ('CA', 'CL') AND schedule_text is not NULL AND schedule_text <> '';'''))
    prod.add_example(Example("What operas are playing in West end?",f'''SELECT prodtitle FROM productions WHERE showgenre IN ('OP') AND market_type_code IN ('PA') AND production_status_code NOT IN ('CA', 'CL') AND schedule_text is not NULL AND schedule_text <> '';'''))
    prod.add_example(Example("Is there any specials in West End" or "What specials are playing in West End",f'''SELECT prodtitle FROM productions WHERE showgenre IN ('SP') AND market_type_code IN ('WE') AND production_status_code NOT IN ('CA', 'CL') AND schedule_text is not NULL AND schedule_text <> '';'''))
    prod.add_example(Example("Are there any ballet shows currently playing on Broadway?",f'''SELECT prodtitle FROM productions WHERE showgenre IN ('BA') AND market_type_code IN ('BR') AND production_status_code NOT IN ('CA', 'CL') AND schedule_text is not NULL AND schedule_text <> '';'''))
    prod.add_example(Example("Are there any shows in the melodrama genre available at the moment in London?",f'''SELECT prodtitle FROM productions WHERE showgenre IN ('ME') AND market_type_code IN ('LN','WE') AND production_status_code NOT IN ('CA', 'CL') AND schedule_text is not NULL AND schedule_text <> '';'''))
    prod.add_example(Example("what are the timings in west end",f'''SELECT schedule_text FROM productions WHERE prodtitle LIKE "%{broadway_show}%" AND market_type_code IN ('WE') AND production_status_code NOT IN ('CA', 'CL') AND schedule_text is not NULL AND schedule_text <> '';'''))
    prod.add_example(Example("what comedy shows are playing in New york",f'''SELECT prodtitle FROM productions WHERE showgenre IN ('MU','OT','PM','UN') AND market_type_code IN ('NY','OF','FF','BR') AND production_status_code NOT IN ('CA', 'CL') AND schedule_text is not NULL AND schedule_text <> '';'''))

    p = prod.submit_request(prompt)

    return p['choices'][0]['text'][8:]

# function to make sql queries for regional shows table
def regionalShows(prompt,broadway_show,city):

    # model to generate the answer
    regional = GPT(engine="text-davinci-003",
            temperature=0.2,
            max_tokens=250)


    regional.add_example(Example("what is the ticket price for Nate the Great show","SELECT ticketprice FROM regionalshows WHERE showname LIKE '%Nate the Great%';"))
    regional.add_example(Example("What's the venue for The Lion King"or"In which theater is The Lion King currently running?"or"What's the name of the theater showing The Lion King?","SELECT theatrename FROM regionalshows WHERE showname LIKE '%Lion King%';"))
    regional.add_example(Example("What's playing at Mountainside Theatre"or"Current shows at Mountainside Theatre"or"Broadway shows at Mountainside Theatre","SELECT showname FROM regionalshows WHERE theatrename LIKE '%Mountainside Theatre%';"))
    regional.add_example(Example("When does Girls in the Boat start" or "When is Girls in the Boat beginning its run" or "When can I see Girls in the Boat?", f"SELECT showstart FROM regionalshows WHERE showname LIKE '%Girls in the Boat%' AND city LIKE '%{city}%';"))
    regional.add_example(Example("What is the end date of Girls in the Boat" or "How long is Girls in the Boat running?" or "When is Girls in the Boat scheduled to end?" or "When is the last performance of Girls in the Boat?","SELECT showend FROM regionalshows WHERE showname LIKE '%Girls in the Boat%';"))
    regional.add_example(Example("What is 'The Masks of Oscar Wilde' about?" or "What's the plot of The Masks of Oscar Wilde?" or "What's the concept of The Masks of Oscar Wilde","SELECT showdesc FROM regionalshows WHERE showname LIKE '%The Masks of Oscar Wilde%';"))
    regional.add_example(Example("What is the phone number for the ticket office?" or "What is the telephone number to purchase tickets?" or "What is the phone number to book tickets?" or "What's the number to call to reserve tickets" or "where can I get tickets for the show",f"SELECT ticketphone FROM regionalshows WHERE showname LIKE '%{broadway_show}%';"))
    regional.add_example(Example("What's the phone number to book tickets for Metropolis" or "Can you give me the number to call for Metropolis tickets" or "Is there a phone number I can call to purchase tickets for Metropolis","SELECT ticketphone FROM regionalshows WHERE showname LIKE '%Metropolis%';"))
    regional.add_example(Example("is there any show in Tokyo" or "What musicals can I see in Tokyo?" or "Can you tell me which shows are currently running in Tokyo?" or "Can you recommend a theater or show to see while in Tokyo?","SELECT showname FROM regionalshows WHERE city LIKE '%Tokyo%';"))
    regional.add_example(Example("Where can I find more details about the show" or "any other links about the show details" or "can I get social media or websibe link of show",f"SELECT website,facebook,twitter,instagram FROM regionalshows WHERE showname LIKE '%{broadway_show}%';"))
    regional.add_example(Example("Where is the venue for the American String Quartet show located?" or "Can you give me the address of the theater where the American String Quartet show is being performed?" or "Are there any nearby landmarks or points of reference that can help me locate the venue for the American String Quartet show?",f"SELECT address,city,Zip FROM regionalshows WHERE showname LIKE '%American String Quartet%' AND city LIKE '{city}';"))
    regional.add_example(Example("where can I get tickets for Girls in the Boat show in Tampa",f"SELECT ticketphone FROM regionalshows WHERE showname LIKE '%Girls in the Boat%' AND city LIKE '%Tampa%';"))
    regional.add_example(Example("where can I get tickets the show" or "can I get contact number to book tickets" or "can I book tickets on phone for the show",f"SELECT ticketphone FROM regionalshows WHERE showname LIKE '%{broadway_show}%' AND city LIKE '%{city}%';"))
    regional.add_example(Example("what is the estimated runtime of Into The Woods show" or "What is the average duration of Into The Woods performance?","SELECT runningttime FROM regionalshows WHERE showname LIKE '%Into the Woods%' LIMIT 1;"))
    regional.add_example(Example("what is the estimated runtime of The show" or "What is the average duration of The performance?",f"SELECT runningttime FROM regionalshows WHERE showname LIKE '%{broadway_show}%' LIMIT 1;"))
    regional.add_example(Example("can you tell me theatre name" or "which theatre" or "can you tell me vanue of the show",f"SELECT theatrename FROM regionalshows WHERE showname LIKE '%{broadway_show}%' AND city LIKE '%{city}%' LIMIT 1;"))
    regional.add_example(Example("Can you show me a poster of the show?" or "Do you have a picture of the poster for the show",f"SELECT logo FROM regionalshows WHERE showname LIKE '%{broadway_show}%' AND city LIKE '%{city}%' LIMIT 1;"))
    regional.add_example(Example("where can I watch American String Quartet show","SELECT address,city,Zip FROM regionalshows WHERE showname LIKE '%American String Quartet%'"))
    regional.add_example(Example("Is there any musical going on in Tokyo" or "Are there any comedy shows in Tokyo","SELECT showname FROM regionalshows WHERE city LIKE '%West End%';"))
    regional.add_example(Example("What shows are going on tonight?" or "is there any show playing tonight",f"SELECT showname FROM regionalshows WHERE city LIKE '%{city}%' AND showstart <= CURDATE() AND showend >= CURDATE();"))
    regional.add_example(Example("where can I watch the show",f"SELECT city FROM regionalshows WHERE showname LIKE '%{broadway_show}%';"))
    regional.add_example(Example("where can I watch the Funny Girl" or "in which city Funny Girl is playing" or "Where is Funny girl going on","SELECT city FROM regionalshows WHERE showname LIKE '%Funny Girl%';"))
    regional.add_example(Example("is there any show of Edges is playing","SELECT city FROM regionalshows WHERE showname LIKE '%Edges%';"))
    regional.add_example(Example("where can I watch it" or "where can I watch the show",f"SELECT city FROM regionalshows WHERE showname LIKE '%{broadway_show}%';"))


    p = regional.submit_request(prompt)

    return p['choices'][0]['text'][8:]


# function to format an answer with data for users question
def ansShows(prompt,broadway_show = '',city= '',people = '',context = ''):

    # model to generate the answer
    ans = GPT(engine="text-davinci-003",
            temperature=0.2,
            max_tokens=500)


    ans.add_example(Example("what are the timings for The Lion King in London,[('Tuesdays: 7:00pm, Wednesdays: 7:00pm, Thursdays: 7:00pm, Fridays: 8:00pm, Saturdays: 2:00pm and 8:00pm, Sundays: 1:00pm and 6:30pm',)]","The timings for The Lion King show in London are as follows: Tuesdays at 7:00pm, Wednesdays at 7:00pm, Thursdays at 7:00pm, Fridays at 8:00pm, Saturdays at 2:00pm and 8:00pm, and Sundays at 1:00pm and 6:30pm. "))
    ans.add_example(Example("what is the timings for The Lion King in London on sunday,[('Tuesdays: 7:00pm, Wednesdays: 7:00pm, Thursdays: 7:00pm, Fridays: 8:00pm, Saturdays: 2:00pm and 8:00pm, Sundays: 1:00pm and 6:30pm',)]","The timing for Sunday show The Lion King in London are 1:00pm and 6:30pm"))
    ans.add_example(Example("what are the show timings on tuesday,[('Mondays: 7:30pm\r\nTuesdays: 7:30pm\r\nWednesdays: 7:30pm\r\nThursdays: 2:30pm and 7:30pm\r\nFridays: 7:30pm\r\nSaturdays: 2:30pm and 7:30pm',)]",f"{broadway_show} is on 7:30pm Tuesday in {city}"))
    ans.add_example(Example("what is ticket price of the show,[('$35',)]",f"The ticket price for the {broadway_show} show is $35 in {city}"))
    ans.add_example(Example("what is estimated runtime of the show,[('2 hours and 30 minutes, with one intermission',)]","The estimated runtime of the show is 2 hours and 30 minutes, with one intermission."))
    ans.add_example(Example('''what shows are currently playing in Portland,[("Where's Bruno?",)]''',"One of the shows currently playing in Portland is 'Where's Bruno?'."))
    ans.add_example(Example("is there any show in Seattle,[('Godspell-2012 Revised Version',), ('Fame',)]","Yes, there are currently two shows playing in Seattle - 'Godspell-2012 Revised Version' and 'Fame'."))
    ans.add_example(Example("can I book tickets on phone,[('408-792-4111',)]",f"Yes you can call on 408-792-4111 to book tickets for {broadway_show}"))
    ans.add_example(Example('''what shows are currently playing in Falls Village,[('94th Season Opening Benefit Concert & Reception',), ('Eleora Piano Quartet',), ('Misha Dichter, Piano & Oskar Espina Ruiz, Clarinet',), ('Horszowski Trio',), ('Arianna String Quartet & Judith Gordon, Piano',), ('Ariel Quartet',), ('PENDERECKI STRING QUARTET & ANYA ALEXEYEV, PIANO',), ('EUCLID QUARTET',), ('American String Quartet',), ('Ulysses Quartet & Oskar Espina Ruiz, Clarinet',), ('Lydian String Quartet & Victoria Schwartzman, Piano',), ('Balourdet Quartet & Simone Dinnerstein, Piano',), ('Parker Quartet & Orion Weiss, Piano',), ('Borromeo String Quartet & Henry Kramer, Piano',), ('Dali Quartet & Vanessa Perez, Piano',), ('Cassatt String Quartet & Ursula Oppens, Piano',), ('PAUL WINTER: JAZZ AT MUSIC MOUNTAIN OPENING CONCERT',), ('NEW BLACK EAGLE JAZZ BAND',), ('WANDA HOUSTON PROJECT',), ('MAUCHA ADNET WITH THE BRAZILIAN TRIO "BOSSA ALWAYS NOVA"',), ('BARBARA FASANO TRIO',), ('SWINGTIME BIG BAND',), ('BILL CHARLAP TRIO',), ('KELLIN HANAS QUINTET',), ('THE CURTIS BROTHERS',), ('NEW YORK GILBERT & SULLIVAN PLAYERS',), ('GALVANIZED JAZZ BAND',)] ''',"There are several shows currently playing in Falls Village. Some of the shows include the 94th Season Opening Benefit Concert & Reception, Eleora Piano Quartet, Horszowski Trio, and the Arianna String Quartet & Judith Gordon, Piano. Other shows include jazz performances by Paul Winter and the New Black Eagle Jazz Band, and performances by the New York Gilbert & Sullivan Players."))
    ans.add_example(Example("what is the ticket price for Jersey Boys in Adrian,[('$22-$44',)]","The ticket prices for Jersey Boys in Adrian range from $22 to $44. Please note that ticket prices may very depending on factors such as seat location and date of performance."))
    ans.add_example(Example("where can I get more information about Jersey Boys,[('https://croswell.org/jerseyboys', 'https://facebook.com/thecroswell', '', 'https://instagram.com/thecroswell')]","You can find more information about Jersey Boys at the Croswell Opera House's website, which is https://croswell.org/jerseyboys. Additionally, you can check out the Croswell Opera House's social media pages on Facebook (https://facebook.com/thecroswell) and Instagram (https://instagram.com/thecroswell) for updates and news about the production."))
    ans.add_example(Example("in which theatre,[('The Orpheum Theatre',)]" or "what is the vanue of the show,[('The Orpheum Theatre',)]",f"{broadway_show} is playing at the Orpheum Theatre"))
    ans.add_example(Example("what is the ticket price of Once On This Island Jr in Racine,[('',)]","sorry but ticket prices are not avaliable yet for Once On This Island Jr show in Racine."))
    ans.add_example(Example("can you tell me address of the vanue,[('1516 Ohio St', 'Racine', '53405')]",f"The address of the venue for {broadway_show} is 1516 Ohio St, Racine, ZIP code- 53405"))
    ans.add_example(Example("what are the timings for fancy nancy the musical,[]",f"Sorry there are no fancy nancy the musical shows in {city}"))
    ans.add_example(Example("what's the vanue of the show,[('Music Mountain',)]" or "vanue name,[('Music Mountain',)]",f"The Vanue for {broadway_show} is Music Mountain"))
    ans.add_example(Example("let's book tickets for the show,[('',)]", f"Sorry ticket details are not avaliable yet for {broadway_show} in {city}"))
    ans.add_example(Example("let's book tickets for the show,[('https://broadwayworld.tixculture.com/london/shows/302',)]",f"sure you can book tickets on <a href='https://broadwayworld.tixculture.com/london/shows/302'>https://broadwayworld.tixculture.com/london/shows/302</a> for {broadway_show} in {city}"))
    ans.add_example(Example("what is the start date of The Addams Family,[('',)]", f"Sorry but no shows are avaliable for {broadway_show} in {city}"))
    ans.add_example(Example('''What Broadway shows has Mandy Gonzalez been in?,[('A Drama Desk and OBIE Award-winning actress. She is best known for her emotional portrayal of Nina Rosario in the original cast of Lin-Manuel Miranda's Tony Award-winning hit musical In the Heights, she also starred as Elphaba in Wicked (Broadway). TV/Film: "Madam Secretary," "Quantico," "Doubt," "The Good Wife," "White Collar," Viral, After, Man on a Ledge, and Across the Universe.  Broadway: AIDA, Lennon, Dance of the Vampires. Mandy has performed with prestigious symphonies across the country and around the world.'),]''','''Mandy Gonzalez has been in the Broadway shows "In the Heights," "Wicked," "AIDA," "Lennon," and "Dance of the Vampires".'''))
    ans.add_example(Example('''What awards has Kristen Hahn has won?,[('Currently a swing in the Broadway production of A Gentleman\'s Guide to Love and Murder. Broadway/Westport Country Playhouse: Rebecca Gibbs in Our Town starring Paul Newman. Film/TV: "Five Flights Up" starring Diane Keaton and Morgan Freeman; "Our Town" (PBS/ Showtime). Repeat soloist with The American Classical Orchestra (NYC). Education: BFA Vocal Performance, Carnegie Mellon University. Thank you to Darko, Binder Casting, and the entire GGLAM team! Love and thanks to my family and teachers!',)]''',"Kristen Hahn has not yet received any awards for her outstanding contributions to Broadway productions."))
    ans.add_example(Example("what shows are currently playing in Apollo theatre,[]","Sorry there are no shows are currently plaing in Apollo theatre"))
    ans.add_example(Example("Can you share any images or pictures showcasing the performances and participants,[('https://cloudimages.broadwayworld.com/columnpiccloud/200200-a57292d1629def3e3f3af11b1b75007a.jpg')]",'''yes I have an image to share with you. Take a look! <img alt="" src="https://cloudimages.broadwayworld.com/columnpiccloud/200200-a57292d1629def3e3f3af11b1b75007a.jpg" style="width:280px"/>'''))
    ans.add_example(Example("Are there any photos available from the Valentina Kozlova International Ballet Competition at The Kaye Playhouse?,[('https://cloudimages.broadwayworld.com/columnpiccloud/200200-a57292d1629def3e3f3af11b1b75007a.jpg')]",'''Yes, we do have photos available from the Valentina Kozlova International Ballet Competition at The Kaye Playhouse. <img alt="" src="https://cloudimages.broadwayworld.com/columnpiccloud/200200-a57292d1629def3e3f3af11b1b75007a.jpg" style="width:280px"/>'''))
    ans.add_example(Example("Where can I watch the show,[('BR',)]",f"You can watch {broadway_show} in Broadway theatre, New York"))
    ans.add_example(Example("In which city Funny Girl is playing,[('LN',)]","Funny Girl is playing in London"))
    ans.add_example(Example("What is the URL of Rosie O'Donnell?,[('http://www.rosie.com/',), ('',)]","The official website for Rosie O'Donnell can be found at <a href='http://www.rosie.com/'>http://www.rosie.com/</a>."))
    ans.add_example(Example("ok I'm searching for the timings of Lion King show in London before 05 may,[]","Sorry there is no shows on exact date you are searching for"))
    ans.add_example(Example("can you tell me more about cast of Tartuffe: Born Again,[('Mariane', 'Jane Krakowski'), ('Tartuffe', 'John Glover'), ('Orgon', 'David Schramm'), ('Dorine', 'Alison Fraser'), ('Mme. Pernelle', 'Patricia Conolly'), ('Ms. De Salle', 'Susie Duff'), ('Damis', 'Kevin Dewey'), ('Elmire', 'Haviland Morris'), ('Damis', 'Peter Rini'), ('Dorine', 'Susie Duff'), ('Elmire', 'Susie Duff'), ('Mariane', 'Jeanne Hime'), ('Mme. Pernelle', 'Angela Pietropinto'), ('Ms. De Salle', 'Angela Pietropinto'), ('Orgon', 'Tom Ligon'), ('Production Assistant', 'Jeanne Hime'), ('Visitor', 'Peter Rini'), ('Visitor', 'Tom Ligon')]","The cast of Tartuffe: Born Again includes Jane Krakowski as Mariane, John Glover as Tartuffe, David Schramm as Orgon, Alison Fraser as Dorine, Patricia Conolly as Mme. Pernelle, Susie Duff as Ms. De Salle, Kevin Dewey as Damis, Haviland Morris as Elmire, Peter Rini as Damis and Visitor, Jeanne Hime as Production Assistant, and Tom Ligon as Orgon and Visitor."))
    ans.add_example(Example("what are the timings of the show in new york,[]",f"Apologies, but currently, there are no {broadway_show} shows taking place in New York."))
    ans.add_example(Example("I would like to book tickets for the show,[('https://secure.georgestreetplayhouse.org/events/awalkonthemoon?startDate=2020-04-01&view=calendar',)]","Sure, you can book tickets for A Walk on the Moon at <a href='https://secure.georgestreetplayhouse.org/events/awalkonthemoon?startDate=2020-04-01&view=calendar'>https://secure.georgestreetplayhouse.org/events/awalkonthemoon?startDate=2020-04-01&view=calendar</a>"))
    ans.add_example(Example("where is the show playing,[]",f"Currently, there are no shows of {broadway_show} playing, Please check back later for updates on upcoming shows."))
    ans.add_example(Example("who was in the cast of Dessa Rose,[]",f"Sorry, I don't have information about the cast members listed for Dessa Rose"))
    ans.add_example(Example("what are the timings in west end,[]",f"Sorry but Currently there are no shows of {broadway_show} in West End"))
    # ans.add_example(Example("",""))
    # ans.add_example(Example("",""))
    p = ans.submit_request(prompt)

    return p['choices'][0]['text'][8:]


# function to extract show name, city name from users message
def extraction_info(prompt):

    # model to generate the answer
    extractor = GPT(engine="text-davinci-003",
            temperature=0.2,
            max_tokens=30)


    extractor.add_example(Example("what are the timings for Hamilton show in New York","Hamilton;New York"))
    extractor.add_example(Example("what shows are currently going on in Falls Village","None;Falls Village"))
    extractor.add_example(Example("where can I watch The Lion King","Lion King;None"))
    extractor.add_example(Example("so how can I book tickets for the show","None;None"))
    extractor.add_example(Example("how can I book tickets for the Chicago in Hamilton city","Chicago;Hamilton"))
    extractor.add_example(Example("ok what's the show timing on sunday","None;None"))
    extractor.add_example(Example("in New York" or "in new york", "None;New York"))
    extractor.add_example(Example("What are the show timings for Bad Cindrella on sunday","Bad Cindrella;None"))
    extractor.add_example(Example("what was the role of Harry Pedersen in The Lady Comes Across","The Lady Comes Across;None"))
    # extractor.add_example(Example("",""))
    # extractor.add_example(Example("",""))
    

    p = extractor.submit_request(prompt)

    both = p['choices'][0]['text'][8:].split(";")

    for i in range(len(both)):
        if both[i] == 'None':
            both[i] = None
    return both

def normpeopleTable(prompt,last_people):

    # model to generate the answer
    norm = GPT(engine="text-davinci-003",
            temperature=0.2,
            max_tokens=250)


    norm.add_example(Example("What Broadway shows has Mandy Gonzalez been in?",'''SELECT bio FROM normpeople WHERE clean_name LIKE "%MandyGonzalez%" AND bio is not NULL AND bio <> '';'''))
    norm.add_example(Example("What Broadway shows has Rosie O'Donnell been in?",'''SELECT bio FROM normpeople WHERE clean_name LIKE "%RosieODonnell%" AND bio is not NULL AND bio <> '';'''))
    norm.add_example(Example("What Broadway shows has Laura Benanti been in?",'''SELECT bio FROM normpeople WHERE clean_name LIKE "%LauraBenanti%" AND bio is not NULL AND bio <> '';'''))
    norm.add_example(Example("What Broadway shows has Tammy Blanchard been in?",'''SELECT bio FROM normpeople WHERE clean_name LIKE "%TammyBlanchard%" AND bio is not NULL AND bio <> '';'''))
    norm.add_example(Example("What is the biography of Mandy Gonzalez?",'''SELECT bio FROM normpeople WHERE clean_name LIKE '%MandyGonzalez%' AND bio IS NOT NULL;'''))
    norm.add_example(Example("What awards has Kristen Hahn won?",'''SELECT bio FROM normpeople WHERE clean_name LIKE '%KristenHahn%' AND bio IS NOT NULL;'''))
    norm.add_example(Example("did Bonita J. Hamilton won any awards",'''SELECT bio FROM normpeople WHERE clean_name LIKE '%BonitaJHamilton%' AND bio IS NOT NULL;'''))
    norm.add_example(Example("What is the death location of Rosie O'Donnell?",'''SELECT death_location FROM normpeople WHERE clean_name LIKE '%RosieODonnell%' AND death_location IS NOT NULL;'''))
    norm.add_example(Example("When was Kirsten Aimee born?",'''SELECT bday FROM normpeople WHERE clean_name LIKE '%KirstenAimee%' AND bday IS NOT NULL;'''))
    norm.add_example(Example("What is the height of Mandy Gonzalez?",'''SELECT height FROM normpeople WHERE clean_name LIKE '%MandyGonzalez%' AND height IS NOT NULL;'''))
    norm.add_example(Example("What is the birthplace of Rosie O'Donnell?",'''SELECT birth_place FROM normpeople WHERE clean_name LIKE '%RosieODonnell%' AND birth_place IS NOT NULL AND birth_place <> '';'''))
    norm.add_example(Example("What is the Twitter username of Mandy Gonzalez?",'''SELECT twitter_name FROM normpeople WHERE clean_name LIKE '%MandyGonzalez%' AND twitter_name IS NOT NULL;'''))
    norm.add_example(Example("What is the URL of Rosie O'Donnell?",'''SELECT url FROM normpeople WHERE clean_name LIKE '%RosieODonnell%' AND url IS NOT NULL;'''))
    norm.add_example(Example("What is the Facebook page of Rosie O'Donnell?",''' SELECT facebook FROM normpeople WHERE clean_name LIKE '%RosieODonnell%' AND facebook IS NOT NULL;'''))
    norm.add_example(Example("What is the birth name of Mandy Gonzalez?",'''SELECT birthname FROM normpeople WHERE clean_name LIKE '%MandyGonzalez%' AND birthname IS NOT NULL;'''))
    norm.add_example(Example("Is Kirsten Aimee's Instagram username available?","SELECT instagram FROM normpeople WHERE clean_name LIKE '%KirstenAimee%' AND instagram IS NOT NULL;"))
    norm.add_example(Example("what awards has Susan Egan won?",'''SELECT bio FROM normpeople WHERE clean_name LIKE "%SusanEgan%" AND bio is not NULL AND bio <> '';'''))
    norm.add_example(Example("awards Melissa Errico won?",'''SELECT bio FROM normpeople WHERE clean_name LIKE "%MelissaErrico%" AND bio is not NULL AND bio <> '';'''))
    norm.add_example(Example("What notable roles has Laura Bell Bundy portrayed in Broadway productions?",'''SELECT bio FROM normpeople WHERE clean_name LIKE "%LauraBellBundy%" AND bio is not NULL AND bio <> '';'''))
    norm.add_example(Example("which actors have won tony award" or "what actors won Tony awards", '''SELECT name FROM normpeople WHERE bio LIKE "%tony award%";'''))
    norm.add_example(Example("What Broadway shows has she been in?",f'''SELECT bio FROM normpeople WHERE clean_name LIKE "{last_people}" AND bio is not NULL AND bio <> '';'''))
    norm.add_example(Example("What Broadway shows has actor been in?",f'''SELECT bio FROM normpeople WHERE clean_name LIKE "{last_people}" AND bio is not NULL AND bio <> '';'''))
    norm.add_example(Example("What Broadway shows has he been in?",f'''SELECT bio FROM normpeople WHERE clean_name LIKE "{last_people}" AND bio is not NULL AND bio <> '';'''))
    norm.add_example(Example("What Broadway shows has he been in?",f'''SELECT bio FROM normpeople WHERE clean_name LIKE "{last_people}" AND bio is not NULL AND bio <> '';'''))
    norm.add_example(Example("what's his Instagram username?",f"SELECT instagram FROM normpeople WHERE clean_name LIKE '{last_people}' AND instagram IS NOT NULL;"))
    
    # norm.add_example(Example("",""))


    p = norm.submit_request(prompt)

    ans = p['choices'][0]['text'][8:]

    pattern = r'WHERE clean_name LIKE "([^"]+)"'
    match = re.search(pattern, ans)
    if match:
        new_people = match.group(1)
    else:
        new_people = None

    return {'ans':ans, 'new_people':new_people}

def columnTable(prompt,context):

    column = GPT(engine="text-davinci-003",
            temperature=0.2,
            max_tokens=250)
    
    column.add_example(Example("What is the theme of Niel Diamond next show","SELECT Title, Blurb FROM columntable WHERE Title LIKE '%NeiL%diamond%';"))
    column.add_example(Example("Who has Green-Wood selected as its third annual artist in residence?" or "What is the profession of the renowned individual chosen by Green-Wood as their artist in residence?" or "What is the significance of selecting Adam Tendler as the artist in residence for Green-Wood's third annual residency?","SELECT Title, Blurb FROM columntable WHERE Title LIKE '%Green%Wood%';"))
    column.add_example(Example("Which renowned ballet competition will be taking place at The Kaye Playhouse this month?" or "Which countries are represented by the 100+ dancers competing in the competition at The Kaye Playhouse this year?","SELECT Title,Blurb FROM columntable WHERE Title LIKE '%kaye%playhouse%';"))
    column.add_example(Example("How has the overall response been to the performance of The Rocky Horror Picture Show at Music Theatre of Connecticut" or "What have been some of the reviews or critical reception for Music Theatre of Connecticut's production of The Rocky Horror Picture Show" or "Can you share some of the feedback or reviews that The Rocky Horror Picture Show at Music Theatre of Connecticut has received from audiences or critics?","SELECT Title,Blurb FROM columntable WHERE Title LIKE '%rocky%horror%picture%';"))
    column.add_example(Example("What is the title of the play that Playhouse on Park will be producing as a world premiere this spring?" or "When will the production of WEBSTER'S BITCH be running at Playhouse on Park?" or "Who will be directing the production of WEBSTER'S BITCH at Playhouse on Park?" or "How does the theme of Perseverance align with the journey of Playhouse on Park during the pandemic?","SELECT Title,Blurb FROM columntable WHERE Title LIKE '%playhouse%on%park%';"))
    column.add_example(Example("Who is the cellist that recently joined Suono Artist Management's roster?" or "Who is the cellist that recently joined Suòno Artist Management's roster?" or "What is the significance of Nicholas Canellakis joining Suòno Artist Management?","SELECT Title,Blurb FROM columntable WHERE Title LIKE '%Suono%Artist%Management%roster%';"))
    column.add_example(Example("What is the name of the play reading series that will be opening at The Vino Theater in September?","SELECT Title,Blurb FROM columntable WHERE Title LIKE '%Vino%Theater%';"))
    column.add_example(Example("What is the main focus or objective of the Neurodivergent New Play Series?" or "Where will the debut of the Neurodivergent New Play Series take place?" or "When can we expect the Neurodivergent New Play Series to start at The Vino Theater?","SELECT Title,Blurb FROM columntable WHERE Title LIKE '%New%Play%Series%';"))
    column.add_example(Example("Who are some of the cast members featured in the video discussing SHUCKED" or "Who are the songwriters and the book writer mentioned in the video?","SELECT Title,Blurb FROM columntable WHERE Title LIKE '%SHUCKED%';"))
    column.add_example(Example("Who will be leading the discussion and what are their roles at Hoff-Barthelson Music School?" or "How does this discussion align with the mission or philosophy of Hoff-Barthelson Music School?","SELECT Title,Blurb FROM columntable WHERE Title LIKE '%Hoff%Barthelson%Music%';"))
    column.add_example(Example("When will the online discussion take place?" or "What platform will be used for the discussion?",f"SELECT Title,Blurb FROM columntable WHERE Title LIKE '{context}';"))
    column.add_example(Example("do you have any date?",f"SELECT Title,Blurb FROM columntable WHERE Title LIKE '{context}';"))
    column.add_example(Example("How does the video contribute to building anticipation or generating excitement for the show?",f"SELECT Title,Blurb FROM columntable WHERE Title LIKE '{context}';"))
    column.add_example(Example("Can you share any photos from the first look of Absurd Person Singular at Stirling Theatre?","SELECT MainSwap FROM columntable WHERE Title LIKE '%Absurd%Person%Singular%';"))
    column.add_example(Example("Can you provide a link or any information on how I can view the first look photos of Absurd Person Singular at Stirling Theatre?" or "Are there any sneak peeks or behind-the-scenes glimpses available for Absurd Person Singular at Stirling Theatre?","SELECT MainSwap FROM columntable WHERE Title LIKE '%Absurd%Person%Singular%';"))
    column.add_example(Example("Are there any photos available from the Valentina Kozlova International Ballet Competition at The Kaye Playhouse?","SELECT MainSwap FROM columntable WHERE Title LIKE '%kaye%playhouse%' AND Title LIKE '%Valentina%Kozlova%';"))
    column.add_example(Example("Can you share any images or pictures showcasing the performances and participants",f"SELECT MainSwap FROM columntable WHERE Title LIKE '{context}';"))
    # column.add_example(Example("",""))

    p = column.submit_request(prompt)

    ans = p['choices'][0]['text'][8:]
    pattern = r"WHERE Title LIKE '([^']+)'"
    match = re.search(pattern, ans)
    if match:
        new_context = match.group(1)
    else:
        new_context = None

    return {'ans':ans, 'new_context':new_context}


def castTable(prompt,broadway_show):

    cast = GPT(engine="text-davinci-003",
            temperature=0.2,
            max_tokens=250)

    cast.add_example(Example("can you tell me about the cast of The Lady Comes Across",f"SELECT role,credited_name FROM cast WHERE productions_id IN (SELECT id FROM productions WHERE prodtitle LIKE '%The Lady Comes Across%') AND role is not NULL AND role <>'' AND credited_name IS NOT NULL AND credited_name <> '' LIMIT 45;"))
    cast.add_example(Example("Who played the role of Jean Valjean in the recent revival of Les Misérables?",f"SELECT role,credited_name FROM cast WHERE productions_id IN (SELECT id FROM productions WHERE prodtitle LIKE '%Les Misérables%') AND role LIKE '%Jean%' AND credited_name IS NOT NULL AND credited_name <> '' LIMIT 45;"))
    cast.add_example(Example("who has done lead role in Hamilton broadway",f"SELECT role,credited_name FROM cast WHERE productions_id IN (SELECT id FROM productions WHERE prodtitle LIKE '%Hamilton%') AND role is not NULL AND role <>'' AND credited_name IS NOT NULL AND credited_name <> '' LIMIT 45;"))
    cast.add_example(Example("what was the role of Harry Pedersen in The Lady Comes Across Broadway production",f"SELECT role,credited_name FROM cast WHERE productions_id IN (SELECT id FROM productions WHERE prodtitle LIKE '%Les Misérables%' AND market_type_code = 'BR') AND credited_name LIKE '%Harry%' AND role is not NULL AND role <>'' LIMIT 45;"))
    cast.add_example(Example("Who played Character Tony",f"SELECT role,credited_name FROM cast WHERE productions_id IN (SELECT id FROM productions WHERE prodtitle LIKE '%{broadway_show}%') AND role LIKE '%Tony%' AND role is not NULL AND role <>'' LIMIT 45;"))
    cast.add_example(Example("who played Betsy Hamilton in the show",f"SELECT role,credited_name FROM cast WHERE productions_id IN (SELECT id FROM productions WHERE prodtitle LIKE '%Hamilton%') AND role LIKE '%Betsy%' AND role is not NULL AND role <>'' LIMIT 45;"))
    cast.add_example(Example("which actor played Usherette in the broadway show",f"SELECT role,credited_name FROM cast WHERE productions_id IN (SELECT id FROM productions WHERE prodtitle LIKE '%{broadway_show}%') AND role LIKE '%Usherette%' AND role is not NULL AND role <>'' LIMIT 45;"))
    cast.add_example(Example("who played the role of Aaron",f"SELECT role,credited_name FROM cast WHERE productions_id IN (SELECT id FROM productions WHERE prodtitle LIKE '%{broadway_show}%') AND role LIKE '%Aaron%' AND role is not NULL AND role <>'' AND credited_name IS NOT NULL AND credited_name <> '' LIMIT 45;"))
    cast.add_example(Example("just name all the crew members not their roles",f"SELECT credited_name FROM cast WHERE productions_id IN (SELECT id FROM productions WHERE prodtitle LIKE '%{broadway_show}%') AND credited_name IS NOT NULL AND credited_name <> '' LIMIT 45;"))
    # cast.add_example(Example("",f""))

    p = cast.submit_request(prompt)
    ans = p['choices'][0]['text'][8:]
    prodtitle = re.search(r"prodtitle LIKE '%(.*?)%'", ans)
    
    if prodtitle:
        prodtitle = prodtitle.group(1)
    return {'ans':ans, 'broadway':prodtitle}


# function to generate sql queries for authors table
def authorTable(prompt,broadway):

    author = GPT(engine="text-davinci-003",
            temperature=0.2,
            max_tokens=250)
    
    author.add_example(Example("Who is the bookwriter of Cindrella","SELECT np.name, a.role FROM normpeople np, authors a WHERE np.normpeopleid = a.names_id AND a.shows_id IN (SELECT p.shows_id FROM productions p WHERE p.prodtitle LIKE 'Cinderella') AND a.role = 'Bookwriter';"))
    author.add_example(Example("Who was the Lyricist of The show Cindrella in West End","SELECT np.name, a.role FROM normpeople np, authors a WHERE np.normpeopleid = a.names_id AND a.shows_id IN (SELECT p.shows_id FROM productions p WHERE p.prodtitle LIKE 'Cinderella' AND p.market_type_code = 'WE') AND a.role = 'Lyricist';"))
    author.add_example(Example("Who is the playwright of The Forty Thieves","SELECT np.name, a.role FROM normpeople np, authors a WHERE np.normpeopleid = a.names_id AND a.shows_id IN (SELECT p.shows_id FROM productions p WHERE p.prodtitle LIKE 'The Forty Thieves') AND role = 'Playright';"))
    author.add_example(Example("name the Librettist of Lischen et Fritzchen show","SELECT np.name, a.role FROM normpeople np, authors a WHERE np.normpeopleid = a.names_id AND a.shows_id IN (SELECT p.shows_id FROM productions p WHERE p.prodtitle LIKE 'Lischen et Fritzchen') AND role = 'Librettist';"))
    author.add_example(Example("do you have information about any authors of Lischen et Fritzchen","SELECT np.name, a.role FROM normpeople np, authors a WHERE np.normpeopleid = a.names_id AND a.shows_id IN (SELECT p.shows_id FROM productions p WHERE p.prodtitle LIKE 'Lischen et Fritzchen');"))
    author.add_example(Example("who was the man as source material for the show",f"SELECT np.name, a.role FROM normpeople np, authors a WHERE np.normpeopleid = a.names_id AND a.shows_id IN (SELECT p.shows_id FROM productions p WHERE p.prodtitle LIKE '{broadway}');"))
    author.add_example(Example("Who is the playwright of The show",f"SELECT np.name, a.role FROM normpeople np, authors a WHERE np.normpeopleid = a.names_id AND a.shows_id IN (SELECT p.shows_id FROM productions p WHERE p.prodtitle LIKE '{broadway}') AND role = 'Playright';"))
    author.add_example(Example("who is the writer of The Play That Goes Wrong","SELECT np.name, a.role FROM normpeople np, authors a WHERE np.normpeopleid = a.names_id AND a.shows_id IN (SELECT p.shows_id FROM productions p WHERE p.prodtitle LIKE 'The Play That Goes Wrong');"))
    author.add_example(Example("What is the source of the show",f"SELECT np.name, a.role FROM normpeople np, authors a WHERE np.normpeopleid = a.names_id AND a.shows_id IN (SELECT p.shows_id FROM productions p WHERE p.prodtitle LIKE '{broadway}');"))
    # author.add_example(Example("",""))
    # author.add_example(Example("",""))
    
    p = author.submit_request(prompt)
    ans = p['choices'][0]['text'][8:]
    prodtitle = re.search(r"prodtitle LIKE '(.*?)'", ans)
    
    if prodtitle:
        prodtitle = prodtitle.group(1)
    else:
        prodtitle = None
    return {'ans':ans, 'broadway':prodtitle}