import os
class LibraryScanner:
    def __init__(self, media_dir=None):
        self.media_dir = media_dir or os.path.join('media','songs')
        self.index = []

    def full_scan(self):
        self.index = []
        if os.path.exists(self.media_dir):
            for root,_,files in os.walk(self.media_dir):
                for f in files:
                    if f.lower().endswith(('.mp3','.wav','.m4a','.flac','.ogg','.mp4')):
                        self.index.append(os.path.join(root,f))
        print('Library scanned, found', len(self.index), 'items')
        return self.index
