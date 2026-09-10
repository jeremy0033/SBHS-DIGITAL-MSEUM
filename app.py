import tkinter as tk

root = tk.Tk()

root.title("SBHS Digital Museum")
root.geometry("900x600")
import tkinter as tk
from tkinter import ttk

# Create the main window
root = tk.Tk()
root.title("SBHS Digital Museum")
root.geometry("900x600")

# Create a main frame
main = ttk.Frame(root, padding=20)
main.pack(fill="both", expand=True)

# Museum heading
title_label = ttk.Label(
    main,
    text="SBHS DIGITAL MUSEUM",
    font=("Segoe UI", 24, "bold")
)
title_label.pack(pady=(80, 10))

# Small description
subtitle_label = ttk.Label(
    main,
    text="Explore the Southland Boys' High School art collection",
    font=("Segoe UI", 11)
)
subtitle_label.pack(pady=(0, 30))

# Navigation buttons
browse_btn = ttk.Button(main, text="Browse Collection")
browse_btn.pack(pady=5)

search_btn = ttk.Button(main, text="Search Collection")
search_btn.pack(pady=5)

about_btn = ttk.Button(main, text="About Museum")
about_btn.pack(pady=5)

# Keep the program running
root.mainloop()
root.mainloop()

