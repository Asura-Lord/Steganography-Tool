

# Steganography Tool - Modern GUI 🔒📷

[![Python Version](https://img.shields.io/badge/python-3.10+-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0-blueviolet)](https://github.com/Asura-Lord/Steganography-Tool)

A modern GUI tool to **hide secret messages in images** and extract them safely. Optional **Fernet encryption** ensures messages remain secure. Perfect for learning steganography, encryption, and cyber awareness.

---

## 🔹 Features

- Hide secret text inside images using **LSB technique**  
- Extract hidden messages from images  
- Optional **Fernet encryption** for secure keys  
- Automatic saving of **encrypted images** and **keys** in `output/` folders  
- Browse for existing `.key` files to decrypt messages  
- Modern, intuitive **GUI interface**  

---

## 📸 Screenshot Preview

<img width="805" height="657" alt="image" src="https://github.com/user-attachments/assets/5b748369-a66b-4a66-8880-dd0ee5e85dcb" />


---

## ⚡ Installation

1. Clone the repository:

```bash
git clone https://github.com/Asura-Lord/Steganography-Tool.git
cd Steganography-Tool
````

2. Install dependencies:

```bash
pip install -r requirements.txt
```

> **Note:** Requires Python 3.10+

---

## 🚀 Usage

Run the tool:

```bash
python main.py
```

**Steps:**

1. Select an image to hide a secret message
2. Enter your secret text in the message box
3. Optionally, check **Encrypt Message (Fernet)**
4. If encrypting, a **key will be generated automatically** and saved in `output/encrypted_keys`
5. Click **Hide / Encrypt Message** to generate the stego-image (saved in `output/encrypted_images`)
6. To extract, click **Extract / Decrypt Message** and optionally select a saved key

---

## 🛠 Tech Stack

* **Python 3.10+**
* **Pillow** → Image processing and manipulation
* **Cryptography (Fernet)** → Optional encryption for secret messages
* **Tkinter** → GUI interface

---

## 💡 Use Cases

* Securely hide confidential messages in images
* Capture The Flag (CTF) challenges
* Learn steganography and encryption basics
* Cybersecurity education and awareness

---

 **"Stay Safe, Stay Dangerous"**

---

## 📁 Folder Structure

```
Steganography-Tool/
├── main.py
├── requirements.txt
├── README.md
├── output/
│   ├── encrypted_images/
│   └── encrypted_keys/
├── screenshots/
```

---

## ⚠️ License

This project is licensed under the **MIT License**.

