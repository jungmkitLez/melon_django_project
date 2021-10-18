from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Artist)
admin.site.register(ArtistPlaylist)
admin.site.register(ArtistSong)
admin.site.register(GenreBig)
admin.site.register(GenreBigSong)
admin.site.register(GenreDetail)
admin.site.register(GenreDetailSong)
admin.site.register(Playlist)
admin.site.register(PlaylistSong)
admin.site.register(Song)
admin.site.register(PlaylistTag)
admin.site.register(Tag)
