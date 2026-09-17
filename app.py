
import tkinter as tk
from tkinter import ttk

artworks = [
    {
        "title": "Still life with Venus",
        "artist": "Takeshi Katori",
        "date": "1984"
    },
    {
        "title": "Fox Glacier",
        "artist": "H. W. Bloxham",
        "date": "Unknown"
    },
    {
        "title": "Woodland Path",
        "artist": "Robert F. Sanson",
        "date": "1968"
    }
]
# Create the main window
root = tk.Tk()
root.title("SBHS Digital Museum")
root.geometry("900x600")

# Create a main frame
main = ttk.Frame(root, padding=20)
main.pack(fill="both", expand=True)

# Removes everything currently shown on the screen
def clear_screen():
    for widget in main.winfo_children():
        widget.destroy()


# Shows the home page
def show_home():
    clear_screen()  
    title_label = ttk.Label(
        main,
        text="SBHS DIGITAL MUSEUM",
        font=("Segoe UI", 24, "bold")
    )
    title_label.pack(pady=(80, 10))

    subtitle_label = ttk.Label(
        main,
        text="Explore the Southland Boys' High School art collection",
        font=("Segoe UI", 11)
    )
    subtitle_label.pack(pady=(0, 30))

    browse_btn = ttk.Button(
        main,
        text="Browse Collection",
        command=show_browse
    )
    browse_btn.pack(pady=5)

    search_btn = ttk.Button(
        main,
        text="Search Collection",
        command=show_search
    )
    search_btn.pack(pady=5)

    about_btn = ttk.Button(
        main,
        text="About Museum",
        command=show_about
    )
    about_btn.pack(pady=5)

def show_browse():
    clear_screen()

    title = ttk.Label(main, text="Browse Collection")
    title.pack(pady=40)

    for artwork in artworks:
        artwork_text = artwork["title"] + " - " + artwork["artist"] + " - " + artwork["date"]

        artwork_btn = ttk.Button(
            main,
            text=artwork_text,
            command=lambda a=artwork: show_artwork(a)
        )
        artwork_btn.pack(pady=5)

    back_btn = ttk.Button(
        main,
        text="Back to Home",
        command=show_home
    )
    back_btn.pack()

def show_search():
    clear_screen()

    title = ttk.Label(
        main,
        text="Search Collection",
        font=("Segoe UI", 22, "bold")
    )
    title.pack(pady=(40, 20))

    search_entry = ttk.Entry(main, width=40)
    search_entry.pack(pady=10)

    search_btn = ttk.Button(
        main,
        text="Search",
        command=lambda: search_artworks(search_entry.get(), results_frame)
    )
    search_btn.pack(pady=5)
    results_frame = ttk.Frame(main)
    results_frame.pack(pady=10)

    back_btn = ttk.Button(
        main,
        text="Back to Home",
        command=show_home
    )
    back_btn.pack(pady=20)

def search_artworks(search_text, results_frame):

    # Clear previous results
    for widget in results_frame.winfo_children():
        widget.destroy()

    search_text = search_text.lower()

    # Check if the search box is empty
    if search_text == "":
        message = ttk.Label(
            results_frame,
            text="Please enter a search term."
        )
        message.pack(pady=5)
        return

    found = False

    # Search through the artworks
    for artwork in artworks:
        if search_text in artwork["title"].lower() or search_text in artwork["artist"].lower():

            result = ttk.Label(
                results_frame,
                text=artwork["title"] + " - " + artwork["artist"]
            )
            result.pack(pady=5)

            found = True

    # If nothing matched
    if found == False:
        message = ttk.Label(
            results_frame,
            text="No artworks found."
        )
        message.pack(pady=5)
            

def show_about():
    clear_screen()

    title = ttk.Label(
        main,
        text="About Museum"
    )
    title.pack(pady=40)

    info = ttk.Label(
        main,
        text="This program is an interactive digital museum catalogue for SBHS."
    )
    info.pack(pady=10)

    back_btn = ttk.Button(
        main,
        text="Back to Home",
        command=show_home
    )
    back_btn.pack()
show_home()

# Keep the program running
root.mainloop()


