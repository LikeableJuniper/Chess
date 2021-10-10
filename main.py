import tkinter as tk
from functools import partial

open("log.log", "w").close()

root = tk.Tk()
root.attributes("-fullscreen", True)
root.title("Chess")
root.iconbitmap("Images/icon.ico")

buttons : list[dict] = list()

selected = None

points = int()
pointsLabel : tk.Label = None

promoter : tk.Toplevel = None


#? is tk.Button command, so has to be func, even if so short
def promote(piece : str = "queen", n : int = 0, playerCol : str = "black"):
    global promoter, buttons
    buttons[n]["piece"] = piece + "_" + playerCol
    render()
    promoter.destroy()
    promoter = None


def render():
    global buttons
    for i in range(len(buttons)):
        try:
            photo = tk.PhotoImage(file=getpng(buttons[i]["piece"].split("_")[0], buttons[i]["piece"].split("_")[1]))
        except:
            photo = ""
        buttons[i]["Button"].config(image=photo)
        buttons[i]["Button"].image = photo


def isCheck(field : list, playerCol):

    compField : list[dict] = list()

    for elem in field:
        compField.append({"piece": elem})

    check = False
    if playerCol == "black":
        oppCol = "white"
    else:
        oppCol = "black"
    for piece in range(len(field)):
        if field[piece] == f"king_{playerCol}":
            for testPos in range(len(field)):
                if field[testPos].split("_")[1] == playerCol:
                    continue # continue if piece is under players control
                if piece in getMovement(field[testPos].split("_")[0], testPos, True, playerCol, compField):
                    check = True

    return check


def checkForCheck(n : int, movement : list[int], playerCol : str = "black"):
    global buttons

    #clone the buttons list to simulate moves
    simul = [elem["piece"] for elem in buttons]

    for pos in movement:
        sim = simul
        pieceInfo = sim[n]
        sim[n] = "none_none"
        sim[pos] = pieceInfo
        if isCheck(sim, playerCol):
            movement.remove(pos)

        


    return movement


def getMovement(piece : str="pawn", n : int=None, oppMove : bool=False, playerCol : str = "black", buttons : list = None):
    if playerCol == "black":
        oppCol = "white"
    else:
        oppCol = "black"
    rightEdges = [(i+1)*7+i for i in range(8)]
    leftEdges = [i*8 for i in range(8)]
    topEdges = [i for i in range(8)]
    lowerEdges = [i for i in range(56, 64)]
    upperPawnLine = range(8, 16)
    lowerPawnLine = range(48, 56)
    movement : list[int] = list()
    if True:
        if piece == "pawn":
            if oppMove:
                if buttons[n+8]["piece"] == "none_none" and not n in lowerEdges:
                    movement.append(n+8)
                    if n in upperPawnLine and buttons[n+16]["piece"].split("_")[1] != oppCol:
                        movement.append(n+16)
                if buttons[n+7]["piece"] != "none_none" and buttons[n+7]["piece"].split("_")[1] != oppCol and not n in leftEdges:
                    movement.append(n+7)
                if buttons[n+9]["piece"] != "none_none" and buttons[n+9]["piece"].split("_")[1] != oppCol and not n in rightEdges:
                    movement.append(n+9)
            else:
                if buttons[n-8]["piece"] == "none_none" and not n in topEdges:
                    movement.append(n-8)
                    if n in lowerPawnLine and buttons[n-16]["piece"].split("_")[1] != playerCol:
                        movement.append(n-16)
                if buttons[n-7]["piece"] != "none_none" and buttons[n-7]["piece"].split("_")[1] != playerCol and not n in rightEdges:
                    movement.append(n-7)
                if buttons[n-9]["piece"] != "none_none" and buttons[n-9]["piece"].split("_")[1] != playerCol and not n in leftEdges:
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

            if oppMove:
                for pos in surrounding:
                    if buttons[pos]["piece"].split("_")[1] != oppCol:
                        movement.append(pos)
            else:
                for pos in surrounding:
                    if buttons[pos]["piece"].split("_")[1] != playerCol:
                        movement.append(pos)
        
        if piece == "knight":
            secondRightLine = [x-1 for x in rightEdges]
            secondLeftLine = [x+1 for x in leftEdges]
            secondTopLine = [x+8 for x in topEdges]
            secondLowerLine = [x-8 for x in lowerEdges]
            if not n in secondRightLine and not n in rightEdges and not n in topEdges and buttons[n-6]["piece"].split("_")[1] != playerCol:
                movement.append(n-6)
            if not n in secondTopLine and not n in topEdges and not n in rightEdges and buttons[n-15]["piece"].split("_")[1] != playerCol:
                movement.append(n-15)
            if not n in secondTopLine and not n in topEdges and not n in leftEdges and buttons[n-17]["piece"].split("_")[1] != playerCol:
                movement.append(n-17)
            if not n in secondLeftLine and not n in leftEdges and not n in topEdges and buttons[n-10]["piece"].split("_")[1] != playerCol:
                movement.append(n-10)
            if not n in secondLeftLine and not n in leftEdges and not n in lowerEdges and buttons[n+6]["piece"].split("_")[1] != playerCol:
                movement.append(n+6)
            if not n in secondLowerLine and not n in lowerEdges and not n in leftEdges and buttons[n+15]["piece"].split("_")[1] != playerCol:
                movement.append(n+15)
            if not n in secondLowerLine and not n in lowerEdges and not n in rightEdges and buttons[n+17]["piece"].split("_")[1] != playerCol:
                movement.append(n+17)
            if not n in secondRightLine and not n in rightEdges and not n in lowerEdges and buttons[n+10]["piece"].split("_")[1] != playerCol:
                movement.append(n+10) 
        
        if piece == "rook":
            if not oppMove:
                testInd = int()
                for i in range(1, 9):
                    if n in rightEdges:
                        break
                    testInd = n+i
                    if testInd in rightEdges and buttons[testInd]["piece"].split("_")[1] != playerCol:
                        movement.append(testInd)
                        break
                    if buttons[testInd]["piece"] == "none_none":
                        movement.append(n+i)
                        continue
                    elif buttons[testInd]["piece"].split("_")[1] != playerCol:
                        movement.append(testInd)
                        break
                    else:
                        break
                for i in [x*8 for x in range(1, 9)]:
                    if n in topEdges:
                        break
                    testInd = n-i
                    if testInd in topEdges and buttons[testInd]["piece"].split("_")[1] != playerCol:
                        movement.append(testInd)
                        break
                    if buttons[testInd]["piece"] == "none_none":
                        movement.append(testInd)
                        continue
                    elif buttons[testInd]["piece"].split("_")[1] != playerCol:
                        movement.append(testInd)
                        break
                    else:
                        break
                for i in range(1, 9):
                    if n in leftEdges:
                        break
                    testInd = n-i
                    if testInd in leftEdges and buttons[testInd]["piece"].split("_")[1] != playerCol:
                        movement.append(testInd)
                        break
                    if buttons[testInd]["piece"] == "none_none":
                        movement.append(testInd)
                        continue
                    elif buttons[testInd]["piece"].split("_")[1] != playerCol:
                        movement.append(testInd)
                        break
                    else:
                        break
                for i in [x*8 for x in range(1, 9)]:
                    if n in lowerEdges:
                        break
                    testInd = n+i
                    if testInd in lowerEdges and buttons[testInd]["piece"].split("_")[1] != playerCol:
                        movement.append(testInd)
                        break
                    if buttons[testInd]["piece"] == "none_none":
                        movement.append(testInd)
                        continue
                    elif buttons[testInd]["piece"].split("_")[1] != playerCol:
                        movement.append(testInd)
                        break
                    else:
                        break
            else:
                testInd = int()
                for i in range(1, 9):
                    if n in rightEdges:
                        break
                    testInd = n+i
                    if testInd in rightEdges and buttons[testInd]["piece"].split("_")[1] != playerCol:
                        movement.append(testInd)
                        break
                    if buttons[testInd]["piece"] == "none_none":
                        movement.append(n+i)
                        continue
                    elif buttons[testInd]["piece"].split("_")[1] != oppCol:
                        movement.append(testInd)
                        break
                    else:
                        break
                for i in [x*8 for x in range(1, 9)]:
                    if n in topEdges:
                        break
                    testInd = n-i
                    if testInd in topEdges and buttons[testInd]["piece"].split("_")[1] != playerCol:
                        movement.append(testInd)
                        break
                    if buttons[testInd]["piece"] == "none_none":
                        movement.append(testInd)
                        continue
                    elif buttons[testInd]["piece"].split("_")[1] != oppCol:
                        movement.append(testInd)
                        break
                    else:
                        break
                for i in range(1, 9):
                    if n in leftEdges:
                        break
                    testInd = n-i
                    if testInd in leftEdges and buttons[testInd]["piece"].split("_")[1] != playerCol:
                        movement.append(testInd)
                        break
                    if buttons[testInd]["piece"] == "none_none":
                        movement.append(testInd)
                        continue
                    elif buttons[testInd]["piece"].split("_")[1] != oppCol:
                        movement.append(testInd)
                        break
                    else:
                        break
                for i in [x*8 for x in range(1, 9)]:
                    if n in lowerEdges:
                        break
                    testInd = n+i
                    if testInd in lowerEdges and buttons[testInd]["piece"].split("_")[1] != playerCol:
                        movement.append(testInd)
                        break
                    if buttons[testInd]["piece"] == "none_none":
                        movement.append(testInd)
                        continue
                    elif buttons[testInd]["piece"].split("_")[1] != oppCol:
                        movement.append(testInd)
                        break
                    else:
                        break    
        
        if piece == "bishop":
            if not oppMove:
                testInd = int()
                y = 1
                for i in [x*8 for x in range(1, 9)]:
                    if n in topEdges or n in rightEdges:
                        break
                    testInd = n-i+y
                    if (testInd in topEdges or testInd in rightEdges) and buttons[testInd]["piece"].split("_")[1] != playerCol:
                        movement.append(testInd)
                        break
                    if buttons[testInd]["piece"] == "none_none":
                        movement.append(testInd)
                    elif buttons[testInd]["piece"].split("_")[1] != playerCol:
                        movement.append(testInd)
                        break
                    else:
                        break

                    y += 1
                y = 1
                for i in [x*8 for x in range(1, 9)]:
                    if n in topEdges or n in leftEdges:
                        break
                    testInd = n-i-y
                    if (testInd in topEdges or testInd in leftEdges) and buttons[testInd]["piece"].split("_")[1] != playerCol:
                        movement.append(testInd)
                        break
                    if buttons[testInd]["piece"] == "none_none":
                        movement.append(testInd)
                    elif buttons[testInd]["piece"].split("_")[1] != playerCol:
                        movement.append(testInd)
                        break
                    else:
                        break

                    y += 1
                y = 1
                for i in [x*8 for x in range(1, 9)]:
                    if n in lowerEdges or n in leftEdges:
                        break
                    testInd = n+i-y
                    if (testInd in lowerEdges or testInd in leftEdges) and buttons[testInd]["piece"].split("_")[1] != playerCol:
                        movement.append(testInd)
                        break
                    if buttons[testInd]["piece"] == "none_none":
                        movement.append(testInd)
                    elif buttons[testInd]["piece"].split("_")[1] != playerCol:
                        movement.append(testInd)
                        break
                    else:
                        break

                    y += 1
                y = 1
                for i in [x*8 for x in range(1, 9)]:
                    if n in lowerEdges or n in rightEdges:
                        break
                    testInd = n+i+y
                    if (testInd in lowerEdges or testInd in rightEdges) and buttons[testInd]["piece"].split("_")[1] != playerCol:
                        movement.append(testInd)
                        break
                    if buttons[testInd]["piece"] == "none_none":
                        movement.append(testInd)
                    elif buttons[testInd]["piece"].split("_")[1] != playerCol:
                        movement.append(testInd)
                        break
                    else:
                        break

                    y += 1
            else:
                testInd = int()
                y = 1
                for i in [x*8 for x in range(1, 9)]:
                    if n in topEdges or n in rightEdges:
                        break
                    testInd = n-i+y
                    if (testInd in topEdges or testInd in rightEdges) and buttons[testInd]["piece"].split("_")[1] != oppCol:
                        movement.append(testInd)
                        break
                    if buttons[testInd]["piece"] == "none_none":
                        movement.append(testInd)
                    elif buttons[testInd]["piece"].split("_")[1] != oppCol:
                        movement.append(testInd)
                        break
                    else:
                        break

                    y += 1

                y = 1
                for i in [x*8 for x in range(1, 9)]:
                    if n in topEdges or n in leftEdges:
                        break
                    testInd = n-i-y
                    if (testInd in topEdges or testInd in leftEdges) and buttons[testInd]["piece"].split("_")[1] != oppCol:
                        movement.append(testInd)
                        break
                    if buttons[testInd]["piece"] == "none_none":
                        movement.append(testInd)
                    elif buttons[testInd]["piece"].split("_")[1] != oppCol:
                        movement.append(testInd)
                        break
                    else:
                        break

                    y += 1
                y = 1
                for i in [x*8 for x in range(1, 9)]:
                    if n in lowerEdges or n in leftEdges:
                        break
                    testInd = n+i-y
                    if (testInd in lowerEdges or testInd in leftEdges) and buttons[testInd]["piece"].split("_")[1] != oppCol:
                        movement.append(testInd)
                        break
                    if buttons[testInd]["piece"] == "none_none":
                        movement.append(testInd)
                    elif buttons[testInd]["piece"].split("_")[1] != oppCol:
                        movement.append(testInd)
                        break
                    else:
                        break

                    y += 1
                y = 1
                for i in [x*8 for x in range(1, 9)]:
                    if n in lowerEdges or n in rightEdges:
                        break
                    testInd = n+i+y
                    if (testInd in lowerEdges or testInd in rightEdges) and buttons[testInd]["piece"].split("_")[1] != oppCol:
                        movement.append(testInd)
                        break
                    if buttons[testInd]["piece"] == "none_none":
                        movement.append(testInd)
                    elif buttons[testInd]["piece"].split("_")[1] != oppCol:
                        movement.append(testInd)
                        break
                    else:
                        break

                    y += 1

        if piece == "queen":
            movement = getMovement("rook", n, oppMove, playerCol, buttons) + getMovement("bishop", n, oppMove, playerCol, buttons)

    return movement


def getpng(file, col):
    return "Images/{0}_{1}.png".format(file, col)


def buttonClick(n, playerCol):
    global buttons, selected, points, pointsLabel, root, promoter

    if promoter is not None:
        return

    if playerCol == "black":
        col = "grey"
    else:
        col = "light grey"

    for i in range(len(buttons)):
        buttons[i]["Button"]["bg"] = buttons[i]["color"]

    if not selected is None:
        mov = checkForCheck(selected, getMovement(piece=buttons[selected]["piece"].split("_")[0], n=selected, oppMove=False, playerCol=playerCol, buttons=buttons))
        if n in mov:
            if buttons[n]["piece"] != "none_none":
                #TODO: points
                pass
            buttons[n]["piece"] = buttons[selected]["piece"]
            buttons[selected]["piece"] = "none_none"
            if n in [i for i in range(8)] and buttons[n]["piece"].split("_")[0] == "pawn":
                promoter = tk.Toplevel(master=root)
                promoter.iconbitmap("Images/icon.ico")
                promoter.geometry("350x150")
                tk.Label(master=promoter, text="Choose piece to promote to.").place(x=10, y=10, height=10, width=300)
                photoQueen = tk.PhotoImage(file=getpng("queen", playerCol))
                queenButton = tk.Button(master=promoter, bg=col, command=partial(promote, "queen", n, playerCol))
                queenButton.place(x=30, y=30, height=50, width=50)
                queenButton.config(image=photoQueen)
                queenButton.image = photoQueen

                photoKnight = tk.PhotoImage(file=getpng("knight", playerCol))
                knightButton = tk.Button(master=promoter, bg=col, command=partial(promote, "knight", n, playerCol))
                knightButton.place(x=110, y=30, height=50, width=50)
                knightButton.config(image=photoKnight)
                knightButton.image = photoKnight

                photoRook = tk.PhotoImage(file=getpng("rook", playerCol))
                rookButton = tk.Button(master=promoter, bg=col, command=partial(promote, "rook", n, playerCol))
                rookButton.place(x=190, y=30, height=50, width=50)
                rookButton.config(image=photoRook)
                rookButton.image = photoRook

                photoBishop = tk.PhotoImage(file=getpng("bishop", playerCol))
                bishopButton = tk.Button(master=promoter, bg=col, command=partial(promote, "bishop", n, playerCol))
                bishopButton.place(x=270, y=30, height=50, width=50)
                bishopButton.config(image=photoBishop)
                bishopButton.image = photoBishop
                
            render()
            return
    if buttons[n]["piece"].split("_")[1] != playerCol:
        selected = None
        return
    else:
        selected = n

    info = buttons[n]
    try:
        movement = checkForCheck(selected, getMovement(piece=info["piece"].split("_")[0], n=selected, oppMove=False, playerCol=playerCol, buttons=buttons))
        for pos in movement:
            if buttons[pos]["piece"] != "none_none":
                buttons[pos]["Button"]["bg"] = "red"
            elif buttons[pos]["Button"]["bg"] == "light grey":
                buttons[pos]["Button"]["bg"] = "light green"
            elif buttons[pos]["Button"]["bg"] == "grey":
                buttons[pos]["Button"]["bg"] = "dark green"
    except:
        pass


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
    
    for _ in range(31):
        images.append("")
        pieces.append("none_none")
    
    images.append(getpng("king", playerCol))
    pieces.append(f"king_{playerCol}")
    
    for _ in range(8):
        images.append(getpng("pawn", playerCol))
        pieces.append(f"pawn_{playerCol}")

    images += [getpng("rook", playerCol), getpng("knight", playerCol), getpng("bishop", playerCol), getpng("queen", playerCol), "", getpng("bishop", playerCol), getpng("knight", playerCol), getpng("rook", playerCol)]
    pieces += [f"rook_{playerCol}", f"knight_{playerCol}", f"bishop_{playerCol}", f"queen_{playerCol}", f"none_none", f"bishop_{playerCol}", f"knight_{playerCol}", f"rook_{playerCol}"]


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
        buttons.append({"Button": tk.Button(root, bg=col, command=partial(buttonClick, i, playerCol)), "piece": pieces[i], "color": col})
        buttons[i]["Button"].place(x=line*buttonsize+400, y=y*buttonsize+40, height=buttonsize, width=buttonsize)
        buttons[i]["Button"].config(image=photo)
        buttons[i]["Button"].image = photo
        line += 1


tk.Button(root, text="Black", fg="white", bg="black", command=partial(init, "grey")).place(x=500, y=40, height=50, width=50)
tk.Button(root, text="White", fg="black", bg="white", command=partial(init, "light grey")).place(x=600, y=40, height=50, width=50)

tk.Button(fg="red", bg="white", text="Exit", command=root.destroy).place(x=10, y=10, height=40, width=50)

root.mainloop()
