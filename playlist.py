import json, os
class PlaylistManager:
    def __init__(self, player):
        self.player = player
        self.queue = []
        self.playlist_file = os.path.join('data','playlist.json')
        os.makedirs('data', exist_ok=True)

    def add(self, path):
        if path and os.path.exists(path):
            self.queue.append(path)
            self._save()

    def pop_next(self):
        if self.queue:
            p = self.queue.pop(0)
            self._save(); return p
        return None

    def _save(self):
        with open(self.playlist_file,'w') as f: json.dump(self.queue,f)
