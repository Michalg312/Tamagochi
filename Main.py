from Car import Car
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

tickspeed = 1000


def center_window(window, width=None, height=None):
    window.update_idletasks()
    if width is None or height is None:
        width = window.winfo_width()
        height = window.winfo_height()

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f'{width}x{height}+{x}+{y}')


def main():
    cars = [
        Car("bmw.jpg", 20, 150, 350, 250),
        Car("bmw1.jpg", 20, 150, 300, 200),
        Car("bmw2.png", 20, 50, 100, 100),
        Car("bmw3.png", 20, 50, 100, 100),
    ]

    car_texts = ["E30", "E36", "BMW", "Mercedes"]

    okno = tk.Tk()
    okno.title("Ty to jest civic?")
    okno.config(bg="#222222")


    okno.minsize(800, 600)
    center_window(okno, 800, 600)

    btn_style = {
        "font": ("Arial", 14, "bold"),
        "bg": "#555555",
        "fg": "white",
        "activebackground": "#777777",
        "activeforeground": "white",
        "relief": "raised",
        "bd": 3,
        "width": 15,
    }

    def create_car_card(parent, row, column, image, text, command=None):
        frame = tk.Frame(parent, bg="#333333", bd=2, relief="groove")
        frame.grid(row=row, column=column, padx=15, pady=15, sticky="nsew")

        label = tk.Label(frame, image=image, bg="#333333")
        label.image = image
        label.pack(padx=10, pady=10)

        text_label = tk.Label(frame, text=text, font=("Arial", 14, "bold"), fg="white", bg="#333333")
        text_label.pack(pady=(0, 10))

        btn = tk.Button(frame, text="Wybieram", command=command, **btn_style)
        btn.pack(pady=(0, 10))

        return frame

    car_images = []
    for car in cars:
        img = Image.open(car.image)
        img = img.resize((200, 150))
        imgTk = ImageTk.PhotoImage(img)
        car_images.append(imgTk)

    for i, car in enumerate(cars):
        row = i // 2
        col = i % 2
        create_car_card(okno, row, col, car_images[i], car_texts[i], command=lambda c=car: mainGame(c, okno))

    okno.grid_columnconfigure(0, weight=1)
    okno.grid_columnconfigure(1, weight=1)
    okno.grid_rowconfigure(0, weight=1)
    okno.grid_rowconfigure(1, weight=1)

    okno.mainloop()


def mainGame(car, okno):
    car.makeNoise()
    for widget in okno.winfo_children():
        widget.destroy()

    okno.config(bg="#222222")
    okno.minsize(800, 600)
    center_window(okno, 800, 600)

    obraz = Image.open(car.image)
    obraz = obraz.resize((400, 300))
    obrazek = ImageTk.PhotoImage(obraz)

    etykieta = tk.Label(okno, image=obrazek, bg="#222222")
    etykieta.image = obrazek
    etykieta.grid(row=0, column=1, padx=20, pady=20)

    spinpaliwo = tk.Spinbox(okno, from_=0, to=100, width=5, font=("Arial", 18), justify='center')
    spinpaliwo.delete(0, "end")
    spinpaliwo.insert(0, "20")

    spinolej = tk.Spinbox(okno, from_=0, to=100, width=5, font=("Arial", 18), justify='center')
    spinolej.delete(0, "end")
    spinolej.insert(0, "20")

    paliwoLabel = tk.Label(okno, text=f"Paliwo: {car.fuel}", font=("Arial", 16, "bold"), fg="white", bg="#444444",
                           relief="sunken", bd=2, width=15)
    paliwoLabel.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

    olejLabel = tk.Label(okno, text=f"Olej: {car.oil}", font=("Arial", 16, "bold"), fg="white", bg="#444444",
                         relief="sunken", bd=2, width=15)
    olejLabel.grid(row=1, column=3, padx=10, pady=5, sticky="ew")

    def end_game():
        for widget in okno.winfo_children():
            widget.destroy()
        okno.config(bg="black")
        obraz = Image.open("ded.png")
        obrazek = ImageTk.PhotoImage(obraz)
        koniec = tk.Label(
            okno,
            text="Koniec gry! Brak paliwa lub oleju.",
            font=("Arial", 20, "bold"),
            fg="red",
            bg="black",
            image=obrazek,
            borderwidth=0,
            highlightthickness=0,
            compound="top",
            padx=20,
            pady=20,
        )
        koniec.image = obrazek
        koniec.pack(expand=True)
        center_window(okno)

    def update_levels():
        car.fuel = max(0, car.fuel - 1)
        car.oil = max(0, car.oil - 1)

        paliwoLabel.config(text=f"Paliwo: {car.fuel}")
        olejLabel.config(text=f"Olej: {car.oil}")

        if car.fuel == 0 or car.oil == 0:
            end_game()
        else:
            okno.after(tickspeed, update_levels)

    def minigra_paliwo(on_success):
        minigra = tk.Toplevel()
        minigra.title("Minigra: Dolej paliwa")
        minigra.config(bg='lightblue')
        minigra.minsize(600, 400)

        canvas = tk.Canvas(minigra, width=600, height=400, bg='lightblue', highlightthickness=0)
        canvas.pack()

        auto_width, auto_height = 128, 128
        auto_x, auto_y = 420, 130

        auto_img = Image.open("auto.png").resize((auto_width, auto_height))
        auto_photo = ImageTk.PhotoImage(auto_img)
        auto = canvas.create_image(auto_x, auto_y, anchor='nw', image=auto_photo)

        fuel_img = Image.open("fuel.png").resize((60, 75))
        fuel_photo = ImageTk.PhotoImage(fuel_img)
        nalewak = canvas.create_image(50, 160, anchor='nw', image=fuel_photo)

        offset_x = offset_y = 0

        def start_drag(event):
            nonlocal offset_x, offset_y
            x1, y1 = canvas.coords(nalewak)
            offset_x = event.x - x1
            offset_y = event.y - y1

        def on_drag(event):
            x = event.x - offset_x
            y = event.y - offset_y
            canvas.coords(nalewak, x, y)

        def check_drop(event):
            nx1, ny1 = canvas.coords(nalewak)
            nx2, ny2 = nx1 + 60, ny1 + 75

            ax1, ay1 = auto_x, auto_y
            ax2, ay2 = ax1 + auto_width, ay1 + auto_height

            if not (nx2 < ax1 or nx1 > ax2 or ny2 < ay1 or ny1 > ay2):
                messagebox.showinfo("Sukces!", "Paliwo dolane!")
                on_success()
                minigra.destroy()
            else:
                messagebox.showwarning("Chybione!", "Spróbuj jeszcze raz!")

        canvas.tag_bind(nalewak, "<ButtonPress-1>", start_drag)
        canvas.tag_bind(nalewak, "<B1-Motion>", on_drag)
        canvas.tag_bind(nalewak, "<ButtonRelease-1>", check_drop)

        minigra.auto_photo = auto_photo
        minigra.fuel_photo = fuel_photo

        center_window(minigra, 600, 400)
        minigra.transient(okno)
        minigra.grab_set()
        okno.wait_window(minigra)

    def dolej_paliwo():
        def on_success():
            try:
                wartosc = int(spinpaliwo.get())
            except ValueError:
                wartosc = 0
            car.addFuel(wartosc)
            if hasattr(car, 'maxFuelCapacity') and car.fuel > car.maxFuelCapacity:
                car.fuel = car.maxFuelCapacity
            paliwoLabel.config(text=f"Paliwo: {car.fuel}")

        minigra_paliwo(on_success)

    def minigra_olej(on_success):
        minigra = tk.Toplevel()
        minigra.title("Minigra: Dolej oleju")
        minigra.config(bg='lightblue')
        minigra.minsize(600, 400)

        canvas = tk.Canvas(minigra, width=600, height=400, bg='lightblue', highlightthickness=0)
        canvas.pack()

        auto_width, auto_height = 128, 128
        auto_x, auto_y = 420, 130

        auto_img = Image.open("auto.png").resize((auto_width, auto_height))
        auto_photo = ImageTk.PhotoImage(auto_img)
        auto = canvas.create_image(auto_x, auto_y, anchor='nw', image=auto_photo)

        oil_img = Image.open("oil.png").resize((60, 60))
        oil_photo = ImageTk.PhotoImage(oil_img)
        nalewak = canvas.create_image(50, 160, anchor='nw', image=oil_photo)

        offset_x = offset_y = 0

        def start_drag(event):
            nonlocal offset_x, offset_y
            x1, y1 = canvas.coords(nalewak)
            offset_x = event.x - x1
            offset_y = event.y - y1

        def on_drag(event):
            x = event.x - offset_x
            y = event.y - offset_y
            canvas.coords(nalewak, x, y)

        def check_drop(event):
            nx1, ny1 = canvas.coords(nalewak)
            nx2, ny2 = nx1 + 60, ny1 + 60

            ax1, ay1 = auto_x, auto_y
            ax2, ay2 = ax1 + auto_width, ay1 + auto_height

            if not (nx2 < ax1 or nx1 > ax2 or ny2 < ay1 or ny1 > ay2):
                messagebox.showinfo("Sukces!", "Olej dolany!")
                on_success()
                minigra.destroy()
            else:
                messagebox.showwarning("Chybione!", "Spróbuj jeszcze raz!")

        canvas.tag_bind(nalewak, "<ButtonPress-1>", start_drag)
        canvas.tag_bind(nalewak, "<B1-Motion>", on_drag)
        canvas.tag_bind(nalewak, "<ButtonRelease-1>", check_drop)

        minigra.auto_photo = auto_photo
        minigra.oil_photo = oil_photo

        center_window(minigra, 600, 400)
        minigra.transient(okno)
        minigra.grab_set()
        okno.wait_window(minigra)

    def dolej_olej():
        def on_success():
            try:
                wartosc = int(spinolej.get())
            except ValueError:
                wartosc = 0
            car.addOil(wartosc)
            if hasattr(car, 'maxOilCapacity') and car.oil > car.maxOilCapacity:
                car.oil = car.maxOilCapacity
            olejLabel.config(text=f"Olej: {car.oil}")

        minigra_olej(on_success)

    btn_style = {
        "font": ("Arial", 14, "bold"),
        "bg": "#555555",
        "fg": "white",
        "activebackground": "#777777",
        "activeforeground": "white",
        "relief": "raised",
        "bd": 3,
        "width": 12,
    }

    paliwoButton = tk.Button(okno, text="Dolej paliwa", command=dolej_paliwo, **btn_style)
    paliwoButton.grid(row=2, column=0, padx=10, pady=10)

    spinpaliwo.grid(row=3, column=0, padx=10, pady=5)

    olejButton = tk.Button(okno, text="Dolej oleju", command=dolej_olej, **btn_style)
    olejButton.grid(row=2, column=3, padx=10, pady=10)

    spinolej.grid(row=3, column=3, padx=10, pady=5)

    okno.grid_columnconfigure(0, weight=1)
    okno.grid_columnconfigure(1, weight=1)
    okno.grid_columnconfigure(3, weight=1)

    update_levels()


if __name__ == "__main__":
    main()