from recommender.rec_models import Recommender

rec = None

def load_recommender():
    global rec
    rec = Recommender()
    rec.make_sparse_matrix()

def get_recommender():
    return rec
