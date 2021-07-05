import tkinter as tk
from functools import partial

root = tk.Tk()
root.attributes("-fullscreen", True)
root.title("Chess")
root.iconbitmap("Images/icon.ico")

buttons : list[dict] = list()

selected = int()


def checkForCheck(movement):
    return movement


def getMovement(piece : str="pawn", n : int=0, oppMove : bool=False, playerCol : str = "black"):
    global buttons
    if playerCol == "black":
        oppCol = "white"
    else:
        oppCol = "black"
    rightEdges = [(i+1)*7+i for i in range(8)]
    leftEdges = [i*8 for i in range(8)]
    topEdges = [i for i in range(8)]
    lowerEdges = [i for i in range(56, 64)]
    movement : list[int] = list()
    if piece == "pawn":
        if oppMove:
            if buttons[n+8]["piece"] == "none" and not n in lowerEdges:
                movement.append(n+8)
            if buttons[n+7]["piece"] != "none" and buttons[n+7]["piece"].split("_")[1] != oppCol and not n in leftEdges:
                movement.append(n+7)
            if buttons[n+9]["piece"] != "none" and buttons[n+9]["piece"].split("_")[1] != oppCol and not n in rightEdges:
                movement.append(n+9)
        else:
            if buttons[n-8]["piece"] == "none" and not n in topEdges:
                movement.append(n-8)
            if buttons[n-7]["piece"] != "none" and buttons[n-7]["piece"].split("_")[1] != playerCol and not n in rightEdges:
                movement.append(n-7)
            if buttons[n-9]["piece"] != "none" and buttons[n-9]["piece"].split("_")[1] != playerCol and not n in leftEdges:
                movement.append(n-9)
    if piece == "king":
        surrounding : list[int] = list()
        if not n in topEdges:
            surrounding.append(n-8)
            if not n in rightEdges:
                surrounding.append(n-7)
            if not n in leftEdges:
                surrounding.append(n-9)
        if not n in rightEdges:
            surrounding.append(n+1)
        if not n in leftEdges:
            surrounding.append(n-1)
        if not n in lowerEdges:
            surrounding.append(n+8)
            if not n in rightEdges:
                surrounding.append(n+9)
            if not n in leftEdges:
                surrounding.append(n+7)
        
        #print(surrounding)

        if oppMove:
            for pos in surrounding:
                if buttons[pos]["piece"].split("_")[1] != oppCol:
                    movement.append(pos)
        else:
            for pos in surrounding:
                if buttons[pos]["piece"].split("_")[1] != playerCol:
                    movement.append(pos)
        

    return movement



def getpng(file, col):
    return "Images/{0}_{1}.png".format(file, col)


def buttonClick(n, playerCol):
    global buttons
    print(n)
    info = buttons[n]
    movement = checkForCheck(getMovement(piece=info["piece"].split("_")[0], n=n, oppMove=False, playerCol=playerCol))



def init(col):
    global buttons
    for button in buttons:
        button["Button"].destroy()
    

    if col == "light grey":
        oppCol = "black"
        playerCol = "white"
    else:
        oppCol = "white"
        playerCol = "black"

    buttons = list()
    buttonsize = 50
    line = 9
    y = 1

    images = [getpng("rook", oppCol), getpng("knight", oppCol), getpng("bishop", oppCol), getpng("queen", oppCol), getpng("king", oppCol), getpng("bishop", oppCol), getpng("knight", oppCol), getpng("rook", oppCol)]

    pieces = [f"rook_{oppCol}", f"knight_{oppCol}", f"bishop_{oppCol}", f"queen_{oppCol}", f"king_{oppCol}", f"bishop_{oppCol}", f"knight_{oppCol}", f"rook_{oppCol}"]

    for _ in range(8):
        images.append(getpng("pawn", oppCol))
        pieces.append(f"pawn_{oppCol}")
    
    for _ in range(32):
        images.append("")
        pieces.append("none_none")
    
    for _ in range(8):
        images.append(getpng("pawn", playerCol))
        pieces.append(f"pawn_{playerCol}")

    images += [getpng("rook", playerCol), getpng("knight", playerCol), getpng("bishop", playerCol), getpng("queen", playerCol), getpng("king", playerCol), getpng("bishop", playerCol), getpng("knight", playerCol), getpng("rook", playerCol)]
    pieces += [f"rook_{playerCol}", f"knight_{playerCol}", f"bishop_{playerCol}", f"queen_{playerCol}", f"king_{playerCol}", f"bishop_{playerCol}", f"knight_{playerCol}", f"rook_{playerCol}"]


    for i in range(64):
        if line == 9:
            line = 1
            y += 1
        else:
            if col == "light grey":
                col = "grey"
            else:
                col = "light grey"
        try:
            photo = tk.PhotoImage(file=images[i])
        except Exception:
            photo = ""
        buttons.append({"Button": tk.Button(root, bg=col, command=partial(buttonClick, i, playerCol)), "piece": pieces[i]})
        buttons[i]["Button"].place(x=line*buttonsize+400, y=y*buttonsize+40, height=buttonsize, width=buttonsize)
        buttons[i]["Button"].config(image=photo)
        buttons[i]["Button"].image = photo
        line += 1

    


tk.Button(root, text="Black", fg="white", bg="black", command=partial(init, "grey")).place(x=500, y=40, height=50, width=50)
tk.Button(root, text="White", fg="black", bg="white", command=partial(init, "light grey")).place(x=600, y=40, height=50, width=50)

tk.Button(fg="red", bg="white", text="Exit", command=root.destroy).place(x=10, y=10, height=40, width=50)

root.mainloop()