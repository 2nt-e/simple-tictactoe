from better_print import *

class Game:
    def __init__(self, n=4):
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
        self.mode = "pvp"
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
         if contraditon == False and change in self.map.keys():
             self.map[change] = chance
             self.ocupation.append(change)
             self.turn += 1
             self.placements[f'r{change[0]}'].append(chance)
             self.placements[f'c{change[1]}'].append(chance)
             if change[0] == change[1]:
                 self.placements['d1'].append(chance)
             if int(change[0]) + int(change[1]) == 4:
                 self.placements['d2'].append(chance)
         else:
              print("invalid input!")

    def victory(self):
         for w in self.placements.values():
              if len(w) == self.n:
                   if (w[0] == w[1] == w[2]):
                        return w[0]

    def game_end(self):
        if len(self.ocupation) == 9:
            return "tie"
        elif self.victory() != None:
             return "victory"
        else:
            return False
    
    def oraganize(self):
        while self.game_end() == False:
            print('\n'*20)
            self.print_grid()
            # print(self.map, self.placements['c1']) # For debugging
            change = better.input(f"Where to put {self.symbols[self.check_chance()]} : ").strip()
            self.implement(change)
        else:
             print()
             messages = {
                  'tie': "Game ended with Tie.",
                  'victory': f"Game ended, Player {self.symbols[self.victory()]}  won!",
             }
             better.print(messages[self.game_end()])
    

obj = Game()
obj.oraganize()
