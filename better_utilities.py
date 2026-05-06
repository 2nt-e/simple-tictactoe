import time
import traceback

class Printer:
    def print(content, sepr = " ", end = "\n"):
        c_word = 1
        for words in content.split(" "):        
            if c_word < len(content.split(" ")):
                print(words, end=sepr, flush=True)
                time.sleep(0.05)
                c_word += 1
            elif c_word == len(content.split(" ")):
                print(words, end=end, flush=True)
                time.sleep(0.05)

    def input(prompt):
        Printer.print(prompt, end="")
        return input()

class Logger:
    def __init__(self, Name):
        self.Name = Name
        self.Is_Enable = False
    
    def add_logging(self, message=None, function=None):
        caller = traceback.extract_stack(limit=2)[0]
        link = f'File "{caller.filename}", line {caller.lineno}'
        if self.Is_Enable:
            print()
            print(f"{self.Name} at {link} Logged: ")
            if message:
                print(message)
            if function:
                function()
            print('\n\n')
    
    def set_logging(self, Is_Enable: bool=True):
        self.Is_Enable = Is_Enable