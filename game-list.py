import os
import json
import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def clean_name(filename):
    name = os.path.splitext(filename)[0]

    # Trim whitespace
    name = name.strip()

    # Remove leading 'cl' ONLY if it is the first two letters
    if name.lower().startswith("cl"):
        name = name[2:]

    # Split camelCase
    name = re.sub(r'([a-z])([A-Z])', r'\1 \2', name)

    # Add spaces between numbers and letters
    name = re.sub(r'(\d)([a-zA-Z])', r'\1 \2', name)
    name = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', name)

    # Replace separators
    name = re.sub(r'[_\-]+', ' ', name)

    # Clean extra spaces
    name = re.sub(r'\s+', ' ', name)

    return name.title().strip()

def generate_json():
    games_dir = games_path.get()
    images_dir = images_path.get()

    if not os.path.isdir(games_dir):
        messagebox.showerror("Error", "Invalid games folder")
        return

    games = []

    for file in os.listdir(games_dir):
        if not file.endswith(".html"):
            continue

        game_name = clean_name(file)
        image_path = None

        if images_dir and os.path.isdir(images_dir):
            base = os.path.splitext(file)[0]
            for ext in ("png", "jpg", "jpeg", "webp"):
                img = os.path.join(images_dir, f"{base}.{ext}")
                if os.path.exists(img):
                    image_path = img
                    break

        games.append({
            "name": game_name,
            "path": os.path.join(games_dir, file),
            "image": image_path,
            "tier": "not_checked",
            "popularity": 0
        })

    with open("games.json", "w", encoding="utf-8") as f:
        json.dump(games, f, indent=2)

    preview.delete(*preview.get_children())
    for g in games[:20]:
        preview.insert("", "end", values=(g["name"], g["path"], g["image"]))

    messagebox.showinfo("Done", f"Generated games.json with {len(games)} games")

# ---------------- UI ----------------

root = tk.Tk()
root.title("HTML Game JSON Generator")
root.geometry("900x500")

games_path = tk.StringVar()
images_path = tk.StringVar()

frm = ttk.Frame(root, padding=10)
frm.pack(fill="x")

ttk.Label(frm, text="Games Folder:").grid(row=0, column=0, sticky="w")
ttk.Entry(frm, textvariable=games_path, width=70).grid(row=0, column=1)
ttk.Button(frm, text="Browse", command=lambda: games_path.set(
    filedialog.askdirectory())).grid(row=0, column=2)

ttk.Label(frm, text="Images Folder (optional):").grid(row=1, column=0, sticky="w")
ttk.Entry(frm, textvariable=images_path, width=70).grid(row=1, column=1)
ttk.Button(frm, text="Browse", command=lambda: images_path.set(
    filedialog.askdirectory())).grid(row=1, column=2)

ttk.Button(root, text="Generate JSON", command=generate_json).pack(pady=10)

preview = ttk.Treeview(root, columns=("Name", "Path", "Image"), show="headings")
preview.heading("Name", text="Game Name")
preview.heading("Path", text="HTML Path")
preview.heading("Image", text="Image Path")
preview.pack(fill="both", expand=True, padx=10, pady=10)

root.mainloop()
