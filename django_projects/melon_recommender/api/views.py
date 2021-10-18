from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, response
from api.rec_model_loader import get_recommender
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Song,RecentSongs
from .serializers import *
from users.models import UserPlaylist
import json 



class TagSongRecommend(APIView):
    def get(self, request, *args, **kwargs):
        tags = request.GET.get('tags')
        tag_list = tags.split()
        
        rec = get_recommender()
        song_list = rec.tag_recommend(tag_list)
        serializer =  SongSerializer( Song.objects.filter(song_id__in= song_list),many = True)

        return Response(serializer.data)

class SingerRecommend(APIView):
    def get(self, request, *args, **kwargs):
        rec = get_recommender()
        if request.user.is_authenticated:
            user = request.user
            # user_playlist_id = UserPlaylist.objects.get(user = user.username).playlist.playlist_id
            user_playlist_id = user.user_playlist.playlist.playlist_id
            user_playlist = rec.train.iloc[[user_playlist_id]]
        else:
            user_playlist = rec.train.sample(1)

        artist_list ,song_list = rec.singer_recommend(user_playlist)

        artist_serializer = ArtistSerializer(Artist.objects.filter(artist_name__in = artist_list), many = True) #이름으로 하면 안되는데...새로 recommender를 만들어야 할듯
        song_serializer = SongSerializer(Song.objects.filter(song_id__in= song_list),many = True)
        
        data = {
            'artists' : artist_serializer.data,
            'songs' : song_serializer.data,
        }
        
        return Response(data)

def index(request):
    
    query = '''select 1 id,artist_name, artist_main_genre,artist_id,song_id,song_name,thumb_url,cnt,genre_big_name from (select artist_name, artist_main_genre, artist_id,lng.song_id,song_name,cnt,thumb_url from (select artist_name, artist_main_genre, ars_cnt.artist_id, song_id, cnt from (select artist_id, s_cnt.song_id, cnt from (select song_id , count(song_id) as cnt  from (select playlist_id,update_date,like_cnt from playlist where like_cnt > 30 and update_date between '2020-01-01' and '2020-04-23' ) as rp join playlist_song as ps on rp.playlist_id = ps.playlist_id group by song_id order by cnt desc limit 10) as s_cnt join artist_song as ars on s_cnt.song_id = ars.song_id) as ars_cnt join artist on artist.artist_id = ars_cnt.artist_id) as lng join song on lng.song_id = song.song_id) as llng join genre_big as gb on gb.genre_big_code = llng.artist_main_genre order by cnt desc;'''
    results = RecentSongs.objects.raw(query)
    context = {
        "tsong_qset" : results,
        "tsong_js" : json.dump([result.json() for result in results]),
        'length' : len(results)
    }

    from django.core import serializers
    data = serializers.serialize('json', UserMcqAnswer.objects.raw(query), fields=('some_field_you_want', 'another_field', 'and_some_other_field'))


    return render(request, 'melon_recommender/index.html',context)


#query = '''select 1 id song_id,artist.artist_id,artist_name,song_name,artist_name,artist_main_genre from (select song.song_id,artist_id,song_name from (select psll.song_id,artist_id from (select psl.song_id from (select song_id,update_date from (select playlist_id,update_date from playlist where update_date > '2020-01-01' and update_date < '2020-04-01') as p join playlist_song as ps on p.playlist_id = ps.playlist_id) as psl join song as s on psl.song_id = s.song_id) as psll join artist_song as asl on psll.song_id = asl.song_id) as sl join song on sl.song_id = song.song_id) as ss join artist on ss.artist_id = artist.artist_id;'''
#data = serializers.serialize('json',Song.objects.raw(query))

# # Create your views here.
# def api_tag_recommend(request):
    
#     if request.method == 'GET':
        
#         tags = request.GET.get('tags')
#         tag_list = tags.split()

#         rec = get_recommender()
#         song_list = rec.tag_recommend(tag_list)
#         print(song_list)
#         # song_string = " ".join(song_list)

#         context = {
#             "songs" : [song_list]
#         }

#     return HttpResponse(json.dumps(context), content_type="application/json")


# def api_singer_recommend(request):
#     if request.method == 'GET':
#         rec = get_recommender()
#         if request.user.is_authenticated:
#             user = request.user
#             # user_playlist_id = UserPlaylist.objects.get(user = user.username).playlist.playlist_id
#             user_playlist_id = user.user_playlist.playlist.playlist_id
#             user_playlist = rec.train.iloc[[user_playlist_id]]
#         else:
#             user_playlist = rec.train.sample(1)
        
#         print(user_playlist)
#         song_list = rec.singer_recommend(user_playlist)
#         print(song_list)

#         queryset = Song.objects.filter(song_id__in = song_list)
#         rec_songs = []
#         for song in queryset.iterator():
#             data = {
#                 "song_name" : song.song_name,
#                 "artist_name": [a.artist_name for a in song.artists.all()],
#             }
#             rec_songs.append(data)

#         print(rec_songs)

#     return HttpResponse(json.dumps({"songs": [rec_songs] }), content_type="application/json")


# class SingerSongRecommend(APIView):
#     def get(self, request, *args, **kwargs):
#         rec = get_recommender()
#         if request.user.is_authenticated:
#             user = request.user
#             # user_playlist_id = UserPlaylist.objects.get(user = user.username).playlist.playlist_id
#             user_playlist_id = user.user_playlist.playlist.playlist_id
#             user_playlist = rec.train.iloc[[user_playlist_id]]
#         else:
#             user_playlist = rec.train.sample(1)

#         _ ,song_list = rec.singer_recommend(user_playlist)
#         serializer = SongSerializer(Song.objects.filter(song_id__in= song_list),many = True)

#         return Response(json.dumps(serializer.data,ensure_ascii = False))