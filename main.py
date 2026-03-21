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
            self.turn += 1
            return self.mode 
        else: 
            self.turn += 1
            return "P1"
    
    def contraditon(self, change):
        try: 
            if change not in self.ocupation:
                return False
            else:
                return "already_occupied"
        except:
            return "invalid_input"
    
    def game_end(self):
        ...


obj = Game()
obj.print()


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


# def game_end(): # function to check if game should still be running and how it will end.
#     global default_structure, ocupation 

# # all conditon for either hash or circle to win the game.

#     r1h = ("#️⃣" ==  default_structure["1"] == default_structure["2"] == default_structure["3"])
#     r2h = ("#️⃣" ==  default_structure["4"] == default_structure["5"] == default_structure["6"])
#     r3h = ("#️⃣" ==  default_structure["7"] == default_structure["8"] == default_structure["9"])

#     c1h = ("#️⃣" ==  default_structure["1"] == default_structure["4"] == default_structure["7"])
#     c2h = ("#️⃣" ==  default_structure["2"] == default_structure["5"] == default_structure["8"])
#     c3h = ("#️⃣" ==  default_structure["3"] == default_structure["6"] == default_structure["9"])

#     d1h = ("#️⃣" ==  default_structure["1"] == default_structure["5"] == default_structure["9"])
#     d2h = ("#️⃣" ==  default_structure["3"] == default_structure["5"] == default_structure["7"])


#     r1c = ("⏺️" ==  default_structure["1"] == default_structure["2"] == default_structure["3"])
#     r2c = ("⏺️" ==  default_structure["4"] == default_structure["5"] == default_structure["6"])
#     r3c = ("⏺️" ==  default_structure["7"] == default_structure["8"] == default_structure["9"])

#     c1c = ("⏺️" ==  default_structure["1"] == default_structure["4"] == default_structure["7"])
#     c2c = ("⏺️" ==  default_structure["2"] == default_structure["5"] == default_structure["8"])
#     c3c = ("⏺️" ==  default_structure["3"] == default_structure["6"] == default_structure["9"])

#     d1c = ("⏺️" ==  default_structure["1"] == default_structure["5"] == default_structure["9"])
#     d2c = ("⏺️" ==  default_structure["3"] == default_structure["5"] == default_structure["7"])

# # condition ends.
 
#     if r1h or r2h or r3h or c1h or c2h or c3h or d1h or d2h == True: # checking for hash's win.
#         return "hw" 
#     elif r1c or r2c or r3c or c1c or c2c or c3c or d1c or d2c == True: # checking for circle's win
#         return "cw" 
#     elif chance_check() == None: # checking if any free space is avalable to fill.
#         return "tie"
#     else:  # if Game has not ended yet.
#         return False
        


# game()
