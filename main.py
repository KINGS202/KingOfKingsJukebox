from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
import os, json
from engine.library_scanner import LibraryScanner
from engine.media_player import MediaPlayer
from engine.playlist import PlaylistManager
from engine.search_engine import SearchEngine
from engine.recommendations import RecommendationEngine

class HomeScreen(Screen): pass
class SearchScreen(Screen): pass
class GenreScreen(Screen): pass
class KaraokeScreen(Screen): pass
class AdminScreen(Screen): pass

class KingScreenManager(ScreenManager): pass

class KingOfKingsApp(App):
    def build(self):
        cfg_path = os.path.join('config','settings.json')
        if os.path.exists(cfg_path):
            with open(cfg_path,'r') as f:
                self.settings = json.load(f)
        else:
            self.settings = {'fullscreen':False,'theme':'king_modern'}

        if self.settings.get('fullscreen', False):
            Window.fullscreen = True
        else:
            Window.size = (1280, 720)

        self.scanner = LibraryScanner()
        self.player = MediaPlayer()
        self.playlist = PlaylistManager(self.player)
        self.search = SearchEngine()
        self.recommend = RecommendationEngine()

        self.scanner.full_scan()
        # start queue watcher for admin remote control
        import threading
        threading.Thread(target=self._watch_admin_queue, daemon=True).start()


        Builder.load_file('kv/main.kv')
        Builder.load_file('kv/theme_manager.kv')

        sm = KingScreenManager(transition=FadeTransition())
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(SearchScreen(name='search'))
        sm.add_widget(GenreScreen(name='genres'))
        sm.add_widget(KaraokeScreen(name='karaoke'))
        sm.add_widget(AdminScreen(name='admin'))

        return sm

    def _watch_admin_queue(self):
        import time, json, os
        qpath = os.path.join('data','queue.json')
        while True:
            try:
                if os.path.exists(qpath):
                    with open(qpath,'r') as f:
                        q = json.load(f) or []
                    if q:
                        # pop first and play
                        song = q.pop(0)
                        with open(qpath,'w') as f: json.dump(q,f)
                        if os.path.exists(song):
                            print('Admin queue requested play:', song)
                            self.playlist.add(song)
                            # if nothing playing, start
                            if self.player.state != 'playing':
                                nxt = self.playlist.pop_next()
                                if nxt: self.player.play(nxt)
                time.sleep(2)
            except Exception as e:
                print('Queue watch error', e)
                time.sleep(5)

if __name__ == '__main__':
    KingOfKingsApp().run()
