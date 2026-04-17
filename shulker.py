import tkinter as tk
from tkinter import messagebox
import pyperclip
import os
import sys
import pathlib

APP_VERSION = "1.0.0"

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def normalize_item(item: str) -> str:
    item = item.strip()

    if not item:
        raise ValueError("empty")

    if " " in item:
        raise ValueError("spaces")

    if ":" not in item:
        item = f"minecraft:{item}"

    return item


def generate_command():
    item = item_entry.get()
    count_input = count_entry.get().strip()

    try:
        item = normalize_item(item)
    except ValueError as e:
        if str(e) == "empty":
            messagebox.showerror("Error", "Please enter an item ID.")
        elif str(e) == "spaces":
            messagebox.showerror("Error", "Item ID cannot contain spaces.")
        return

    try:
        count = int(count_input) if count_input else 64
    except ValueError:
        messagebox.showerror("Error", "Count must be a number.")
        return

    slots = []
    for slot in range(27):
        slot_data = f'{{slot:{slot},item:{{id:"{item}",count:{count}}}}}'
        slots.append(slot_data)

    container_data = ",".join(slots)
    command = f'/give @p shulker_box[container=[{container_data}]] 1'

    # Show in output box
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, command)

    #  Only copy if checkbox is ticked
    if copy_var.get():
        pyperclip.copy(command)
        messagebox.showinfo("Done", "Command copied to clipboard!")
    else:
        messagebox.showinfo("Done", "Command generated!")


# --- GUI setup ---
root = tk.Tk()
root.title("Shulker Box Generator")
root.geometry("500x420")
tk.Label(root, text=f"Version {APP_VERSION}").pack()

icon_path = pathlib.Path(resource_path("icon.ico")).resolve()

if icon_path.exists():
    try:
        root.iconbitmap(str(icon_path))
    except:
        try:
            root.wm_iconbitmap(str(icon_path))
        except:
            pass

# Item input
tk.Label(root, text="Item ID:").pack(pady=5)
item_entry = tk.Entry(root, width=40)
item_entry.insert(0, "minecraft:stone")
item_entry.pack()

# Count input
tk.Label(root, text="Stack Count (default 64):").pack(pady=5)
count_entry = tk.Entry(root, width=20)
count_entry.pack()

#  Checkbox variable
copy_var = tk.BooleanVar(value=True)  # default ON

#  Checkbox itself
tk.Checkbutton(root, text="Copy to clipboard?", variable=copy_var).pack(pady=5)

# Generate button
tk.Button(root, text="Generate", command=generate_command).pack(pady=15)

# Output box
output_text = tk.Text(root, height=10, wrap="word")
output_text.pack(padx=10, pady=10)

root.mainloop()