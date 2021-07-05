# importing only those functions
# which are needed
import tkinter, random, os

# creating tkinter window
root = tkinter.Tk()

# Creating a photoimage object to use image

button = None


def randomPicture():
    global button
    img = tkinter.PhotoImage(file=f"Images/{random.choice(os.listdir('Images'))}")
    button.config(image=img)
    button.image = img


button = tkinter.Button(root, image=tkinter.PhotoImage(file="Images/test_bishop_white.png"), command=randomPicture); button.place(x=10, y=10, height=50, width=50)
button.image = tkinter.PhotoImage(file="Images/test_bishop_white.png")

root.mainloop()