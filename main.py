from better_print import *

import tkinter as tk
import winsound

import asyncio


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

    def print_grid(self): # For printing structure, For testing.
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
         elif value == 'online':
              self._mode = 'Opt'
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
    
    

class GameButton(tk.Button):
    def __init__(self, master=None, cid=[], **kwargs):
        self.cid = cid
        super().__init__(master, **kwargs)
        self.images = {'0': tk.PhotoImage(file='resource/white.png'),
                       'P1': tk.PhotoImage(file='resource/red.png'),
                       'P2': tk.PhotoImage(file='resource/blue.png')}
        self.top = self.master.master.master
        self.engine = self.top.engine
        self.gamemodes = {'P2': self.OffPVP, 'Opt': self.OnnPVP}
        self.configure(command=self.gamemodes[self.top.engine.mode], image=self.images['0'], borderwidth=0, highlightthickness=0, bd=0)

    def OffPVP(self):
        if not self.engine.game_end():
            p = self.engine.check_chance()
            colors = {'P1': '#9C6C6C', 'P2': '#6C879C'}
            colors_name = {'P1': 'Red', 'P2': 'Blue', None: None}
            print(f"Player-{p} proceed at {self.cid}")
            self.configure(state=tk.DISABLED, image=self.images[p])
            self.engine.implement(change=f'{self.cid[0]}{self.cid[1]}')
            self.top.backframe.configure(background=colors[self.engine.check_chance()])
            self.top.text.configure(background=colors[self.engine.check_chance()], foreground=colors_name[self.engine.check_chance()])
            self.top.txtvar.set(f"{colors_name[self.engine.check_chance()]}'s Turn!")
            self.engine.print_grid()
            winsound.PlaySound(r'resource\effect.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
        if self.engine.game_end():
             self.continue_game = False
             end = self.engine.game_end()
             messages = {
                  'tie': "Game ended with Tie.",
                  'victory': f"Game ended, {colors_name[self.engine.victory()]} won!",}
             better.print(messages[end])
             self.master.master.master.txtvar.set(messages[self.engine.game_end()])
             winsound.PlaySound(rf'resource\{end}.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
             self.top.backframe.configure(background='silver')
             self.top.text.configure(background='silver', foreground='white')
             self.top.disallCbutton()

    def OnnPVP(self):
        if not self.engine.game_end():
            p = self.engine.check_chance()
            colors = {'P1': '#9C6C6C', 'P2': '#6C879C'}
            colors_name = {'P1': 'Red', 'P2': 'Blue', None: None}
            print(f"Player-{p} proceed at {self.cid}")
            self.configure(state=tk.DISABLED, image=self.images[p])
            self.engine.implement(change=f'{self.cid[0]}{self.cid[1]}')
            self.top.backframe.configure(background=colors[self.engine.check_chance()])
            self.top.text.configure(background=colors[self.engine.check_chance()], foreground=colors_name[self.engine.check_chance()])
            self.top.txtvar.set(f"{colors_name[self.engine.check_chance()]}'s Turn!")
            self.engine.print_grid()
            winsound.PlaySound(r'resource\effect.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
        if self.engine.game_end():
             self.continue_game = False
             end = self.engine.game_end()
             messages = {
                  'tie': "Game ended with Tie.",
                  'victory': f"Game ended, {colors_name[self.engine.victory()]} won!",}
             better.print(messages[end])
             self.master.master.master.txtvar.set(messages[self.engine.game_end()])
             winsound.PlaySound(rf'resource\{end}.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
             self.top.backframe.configure(background='silver')
             self.top.text.configure(background='silver', foreground='white')
             self.top.disallCbutton()



class GameWindow(tk.Tk):
    def __init__(self, engine, n, *args, **kwargs):
        self.n = n
        self.engine = engine(n=self.n)

        super().__init__(*args, **kwargs)
        size = self.n * 100 + 200
        self.geometry(f'{size}x{size}')
        self.title("Simple TicTacToe")
        self.iconbitmap('resource/icon.ico')
        self.resizable(width=False, height=False)

        self.backframe = tk.Frame(self, background='silver')
        self.backframe.grid(row=0, column=0)

        self.txtvar = tk.StringVar()
        self.txtvar.set("Simple TicTacToe")
        self.text = tk.Label(self.backframe, textvariable=self.txtvar, background='silver', font=("Franklin Gothic Heavy", 22, "bold"), foreground='white')
        self.text.grid(row=1, column=0, pady=10)

        self.gameframe = tk.Frame(self.backframe, border=1, borderwidth=5, relief="solid", background="#212124")
        self.gameframe.grid(row=2, column=0, padx=100, pady=50)
    
        for i in range(1, self.n+1):
            for j in range(1, self.n+1):
                GameButton(self.gameframe, cid=[i, j]).grid(row=i, column=j, padx=1, pady=1)

    def run(self):
        self.engine.print_grid()
        self.mainloop()
        
    def disallCbutton(self):
        for button in self.gameframe.winfo_children():
            button.configure(state=tk.DISABLED)



class GridButton(tk.Button):
    def __init__(self, master=None, gid='3x3', **kwargs):
        self.gid = gid
        super().__init__(master, **kwargs)
        self.image =tk.PhotoImage(file=f'resource/{self.gid}.png')
        self.configure(command=self.Toggle, image=self.image, borderwidth=0, highlightthickness=0, bd=0)
    
    def Toggle(self):
        winsound.PlaySound(rf'resource\tick.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
        self.master.n = int(self.gid[0])
        for button in self.master.winfo_children():
            if str(button)[2] == 'g':
               button.configure(state=tk.NORMAL)
        self.configure(state=tk.DISABLED)


class MenuWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        self.n = 3
        super().__init__(*args, **kwargs)
        self.geometry('500x500')
        self.title("Simple TicTacToe")
        self.iconbitmap('resource/icon.ico')
        self.resizable(width=False, height=False)
        self.mainframe = tk.Frame(self, background='gray').grid(row=0, column=0)

        tk.Label(self.mainframe, text="Select Grid Size & Game Mode!", font=("Franklin Gothic Heavy", 22, "bold"), background='gray').grid(row=1, column=1, padx=20)
        
        GridButton(self.mainframe, gid='3x3').grid(column=1, row=2, pady=20)
        GridButton(self.mainframe, gid='4x4').grid(column=1, row=3, pady=20)
        
        tk.Button(self.mainframe, text="Start Game", command=self.start_game).grid(row=4,column=1, pady=20)

    def start_game(self):
        self.destroy()
        game = GameWindow(engine=MainEngine, n=self.n)
        game.run()


main = MenuWindow()
main.mainloop()
