import numpy as np
import pandas as pd
from itertools import chain, combinations
from scipy.sparse import csr_matrix
from collections import Counter, defaultdict
from gensim.models import Word2Vec
import json
from random import sample
import random



class Recommender:
    
    def __init__(self):
        self.song_meta = pd.read_json('./recommender/data/song_meta_pop.json')   # manage.py 가 있는 위치 기준인가봄.
        self.train = pd.read_json('./recommender/data/new_train.json')
        self.all_tags_set = set(chain(*self.train['tags']))
        self.id_to_tag = dict(zip(range(len(self.all_tags_set)), self.all_tags_set))
        self.tag_to_id = dict(zip(self.all_tags_set, range(len(self.all_tags_set)) ))

         #for singer_recommend
        self.artist_w2v_model = Word2Vec.load('./recommender/data/artist_w2v.model')
        self.artist_song_dict = dict(json.loads(open('./recommender/data/artist_song_dict.json', 'r').read()))
        
    def make_sparse_matrix(self):
        tag_cnt = self.train['tags'].apply(lambda x : len(x)).tolist()
        id_tag_lists = [list(map(lambda x : self.tag_to_id[x], tags)) for tags in self.train['tags']]
        
        row = np.repeat(np.arange(len(self.train)), tag_cnt)
        col = np.concatenate(id_tag_lists)
        data = np.ones(col.shape[0])
        
        self.ply_tag = csr_matrix((data,(row,col)))
        
    def tag_recommend(self,input_tags):  
    
        input_tag_id = [self.tag_to_id.get(x) for x in input_tags if self.tag_to_id.get(x) is not None]
        if not input_tag_id:
            # print('입력하신 태그가 모두 존재하지 않습니다.')
            return None

        selected_playlists = []
        for tag_id in input_tag_id:
            # tag_id인 열 가져오기
            temp_list = self.ply_tag[:,tag_id].toarray().reshape(-1)
            # 그 중 1인 것만 playlist에 넣기
            selected_playlists.append(np.argwhere(temp_list == 1).reshape(-1))

        tag_playlist_songs = []
        for playlist in selected_playlists:
            # 태그에 딸린 플레이리스트들의 곡을 합친 리스트.
            temp = np.concatenate(self.train.iloc[playlist]['songs'].tolist())
            tag_playlist_songs.append(temp)

        counts = []
        for song in tag_playlist_songs:
            counts.append(dict(Counter(song)))

        popular_songs_each_tag = []
        for count in counts:
            popular_songs_each_tag.append(sorted(count, key= count.get, reverse = True)[:200])


        # 인풋 태그가 한개면 그냥 상위 30곡 리턴
        input_tag_cnt = len(input_tag_id)
        if input_tag_cnt < 2:
            return self.song_meta.iloc[popular_songs_each_tag[0]]['id'].head(30).tolist()


        # 모든 조합 구하기
        combs = list(chain.from_iterable(combinations(popular_songs_each_tag, r) for r in range(2, (input_tag_cnt + 1))))

        rec_playlist = []
        for comb in combs:
            rec_playlist.extend(list(set.intersection(*map(set,comb))))
        rec_playlist.reverse()


        rec_df = pd.DataFrame(rec_playlist)
        rec_df.drop_duplicates(inplace= True, ignore_index = True)

        if len(rec_df) == 0:
            return None

        return rec_df[0].head(30).tolist()

    def singer_recommend(self, user, rec_songs_cnt = 30, rate_of_familiar_songs = 0.3, artist_sample = 5 , only_singer = False):
        song_cnt_from_fam = int(rec_songs_cnt * rate_of_familiar_songs)
        song_cnt_from_rec = int(rec_songs_cnt * (1-rate_of_familiar_songs))
        
        artist_songs = []
        new_artist_songs = []
        final_recommendation = []
        user_recommend_artists = []
    
        #유저 아티스트 랜덤 샘플 가져오기
        if len(user['artists'].values) > artist_sample:
            user_random_artist_list = random.sample(*user['artists'].values, artist_sample)
        else:
            user_random_artist_list = list(*user['artists'].values)
        
        #유사 가수 찾기 (전체로 찾기)
        temp = self.artist_w2v_model.wv.most_similar(user_random_artist_list, topn = 6)
        user_recommend_artists.extend([x for x , _ in temp])

        # 기존 가수 노래 가져오기
        for artist_ in user_random_artist_list:
            temp_songs = self.song_meta.iloc[self.artist_song_dict[artist_]].sort_values(by= 'popularity', ascending = False)[:10]
            artist_songs.extend(temp_songs['id'])
        # 새 가수 노래 가져오기    
        for artist_ in user_recommend_artists:
            temp_songs = self.song_meta.iloc[self.artist_song_dict[artist_]].sort_values(by= 'popularity', ascending = False)[:10]
            new_artist_songs.extend(temp_songs['id'])
        # 이미 있는 노래는 제거
        artist_songs =  set(artist_songs) - set(*user['songs'])
        
        #노래 샘플로 뽑기
        if len(artist_songs) >= song_cnt_from_fam:
            final_recommendation.extend(sample(artist_songs,  song_cnt_from_fam   ))
        else:
            final_recommendation.extend(artist_songs)

        if len(new_artist_songs) >= song_cnt_from_rec:
            final_recommendation.extend(sample(new_artist_songs,  song_cnt_from_rec    ))
        else:
            final_recommendation.extend(new_artist_songs)
            
        return user_recommend_artists ,final_recommendation