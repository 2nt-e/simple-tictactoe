from better_print import *
import tkinter as tk
import os
import sys
try:
    import playsound
except:
    os.system(f'"{sys.executable}" -m pip install playsound')
    import playsound
try:
    import winsound
    soundplayer = 'winsound'
except:
    soundplayer = 'playsound'
import asyncio
try:
    from websockets.asyncio.client import connect
except:
    os.system(f'"{sys.executable}" -m pip  install websockets')
    from websockets.asyncio.client import connect
import json


def MainCode():
    class Core:
        def __init__(self):
            self.create_memory()
            self.Window = None
            self.menu = None
            self.onlinemenu = None
            self.Engine = None
            self.WSClient = None
            self.Game = None
            self.gui_loop = None
            self.background_loop = None
        def create_memory(self):
            self.order = 3
            self.mode = 'offline'
            self.address = None
            self.room_code = None
            self.you = None
        
        def background_music(self):
            import playsound
            while True:
                playsound.playsound(r'resource\bg_music.wav')

        def create_loops(self):
            self.gui_loop = asyncio.new_event_loop()
            self.gui_loop.set_debug(True)
            asyncio.set_event_loop(self.gui_loop)
            self.background_loop = asyncio.new_event_loop()
            self.background_loop.set_debug(True)
            self.gui_loop.run_in_executor(None, self.background_loop.run_forever)
            self.gui_loop.run_in_executor(None, self.background_music)
            if soundplayer != 'winsound':
                self.sounds_loop = asyncio.new_event_loop()
                self.sounds_loop.set_debug(True)
                self.gui_loop.run_in_executor(None, self.sounds_loop.run_forever)
        def create_GEngine(self):
            self.Engine = ArialEngine()
        def create_WSClient(self):
            self.WSClient = WSClient()
        def create_Game(self):
            self.Game = GameWindow(self.Window)
        def create_mainmenu(self):
            self.Window.geometry('485x500')
            self.menu = MenuWindow(self.Window)
        def create_onlinemenu(self):
            self.Window.geometry('485x275')
            self.onlinemenu = OnlineWindow(self.Window)

        async def StartWindow(self):
            self.Window = MainWindow()
            self.create_mainmenu()
            Inventory.Window.change_frame(self.menu)
            self.Window.mainloop()


    class MainWindow(tk.Tk):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.geometry('50x50')
            self.title("TicTacToe")
            self.iconbitmap('resource/icon.ico')
            self.resizable(width=False, height=False)
            self.Mframe = None

        def change_frame(self, Nframe):
            if self.Mframe:
                self.Mframe.destroy()
            self.Mframe = Nframe
            self.Mframe.grid(row=0, column=0)


    class ArialEngine:
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
            self.WSClient = Inventory.WSClient 
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


    class WSClient:
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
            self.Data['room_code'] = Inventory.room_code = respond['game_id']
        
        async def WaitJoin(self):
            while self.Data['State'] != 'room_created':
                await asyncio.sleep(0.1)
            respond = json.loads(await self.websocket.recv())
            print(respond)
        
        async def JoinRoom(self):
            while not self.websocket:
                await asyncio.sleep(0.1)
            self.Data['State'] = 'join_room'
            await self.websocket.send(json.dumps(self.Data))
            respond = json.loads(await self.websocket.recv())
            print(respond)
            if respond['State'] == 'room_created':
                self.Data['State'] = respond['State']

        async def Game_send(self, change):
            self.Data['State'] = 'game_send'
            self.Data['change'] = change
            await self.websocket.send(json.dumps(self.Data))
        async def Game_recv(self):
            respond = json.loads(await self.websocket.recv())
            # print(respond)
            return respond['change']

                
    class GameWindow(tk.Frame):
        def __init__(self, master=None, *args, **kwargs):

            super().__init__(master, *args, **kwargs)
            Inventory.GB_Images = {'0': tk.PhotoImage(file='resource/white.png'),
                        'P1': tk.PhotoImage(file='resource/red.png'),
                        'P2': tk.PhotoImage(file='resource/blue.png')}
            self.player_colors = {'P1': '#9C6C6C', 'P2': '#6C879C'}
            self.colors_name = {'P1': 'red', 'P2': 'blue'}
            self.backframe = tk.Frame(self, background='silver')
            self.backframe.grid(row=0, column=0)
            self.txtvar = tk.StringVar()
            self.txtvar.set("Simple TicTacToe")
            self.text = tk.Label(self.backframe, textvariable=self.txtvar, background='silver', font=("Franklin Gothic Heavy", 22, "bold"), foreground='white')
            self.text.grid(row=1, column=0, pady=10)
            self.gameframe = tk.Frame(self.backframe, border=1, borderwidth=5, relief="solid", background="#212124")
            self.gameframe.grid(row=3, column=0, padx=100, pady=50)
            self.gamemodes = {'offline': self.OfflineClick,
                               'online': self.OnlineClick
                               }
            self.EnabledGB = {}

        def GameButton(self):
            Button = tk.Button(self.gameframe)
            Button.configure(command=lambda:self.GBclick(Button), image=Inventory.GB_Images['0'], borderwidth=0, highlightthickness=0, bd=0)
            return Button
        def GBclick(self, Button):
            future_asynclick = asyncio.run_coroutine_threadsafe(self.gamemodes[self.engine.mode](Button), Inventory.background_loop)
            future_asynclick.add_done_callback(handle_result)

        def run(self):
            Inventory.create_GEngine()
            Inventory.Engine.run()
            self.n = Inventory.order
            size = self.n * 100 + 200
            self.master.geometry(f'{size}x{size - 20}')
            self.mode = Inventory.mode
            self.engine = Inventory.Engine
            for i in range(1, self.n+1):
                for j in range(1, self.n+1):
                    Cid = [i, j]
                    GB = self.GameButton()
                    GB.grid(row=i, column=j, padx=1, pady=1)
                    self.EnabledGB[f'{Cid[0]}{Cid[1]}'] = GB
            # self.engine.print_grid()
            if self.mode == 'online':
                if Inventory.you == 'P2':
                    self.player_names = {'P1': 'Opponent\'s ', 'P2': 'Your', None: None}
                    f= asyncio.run_coroutine_threadsafe(self.WaitClick(), Inventory.background_loop)
                    f.add_done_callback(handle_result)
                elif Inventory.you == 'P1':
                    self.player_names = {'P2': 'Opponent\'s ', 'P1': 'Your', None: None}
                self.change_colors_texts_after('P2')
            elif self.mode == 'offline':
                self.player_names = {'P1': 'Red\'s ', 'P2': 'Blue\'s', None: None}
        def disable_all_Gbuttons(self):
            for button in self.gameframe.winfo_children():
                button.configure(state=tk.DISABLED)
        def enable_enabled_Gbuttons(self):
            for button in self.EnabledGB.values():
                button.configure(state=tk.NORMAL)

        async def OfflineClick(self, Gbutton):
            chance = self.engine.check_chance()
            # print(f"Player-{p} proceed at {Gbutton.cid}")
            cid = self.cid_of_button(Gbutton)
            Gbutton.configure(state=tk.DISABLED, image=Inventory.GB_Images[chance])
            self.EnabledGB.pop(f'{cid[0]}{cid[1]}')
            await self.engine.implement(change=f'{cid[0]}{cid[1]}')
            self.change_colors_texts_after(chance)
            # self.engine.print_grid()
            if soundplayer == 'winsound':
                winsound.PlaySound(r'resource\effect.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
            else:
                asyncio.run_coroutine_threadsafe(Splayer(lambda:playsound.playsound(r'resource\effect.wav')), Inventory.sounds_loop)
            end = self.engine.game_end()
            if end:
                messages = {
                    'tie': "Game ended with Tie.",
                    'victory': f"Game ended, {self.player_names[self.engine.victory()]} Victory!",}
                self.txtvar.set(messages[end])
                if soundplayer == 'winsound':
                    winsound.PlaySound(rf'resource\{end}.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
                else:
                    asyncio.run_coroutine_threadsafe(Splayer(lambda:playsound.playsound(rf'resource\{end}.wav')), Inventory.sounds_loop)
                self.backframe.configure(background='silver')
                self.text.configure(background='silver', foreground='white')
                self.disable_all_Gbuttons() 
                ExitButton = tk.Button(self.backframe, text="<==| Exit to Menu", command=self.restart_and_menu)
                ExitButton.grid(row=2, column=0, pady=10)
            return cid
        async def OnlineClick(self, Gbutton):
            cid = await self.OfflineClick(Gbutton)
            await Inventory.WSClient.Game_send(cid)
            if not self.engine.game_end():
                await self.WaitClick()
        async def WaitClick(self):
            self.disable_all_Gbuttons()
            Cid = await Inventory.WSClient.Game_recv()
            await self.OfflineClick(self.EnabledGB[f'{Cid[0]}{Cid[1]}'])
            self.enable_enabled_Gbuttons()
        
        def cid_of_button(self, button):
            for _ in self.EnabledGB:
                if self.EnabledGB[_] == button:
                    return _
        def change_colors_texts_after(self, chance):
            if chance == 'P1':
                now_turn = 'P2'
            elif chance == 'P2':
                now_turn = 'P1'
            self.backframe.configure(background=self.player_colors[now_turn])
            self.text.configure(background=self.player_colors[now_turn], foreground=self.colors_name[now_turn])
            self.txtvar.set(f"{self.player_names[now_turn]} Turn!")
        def restart_and_menu(self):
                Inventory.create_memory()
                Inventory.create_mainmenu()
                Inventory.Window.change_frame(Inventory.menu)


    class GridButton(tk.Button):
        def __init__(self, master=None, gid='3x3', **kwargs):
            self.gid = gid
            super().__init__(master, **kwargs)
            self.image =tk.PhotoImage(file=f'resource/{self.gid}.png')
            self.configure(command=self.Toggle, image=self.image, borderwidth=0, highlightthickness=0, bd=0)
        
        def Toggle(self):
            if soundplayer == 'winsound':
                winsound.PlaySound(rf'resource\tick.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
            else:
                asyncio.run_coroutine_threadsafe(Splayer(lambda:playsound.playsound(rf'resource\tick.wav')), Inventory.sounds_loop)
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
            Inventory.create_WSClient()
            Inventory.WSClient.run()
            await Inventory.WSClient.CreateRoom()
            CMessage = MessageWindow(Inventory.Window, message=f"Room Created! Code: {Inventory.room_code}")
            Inventory.Window.change_frame(CMessage)
            print('waiting started')
            await Inventory.WSClient.WaitJoin()
            print('waiting ended')
            Inventory.create_Game()
            Inventory.Game.run()
            Inventory.Window.change_frame(Inventory.Game)
        async def join_room(self):
            Inventory.address = self.address.get()
            Inventory.room_code = self.room.get()
            Inventory.you = 'P2'
            Inventory.create_WSClient()
            Inventory.WSClient.run()
            await Inventory.WSClient.JoinRoom()
            Inventory.create_Game()
            Inventory.Game.run()
            Inventory.Window.change_frame(Inventory.Game)
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

    async def Splayer(sound):
        sound()


    Inventory = Core()
    # Inventory.create_Instances()
    Inventory.create_loops()
    Inventory.gui_loop.run_until_complete(Inventory.StartWindow())
    if Inventory.WSClient:
        f= asyncio.run_coroutine_threadsafe(Inventory.WSClient.disconnect(), Inventory.background_loop)
        f.add_done_callback(handle_result)
 


if __name__ == "__main__":
    MainCode()