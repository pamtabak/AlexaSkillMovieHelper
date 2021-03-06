from __future__ import print_function

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

def create_genre_attributes(chosen_genre):
    return {"chosenGenre": chosen_genre}

# --------------- Functions that control the skill's behavior ------------------
def get_welcome_response():
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Alexa Skills Kit sample. " \
                    "Please tell me which kind of movie you want to watch by saying I want to watch a romance"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me which kind of movie you want to watch by saying I want to watch a romance."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))
        
def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skills Kit sample. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def set_genre_in_session(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'Genres' in intent['slots']:
        chosen_genre = intent['slots']['Genres']['value']
        print(chosen_genre)
        session_attributes = create_genre_attributes(chosen_genre)
        speech_output = "I now know you want to watch a " + chosen_genre
        reprompt_text = "I now know you want to watch a " + chosen_genre
        if (chosen_genre == "musical"):
            speech_output += ". I would recommend La La Land and Mamma Mia. Would you like to hear more about them?"
        elif (chosen_genre == "thriller"):
            speech_output += ". I have to admit that I do not link scary movies, so I suggest you choose another genre."
        elif (chosen_genre == "romance"):
            speech_output += ". I would recommend Titanic and The Notebook. Would you like to hear more about them?"
        elif (chosen_genre == "drama"):
            speech_output += ". I would recommend The Godfather and Moonlight. Would you like to hear more about them?"
        elif (chosen_genre == "comedy"):
            speech_output += ". Ha Ha Ha. I would recommend Baywatch and Hangover. Would you like to hear more about them?"
        elif (chosen_genre == "action"):
            speech_output += ". I love superhero movies! So what about Batman or Wonder Woman?"
    else:
        speech_output = "I'm not sure what kind of movie you want to watch. " \
                        "Please try again."
        reprompt_text = "I'm not sure what kind of movie you want to watch." \
                        "You can tell me which kind of movie you want to watch by saying I want to watch a romance."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def set_movie_in_session(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'Movies' in intent['slots']:
        chosen_movie = intent['slots']['Movies']['value'].lower()
        print(chosen_movie)
        speech_output = "I now know you want to hear about " + chosen_movie
        reprompt_text = "I now know you want to hear about " + chosen_movie
        if (chosen_movie == "la la land"):
            speech_output += ". It has Ryan Gosling and Emma Stone in it!"
        elif (chosen_movie == "mamma mia" or chosen_movie == "mama mia"):
            speech_output += ". It`s movie made by Universal Pictures, staring Meryl Streep and Amanda Seyfried!"
        elif (chosen_movie == "titanic"):
            speech_output += ". It`s a real story about a person that do not share a piece of wood and let her beloved one die."
        elif (chosen_movie == "the notebook"):
            speech_output += ". It`s a movie that stares Ryan Gosling. It has Regina George on it as well, and we don`t like her."
        elif (chosen_movie == "the godfather"):
            speech_output += ". It`s a classic movie, starring Al Pacino. It`s about the italian mob."
        elif (chosen_movie == "baywatch"):
            speech_output += ". We all know about Baywatch. Or we`ve never watched Friends."
        elif (chosen_movie == "hangover"):
            speech_output += ". Basically, people getting drunk in Las Vegas. That`s enough, right?"
        elif (chosen_movie == "batman"):
            speech_output += ". NANANANANANA BATMAN!"
        elif (chosen_movie == "wonder woman"):
            speech_output += ". It`s a woman who kicks everyone`s butts."
    else:
        speech_output = "I'm not sure what movie you want to watch. " \
                        "Please try again."
        reprompt_text = "I'm not sure what movie you want to watch." \
                        "You can tell me which kind of movie you want to watch by saying I want to watch a romance."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()

def on_intent(intent_request, session):
    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent      = intent_request['intent']
    intent_name = intent_request['intent']['name']

    print(intent_name)

    if intent_name == "GetMovies":
        return set_movie_in_session(intent, session)
    elif intent_name == "GetGenres":
        return set_genre_in_session(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")

def on_session_ended(session_ended_request, session):
    print("on_session_ended requestId=" + session_ended_request['requestId'] + ", sessionId=" 
    + session['sessionId'])
    
# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])
    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])