from better_print import *

class Game:
    def __init__(self):
        self.map = {
            "11" : "1️⃣",
            "12" : "2️⃣",
            "13" : "3️⃣",
            "21" : "4️⃣",
            "22" : "5️⃣",
            "23" : "6️⃣",
            "31" : "7️⃣",
            "32" : "8️⃣",
            "33" : "9️⃣",
            }
        self.turn = 1
        self.ocupation = []
        self.mode = "pvp"

        self.placements = {
             'r1' : [],
             'r2' : [],
             'r3' : [],
             'c1' : [],
             'c2' : [],
             'c3' : [],
             'd1' : [],
             'd2' : []
        }

        self.player_sylmbols = {
             'P1' : '⏺️',
             'P2' : '#️⃣',
             'ai' : '#️⃣'
        }

    def print_grid(self): # For printing structure
                for r in range(1, 4):
                    for c in range(1, 4):
                        print(self.map[f'{r}{c}'], end=" ")
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
             self.placements[f'r{change[0]}'] = chance
             self.placements[f'c{change[1]}'] = chance
             if change[0] == change[1]:
                 self.placements['d1'] = chance
             if int(change[0]) + int(change[1]) == 4:
                 self.placements['d2'] = chance
         else:
              print("invalid input!")

    def victory(self):
         for w in self.placements:
              if len(w) == 3:
                   if (w[0] == w[1] == w[2]):
                        return w[0]


    def game_end(self):
        if len(self.ocupation) == 9:
            return "tie"
        elif self.victory() == "P1" or self.victory() == "P2":
             return "victory"
        else:
            return False
    
    def oraganize(self):
        while self.game_end() == False:
            self.print_grid()
            change = better.input(f"Where to put {self.player_sylmbols[self.check_chance()]} : ").strip()
            self.implement(change)
        else:
             messages = {
                  'tie': "Game ended with Tie.",
                  'victory': f"Game ended, Player {self.player_sylmbols[self.victory()]} won!",
             }
             better.print(messages[self.game_end()])
    




obj = Game()
obj.oraganize()


# def game():
#     better.print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")  # Clear the console for better visibility
#     while game_end() == False: # if game is still running.

#         global turn, ocupation, default_structure
#         print("\n")
#         print_structure() # printing structre.

#         cc = chance_check() # checking whose chance this is.
#         change = better.input(f"Where to put {cc} : ").strip() # takling input fomr that player.
#         contra = contraditon(change= change) # checking for contraditon

#         if contra == False: # if no contraditon.
#             default_structure[change] = cc # editing default structue.
#             ocupation.append(int(change)) # adding occupation.
#             turn = turn + 1 # incereaseing value for turn.
#         # for contraditon.
#         elif contra == "o": #
#             better.print("That Place is already occupied!")
#         elif contra == "uv" or "e":
#             better.print("Please Enter a Valid Value!")
#         # contraditon ends.


#     if game_end() == "tie": # telling tie.
#         better.print("")
#         print_structure()
#         better.print("Game Ended with a Tie!")
#     elif game_end() == "hw": # telling hash won.
#         better.print("")
#         print_structure()
#         better.print("⏺️ lost the game!") 
#     elif game_end() == "cw": # telling circle won.
#         better.print("")
#         print_structure()
#         better.print("#️⃣ lost the game!")
#     else: # if something went wrong
#         better.print("")
#         print_structure()
#         better.print("something wrong went!")

# game()
