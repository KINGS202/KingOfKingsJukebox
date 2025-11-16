import random, os
class RecommendationEngine:
    def __init__(self): pass
    def more_like_this(self, filepath, count=10):
        base = os.path.join('media','songs')
        allf = []
        for root,_,files in os.walk(base):
            for f in files:
                if f.lower().endswith(('.mp3','.wav')):
                    allf.append(os.path.join(root,f))
        if filepath in allf:
            allf.remove(filepath)
        random.shuffle(allf)
        return allf[:count]
