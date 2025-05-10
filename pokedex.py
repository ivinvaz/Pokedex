from tkinter import *
import requests

#API handler

def apiHandler(get):
    linkName = f"https://pokeapi.co/api/v2/pokemon/{get}"
    pkm = requests.get(url=linkName)
    pkm.raise_for_status()
    name    = pkm.json()["name"]
    number  = pkm.json()["id"]
    typeBrute    = [x for x in pkm.json()["types"]]
    type = []
    for x in range(len(typeBrute)):
        type.append(typeBrute[x-1]["type"]["name"])
    cry     = pkm.json()["cries"]["latest"]
    sprite  = pkm.json()["sprites"]["other"]["showdown"]["front_default"]
    return({"name":name,"number":number,"type":type,"cry":cry,"sprite":sprite})

#Button Function


#Interface

window = Tk()
window.title("Pokedex")
window.config(padx=0, pady=0)

canvas = Canvas(width=430, height=640)
pokedex_bg = PhotoImage(file="./src/pokedex.png")
canvas.create_image(217,321, image=pokedex_bg)
canvas.grid(column=0,row=0)

window.mainloop()