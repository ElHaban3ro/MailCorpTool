# Libs.
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# Import configs.
from config import *


# Other imports
import os
import time
import json



class MailCorpTool():
    def __init__(self) -> None:

        self.SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

        if AUTH_TOKEN_FILE_BOOl:
            if os.path.exists(AUTH_TOKEN_FILE):
                try:
                    
                    
                    if os.path.exists('./../token.json'):
                        self.creds = Credentials.from_authorized_user_file('./../token.json', self.SCOPES)

                    else:
                        flow = InstalledAppFlow.from_client_secrets_file(AUTH_TOKEN_FILE, self.SCOPES)
                        self.creds = flow.run_local_server(port = 0)


                        with open('./../token.json', 'w') as token:
                            token.write(self.creds.to_json())

                except:
                    print('No connected with the Gmail API.')
                    exit()

            else:
                print("Auth file not found.")
                exit()


        else:
            print('AUTH_TOKEN_FILE_BOOL = False, not allow.')




    def start(self, sleepTime = 5):
        print(self.SCOPES)
        while(True):
            if self.creds:
                # Conecting to gmail.
                service = build('gmail', 'v1', credentials = self.creds)
                mails = service.users().messages().list(userId = 'me').execute() # ???
                
                
                
                if (mails['resultSizeEstimate'] > 0): # Hay emails dentro.
                    for mail in mails['messages']:
                        # Email Object
                        mailContent = service.users().messages().get(userId = 'me', id = mail['id']).execute()


                        # Email Info.
                        emailFrom = mailContent['payload']['headers'][6]['value'][1:-1]


                else:
                    print('Waiting for messages... ¿Nothing? :(')



            time.sleep(sleepTime)


client = MailCorpTool()
client.start(20)