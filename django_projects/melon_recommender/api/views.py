from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, response
from api.rec_model_loader import get_recommender
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Song
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




#query = '''select song_id,artist.artist_id,artist_name,song_name,artist_name,artist_main_genre from (select song.song_id,artist_id,song_name from (select psll.song_id,artist_id from (select psl.song_id from (select song_id,update_date from (select playlist_id,update_date from playlist where update_date > '2020-01-01' and update_date < '2020-04-01') as p join playlist_song as ps on p.playlist_id = ps.playlist_id) as psl join song as s on psl.song_id = s.song_id) as psll join artist_song as asl on psll.song_id = asl.song_id) as sl join song on sl.song_id = song.song_id) as ss join artist on ss.artist_id = artist.artist_id;'''
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