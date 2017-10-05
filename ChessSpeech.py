#Python 2.x program for Speech Recognition
 
import speech_recognition as sr
from luis_sdk import LUISClient

class ChessSpeech():

    def Speech(self):
        #enter the name of usb microphone that you found
        #using lsusb
        #the following name is based on my machine, please find the appropriate for yours
        mic_name = "Headset Microphone (ASTRO Wirel"
        #Sample rate is how often values are recorded
        sample_rate = 48000
        #Chunk is like a buffer. It stores 2048 samples (bytes of data)
        #here. 
        #it is advisable to use powers of 2 such as 1024 or 2048
        chunk_size = 2048
        #Initialize the recognizer
        r = sr.Recognizer()
         
        #generate a list of all audio cards/microphones
        mic_list = sr.Microphone.list_microphone_names()
         
        #the following loop aims to set the device ID of the mic that
        #we specifically want to use to avoid ambiguity.
        for i, microphone_name in enumerate(mic_list):
            if microphone_name == mic_name:
                device_id = i
         
        #use the microphone as source for input. Here, we also specify 
        #which device ID to specifically look for incase the microphone 
        #is not working, an error will pop up saying "device_id undefined"
        with sr.Microphone(device_index = device_id, sample_rate = sample_rate, 
                                chunk_size = chunk_size) as source:
            #wait for a second to let the recognizer adjust the 
            #energy threshold based on the surrounding noise level
            r.adjust_for_ambient_noise(source)
            print "Say Something"
            #listens for the user's input

            audio = r.listen(source)
            print "Done Listening"
            try:
                text = r.recognize_google(audio)
                if 'for' in text:
                    text = text.replace('for', 'four')
                

                print "you said: " + text
                return text
             
            #error occurs when google could not understand what was said
             
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
                return ("Google could not understand the audio.")
             
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
                return ("Unable to reach Google Speech Recognition service.")

    def process_res(self, res, TEXT):
            typeList = []
            entityList = []
            print(u'---------------------------------------------')
            print(u'LUIS Response: ')
            print(u'Query: ' + res.get_query())
            print(u'Top Scoring Intent: ' + res.get_top_intent().get_name())
            if res.get_dialog() is not None:
                if res.get_dialog().get_prompt() is None:
                    print(u'Dialog Prompt: None')
                else:
                    print(u'Dialog Prompt: ' + res.get_dialog().get_prompt())
                if res.get_dialog().get_parameter_name() is None:
                    print(u'Dialog Parameter: None')
                else:
                    print('Dialog Parameter Name: ' + res.get_dialog().get_parameter_name())
                print(u'Dialog Status: ' + res.get_dialog().get_status())
            print(u'Entities:')
            for entity in res.get_entities():
                print(u'"%s":' % entity.get_name())
                print(u'Type: %s, Score: %s' % (entity.get_type(), entity.get_score()))
                entityList.append(entity.get_type())
                entityList.append(entity.get_name())

            if not entityList:
                entityList.append('none')
                print "list is empty"

            return entityList

    def LUIS_api(self, TEXT):
        '''
        A function that processes the luis_response object and prints info from it.
        :param res: A LUISResponse object containing the response data.
        :return: None
        '''
        try:
            APPID = '7450cf5d-8f8e-470d-9bf2-4b4d10e706c3'
            APPKEY = '77863426d1f047f3981614871fa3e590'
            CLIENT = LUISClient(APPID, APPKEY, True)
            res = CLIENT.predict(TEXT)
            while res.get_dialog() is not None and not res.get_dialog().is_finished():
                TEXT = raw_input(u'%s\n'%res.get_dialog().get_prompt())
                res = CLIENT.reply(TEXT, res)
            ent = self.process_res(res, TEXT)
            return ent
        except Exception, exc:
            print(exc)


    def findPieceLocation(self, query, board):
        '''
            Uses the text given from LUISapi to find the location of the piece on the board.
        '''
        cps = {'queen' : 'wQ', 'king' : 'wK1', 'rook one' : 'wR1', 'rook 1' : 'wR1', 'rook two' : 'wR2', 'rook 2' : 'wR2', 'knight one' : 'wT1', 'knight 1' : 'wT1', 'knight two' : 'wT2', 'knight 2' : 'wT2', 'bishop one' : 'wB1', 'bishop 1' : 'wB1', 'bishop two' : 'wB2', 'bishop 2' : 'wB2', 'pawn one' : 'wP1', 'pawn 1' : 'wP1', 'pawn two' : 'wP2', 'pawn 2' : 'wP2', 'pawn three' : 'wP3', 'pawn 3' : 'wP3', 'pawn four' : 'wP4', 'pawn 4' : 'wP4', 'pawn five' : 'wP5', 'pawn 5' : 'wP5', 'pawn six' : 'wP6', 'pawn 6' : 'wP6', 'pawn seven' : 'wP7', 'pawn 7' : 'wP7', 'pawn eight' : 'wP8', 'pawn 8' : 'wP8'}

        piece = 'not found'
        location = (-1, -1)

        for e in query:
            if e in cps:
                piece = cps.get(e)


        if (piece != 'not found'):
            for i in range(0, 8):
                for j in range(0, 8):
                    if (board[i][j] == piece):
                        location = (i, j)

        return location

    def moveToLocation(self, query, board):
        '''
            Uses the text given from LUIS api to find the location on the board from where you'd like to move.

            Ex.
            move to B3

            B3 would return (1, 5)
        '''

        numb = {}
        numb.update({'a1' : (7,0), 'a2' : (6,0), 'a3' : (5,0), 'a4' : (4,0), 'a5' : (3,0), 'a6' : (2,0), 'a7' : (1,0), 'a8' : (0,0)})
        numb.update({'b1' : (7,1), 'b2' : (6,1), 'b3' : (5,1), 'b4' : (4,1), 'b5' : (3,1), 'b6' : (2,1), 'b7' : (1,1), 'b8' : (0,1)})
        numb.update({'c1' : (7,2), 'c2' : (6,2), 'c3' : (5,2), 'c4' : (4,2), 'c5' : (3,2), 'c6' : (2,2), 'c7' : (1,2), 'c8' : (0,2)})
        numb.update({'d1' : (7,3), 'd2' : (6,3), 'd3' : (5,3), 'd4' : (4,3), 'd5' : (3,3), 'd6' : (2,3), 'd7' : (1,3), 'd8' : (0,3)})
        numb.update({'e1' : (7,4), 'e2' : (6,4), 'e3' : (5,4), 'e4' : (4,4), 'e5' : (3,4), 'e6' : (2,4), 'e7' : (1,4), 'e8' : (0,4)})
        numb.update({'f1' : (7,5), 'f2' : (6,5), 'f3' : (5,5), 'f4' : (4,5), 'f5' : (3,5), 'f6' : (2,5), 'f7' : (1,5), 'f8' : (0,5)})
        numb.update({'g1' : (7,6), 'g2' : (6,6), 'g3' : (5,6), 'g4' : (4,6), 'g5' : (3,6), 'g6' : (2,6), 'g7' : (1,6), 'g8' : (0,6)})
        numb.update({'h1' : (7,7), 'h2' : (6,7), 'h3' : (5,7), 'h4' : (4,7), 'h5' : (3,7), 'h6' : (2,7), 'h7' : (1,7), 'h8' : (0,7)})

        numb.update({'a 1' : (7,0), 'a 2' : (6,0), 'a 3' : (5,0), 'a 4' : (4,0), 'a 5' : (3,0), 'a 6' : (2,0), 'a 7' : (1,0), 'a 8' : (0,0)})
        numb.update({'b 1' : (7,1), 'b 2' : (6,1), 'b 3' : (5,1), 'b 4' : (4,1), 'b 5' : (3,1), 'b 6' : (2,1), 'b 7' : (1,1), 'b 8' : (0,1)})
        numb.update({'c 1' : (7,2), 'c 2' : (6,2), 'c 3' : (5,2), 'c 4' : (4,2), 'c 5' : (3,2), 'c 6' : (2,2), 'c 7' : (1,2), 'c 8' : (0,2)})
        numb.update({'d 1' : (7,3), 'd 2' : (6,3), 'd 3' : (5,3), 'd 4' : (4,3), 'd 5' : (3,3), 'd 6' : (2,3), 'd 7' : (1,3), 'd 8' : (0,3)})
        numb.update({'e 1' : (7,4), 'e 2' : (6,4), 'e 3' : (5,4), 'e 4' : (4,4), 'e 5' : (3,4), 'e 6' : (2,4), 'e 7' : (1,4), 'e 8' : (0,4)})
        numb.update({'f 1' : (7,5), 'f 2' : (6,5), 'f 3' : (5,5), 'f 4' : (4,5), 'f 5' : (3,5), 'f 6' : (2,5), 'f 7' : (1,5), 'f 8' : (0,5)})
        numb.update({'g 1' : (7,6), 'g 2' : (6,6), 'g 3' : (5,6), 'g 4' : (4,6), 'g 5' : (3,6), 'g 6' : (2,6), 'g 7' : (1,6), 'g 8' : (0,6)})
        numb.update({'h 1' : (7,7), 'h 2' : (6,7), 'h 3' : (5,7), 'h 4' : (4,7), 'h 5' : (3,7), 'h 6' : (2,7), 'h 7' : (1,7), 'h 8' : (0,7)}) 

        numb.update({'a one' : (7,0), 'a two' : (6,0), 'a three' : (5,0), 'a four' : (4,0), 'a five' : (3,0), 'a six' : (2,0), 'a seven' : (1,0), 'a eight' : (0,0)})
        numb.update({'b one' : (7,1), 'b two' : (6,1), 'b three' : (5,1), 'b four' : (4,1), 'b five' : (3,1), 'b six' : (2,1), 'b seven' : (1,1), 'b eight' : (0,1)})
        numb.update({'c one' : (7,2), 'c two' : (6,2), 'c three' : (5,2), 'c four' : (4,2), 'c five' : (3,2), 'c six' : (2,2), 'c seven' : (1,2), 'c eight' : (0,2)})
        numb.update({'d one' : (7,3), 'd two' : (6,3), 'd three' : (5,3), 'd four' : (4,3), 'd five' : (3,3), 'd six' : (2,3), 'd seven' : (1,3), 'd eight' : (0,3)})
        numb.update({'e one' : (7,4), 'e two' : (6,4), 'e three' : (5,4), 'e four' : (4,4), 'e five' : (3,4), 'e six' : (2,4), 'e seven' : (1,4), 'e eight' : (0,4)})
        numb.update({'f one' : (7,5), 'f two' : (6,5), 'f three' : (5,5), 'f four' : (4,5), 'f five' : (3,5), 'f six' : (2,5), 'f seven' : (1,5), 'f eight' : (0,5)})
        numb.update({'g one' : (7,6), 'g two' : (6,6), 'g three' : (5,6), 'g four' : (4,6), 'g five' : (3,6), 'g six' : (2,6), 'g seven' : (1,6), 'g eight' : (0,6)})
        numb.update({'h one' : (7,7), 'h two' : (6,7), 'h three' : (5,7), 'h four' : (4,7), 'h five' : (3,7), 'h six' : (2,7), 'h seven' : (1,7), 'h eight' : (0,7)})

        for i in range(len(query)):
            if (query[i] == 'location'):
                loc = i + 1

        location = (-1, -1)

        print query[loc]
        if (query[loc] in numb):
            location = numb.get(query[loc])
        else:
            location = (-1, -1)

        return location