
import tkinter as tk
from tkinter import ttk
from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "artworks.json"


# Load catalogue safely
def load_artworks():
    try:
        with open(DATA_FILE, encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            return [], "Catalogue error: artworks.json must contain a list."

        # Ignore invalid records without crashing
        valid_records = [item for item in data if isinstance(item, dict)]

        if len(valid_records) != len(data):
            return valid_records, "Warning: Some invalid records were skipped."

        return valid_records, None

    except FileNotFoundError:
        return [], "Catalogue file not found. Please check artworks.json."

    except json.JSONDecodeError:
        return [], "Catalogue file is damaged or contains invalid JSON."

    except OSError:
        return [], "Unable to read the catalogue file."


artworks, catalogue_error = load_artworks()


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


# Safely retrieve artwork information
def get_info(artwork, field):
    value = artwork.get(field)
    if value is None or str(value).strip() == "":
        return "Not provided"
    return str(value)


def clear_screen():
    for widget in main.winfo_children():
        widget.destroy()


def show_home():
    clear_screen()

    # School logo
    logo_path = Path(__file__).parent / "images" / "school_logo.png"

    try:
        logo = Image.open(logo_path)
        logo.thumbnail((200, 200), Image.Resampling.LANCZOS)

        logo_photo = ImageTk.PhotoImage(logo)

        logo_label = ttk.Label(main, image=logo_photo)
        logo_label.image = logo_photo
        logo_label.pack(pady=(25, 10))

    except (FileNotFoundError, OSError):
        ttk.Label(
            main,
            text="School logo unavailable"
        ).pack(pady=10)

    ttk.Label(
        main,
        text="L&R DEAR MUSUEM",
        font=("Segoe UI", 24, "bold")
    ).pack(pady=(10, 10))

    ttk.Label(
        main,
        text="Explore the Southland Boys' High School art collection",
        font=("Segoe UI", 11)
    ).pack(pady=(0, 30))

    if catalogue_error:
        ttk.Label(
            main,
            text=catalogue_error,
            foreground="red",
            wraplength=750
        ).pack(pady=10)

    ttk.Button(
        main, text="Browse Collection", command=show_browse
    ).pack(pady=5)

    ttk.Button(
        main, text="Search Collection", command=show_search
    ).pack(pady=5)

    ttk.Button(
        main, text="About Museum", command=show_about
    ).pack(pady=5)

    ttk.Button(
        main, text="Quit", command=root.destroy
    ).pack(pady=5)


def scrollable_area():
    area = ttk.Frame(main)
    area.pack(fill="both", expand=True)

    canvas = tk.Canvas(area, highlightthickness=0)

    scrollbar = ttk.Scrollbar(
        area, orient="vertical", command=canvas.yview
    )

    inside = ttk.Frame(canvas)

    inside.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    window = canvas.create_window(
        (0, 0), window=inside, anchor="nw"
    )

    canvas.bind(
        "<Configure>",
        lambda e: canvas.itemconfigure(
            window, width=e.width
        )
    )

    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    return inside



def show_browse():
    clear_screen()

    ttk.Label(
        main,
        text="Browse Collection",
        font=("Segoe UI", 22, "bold")
    ).pack(pady=(10, 15))

    ttk.Button(
        main,
        text="Back to Home",
        command=show_home
    ).pack(pady=(0, 12))

    inside = scrollable_area()
    inside.photo_references = []

    if not artworks:
        ttk.Label(
            inside,
            text="No artworks are currently available."
        ).grid(row=0, column=0, pady=20)
        return

    # Three columns
    for column in range(3):
        inside.columnconfigure(column, weight=1, uniform="gallery")

    for index, artwork in enumerate(artworks):
        card = ttk.Frame(inside, padding=8)

        card.grid(
            row=index // 3,
            column=index % 3,
            padx=5,
            pady=10,
            sticky="n"
        )

        image_name = artwork.get("image")
        photo = None

        if isinstance(image_name, str) and image_name.strip() and Image:
            path = BASE_DIR / image_name

            if path.is_file():
                try:
                    with Image.open(path) as img:
                        img.thumbnail((215, 150))
                        photo = ImageTk.PhotoImage(img.copy())
                except (OSError, ValueError):
                    photo = None

        if photo:
            inside.photo_references.append(photo)

            tk.Button(
                card,
                image=photo,
                borderwidth=0,
                cursor="hand2",
                command=lambda a=artwork: show_artwork(a)
            ).pack(pady=(0, 8))
        else:
            ttk.Button(
                card,
                text="Image unavailable",
                command=lambda a=artwork: show_artwork(a)
            ).pack(pady=(45, 50))

        ttk.Button(
            card,
            text=get_info(artwork, "title"),
            command=lambda a=artwork: show_artwork(a)
        ).pack(fill="x")

        ttk.Label(
            card,
            text=get_info(artwork, "artist"),
            wraplength=215,
            anchor="center",
            justify="center"
        ).pack(pady=(4, 0))


def show_artwork(artwork):
    global photo_reference

    clear_screen()

    ttk.Label(
        main,
        text=get_info(artwork, "title"),
        font=("Segoe UI", 22, "bold"),
        wraplength=800
    ).pack(pady=(10, 10))

    ttk.Label(
        main,
        text="Artist: " + get_info(artwork, "artist")
    ).pack(pady=3)

    ttk.Label(
        main,
        text="Date: " + get_info(artwork, "date")
    ).pack(pady=3)

    for key, title in [
        ("medium", "Medium"),
        ("category", "Category"),
        ("description", "Description")
    ]:
        ttk.Label(
            main,
            text=title + ": " + get_info(artwork, key),
            wraplength=780
        ).pack(pady=3)

    photo_reference = None
    image_name = artwork.get("image")
    image_loaded = False

    if isinstance(image_name, str) and image_name.strip() and Image:
        path = BASE_DIR / image_name

        if path.is_file():
            try:
                with Image.open(path) as img:
                    img.thumbnail((650, 280))
                    photo_reference = ImageTk.PhotoImage(
                        img.copy()
                    )

                ttk.Label(
                    main, image=photo_reference
                ).pack(pady=12)

                image_loaded = True

            except (OSError, ValueError):
                image_loaded = False

    if not image_loaded:
        ttk.Label(
            main, text="Image unavailable"
        ).pack(pady=15)

    ttk.Button(
        main,
        text="Back to Browse",
        command=show_browse
    ).pack(pady=10)


def show_search():
    clear_screen()

    ttk.Label(
        main,
        text="Search Collection",
        font=("Segoe UI", 22, "bold")
    ).pack(pady=(15, 15))

    search_entry = ttk.Entry(main, width=40)
    search_entry.pack(pady=10)
    
def show_search():
    clear_screen()

    ttk.Label(
        main,
        text="Search Collection",
        font=("Segoe UI", 22, "bold")
    ).pack(pady=(15, 15))

    # Artwork titles for recognition rather than recall
    artwork_titles = sorted({
        get_info(artwork, "title")
        for artwork in artworks
        if get_info(artwork, "title") != "Not provided"
    })

    search_box = ttk.Combobox(
        main,
        width=40,
        values=artwork_titles
    )
    search_box.pack(pady=10)

    ttk.Label(
        main,
        text="Type an artwork title or choose from the dropdown."
    ).pack(pady=(0, 8))

    ttk.Button(
        main,
        text="Back to Home",
        command=show_home
    ).pack(pady=5)

    results_frame = scrollable_area()

    ttk.Button(
        main,
        text="Search",
        command=lambda: search_artworks(
            search_box.get(), results_frame
        )
    ).pack(before=results_frame.master, pady=5)

    search_box.bind(
        "<Return>",
        lambda event: search_artworks(
            search_box.get(), results_frame
        )
    )

    # Filter dropdown suggestions as the user types
    def update_suggestions(event):
        if event.keysym in ("Up", "Down", "Return", "Escape"):
            return

        typed = search_box.get().strip().lower()

        if typed:
            matches = [
                title for title in artwork_titles
                if typed in title.lower()
            ]
        else:
            matches = artwork_titles

        search_box["values"] = matches

    search_box.bind("<KeyRelease>", update_suggestions)


    
    


def search_artworks(search_text, results_frame):
    for widget in results_frame.winfo_children():
        widget.destroy()

    search_text = search_text.strip().lower()

    if not artworks:
        ttk.Label(
            results_frame,
            text="No artworks are currently available."
        ).pack(pady=5)
        return

    if not search_text:
        ttk.Label(
            results_frame,
            text="Please enter a search term."
        ).pack(pady=5)
        return

    found = False

    for artwork in artworks:
        title = get_info(artwork, "title")
        artist = get_info(artwork, "artist")

        if (
            search_text in title.lower()
            or search_text in artist.lower()
        ):
            ttk.Button(
                results_frame,
                text=title + " - " + artist,
                command=lambda a=artwork: show_artwork(a)
            ).pack(pady=5, fill="x")

            found = True

    if not found:
        ttk.Label(
            results_frame,
            text="No artworks found."
        ).pack(pady=5)


def show_about():
    clear_screen()

    ttk.Label(
        main,
        text="About Museum",
        font=("Segoe UI", 22, "bold")
    ).pack(pady=40)

    ttk.Label(
        main,
        text=(
            "This program is an interactive digital museum "
            "catalogue for Southland Boys' High School."
        ),
        wraplength=750
    ).pack(pady=10)

    ttk.Button(
        main,
        text="Back to Home",
        command=show_home
    ).pack(pady=10)


show_home()
root.mainloop()


