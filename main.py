from tkinter import *
import pandas as pd
import random


current_card = {}
to_learn = {}
BACKGROUND_COLOR = "#B1DDC6"
try:
    data = pd.read_csv("data/words to learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")

else:
    to_learn = data.to_dict(orient="records")


# ---------------------------- extracting word from csv ------------------------------- #
def next_card():
    global current_card, flip_timer
    windows.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    title_text = current_card["French"]
    canvas.itemconfig(card_title, text="French", fil="black")
    canvas.itemconfig(card_text, text=title_text, fill="black")
    canvas.itemconfig(canvas_image, image=front_images)
    flip_timer = windows.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="English")
    canvas.itemconfig(card_text, text=current_card["English"], fill="white")
    canvas.itemconfig(canvas_image, image=back_image)


def is_know():
    to_learn.remove(current_card)
    data_learn = pd.DataFrame(to_learn)
    data_learn.to_csv("data/words to learn.csv", index=False)

    next_card()


# ---------------------------- UI SETUP ------------------------------- #
windows = Tk()
windows.title("Flashy")
windows.config(bg=BACKGROUND_COLOR, pady=50, padx=50)
flip_timer = windows.after(3000, func=flip_card)

canvas = Canvas(height=526, width=800)
front_images = PhotoImage(file="images/card_front.png")
back_image = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=front_images)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
card_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
card_text = canvas.create_text(400, 263, text="word", font=("Ariel", 60, "bold "))
canvas.grid(column=0, row=0, columnspan=2)

unknown_button_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=unknown_button_image, highlightthickness=0, command=next_card)
unknown_button.grid(column=0, row=1)

known_button_image = PhotoImage(file="images/right.png")
known_button = Button(image=known_button_image, highlightthickness=0, command=is_know)
known_button.grid(column=1, row=1)

next_card()
windows.mainloop()
