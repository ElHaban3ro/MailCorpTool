# Libs.
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Import configs.
from config import *


# Other imports
import os
import time
import json



class MailCorpTool():
    def __init__(self) -> None:
        
        self.AllowedEmails = json.load(open('./../registredAccounts.json')) # Diccionary!


        self.SCOPES = ['https://mail.google.com/']

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
        print('MailCorpTool is running. Handler Emails.')
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
                        emailFrom = ''
                        nameFrom = ''


                        # Find Title
                        for cname, name in enumerate(mailContent['payload']['headers']):
                            
                            if (name['name'] == 'From'):
                                splitInfo = name['value'].split('<')


                                emailFrom = splitInfo[1][:-1].strip()
                                nameFrom = splitInfo[0].strip()
                                break

                            else:
                                continue



                        titleEmail = ''
                        redirectToEmail = ''
                        allowRedirectEmail = False


                        # Find Title
                        for cname, name in enumerate(mailContent['payload']['headers']):
                            auth = False

                            if (name['name'] == 'Subject'):

                                titleEmailRaw = name['value'].split('>') # To target determined with ">" in the title. 
                                titleEmail = titleEmailRaw[0].strip()


                                if len(titleEmailRaw) == 2:
                                    redirectToEmail = titleEmailRaw[1].strip()
                                    allowRedirectEmail = True

                                else:
                                    redirectToEmail = None
                                    allowRedirectEmail = False # Redundancia.


                                # Example of this:
                                # Subject: important meeting! > MyEmployee@enterprise.com
                                # Details: Come to, paaa.


                                # This email will be redirected to MyEmployee@enterprise.com.
                                # If there is nothing, the mail is not sent.


                                break

                            else:
                                continue    


                        emailTextContent = mailContent['payload']['parts']
                        if emailTextContent[0]['mimeType'] == 'text/plain': # Validamos la codificación del texto.
                            RawEmailTextContent = emailTextContent[0]['body']['data']
                            emailTextContent = emailTextContent[0]['body']['data'].replace('-', '+').replace('_', '/')
                            emailTextContent = base64.b64decode(emailTextContent).decode()


                        
                        redirectFromEmail = ''

                        if emailFrom in list(self.AllowedEmails['TeamEmails'].keys()): # Las Keys representan los emails nativos que permitiremos.
                            if allowRedirectEmail:
                                auth = True

                                authEmailIndex = list(self.AllowedEmails['TeamEmails'].keys()).index(emailFrom)
                                redirectFromEmail = list(self.AllowedEmails['TeamEmails'].values())[authEmailIndex]

                                


                            else:
                                auth = False


                            
                        else:
                            auth = False





                        if allowRedirectEmail:
                            print(f'\n\n--------------- MailCorpTool --------------------\nNew message detected from {emailFrom} with name {nameFrom}, to {redirectToEmail}, with title "{titleEmail}" and the text:\n{emailTextContent}\nAuthorized: {allowRedirectEmail}. ')

                            message = MIMEMultipart() # Message component. To send.

                            #TODO: Intenar añadir el texto raw.
                            bodyEmail = MIMEText(emailTextContent) # The body is compresed
                            message.attach(bodyEmail) # Se añade este mensado comprimido
                            message['to'] = redirectToEmail
                            message['subject'] = titleEmail
                            message['from'] = redirectFromEmail
                            
                            create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()} # Se crea el "constructor del mensaje."

                            send_message = service.users().messages().send(userId = 'me', body = create_message).execute()

                            delete_original_message = service.users().messages().delete(userId = 'me', id = mail['id']).execute()

                            time.sleep(5) # Si va demasiado rapido, el mensaje aún no se envia.

                            delete_resend_message = service.users().messages().delete(userId = 'me', id = send_message['id']).execute()


                            print('The message was correctly sent to the addressee.\n\n--------------- MailCorpTool --------------------\n\n\n')
                            continue

                        else:
                            continue

                else:
                    print('Waiting for messages... ¿Nothing? :(')



            time.sleep(sleepTime)


client = MailCorpTool()
client.start(5)