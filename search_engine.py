import os

def smart_search(query, media_dir=None):
    if media_dir is None: media_dir = os.path.join('media','songs')
    results = []
    q = query.lower()
    for root,_,files in os.walk(media_dir):
        for f in files:
            if q in f.lower():
                results.append(os.path.join(root,f))
    return results

class SearchEngine:
    def search(self, q):
        return smart_search(q)
