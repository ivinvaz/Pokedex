from tkinter import *
import requests
from PIL import Image, ImageTk
from io import BytesIO

# API handler
def apiHandler(get):
    linkName = f"https://pokeapi.co/api/v2/pokemon/{get}"

    try:
        pkm = requests.get(url=linkName)
        pkm.raise_for_status()  
        data = pkm.json()
        name = data["name"]
        number = data["id"]
        type_brute = [t["type"]["name"] for t in data["types"]]
        sprite = data["sprites"]["front_default"]
        return {"name": name, "number": number, "type": type_brute, "sprite": sprite}
    except requests.exceptions.RequestException as e:
        print(f"API request error: {e}")
        return None
    except KeyError as e:
        print(f"Error accessing API data: {e}")
        return None

# Initial Pokemon data
initial_pokemon = apiHandler(1)
pokeName = initial_pokemon["name"] if initial_pokemon else "Not Found"
pokeNum = initial_pokemon["number"] if initial_pokemon else "0"
pokeType = initial_pokemon["type"] if initial_pokemon else []
pokeSprite = initial_pokemon["sprite"] if initial_pokemon else ""

# Sprite Loader
def changeSprite(url_png):
    try:
        response = requests.get(url_png)
        response.raise_for_status()
        image_data = BytesIO(response.content)
        img = Image.open(image_data)
        photo = ImageTk.PhotoImage(img)
        canvas.itemconfig(pkmImage, image=photo)
        canvas.image_cache = photo
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error loading image: {e}")
        erroImage = PhotoImage(file="./src/close.png")
        canvas.itemconfig(pkmImage, image=erroImage)
        return False

# Button Functions
def captureContent(event):
    global pokeName, pokeNum, pokeType, pokeSprite
    eventGet = event.widget.get()
    apiResult = apiHandler(eventGet)
    if apiResult:
        pokeName = apiResult["name"]
        pokeNum = apiResult["number"]
        pokeType = apiResult["type"]
        pokeSprite = apiResult["sprite"]
        changeSprite(pokeSprite)
        canvas.itemconfig(titulo, text=f"{pokeNum}-{pokeName}", fill="black")
    else:
        canvas.itemconfig(titulo, text="Not Found", fill="red")
        erroImage = PhotoImage(file="./src/close.png")
        canvas.itemconfig(pkmImage, image=erroImage)
    entryBar.delete(0, END)

def nextPkm():
    global pokeName, pokeNum, pokeType, pokeSprite
    next_num = pokeNum + 1
    apiResult = apiHandler(next_num)
    if apiResult:
        pokeName = apiResult["name"]
        pokeNum = apiResult["number"]
        pokeType = apiResult["type"]
        pokeSprite = apiResult["sprite"]
        changeSprite(pokeSprite)
        canvas.itemconfig(titulo, text=f"{pokeNum}-{pokeName}", fill="black")
    else:
        canvas.itemconfig(titulo, text="Not Found", fill="red")
        erroImage = PhotoImage(file="./src/close.png")
        canvas.itemconfig(pkmImage, image=erroImage)

def backPkm():
    global pokeName, pokeNum, pokeType, pokeSprite
    prev_num = pokeNum - 1
    if prev_num > 0:
        apiResult = apiHandler(prev_num)
        if apiResult:
            pokeName = apiResult["name"]
            pokeNum = apiResult["number"]
            pokeType = apiResult["type"]
            pokeSprite = apiResult["sprite"]
            changeSprite(pokeSprite)
            canvas.itemconfig(titulo, text=f"{pokeNum}-{pokeName}", fill="black")
        else:
            canvas.itemconfig(titulo, text="Not Found", fill="red")
            erroImage = PhotoImage(file="./src/close.png")
            canvas.itemconfig(pkmImage, image=erroImage)

# Interface
window = Tk()
window.title("Pokedex")
window.config(padx=0, pady=0)

# Canva Create
canvas = Canvas(width=430, height=640)
canvas.grid(row=0, column=0)
pokedex_bg = PhotoImage(file="./src/pokedex.png")
bg = canvas.create_image(217, 321, image=pokedex_bg)
titulo = canvas.create_text(220, 370, font=("Arial", 20), text=f"{pokeNum}-{pokeName}")

# Search Bar Interface
entryBar = Entry(width=41)
entryBar.focus()
entryBarWindow = canvas.create_window(215, 415, window=entryBar)
entryBar.bind("<Return>", captureContent)

# Button Interface
buttonBack = Button(canvas, text="Anterior", command=backPkm)
buttonBackWindow = canvas.create_window(155, 480, window=buttonBack)
buttonNext = Button(canvas, text="Próximo", command=nextPkm)
buttonNextWindow = canvas.create_window(255, 480, window=buttonNext)

# Pokemon Interface
startImage = PhotoImage(file="./src/1.png")
pkmImage = canvas.create_image(200, 270, image=startImage)
if pokeSprite:
    changeSprite(pokeSprite)

window.mainloop()