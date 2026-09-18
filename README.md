# Spotify Cache Recover

A lightweight desktop utility for Windows that extracts track URIs from Spotify's local cache files (`list_player_play_history`) so you can quickly restore your recent listening history into a new playlist.

I built this app after my Spotify account was deleted without warning, leaving me with no easy way to get my recent tracks back.

---

### Features
* **Automated & Manual Search:** Automatically checks default Spotify cache locations or lets you select the cache file manually.
* **Smart Parsing:** Deduplicates track IDs while preserving play order.
* **One-Click Export:** Copies formatted Spotify URIs straight to your clipboard for instant pasting.
* **Bilingual UI:** Easily switch between English and Russian.

---

### How to Use

1. Run **`SpotifyCacheRecover.exe`** (or execute `app.py` from source).
2. The app will automatically scan for your cache file. If found, click **Copy URLs to Clipboard**.
3. Open Spotify, create a **New Playlist**, and press `Ctrl + V`.

> **Note:** If the auto-search fails, locate your cache file manually at:
> `C:\Users\<Username>\AppData\Local\Spotify\Users\<User_ID>\list_player_play_history`

---

### Running & Building from Source

```bash
# Clone repository
git clone [https://github.com/lov3llama/SpotifyCacheRecover.git](https://github.com/lov3llama/SpotifyCacheRecover.git)
cd SpotifyCacheRecover

# Run application
python app.py

# Build executable using PyInstaller
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed --name "SpotifyCacheRecover" app.py
```

---

### Support & Feedback
If this tool saved your playlist, feel free to drop a star on the repository or support the project via [PayPal](https://paypal.me/lov3llama).
