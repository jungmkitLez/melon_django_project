# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Playlist(models.Model):
    playlist_id = models.IntegerField(primary_key=True)
    playlist_title = models.TextField(blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)
    like_cnt = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'playlist'
        ordering = ['-like_cnt']

    def __str__(self):
        return self.playlist_title

class Artist(models.Model):
    artist_id = models.IntegerField(primary_key=True)
    artist_name = models.TextField(blank=True, null=True)
    artist_main_genre = models.TextField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'artist'

    def __str__(self):
        return self.artist_name


class Song(models.Model):
    song_id = models.IntegerField(primary_key=True)
    issue_date = models.TextField(blank=True, null=True)
    album_name = models.TextField(blank=True, null=True)
    album_id = models.IntegerField(blank=True, null=True)
    song_name = models.TextField(blank=True, null=True)
    added_cnt = models.IntegerField(blank=True, null=True)
    thumb_url = models.TextField(blank=True, null=True)
    artists = models.ManyToManyField(Artist, related_name='songs', through = "ArtistSong")

    class Meta:
        managed = False
        db_table = 'song'

    def __str__(self):
        return self.song_name
    
class Tag(models.Model):
    tag_id = models.IntegerField(primary_key=True)
    tag = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tag'


class ArtistPlaylist(models.Model):
    playlist = models.ForeignKey(Playlist, models.DO_NOTHING, blank=True, null=True)
    artist = models.ForeignKey(Artist, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'artist_playlist'


class ArtistSong(models.Model):
    song = models.ForeignKey(Song, models.DO_NOTHING, blank=True, null=True)
    artist = models.ForeignKey(Artist, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'artist_song'


class GenreBig(models.Model):
    genre_big_id = models.IntegerField(primary_key=True)
    genre_big_code = models.TextField(blank=True, null=True)
    genre_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'genre_big'


class GenreBigSong(models.Model):
    genre_big = models.ForeignKey(GenreBig, models.DO_NOTHING, blank=True, null=True)
    song = models.ForeignKey(Song, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'genre_big_song'


class GenreDetail(models.Model):
    genre_detail_id = models.IntegerField(primary_key=True)
    genre_detail_code = models.TextField(blank=True, null=True)
    genre_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'genre_detail'


class GenreDetailSong(models.Model):
    genre_detail = models.ForeignKey(GenreDetail, models.DO_NOTHING, blank=True, null=True)
    song = models.ForeignKey(Song, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'genre_detail_song'


class PlaylistSong(models.Model):
    playlist = models.ForeignKey(Playlist, models.DO_NOTHING, blank=True, null=True)
    song = models.ForeignKey(Song, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'playlist_song'


class PlaylistTag(models.Model):
    tag = models.ForeignKey(Tag, models.DO_NOTHING, blank=True, null=True)
    playlist = models.ForeignKey(Playlist, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'playlist_tag'



    


