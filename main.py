from datetime import datetime
import speech_recognition as sr 
import pyttsx3
import webbrowser
import wikipedia
import wolframalpha
import pyautogui

# speech engine install
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id) # voice for male
activation_word = 'computer' # single activation word

# config browser
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

# wolfram alpha client
appId = 'JGPU5G-689LWKWGA3'
wolframClient = wolframalpha.Client(appId)

# speaking
def speak(text, rate = 120):
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()

# parses the list passed through
def parseCommand():
    listener = sr.Recognizer()
    print('Listening for a command')

    with sr.Microphone() as source:
        input_speech = listener.listen(source, timeout=10)

    try:
        print('Recognizing speech...')
        query = listener.recognize_google(input_speech, language = 'en_gb')
        print(f'The input was: {query}')
    except Exception as exception:
        print('I did not quite catch that')
        speak('I did not quite catch that')
        print(exception)
        return 'None'
    
    return query

# Will search through wikipedia and read the result
def search_wikipedia(query = ''):
    searchResults = wikipedia.search(query)
    if not searchResults:
        print('No wikipedia result')
        return 'No result recieved'
    try:
        wikiPage = wikipedia.page(searchResults[0])
    except wikipedia.DisambiguationError as error:
        wikiPage = wikipedia.page(error.options[0])
    print(wikiPage.title)
    wikiSummary = str(wikiPage.summary)
    return wikiSummary

# decides between a list and a dict
def listOrDict(var):
    if isinstance(var, list):
        return var[0]['plaintext']
    else:
        return var['plaintext']

# searches the wolframalpha app
def search_wolframalpha(query = ''):
    response = wolframClient.query(query)
    if response['@success'] == 'false':
        return 'Could not calculate'
    else:
        result = ''

        pod0 = response['pod'][0]
        pod1 = response['pod'][1]

        if (('result') in pod1['@title'].lower()) or (pod1.get('@primary', 'false') or ('definition' in pod1['@title'].lower())):
            result = listOrDict(pod1['subpod'])
            return result.split('(')[0]
        else:
            question = listOrDict(pod0['subpod'])
            question.split('(')[0]
            speak('Calculation failed, searching the world wide web')
            return search_wikipedia(question)

# types keyboard inputs 
def type_keyboard(query = ''):
    if 'write' in query:
        text_to_type = ' '.join(query[1:])
        pyautogui.write(text_to_type, interval = 0.1)
    elif 'press' in query:
        key_to_press = ' '.join(query[1:])
        pyautogui.press(key_to_press, interval = 0.1)
    else:
        speak('Command not regognized')

# main

if __name__ == '__main__':
    speak('Hello I am here to help.')

    while True:
        # Parse as list
        query = parseCommand().lower().split()

        if query[0] == activation_word and len(query) != 1:
            query.pop(0)

            #### TALKING COMMANDS ####

            # Hello command
            if query[0] == 'say':
                if 'hello' in query:
                    speak('Grettings')
                else:
                    query.pop(0) # Remove say
                    speech = ' '.join(query)
                    speak(speech)

            # Stops AI
            elif query[0] == 'exit':
                speak('Exiting')
                break

            #### NAVIGATION COMMANDS ####
                    
            elif query[0] == 'go' and query[1] == 'to':
                speak('Opening...')
                query = ' '.join(query[2:])
                webbrowser.get('chrome').open_new(query)

            # Wiki
                
            elif query[0] == 'wikipedia':
                query = ' '.join(query[1:])
                speak('Getting information from universal data')
                speak(search_wikipedia(query))

            # wolfram alpha
            
            elif query[0] == 'calculate':
                query = ' '.join(query[1:])
                speak('Calculating...')
                try:
                    result = search_wolframalpha(query)
                    speak(result)
                except:
                    speak('Unable to calculate')

            # note taking
            
            elif query[0] == 'log':
                speak('Ready to record your note')
                newNote = parseCommand().lower()
                now = datetime.now().strftime('%Y-%m-%D-%H-%M-%S')

                with open('note.txt', 'a+') as newFile:
                    newFile.write('\n' + now + '\n' + newNote + '\n-----------------------------')
                speak('Note Written')
            
            elif query[0] == 'clear' and query[1] == 'notes':
                speak('Are you sure you want to delete your notes?')
                query = parseCommand().lower().split()
                if query[0] == 'yes':
                    speak('The contents of the notes are being deleted')
                    with open('note.txt', 'w') as file:
                        pass
                else:
                    speak('The contents of the notes are not deleted')
            
            elif query[0] == 'type':
                query[0] = 'write'
                type_keyboard(query)

            elif query[0] == 'press':
                type_keyboard(query)

            ### HELP COMMANDS ###

            elif query[0] == 'help':
                speak('Here are a list of commands you can use')
                print("Usage: computer <command>\n"
                      "Commands: \n"
                      "\t--help--\n"
                      "\t--say hello--\n"
                      "\t--exit--\n"
                      "\t--go to <link to webpage>--\n"
                      "\t--wikipedia <name of search>--\n"
                      "\t--calculate--\n"
                      "\t--log--\n"
                      "\t--clear notes--\n"
                      "\t--type <word>--\n"
                      "\t--press <Key>--\n"
                      "Examples:\n"
                      "\t--computer help--\n"
                      "\t--computer say hello--\n"
                      "\t--computer exit--\n"
                      "\t--computer go to google.com--\n"
                      "\t--computer calculate the distance from canada to america--\n"
                      "\t--computer wikipedia dog--\n"
                      "\t--computer log--\n"
                      "\t" + "\t This is a test message\n"
                      "\t--computer clear notes--\n"
                      "\t" + "\t yes \n"
                      "\t--type hello--\n"
                      "\t--press a--\n")
            else:
                speak(f'You said {query} which is not a valid command\n')
                print("Refer to the help page (computer help) for commands")

                