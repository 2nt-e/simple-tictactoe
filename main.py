from better_print import *

import tkinter as tk
import winsound



class MainEngine:
    def __init__(self, n=3, mode='pvp'):
        self.n = n
        self.symbols = {'cornor': "🟦", # For testing.
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
        self.placements = {'d1' : [], 'd2' : []}
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
        if self.victory() != None:
             return "victory"
        elif len(self.ocupation) == self.n**2:
            return "tie"
        else:
            return False
    
    

class CButton(tk.Button):
    def __init__(self, master=None, cid=[], engine=None, **kwargs):
        self.engine = engine
        self.cid = cid
        self.continue_game = True
        super().__init__(master, **kwargs)
        self.images = {'0': tk.PhotoImage(file='resource/white.png'),
                       'P1': tk.PhotoImage(file='resource/red.png'),
                       'P2': tk.PhotoImage(file='resource/blue.png')}
        self.configure(command=self.proceed, image=self.images['0'], borderwidth=0, highlightthickness=0)

    def proceed(self):
        if not self.engine.game_end():
            p = self.engine.check_chance()
            colors = {'P1': '#9C6C6C', 'P2': '#6C879C'}
            colors_name = {'P1': 'Red', 'P2': 'Blue', None: None}
            print(f"Player-{p} proceed at {self.cid}")
            self.configure(state=tk.DISABLED, image=self.images[p])
            self.engine.implement(change=f'{self.cid[0]}{self.cid[1]}')
            self.master.master.master.backframe.configure(background=colors[self.engine.check_chance()])
            self.master.master.master.text.configure(background=colors[self.engine.check_chance()], foreground=colors_name[self.engine.check_chance()])
            self.master.master.master.txtvar.set(f"{colors_name[self.engine.check_chance()]}'s Turn!")
            self.engine.print_grid()
            winsound.PlaySound(r'resource\effect.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)

        if self.engine.game_end():
             self.continue_game = False
             messages = {
                  'tie': "Game ended with Tie.",
                  'victory': f"Game ended, {colors_name[self.engine.victory()]} won!",}
             better.print(messages[self.engine.game_end()])
             self.master.master.master.txtvar.set(messages[self.engine.game_end()])
             winsound.PlaySound(r'resource\victory.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
             self.master.master.master.backframe.configure(background='silver')
             self.master.master.master.text.configure(background='silver', foreground='white')




class GameWindow(tk.Tk):
    def __init__(self, engine, n, *args, **kwargs):
        self.n = n
        self.engine = engine(n=self.n)

        super().__init__(*args, **kwargs)
        self.geometry('500x500')
        self.title("Simple TicTacToe")
        self.iconbitmap('resource/icon.ico')
        self.resizable(width=False, height=False)

        self.backframe = tk.Frame(self, background='silver')
        self.backframe.grid(row=0, column=0)

        self.txtvar = tk.StringVar()
        self.txtvar.set("Simple TicTacToe")
        self.text = tk.Label(self.backframe, textvariable=self.txtvar, background='silver', font=("Helvetica", 22, "bold"), foreground='white')
        self.text.grid(row=1, column=0, pady=10)

        self.gameframe = tk.Frame(self.backframe, border=1, borderwidth=5, relief="solid", background="#212124")
        self.gameframe.grid(row=2, column=0, padx=100, pady=50)
    
        for i in range(1, self.n+1):
            for j in range(1, self.n+1):
                CButton(self.gameframe, cid=[i, j], engine=self.engine).grid(row=i, column=j, padx=1, pady=1)

    def run(self):
        self.engine.print_grid()
        self.mainloop()
        
    



main = GameWindow(engine=MainEngine, n=3)
main.run()

