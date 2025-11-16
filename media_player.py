import os, threading, time
try:
    import vlc
    VLC_AVAILABLE = True
except Exception:
    VLC_AVAILABLE = False

class MediaPlayer:
    def __init__(self):
        self.current = None
        self.state = 'stopped'
        self.player = None
        self.lock = threading.Lock()
        self.volume = 80

    def play(self, path):
        with self.lock:
            if not os.path.exists(path):
                print('File not found', path); return
            print('Playing', path)
            self.current = path
            self.state = 'playing'
            if VLC_AVAILABLE:
                instance = vlc.Instance('--no-video-title-show')
                media = instance.media_new(path)
                p = instance.media_player_new()
                p.set_media(media)
                try:
                    p.audio_set_volume(self.volume)
                except:
                    pass
                p.play()
                self.player = p
                threading.Thread(target=self._watch, args=(p,), daemon=True).start()
            else:
                threading.Thread(target=self._fake_play, args=(path,), daemon=True).start()

    def _fake_play(self, path):
        time.sleep(5)
        self.on_end()

    def _watch(self, p):
        try:
            while True:
                st = p.get_state()
                if st in (6,3,7): break
                time.sleep(0.5)
        except Exception:
            pass
        self.on_end()

    def on_end(self):
        print('Track finished', self.current)
        self.current = None
        self.state = 'stopped'

    def stop(self):
        with self.lock:
            if self.player:
                try: self.player.stop()
                except: pass
            self.state = 'stopped'
            self.current = None

    def set_volume(self, v):
        self.volume = int(v)
        if self.player and VLC_AVAILABLE:
            try: self.player.audio_set_volume(self.volume)
            except: pass
