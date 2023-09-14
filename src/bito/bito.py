"""
Handles operations with bito AI
"""

import os
import json
import time
import subprocess
import multiprocessing
from time import monotonic as _time

from mail import Mail
from loader import load_accounts


class Bito(object):
    def __init__(self) -> None:
        self.cli: str = "bito"
        self.max_processes = 60     # keep it lower than daily limit for one account (~200)
        
        self.accounts: list[list[str, str]] = load_accounts()
        
        self.current_account: int = 0
        self._communication_started = False
        self.number_of_accounts = len(self.accounts)
       

    def shrink_multiple_textes(self, textes: list[str]) -> list[str]:
        processes_count = min(self.max_processes, len(textes))
        
        with multiprocessing.Pool(processes_count) as pool:
            result = pool.map(self.shrink_text, textes)
            
            unprocessed_indexes = [index for index, text in enumerate(result) if text.find("we have limited your usage") != -1]
            if unprocessed_indexes:
                unprocessed_textes = [textes[index] for index in unprocessed_indexes]
                self.next_account()
                new_result = pool.map(self.shrink_text, unprocessed_textes)
                for i in range(len(unprocessed_indexes)):
                    result[unprocessed_indexes[i]] = new_result[i]
            
        return result
        
        

    
    def shrink_text_file(self, input_file_path: str, output_file_path: str) -> None:
        """
        :param input_file: Path to file with initial text
        :param output_file: Path to file to append modified text 
        """
        input_file = open(input_file_path, 'r')
                
        for input_line in input_file:
            input_line: str = input_line.strip()  
            modified_line: str = self.shrink_text(input_line)
            with open(output_file_path, 'a') as output_file:
                output_file.write(modified_line + '\n')
        
        input_file.close()
        

    def shrink_text(self, text: str) -> str:
        """
        :param text: String with text to modify
        
        :return: Text modified by AI
        """
        task: str = "Ответь на русском языке в одну строку. \
                    Сократи текст до 5 предложений. Выдели главные мысли:\n"
        text = task + text
        
        output: str = self.get_cli_answer(text)
        
        return output


    def get_cli_answer(self, input_str: str) -> str:
        """
        :input_str: String to be sent to cli
        
        :return: Answer from cli
        """
        # Start the CLI application as a subprocess
        process = subprocess.Popen(
            self.cli, 
            stdin=subprocess.PIPE, 
            stdout=subprocess.PIPE, shell=True
        )

        # Pass the input to the CLI application
        process.stdin.write(input_str.encode())

        # Read the output from the CLI application
        output, _ = process.communicate()
        output = output.decode().strip()

        # Close the subprocess
        process.stdin.close()
        process.stdout.close()
        process.wait()

        # Return the output
        return output

    def next_account(self) -> bool:
        self.current_account += 1
        if self.number_of_accounts == self.current_account:
            self.current_account = 0
            print("Warning: Last account reached! Using first one.")

        
        self.logout()
        self.login()
        
        return True
    
    def get_answer(query: list[str]) -> list[str]:
        return query
    
    def logout(self):
        os.remove("C:\\Users\\MANDR\\.bitoai\\etc\\bito-cli.yaml")
        
    def login(self):
        print(self.accounts)
        account = self.accounts[self.current_account]
        nickname = account[0]
        password = account[1]
        
        # Start the CLI application as a subprocess
        process = subprocess.Popen(
            self.cli, 
            stdin=subprocess.PIPE, 
            stdout=subprocess.PIPE, shell=True
        )
        # process.stdin.write(nickname.encode())
        process.stdin.write(nickname.encode())
        output, _ = process.communicate()
        print(output)
        time.sleep(5)
        
        process.wait(timeout=5)
        print(process.stdout.readlines())
        
        mail = Mail(nickname, password)
        code = mail.get_code()
        
        process.communicate(code.encode())

        process.stdin.close()
        process.stdout.close()
        process.wait()
        
        
if __name__ == '__main__':
    bito = Bito()
    bito.login()
