import re
import imaplib
import json


class Mail:
    def __init__(self, nickname, password):
        self.nickname = nickname
        self.password = password
        
        self.imap_server = 'imap.rambler.ru'
        self.imap_port = 993

    def get_unseen_messages(self):
        try:
            # Connect to the IMAP server
            mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            mail.login(self.nickname, self.password)

            # Select the mailbox
            mail.select('INBOX')

            # Search for unseen messages
            status, response = mail.search(None, 'UNSEEN')

            # Fetch the unseen messages
            if status == 'OK':
                unseen_message_ids = response[0].split()
                messages = []
                for msg_id in unseen_message_ids:
                    _, data = mail.fetch(msg_id, '(RFC822)')
                    messages.append(data[0][1])
                return messages
            else:
                return []

        except Exception as e:
            print(f"Error: {e}")
            return []

        finally:
            # Close the connection
            mail.logout()

    def find_verification_code(self, byte_string): 
        pattern = rb"Verification Code: (\d{6})"
        print(byte_string)
        match = re.search(pattern, byte_string)
        if match:
            return match.group(1).decode()
        else:
            return None
    
    def get_code(self):
        unseen_messages = self.get_unseen_messages()
        code = self.find_verification_code(unseen_messages)
        
        return code


if __name__ == "__main__": 
    nickname = "bito0001@ro.ru"
    password = "Bito0001"
    
    mail = Mail(nickname, password)
    unseen_messages = mail.get_unseen_messages()
    print(unseen_messages)