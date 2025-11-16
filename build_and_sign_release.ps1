# Simplified build script - customize paths and PFX
python -m pip install --upgrade pip
pip install pyinstaller kivy python-vlc flask pyjwt pillow
pyinstaller --noconfirm --onefile --windowed --name KingOfKingsJukebox main.py
