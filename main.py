import tkinter as tk
from functools import partial

root = tk.Tk()
root.attributes("-fullscreen", True)
root.title("Chess")
root.iconbitmap("Images/icon.ico")

buttons : list[dict] = list()

selected = None

points = int()
pointsLabel : tk.Label = None


def render():
    global buttons
    images = []
    for i in range(len(buttons)):
        try:
            photo = tk.PhotoImage(file=getpng(buttons[i]["piece"].split("_")[0], buttons[i]["piece"].split("_")[1]))
        except:
            photo = ""
        buttons[i]["Button"].config(image=photo)
        buttons[i]["Button"].image = photo


def isCheck(field : list):
    check = False
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
        if isCheck(sim):
            print(f"Popped {pos}")
            movement.pop(pos)


    return movement


def getMovement(piece : str="pawn", n : int=None, oppMove : bool=False, playerCol : str = "black"):
    global buttons
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
        
        print(surrounding)

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
        movement = getMovement("rook", n, oppMove, playerCol) + getMovement("bishop", n, oppMove, playerCol)

    return movement


def getpng(file, col):
    return "Images/{0}_{1}.png".format(file, col)


def buttonClick(n, playerCol):
    global buttons, selected, points, pointsLabel

    for i in range(len(buttons)):
        buttons[i]["Button"]["bg"] = buttons[i]["color"]
    
    if not selected is None:
        mov = checkForCheck(selected, getMovement(piece=buttons[selected]["piece"].split("_")[0], n=selected, oppMove=False, playerCol=playerCol))
        if n in mov:
            if buttons[n]["piece"] != "none_none":
                #TODO: points
                pass
            buttons[n]["piece"] = buttons[selected]["piece"]
            buttons[selected]["piece"] = "none_none"
            render()
            return
    if buttons[n]["piece"].split("_")[1] != playerCol:
        selected = None
        return
    else:
        selected = n
    
    info = buttons[n]
    try:
        movement = checkForCheck(selected, getMovement(piece=info["piece"].split("_")[0], n=selected, oppMove=False, playerCol=playerCol))
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
    
    images.append(getpng("pawn", oppCol))
    pieces.append(f"pawn_{oppCol}")
    
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
        buttons.append({"Button": tk.Button(root, bg=col, command=partial(buttonClick, i, playerCol)), "piece": pieces[i], "color": col})
        buttons[i]["Button"].place(x=line*buttonsize+400, y=y*buttonsize+40, height=buttonsize, width=buttonsize)
        buttons[i]["Button"].config(image=photo)
        buttons[i]["Button"].image = photo
        line += 1


tk.Button(root, text="Black", fg="white", bg="black", command=partial(init, "grey")).place(x=500, y=40, height=50, width=50)
tk.Button(root, text="White", fg="black", bg="white", command=partial(init, "light grey")).place(x=600, y=40, height=50, width=50)

tk.Button(fg="red", bg="white", text="Exit", command=root.destroy).place(x=10, y=10, height=40, width=50)

root.mainloop()
