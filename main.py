from better_print import *

import tkinter as tk
from tkinter import ttk
import winsound

class CButton(tk.Button):
    def __init__(self, master=None, cid=[], engine=None, **kwargs):
        self.engine = engine
        self.cid = cid
        
        super().__init__(master, **kwargs)
        self.whiteimg = tk.PhotoImage(file='resource/white.png')
        self.redimg = tk.PhotoImage(file='resource/red.png')
        self.blueimg = tk.PhotoImage(file='resource/blue.png')
        self.configure(command=self.proceed, image=self.whiteimg, borderwidth=0, highlightthickness=0)

    def proceed(self):
        print(f"proceed: {self.cid}")
        self.engine.implement(f'{self.cid[0]}{self.cid[1]}')
        self.configure(state=tk.DISABLED, image=self.redimg)
        winsound.PlaySound(r'C:\Users\OK\Documents\! PYTHON\simple-tictactoe\resource\effect.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)



class application(tk.Tk):
    def __init__(self, engine, *args, **kwargs):
        self.engine = engine

        super().__init__(*args, **kwargs)
        self.geometry('500x500')
        self.title("Chromyl TicTacToe")
        self.iconbitmap('resource/icon.ico')
        self.resizable(width=False, height=False)

        self.backframe = tk.Frame(self, background='gray')
        self.backframe.grid(row=0, column=0)

        self.txtvar = tk.StringVar()
        self.txtvar.set("Chromyl TicTacToe")
        self.text = tk.Label(self.backframe, textvariable=self.txtvar, background='gray', font=("Helvetica", 22, "bold"))
        self.text.grid(row=1, column=0, pady=10)

        self.gameframe = tk.Frame(self.backframe, border=1, borderwidth=5, relief=tk.GROOVE)
        self.gameframe.grid(row=2, column=0, padx=100, pady=80)
    
    def run(self):
        self.mainloop()
    
    def expand(self, n=3):
        for i in range(1, n+1):
            for j in range(1, n+1):
                CButton(self.gameframe, cid=[i, j]).grid(row=i, column=j, engine=self.engine)


m = application()
m.expand(n=3)
m.run()




class Game:
    def __init__(self, n=3, mode='pvp'):
        self.n = n
        self.symbols = {'cornor': "🟦",
                        'void': "0️⃣",
                        '1': "1️⃣",
                        '2': "2️⃣",
                        '3': "3️⃣",
                        '4': "4️⃣",
                        '5': "5️⃣",
                        '6': "6️⃣",
                        '7': "7️⃣",
                        '8': "8️⃣",
                        '9': "9️⃣",
                        'P1' : '⏺️',
                        'P2' : '#️⃣',
                        'ai' : '#️⃣',
                        None: "baka!"
                        }
        self.map = {}
        for r in range(1, n+1):
            for c in range(1, n+1):
                self.map[f'{r}{c}'] = 'void'
        self.turn = 1
        self.ocupation = []
        self.mode = mode
        self.placements = {
             'd1' : [],
             'd2' : []
        }
        for i in range(1, n+1):
            self.placements[f'r{i}'] = []
            self.placements[f'c{i}'] = []

    def print_grid(self): # For printing structure
                print(self.symbols['cornor'], end="")
                for f in range(1, self.n+1):
                    print(self.symbols[str(f)], end=" ")
                print()
                for r in range(1, self.n+1):
                    print(self.symbols[str(r)], end=" ")
                    for c in range(1,self.n+1):
                        print(self.symbols[self.map[f'{r}{c}']], end=" ")
                    print()

    @property
    def mode(self): #WIP, mode
         return self._mode
    @mode.setter
    def mode(self, value): #WIP, mode
         if value == "pvp":
              self._mode = 'P2'
         elif value == 'ai':
              self._mode = 'ai' 
         else:
              self._mode = 'invalid_mode'

    def check_chance(self): # checking for chance
        if self.turn%2 == 0: 
            return self.mode 
        else: 
            return "P1"

    def contraditon(self, change):
        try: 
            if change not in self.ocupation:
                return False
            else:
                return "already_occupied"
        except:
            return "invalid_input"
    
    def implement(self, change): #Implementing on every move
         chance = self.check_chance() 
         contraditon = self.contraditon(change)
         if self.mode == 'ai':
              ... #WIP
         elif contraditon == False and change in self.map.keys():
             self.map[change] = chance
             self.ocupation.append(change)
             self.turn += 1
             self.placements[f'r{change[0]}'].append(chance)
             self.placements[f'c{change[1]}'].append(chance)
             if change[0] == change[1]:
                 self.placements['d1'].append(chance)
             if int(change[0]) + int(change[1]) == self.n+1:
                 self.placements['d2'].append(chance)

    def victory(self):
         for w in self.placements.values():
              if len(w) == self.n:
                   if len(set(w))==1:
                        return w[0]

    def game_end(self):
        if len(self.ocupation) == self.n**2:
            return "tie"
        elif self.victory() != None:
             return "victory"
        else:
            return False
    
    def oraganize(self):
        while self.game_end() == False:
            self.print_grid()
            # print(self.map, self.placements['c1']) # For debugging
            change = better.input(f"Where to put {self.symbols[self.check_chance()]} : ").strip()
            self.implement(change)
            print('\n'*2)
        else:
             print()
             messages = {
                  'tie': "Game ended with Tie.",
                  'victory': f"Game ended, Player {self.symbols[self.victory()]}  won!",
             }
             better.print(messages[self.game_end()])
    

# obj = Game(n=4)
# obj.oraganize()
