
import threading, time, os
try:
    import vlc
    VLC = True
except Exception:
    VLC = False

class CrossFader:
    def __init__(self, player, cross_seconds=6):
        self.player = player
        self.cross_seconds = cross_seconds
        self.lock = threading.Lock()

    def crossfade_play(self, next_path):
        # If VLC available, attempt a simple crossfade by controlling volumes
        if not os.path.exists(next_path):
            return
        if VLC and getattr(self.player,'player',None):
            try:
                instance = vlc.Instance('--no-video-title-show')
                media = instance.media_new(next_path)
                newp = instance.media_player_new()
                newp.set_media(media)
                newp.audio_set_volume(0)
                newp.play()
                # fade out current, fade in new
                for i in range(self.cross_seconds*10):
                    frac = i/(self.cross_seconds*10)
                    try:
                        if getattr(self.player,'player',None):
                            self.player.player.audio_set_volume(int((1-frac)*self.player.volume))
                        newp.audio_set_volume(int(frac* self.player.volume))
                    except Exception:
                        pass
                    time.sleep(0.1)
                # stop old
                try:
                    if getattr(self.player,'player',None):
                        self.player.player.stop()
                except:
                    pass
                self.player.player = newp
            except Exception:
                # fallback to simple play
                self.player.play(next_path)
        else:
            # fallback: simple play next after short delay
            time.sleep(0.5)
            self.player.play(next_path)
