from better_print import *
import tkinter as tk
import winsound
import asyncio
from websockets.asyncio.client import connect
import json


def MainCode():


    class MainWindow(tk.Tk):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.geometry('485x500')
            self.title("TicTacToe")
            self.iconbitmap('resource/icon.ico')
            self.resizable(width=False, height=False)
            self.Mframe = None

        def change_frame(self, Nframe):
            if self.Mframe:
                self.Mframe.destroy()
            self.Mframe = Nframe
            self.Mframe.grid(row=0, column=0)


    class Core:
        def __init__(self):
            self.memory()
            self.Engine = None
            self.Client = None
            self.Game = None
            self.background_loop = None
        def memory(self):
            self.order = 3
            self.mode = 'offline'
            self.address = None
            self.room_code = None
            self.you = None

        def create_Instances(self):
            self.Engine = MainEngine()
            self.Client = ClientSide()
        def create_Game(self):
            self.Game = GameWindow(self.Window)
        def create_mainmenu(self):
            self.menu = MenuWindow(self.Window)
        def create_onlinemenu(self):
            self.Window.geometry('485x275')
            self.onlinemenu = OnlineWindow(self.Window)

        async def StartWindow(self):
            self.Window = MainWindow()
            self.create_mainmenu()
            Inventory.Window.change_frame(self.menu)
            self.Window.mainloop()


    class MainEngine:
        def __init__(self):
            # For testing.
            self.symbols = {'cornor': "🟦", 'void': "0️⃣", 
                            '1': "1️⃣", '2': "2️⃣", '3': "3️⃣", '4': "4️⃣", '5': "5️⃣", '6': "6️⃣", '7': "7️⃣", '8': "8️⃣", '9': "9️⃣", 
                            'P1' : '⏺️', 'P2' : '#️⃣', 'ai' : '#️⃣', None: "baka!"}
            self.map = {} # Maping for game grid.
            self.turn = 1 # For tracking Turns.
            self.ocupation = [] # For tracking Occupied in grid.
            self.placements = {'d1' : [], 'd2' : []} # For tracking palcements of markers in rows, columns, digonals.

        def run(self):
            # fetching stuff from Core.
            self.n = Inventory.order 
            self.ClientSide = Inventory.Client 
            self.mode = Inventory.mode 
            for r in range(1, self.n+1): # Constructing map.
                for c in range(1, self.n+1):
                    self.map[f'{r}{c}'] = 'void'
            for i in range(1, self.n+1): # Constructing placements.
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

        def check_chance(self): # checking for chance
            if self.turn%2 == 0: 
                return "P2"
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
        
        async def implement(self, change): #Implementing on every move
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
            if self.mode == 'online':
                await self.Onhand.push() 
                fetch = await self.Onhand.pull()
                self.map = fetch['map']
                self.ocupation = fetch['ocupation']
                self.placements = fetch['placements']
                self.turn += 1

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
        

    class ClientSide:
        def __init__(self):
            self.Data = {'State': None,
                         'GameData': None,
                         'room_code': None}
            self.websocket = None
        def run(self):
            self.engine = Inventory.Engine
            self.Data['room_code'] = Inventory.room_code
            self.you = Inventory.you
            future_connect = asyncio.run_coroutine_threadsafe(self.connect(Inventory.address), Inventory.background_loop)
            future_connect.add_done_callback(handle_result)
        async def connect(self, address):
            self.websocket = await connect(f"ws://{address}")
        async def disconnect(self):
            Tws = self.websocket
            if Tws:
                await Tws.send(json.dumps({'State': 'Disconnected'}))
                await Tws.close()

        async def CreateRoom(self):
            while not self.websocket:
                await asyncio.sleep(0.1)
            self.Data['State'] = 'create_room'
            await self.websocket.send(json.dumps(self.Data))
            respond = json.loads(await self.websocket.recv())
            print(respond)
            self.Data['State'] = respond['State']
            self.room_code = Inventory.room_code = respond['game_id']
        
        async def WaitJoin(self):
            # while not self.websocket:
            #     await asyncio.sleep(0.1)
            # while self.Data['State'] != 'room_ready':
            #     await asyncio.sleep(0.1)
            respond = json.loads(await self.websocket.recv())
            print(respond)
        
        async def JoinRoom(self):
            while not self.websocket:
                await asyncio.sleep(0.1)
            self.Data['State'] = 'join_room'
            await self.websocket.send(json.dumps(self.Data))
            respond = json.loads(await self.websocket.recv())
            print(respond)
            if respond['State'] == 'room_ready':
                self.Data['State'] = respond['State']

                
    class GameButton(tk.Button):
        def __init__(self, master=None, cid=[], **kwargs):
            self.cid = cid
            super().__init__(master, **kwargs)
            self.images = Inventory.GB_Images
            self.top = self.master.master.master
            self.engine = self.top.engine
            self.gamemodes = {'offline': self.OfflinePVP, 'online': self.OnlinePVP}
            self.configure(command=self.asynclick, image=self.images['0'], borderwidth=0, highlightthickness=0, bd=0)
        def asynclick(self):
            future_asynclick = asyncio.run_coroutine_threadsafe(self.gamemodes[self.top.engine.mode](), Inventory.background_loop)
            future_asynclick.add_done_callback(handle_result)
            
        async def OfflinePVP(self):
            if not self.engine.game_end():
                p = self.engine.check_chance()
                colors = {'P1': '#9C6C6C', 'P2': '#6C879C'}
                self.colors_name = {'P1': 'Red', 'P2': 'Blue', None: None}
                print(f"Player-{p} proceed at {self.cid}")
                self.configure(state=tk.DISABLED, image=self.images[p])
                await self.engine.implement(change=f'{self.cid[0]}{self.cid[1]}')
                self.top.backframe.configure(background=colors[self.engine.check_chance()])
                self.top.text.configure(background=colors[self.engine.check_chance()], foreground=self.colors_name[self.engine.check_chance()])
                self.top.txtvar.set(f"{self.colors_name[self.engine.check_chance()]}'s Turn!")
                self.engine.print_grid()
                winsound.PlaySound(r'resource\effect.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
            if self.engine.game_end():
                end = self.engine.game_end()
                messages = {
                    'tie': "Game ended with Tie.",
                    'victory': f"Game ended, {self.colors_name[self.engine.victory()]} won!",}
                better.print(messages[end])
                self.master.master.master.txtvar.set(messages[self.engine.game_end()])
                winsound.PlaySound(rf'resource\{end}.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
                self.top.backframe.configure(background='silver')
                self.top.text.configure(background='silver', foreground='white')
                self.top.disallCbutton()

        async def OnlinePVP(self):
            if not self.engine.game_end():
                p = self.engine.check_chance()
                if Inventory.you == 'P1':
                    colors = {'P1': '#9C6C6C', 'P2': '#6C879C'}
                    colors_name = {'P1': 'You', 'P2': 'They', None: None}
                else:
                    colors = {'P2': '#9C6C6C', 'P1': '#6C879C'}
                    colors_name = {'P1': 'They', 'P2': 'You', None: None}
                print(f"Player-{p} proceed at {self.cid}")
                self.configure(state=tk.DISABLED, image=self.images[p])
                await self.engine.implement(change=f'{self.cid[0]}{self.cid[1]}')
                self.top.backframe.configure(background=colors[self.engine.check_chance()])
                self.top.text.configure(background=colors[self.engine.check_chance()], foreground=colors_name[self.engine.check_chance()])
                self.top.txtvar.set(f"{colors_name[self.engine.check_chance()]}'s Turn!")
                self.engine.print_grid()
                winsound.PlaySound(r'resource\effect.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
            if self.engine.game_end():
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


    class GameWindow(tk.Frame):
        def __init__(self, master=None, *args, **kwargs):

            super().__init__(master, *args, **kwargs)
            Inventory.GB_Images = {'0': tk.PhotoImage(file='resource/white.png'),
                        'P1': tk.PhotoImage(file='resource/red.png'),
                        'P2': tk.PhotoImage(file='resource/blue.png')}
            self.backframe = tk.Frame(self, background='silver')
            self.backframe.grid(row=0, column=0)
            self.txtvar = tk.StringVar()
            self.txtvar.set("Simple TicTacToe")
            self.text = tk.Label(self.backframe, textvariable=self.txtvar, background='silver', font=("Franklin Gothic Heavy", 22, "bold"), foreground='white')
            self.text.grid(row=1, column=0, pady=10)
            self.gameframe = tk.Frame(self.backframe, border=1, borderwidth=5, relief="solid", background="#212124")
            self.gameframe.grid(row=2, column=0, padx=100, pady=50)

        def run(self):
            Inventory.Engine.run()
            self.n = Inventory.order
            size = self.n * 100 + 200
            self.master.geometry(f'{size}x{size - 20}')
            self.mode = Inventory.mode
            self.engine = Inventory.Engine
            for i in range(1, self.n+1):
                for j in range(1, self.n+1):
                    GameButton(self.gameframe, cid=[i, j]).grid(row=i, column=j, padx=1, pady=1)
            self.engine.print_grid()
            
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
            Inventory.order = int(self.gid[0])
            for button in self.master.winfo_children():
                if str(button).split('.')[-1][1] == 'g':
                    button.configure(state=tk.NORMAL)
            self.configure(state=tk.DISABLED)


    class MenuButton(tk.Button):
        def __init__(self, master=None, sideffect=None, **kwargs):
            super().__init__(master, **kwargs)
            self.sideffect = sideffect
            self.configure(command=self.asyncEffect)
        def asyncEffect(self):
            f= asyncio.run_coroutine_threadsafe(self.master.effects[self.sideffect](), Inventory.background_loop)
            f.add_done_callback(handle_result)


    class MenuWindow(tk.Frame):
        def __init__(self, master=None, *args, **kwargs):
            self.n = 3
            super().__init__(master, *args, **kwargs)
            self.configure(background='gray')
            self.effects = {'start_offline': self.start_offline,
                            'online_menu': self.start_online_menu}
            tk.Label(self, text="Select Grid Size & Game Mode!", font=("Franklin Gothic Heavy", 22, "bold"), background='gray').grid(row=1, column=1, padx=20)
            GridButton(self, gid='3x3').grid(column=1, row=2, pady=20)
            GridButton(self, gid='4x4').grid(column=1, row=3, pady=20)
            MenuButton(self, text="Start Game In Offline Mode", sideffect='start_offline').grid(row=4,column=1, pady=20)
            MenuButton(self, text='Start Game In Online Mode', sideffect='online_menu').grid(row=5,column=1, pady=20)

        async def start_offline(self):
            Inventory.mode = 'offline'
            Inventory.create_Game()
            Inventory.Game.run()
            Inventory.Window.change_frame(Inventory.Game)
        async def start_online_menu(self):
            Inventory.mode = 'online'
            Inventory.create_onlinemenu()
            Inventory.Window.change_frame(Inventory.onlinemenu)


    class OnlineWindow(tk.Frame):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.configure(background='gray')
            self.effects = {'join_room': self.join_room, 
                            'create_room': self.create_room,
                            'back': self.back}
            MenuButton(self, text='back', sideffect='back').grid(row=0, column=1, sticky="nw")
            tk.Label(self, text="Create or Join Room in Server!", font=("Franklin Gothic Heavy", 22, "bold"), background='gray').grid(row=1, column=1, padx=20)
            self.address = tk.StringVar()
            tk.Label(self, text="Host:").grid(row=2,column=1, pady=5)
            tk.Entry(self, textvariable=self.address).grid(row=3,column=1, pady=1)
            MenuButton(self, text="Create a Room", sideffect='create_room').grid(row=4,column=1, pady=5)
            self.room = tk.StringVar()
            tk.Label(self, text="Room ID:").grid(row=5,column=1, pady=5)
            tk.Entry(self, textvariable=self.room).grid(row=6,column=1, pady=1)
            MenuButton(self, text="Or join a Room", sideffect='join_room').grid(row=7,column=1, pady=5)

        async def create_room(self):
            Inventory.address = self.address.get()
            Inventory.you = 'P1'
            Inventory.Client.run()
            await Inventory.Client.CreateRoom()
            # while Inventory.room_code == None:
            #     await asyncio.sleep(0.1)
            CMessage = MessageWindow(Inventory.Window, message=f"Room Created! Code: {Inventory.room_code}")
            Inventory.Window.change_frame(CMessage)
            await Inventory.Client.WaitJoin()
        async def join_room(self):
            Inventory.address = self.address.get()
            Inventory.room_code = self.room.get()
            Inventory.you = 'P2'
            Inventory.Client.run()
            await Inventory.Client.JoinRoom()
            self.master.destroy()
        async def back(self):
            Inventory.create_mainmenu()
            Inventory.Window.geometry('485x500')
            Inventory.Window.change_frame(Inventory.menu)


    class MessageWindow(tk.Frame):
        def __init__(self, master, message, *args, **kwags):
            super().__init__(master, *args, **kwags)
            self.master.geometry('1000x100')
            self.configure(background='gray')
            self.MLabel = tk.Label(self, text=message, background='gray', font=("Franklin Gothic Heavy", 22, "bold"))
            self.MLabel.grid(row=0, column=0)



    def handle_result(future):
        try:
            future.result()
        except Exception as e:
            print(f"Exception in Thread_A: {e}")
            import traceback
            traceback.print_exc()
    
    Inventory = Core()
    Inventory.create_Instances()
    mainloop = asyncio.new_event_loop()
    mainloop.set_debug(True)
    asyncio.set_event_loop(mainloop)
    Inventory.background_loop = asyncio.new_event_loop()
    Inventory.background_loop.set_debug(True)
    mainloop.run_in_executor(None, Inventory.background_loop.run_forever)
    mainloop.run_until_complete(Inventory.StartWindow())
    asyncio.run_coroutine_threadsafe(Inventory.Client.disconnect(), Inventory.background_loop)



if __name__ == "__main__":
    MainCode()