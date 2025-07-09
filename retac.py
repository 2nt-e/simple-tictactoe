import time
from better_print import *

# adding some imp varibles for furthur use.
default_structure = {
    "1" : "1️⃣",
    "2" : "2️⃣",
    "3" : "3️⃣",
    "4" : "4️⃣",
    "5" : "5️⃣",
    "6" : "6️⃣",
    "7" : "7️⃣",
    "8" : "8️⃣",
    "9" : "9️⃣",
}

turn = 1
ocupation = []
# end of variable.

def game():
    better.print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")  # Clear the console for better visibility
    while game_end() == False: # if game is still running.

        global turn, ocupation, default_structure
        print("\n")
        print_structure() # printing structre.

        cc = chance_check() # checking whose chance this is.
        change = better.input(f"Where to put {cc} : ").strip() # takling input fomr that player.
        contra = contraditon(change= change) # checking for contraditon

        if contra == False: # if no contraditon.
            default_structure[change] = cc # editing default structue.
            ocupation.append(int(change)) # adding occupation.
            turn = turn + 1 # incereaseing value for turn.
        # for contraditon.
        elif contra == "o": #
            better.print("That Place is already occupied!")
        elif contra == "uv" or "e":
            better.print("Please Enter a Valid Value!")
        # contraditon ends.


    if game_end() == "tie": # telling tie.
        better.print("")
        print_structure()
        better.print("Game Ended with a Tie!")
    elif game_end() == "hw": # telling hash won.
        better.print("")
        print_structure()
        better.print("⏺️ lost the game!") 
    elif game_end() == "cw": # telling circle won.
        better.print("")
        print_structure()
        better.print("#️⃣ lost the game!")
    else: # if something went wrong
        better.print("")
        print_structure()
        better.print("something wrong went!")



def print_structure(): # Function to print the structure as 3x3 grid.

    x = 1
    while x < 10:
        if x % 3 == 0:
            better.print(default_structure[f"{x}"], end="\n")
        else:
            better.print(default_structure[f"{x}"], end=" ")
        x += 1



def chance_check(): # function to check for chance.
    global turn 
    if turn in [1,3,5,7,9]: # checking for hash's chance.
        return "#️⃣" 
    elif turn in [2,4,6,8]: # checking for circle's chance.
        return "⏺️"


def contraditon(change): # function for checking for any kind of contrdicton.
    if change == "": # checking for empty spaces
        return "e" 
    elif change not in str([1,2,3,4,5,6,7,8,9]): # checking for unvalid value.
        return "uv" 
    elif change in str(ocupation): # checking for occupation.
        return "o" 
    else: # if there is no contraditon
        return False 

def game_end(): # function to check if game should still be running and how it will end.
    global default_structure, ocupation 

# all conditon for either hash or circle to win the game.

    r1h = ("#️⃣" ==  default_structure["1"] == default_structure["2"] == default_structure["3"])
    r2h = ("#️⃣" ==  default_structure["4"] == default_structure["5"] == default_structure["6"])
    r3h = ("#️⃣" ==  default_structure["7"] == default_structure["8"] == default_structure["9"])

    c1h = ("#️⃣" ==  default_structure["1"] == default_structure["4"] == default_structure["7"])
    c2h = ("#️⃣" ==  default_structure["2"] == default_structure["5"] == default_structure["8"])
    c3h = ("#️⃣" ==  default_structure["3"] == default_structure["6"] == default_structure["9"])

    d1h = ("#️⃣" ==  default_structure["1"] == default_structure["5"] == default_structure["9"])
    d2h = ("#️⃣" ==  default_structure["3"] == default_structure["5"] == default_structure["7"])


    r1c = ("⏺️" ==  default_structure["1"] == default_structure["2"] == default_structure["3"])
    r2c = ("⏺️" ==  default_structure["4"] == default_structure["5"] == default_structure["6"])
    r3c = ("⏺️" ==  default_structure["7"] == default_structure["8"] == default_structure["9"])

    c1c = ("⏺️" ==  default_structure["1"] == default_structure["4"] == default_structure["7"])
    c2c = ("⏺️" ==  default_structure["2"] == default_structure["5"] == default_structure["8"])
    c3c = ("⏺️" ==  default_structure["3"] == default_structure["6"] == default_structure["9"])

    d1c = ("⏺️" ==  default_structure["1"] == default_structure["5"] == default_structure["9"])
    d2c = ("⏺️" ==  default_structure["3"] == default_structure["5"] == default_structure["7"])

# condition ends.

    if ocupation == [1,2,3,4,5,6,7,8,9]: # checking if any free space is avalable to fill.
        return "tie" 
    elif r1h or r2h or r3h or c1h or c2h or c3h or d1h or d2h == True: # checking for hash's win.
        return "hw" 
    elif r1c or r2c or r3c or c1c or c2c or c3c or d1c or d2c == True: # checking for circle's win
        return "cw" 
    else:  # if Game has not ended yet.
        return False
        


game()