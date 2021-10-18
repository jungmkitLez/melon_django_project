from rest_framework import serializers
from .models import Song, Artist


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('artist_name',) 

class SongSerializer(serializers.ModelSerializer):
    artists = ArtistSerializer(read_only = True, many = True)
    class Meta:
        model = Song
        fields = ('song_name', 'artists',)