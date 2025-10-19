# main.py
import os
from tkinter import Tk, Label, Entry, Text, Button, filedialog, messagebox, IntVar, Checkbutton, Frame
from PIL import Image
from cryptography.fernet import Fernet

# ------------------- Folder Setup -------------------
os.makedirs("output/encrypted_images", exist_ok=True)
os.makedirs("output/encrypted_keys", exist_ok=True)

# ------------------- Steganography Functions -------------------
def text_to_bin(text):
    return ''.join([format(ord(c), '08b') for c in text])

def bin_to_text(binary):
    chars = [chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8)]
    return ''.join(chars)

def hide_secret_in_image(img_path, secret, save_path, key=None):
    img = Image.open(img_path)
    img = img.convert('RGB')
    pixels = img.load()

    if key:
        f = Fernet(key)
        secret = f.encrypt(secret.encode()).decode()

    binary_secret = text_to_bin(secret) + '1111111111111110'  # EOF marker
    data_index = 0
    for y in range(img.height):
        for x in range(img.width):
            if data_index >= len(binary_secret):
                break
            r, g, b = pixels[x, y]
            r = (r & ~1) | int(binary_secret[data_index])
            data_index += 1
            if data_index < len(binary_secret):
                g = (g & ~1) | int(binary_secret[data_index])
                data_index += 1
            if data_index < len(binary_secret):
                b = (b & ~1) | int(binary_secret[data_index])
                data_index += 1
            pixels[x, y] = (r, g, b)
        if data_index >= len(binary_secret):
            break

    img.save(save_path)

def extract_secret_from_image(img_path, key=None):
    img = Image.open(img_path)
    img = img.convert('RGB')
    pixels = img.load()
    binary_data = ''
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = pixels[x, y]
            binary_data += str(r & 1)
            binary_data += str(g & 1)
            binary_data += str(b & 1)

    eof_index = binary_data.find('1111111111111110')
    if eof_index == -1:
        raise ValueError("No hidden message found")
    binary_data = binary_data[:eof_index]

    message = bin_to_text(binary_data)
    if key:
        f = Fernet(key)
        message = f.decrypt(message.encode()).decode()
    return message

# ------------------- GUI Functions -------------------
def browse_image():
    path = filedialog.askopenfilename(title="Select Image", filetypes=[("PNG Images", "*.png"), ("All Files", "*.*")])
    if path:
        img_entry.delete(0, 'end')
        img_entry.insert(0, path)

def browse_key():
    path = filedialog.askopenfilename(title="Select Key File", filetypes=[("Key Files", "*.key")])
    if path:
        with open(path, "rb") as f:
            key_data = f.read()
        key_entry.delete(0, 'end')
        key_entry.insert(0, key_data.decode())

def hide_message_action():
    img_path = img_entry.get()
    secret = msg_entry.get("1.0", "end").strip()
    use_encryption = encrypt_var.get()
    key_text = key_entry.get().strip()

    if not img_path or not secret:
        messagebox.showwarning("Error", "Please select an image and enter a secret message!")
        return

    # Handle encryption key
    key_bytes = None
    if use_encryption:
        if key_text:
            key_bytes = key_text.encode()
        else:
            key_bytes = Fernet.generate_key()
            messagebox.showinfo("Generated Key", f"Save this key to decrypt later:\n{key_bytes.decode()}")
        # Save key automatically
        key_file = os.path.join("output/encrypted_keys", f"key_{os.path.basename(img_path)}.key")
        with open(key_file, "wb") as kf:
            kf.write(key_bytes)

    # Save stego image automatically
    stego_path = os.path.join("output/encrypted_images", f"hidden_{os.path.basename(img_path)}")
    hide_secret_in_image(img_path, secret, stego_path, key=key_bytes)

    messagebox.showinfo("Success", f"Secret message hidden!\nSaved as {stego_path}")

def extract_message_action():
    img_path = filedialog.askopenfilename(title="Select Stego Image", filetypes=[("PNG Images", "*.png")])
    if not img_path:
        return
    key_text = key_entry.get().strip()
    key_bytes = key_text.encode() if key_text else None
    try:
        message = extract_secret_from_image(img_path, key=key_bytes)
        messagebox.showinfo("Hidden Message", message)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# ------------------- Main GUI -------------------
root = Tk()
root.title("Steganography Tool - Modern GUI")
root.geometry("650x500")

# Image selection
Label(root, text="Select Image:").pack(pady=5)
img_entry = Entry(root, width=50)
img_entry.pack()
Button(root, text="Browse Image", command=browse_image).pack(pady=5)

# Secret message
Label(root, text="Secret Message:").pack(pady=5)
msg_entry = Text(root, height=5, width=50)
msg_entry.pack(pady=5)

# Encryption option
encrypt_var = IntVar()
Checkbutton(root, text="Encrypt Message (Fernet)", variable=encrypt_var).pack(pady=5)

# Key entry with browse
Label(root, text="Encryption Key (optional, leave blank to auto-generate):").pack(pady=5)
key_frame = Frame(root)
key_frame.pack(pady=5)

key_entry = Entry(key_frame, width=40)
key_entry.pack(side='left', padx=5)

Button(key_frame, text="Browse Key", command=browse_key).pack(side='left', padx=5)

# Action buttons
Button(root, text="Hide / Encrypt Message", command=hide_message_action).pack(pady=10)
Button(root, text="Extract / Decrypt Message", command=extract_message_action).pack(pady=5)

root.mainloop()
