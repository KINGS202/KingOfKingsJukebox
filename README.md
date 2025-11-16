# KingOfKings Jukebox — Final Build
This build contains a more complete skeleton for the jukebox.

## Enhancements added (v1.1.0)
- Crossfader Auto-DJ (engine/crossfader_adv.py)
- Karaoke engine stub and dual-screen helper (engine/karaoke.py, engine/dual_display.py)
- React admin UI with JWT token endpoint
- Polished KV widgets and layouts

## Run locally
1. python -m venv venv
2. Windows: .\\venv\\Scripts\\Activate.ps1
3. pip install kivy python-vlc flask pyjwt pillow
4. python server/admin_server.py
5. python main.py
