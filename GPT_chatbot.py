import threading
import customtkinter
import json
from pathlib import Path
from google import genai
from google.genai import types
from PIL import Image, ImageTk

#startkarakter (mattelærer)
karakter = 1
instruksjoner=("Du er en mattelærer. \
                Du er flink til å lære bort, bruker enkelt og konsist språk, og er hyggelig.")


#load json filen
content = Path("conversation.json").read_text(encoding="utf-8")
data = json.loads(content)

name = (data["name"])

customtkinter.set_appearance_mode("system")

customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()

root.geometry("600x400")

root.title("chatbot GPT")
root.iconbitmap("icon.ico")



if len(data["name"]) == 0:
   displaytext = "Hva er ditt navn?"
else:
   displaytext = (f"Still ett spørsmål {data["name"]}. Jeg hjelper deg med matte!")

#GPT

def delete_entry():
  entry1.delete(0, "end")
  return

def delete_message():
  entry2.configure(state="normal")
  entry2.delete("1.0", "end")
  entry2.configure(state="disabled")
  return




def GPT():
  global displaytext, message
  message = entry1.get()

  if len(data["name"]) == 0:              
    navn()
    entry1.delete(0, "end")

  else:
    message = entry1.get()
    api_thread = threading.Thread(target=gemini)
    api_thread.start()
    loading_animation()
    entry1.delete(0, "end")


def display():
   prepare_update()

   update()



#Sletter convo
def delete_convo():
    global displaytext
    if karakter == 1:
      displaytext = (f"Laget en ny samtale {data["name"]}. Jeg hjelper deg med matte!")
      display()
    elif karakter == 2:
      displaytext = (f"Laget en ny samtale {data["name"]}. Voff Voff :D")
      display()   
    elif karakter == 3:
      displaytext = (f"Laget en ny samtale! Du snakker med bombe eksperten {data["name"]}")
      display() 
    enter = {
    "conversation": []
    }
    data.update(enter)
    Path("conversation.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    delete_message()
    display()

#Sletter alt
def delete_all():
    enter = {
    "name": "",
    "conversation": []
    }
    Path("conversation.json").write_text(json.dumps(enter, indent=2), encoding="utf-8")
    delete_message()


#gif loading
transparent_img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
transparent_photo = ImageTk.PhotoImage(transparent_img)

def loading_animation():
    gif = Image.open("loading.gif")
    frames = []
    desired_size = (120, 90) 
    try:
        while True:
            frame = gif.copy()
            frame = frame.convert("RGBA")
            frame = frame.resize(desired_size, Image.LANCZOS)
            frames.append(ImageTk.PhotoImage(frame))
            gif.seek(len(frames))
    except EOFError:
        pass
    def animate(idx=0):
        if not getattr(loading_gif, 'animating', False):
            loading_gif.configure(image=transparent_photo, text="")
            loading_gif.image = transparent_photo
            return
        loading_gif.configure(image=frames[idx])
        loading_gif.image = frames[idx]
        loading_gif.after(100, animate, (idx+1) % len(frames))
    loading_gif.animating = True
    animate()

def stop_loading_animation():
    loading_gif.animating = False
   





#kaller på gemini (sett inn api keyen din under)
def gemini():
        global message, displaytext, name, instruksjoner
        question = message

        disable_interaction()

        client = genai.Client(api_key="SETT INN DIN API KEY")

        response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f'"system_instruksjoner": {instruksjoner}\
                "Brukerdata": Navn: {name}"konversasjonslogg": {data["conversation"]} \
                "ny_brukerinput": {question}',
                config=types.GenerateContentConfig(
                    thinking_config=types.ThinkingConfig(thinking_budget=0) # Disables thinking
                ),
            )   




        displaytext = response.text
        display()
        stop_loading_animation()
        enable_interaction()

        #lagre
        conversation = response.text

        data["conversation"].append(conversation)

        Path("conversation.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
        





def prepare_update():
  entry2.configure(state="normal")
  entry2.delete("1.0", "end")
  return

def update():
  entry2.insert("1.0", displaytext)
  entry2.configure(state="disabled")
  return

def navn():
    global displaytext
    name = message
    entry = {
    "name": name,
    "conversation": []
    }
    data.update(entry)
    Path("conversation.json").write_text(json.dumps(entry, indent=2), encoding="utf-8")

    if karakter == 1:
      displaytext = (f"Still et spørsmål {data["name"]}. Jeg hjelper deg med matte!")
      display()
    elif karakter == 2:
      displaytext = (f"Still et spørsmål {data["name"]}. Voff Voff :D")
      display()   
    elif karakter == 3:
      displaytext = (f"Still et spørsmål til bombe eksperten {data["name"]}")
      display()  
    


def disable_interaction():
  entry1.configure(state="disabled")
  button.configure(state="disabled")
  button2.configure(state="disabled")
  button3.configure(state="disabled")
  combobox.configure(state="disabled")


def enable_interaction():
  entry1.configure(state="normal")
  button.configure(state="normal")
  button2.configure(state="normal")
  button3.configure(state="normal")
  combobox.configure(state="readonly")

def close():
  root.destroy()


def lukkervindusnart():
  global displaytext
  displaytext = (f"lukker vindu...")
  display()
  root.after(1000, close)




def deletee():
  global displaytext
  disable_interaction()
  displaytext = (f"Jeg sletter for deg {name}")
  delete_all()
  display()
  root.after(1000, lukkervindusnart)


#konfigurere oppsett

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(2, weight=1)

frame = customtkinter.CTkFrame(master=root)
frame.grid(row=1, column=1, sticky="nsew")

frame.grid_rowconfigure(0, weight=1)
frame.grid_rowconfigure(1, weight=1)
frame.grid_rowconfigure(2, weight=1)
frame.grid_rowconfigure(3, weight=1)
frame.grid_rowconfigure(4, weight=1)
frame.grid_rowconfigure(5, weight=1)
frame.grid_rowconfigure(6, weight=0, minsize=100)


frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)
frame.grid_columnconfigure(2, weight=1)

buttons = customtkinter.CTkFrame(master=frame, corner_radius=32)
buttons.grid(row=5, column=1, sticky="nsew", padx=10, pady=10)

buttons.grid_rowconfigure(0, weight=1)

buttons.grid_columnconfigure(0, weight=1)
buttons.grid_columnconfigure(1, weight=1)







def selection(choice):
    global name, karakter, message, instruksjoner
    if choice == "Matte lærer":
        instruksjoner=("Du er en mattelærer. \
                Du er flink til å lære bort, bruker enkelt og konsist språk, og er hyggelig.")
        if len(data["name"]) == 0:
           karakter = 1
           navn()
        else:
          karakter = 1
          delete_convo()
    elif choice == "Hund":
        instruksjoner=("Du er en hund. \
                Du bjeffer mye, og er ltt irriterende, din favoritt ting er godbit.")
        
        if len(data["name"]) == 0:
          karakter = 2
          navn()
        else:
          karakter = 2
          delete_convo()

    elif choice == "Bombe":
        instruksjoner=("Du er bombe ekspert. \
                Du er hjelpsom og liker å lage destruksjonvåpen.")
        if len(data["name"]) == 0:
          karakter = 3
          navn()
        else:
          karakter = 3
          delete_convo()



#layout

label = customtkinter.CTkLabel(master=frame, text="chatbot GPT", font=("roboto", 24, "bold"))
label.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)


#SELECT
combobox = customtkinter.CTkComboBox(
    master=frame,
    values=["Matte lærer", "Hund", "Bombe"],
    command=selection, state="readonly")
combobox.grid(row=1, column=1, sticky="ew", padx=10, pady=10)

combobox.set("Matte lærer")



entry2 = customtkinter.CTkTextbox(master=frame, wrap="word", width=300, height=100, 
                                  scrollbar_button_color="blue")
entry2.insert("1.0", displaytext)
entry2.configure(state="disabled")  # Make it read-only
entry2.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)





entry1 = customtkinter.CTkEntry(master=frame, placeholder_text= "Skriv", font=("roboto", 12, "bold"), width=200)
entry1.grid(row=3, column=1)

entry1.bind("<Return>", lambda event: GPT())





send_image = Image.open("send.png")

button = customtkinter.CTkButton(master=frame, text="Send", command=GPT, font=("roboto", 12, "bold"), 
                                 image=customtkinter.CTkImage(send_image, size=(10, 10)), corner_radius=32)
button.grid(row=4, column=1, padx=10, pady=10)

button2 = customtkinter.CTkButton(master=buttons, text="Slett", command=deletee, fg_color="darkred", font=("roboto", 12, "bold"), 
                                  corner_radius=32, width=100)
button2.grid(row=0, column=0, padx=10, pady=10, sticky="e")

button3 = customtkinter.CTkButton(master=buttons, text="Ny samtale", command=delete_convo, fg_color="green", font=("roboto", 12, "bold"), 
                                  corner_radius=32, width=100)

button3.grid(row=0, column=1, padx=10, pady=10, sticky="w")




loading_gif = customtkinter.CTkLabel(master=frame, text="")
loading_gif.grid(row=6, column=1)




def on_closing():
   delete_convo()
   root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()




