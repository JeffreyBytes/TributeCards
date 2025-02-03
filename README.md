# TributeCards - ESO Tales of Tribute Card Generator

This project is a **Python-based tool** for generating card images for **Tales of Tribute**, a card game from *The Elder Scrolls Online (ESO)*.

🔹 **Primarily designed for generating card art for the [UESP Wiki](https://en.uesp.net/wiki/Main_Page)** to document Tribute cards in a consistent style.  
🔹 Can also be used for **personal projects**, such as custom Tribute decks.

## 📌 Features
- **Automated Card Rendering** – Generates full card images using layered assets.
- **Mechanic Handling** – Correctly places play, combo, and while-in-play effects.
- **Modular & Extensible** – Designed to allow easy customization and expansion.

---

## 📂 Folder Structure
```
TributeCards/
│── assets/             # (Folder for game assets, NOT included in repo) 
│ ├── cards/            # Stores card art assets 
│ ├── fonts/            # Contains required fonts 
│ ├── mechanics/        # Icons for card effects 
│ ├── patrons/          # Patron suit assets
│── decks/              # JSON definitions for each Tribute deck
│── output/             # Stores generated card images 
│── scripts/            # Main Python scripts for rendering 
│── requirements.txt    # Python dependencies
```

---

## 🚀 Getting Started

### 1️⃣ **Clone the Repository**
```bash
git clone https://github.com/JeffreyBytes/TributeCards.git
cd TributeCards
```

### 2️⃣ **Install Dependencies**
Make sure you have Python installed, then run:
```bash
pip install -r requirements.txt
```

### 3️⃣ **Add Assets**
Place the required asset files inside the `assets/` folder.

#### Where to Get the Assets?
The game assets **are not included in this repository** due to legal reasons.

To generate the cards, you will need:
- ESO game files (Tales of Tribute assets)

OR

- Custom art assets that match the official dimensions

🔹 **I will not provide direct links or instructions**, but a quick search for ESO modding tools should help.

---

## ⚙️ Usage
Define the deck in `./decks/<deck_name>.json` (see the existing files for an example).

Run the script to generate card images:
```bash
python scripts/main.py
```

---

## 🛠️ Configuration
You can modify constants.py to adjust:
- Default asset paths
- Font settings
- Card layout adjustments

---

## 🎯 Future Improvements

- Complete all official card decks
- More automation & batch processing
- Better asset management tools

--- 

## 💡 Contributing

Pull requests are welcome! If you have suggestions, feel free to open an issue.

---

## 📜 License

This project is **not affiliated with Zenimax/Bethesda**. It is a fan-made tool for personal use.

This project is licensed under the **GNU General Public License v3.0** (GPLv3).
You are free to use, modify, and distribute this software under the terms of the license.

🔗 See the full license in the [LICENSE](LICENSE) file.

---

## ⭐ Like the project? Consider giving it a star! ⭐