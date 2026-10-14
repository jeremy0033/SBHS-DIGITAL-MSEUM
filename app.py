import tkinter as tk
from tkinter import ttk
from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent
with open(BASE_DIR / "artworks.json", encoding="utf-8") as file:
    artworks = json.load(file)

try:
    from PIL import Image, ImageTk
except ImportError:
    Image = ImageTk = None

root = tk.Tk()
root.title("SBHS Digital Museum")
root.geometry("900x600")
main = ttk.Frame(root, padding=20)
main.pack(fill="both", expand=True)
photo_reference = None


def clear_screen():
    for widget in main.winfo_children():
        widget.destroy()


def show_home():
    clear_screen()
    ttk.Label(main, text="SBHS DIGITAL MUSEUM", font=("Segoe UI", 24, "bold")).pack(pady=(80, 10))
    ttk.Label(main, text="Explore the Southland Boys' High School art collection", font=("Segoe UI", 11)).pack(pady=(0, 30))
    ttk.Button(main, text="Browse Collection", command=show_browse).pack(pady=5)
    ttk.Button(main, text="Search Collection", command=show_search).pack(pady=5)
    ttk.Button(main, text="About Museum", command=show_about).pack(pady=5)


def scrollable_area():
    area = ttk.Frame(main)
    area.pack(fill="both", expand=True)
    canvas = tk.Canvas(area, highlightthickness=0)
    scrollbar = ttk.Scrollbar(area, orient="vertical", command=canvas.yview)
    inside = ttk.Frame(canvas)
    inside.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    window = canvas.create_window((0, 0), window=inside, anchor="nw")
    canvas.bind("<Configure>", lambda e: canvas.itemconfigure(window, width=e.width))
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    return inside


def show_browse():
    clear_screen()
    ttk.Label(main, text="Browse Collection", font=("Segoe UI", 22, "bold")).pack(pady=(10, 15))
    ttk.Button(main, text="Back to Home", command=show_home).pack(pady=5)
    inside = scrollable_area()
    for artwork in artworks:
        label = artwork["title"] + " - " + artwork["artist"] + " - " + artwork["date"]
        ttk.Button(inside, text=label, command=lambda a=artwork: show_artwork(a)).pack(pady=5, padx=10, fill="x")


def show_artwork(artwork):
    global photo_reference
    clear_screen()
    ttk.Label(main, text=artwork["title"], font=("Segoe UI", 22, "bold"), wraplength=800).pack(pady=(10, 10))
    ttk.Label(main, text="Artist: " + artwork["artist"]).pack(pady=3)
    ttk.Label(main, text="Date: " + artwork["date"]).pack(pady=3)
    for key, title in [("medium", "Medium"), ("category", "Category"), ("description", "Description")]:
        if artwork.get(key):
            ttk.Label(main, text=title + ": " + artwork[key], wraplength=780).pack(pady=3)
    photo_reference = None
    path = BASE_DIR / artwork.get("image", "") if artwork.get("image") else None
    if path and path.is_file() and Image:
        img = Image.open(path)
        img.thumbnail((650, 280))
        photo_reference = ImageTk.PhotoImage(img)
        ttk.Label(main, image=photo_reference).pack(pady=12)
    else:
        ttk.Label(main, text="Image unavailable").pack(pady=15)
    ttk.Button(main, text="Back to Browse", command=show_browse).pack(pady=10)


def show_search():
    clear_screen()
    ttk.Label(main, text="Search Collection", font=("Segoe UI", 22, "bold")).pack(pady=(15, 15))
    search_entry = ttk.Entry(main, width=40)
    search_entry.pack(pady=10)
    ttk.Button(main, text="Search", command=lambda: search_artworks(search_entry.get(), results_frame)).pack(pady=5)
    ttk.Button(main, text="Back to Home", command=show_home).pack(pady=5)
    results_frame = scrollable_area()


def search_artworks(search_text, results_frame):
    for widget in results_frame.winfo_children():
        widget.destroy()
    search_text = search_text.strip().lower()
    if not search_text:
        ttk.Label(results_frame, text="Please enter a search term.").pack(pady=5)
        return
    found = False
    for artwork in artworks:
        if search_text in artwork["title"].lower() or search_text in artwork["artist"].lower():
            ttk.Button(results_frame, text=artwork["title"] + " - " + artwork["artist"], command=lambda a=artwork: show_artwork(a)).pack(pady=5, fill="x")
            found = True
    if not found:
        ttk.Label(results_frame, text="No artworks found.").pack(pady=5)


def show_about():
    clear_screen()
    ttk.Label(main, text="About Museum").pack(pady=40)
    ttk.Label(main, text="This program is an interactive digital museum catalogue for SBHS.").pack(pady=10)
    ttk.Button(main, text="Back to Home", command=show_home).pack()

show_home()
root.mainloop()



