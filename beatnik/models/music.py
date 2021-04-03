from beatnik.api_manager import ApiManager, LinkParser
from django.db import IntegrityError
from django.db.models import Manager, Model, Q, CharField, IntegerField, URLField
from urllib import parse

class MusicManager(Manager):
    def convert(self, music):
        api_manager = ApiManager()
        music = api_manager.convert_link(music)

        return music

    def get_and_populate_existing(self, music):
        query = Q(apple_url = music.apple_url) |\
                Q(soundcloud_url = music.soundcloud_url) |\
                Q(spotify_url = music.spotify_url) |\
                Q(tidal_url = music.tidal_url)

        existing_music = self.filter(query, ~Q(pk = music.pk)).first()

        return self.merge(existing_music, music)

    # get_or_create :: Url -> Music
    def get_or_create(self, url):
        if LinkParser.apple_netloc in url.netloc:
            link = parse.urlunparse(url)
            music, new = super().get_or_create(apple_url=link)
        elif LinkParser.soundcloud_netloc in url.netloc:
            link = parse.urlunparse(url)
            music, new = super().get_or_create(soundcloud_url=link)
        elif LinkParser.spotify_netloc in url.netloc:
            link = parse.urlunparse(url)
            music, new = super().get_or_create(spotify_url=link)
        elif LinkParser.tidal_netloc in url.netloc:
            link = parse.urlunparse(url)
            music, new = super().get_or_create(tidal_url=link)
        else:
            raise ValueError("{0} is not a supported url".format(url))

        if new:
            music = self.convert(music)
            try:
                music.save()
            except IntegrityError as exception:
                existing_music = self.get_and_populate_existing(music)
                music.delete()
                existing_music.save()
                music = existing_music

        return music

    def merge(self, old, new):
        if old is None:
            return new

        if old.artwork is None:
            old.artwork = new.artwork
        if old.apple_url is None:
            old.apple_url = new.apple_url
        if old.soundcloud_url is None:
            old.soundcloud_url = new.soundcloud_url
        if old.spotify_url is None:
            old.spotify_url = new.spotify_url
        if old.tidal_url is None:
            old.tidal_url = new.tidal_url

        return old

    # verify_url :: (6)Tuple -> Boolean
    def verify_url(self, url):
        if (url.scheme == ''):
            return False

        return LinkParser.apple_netloc in url.netloc \
            or LinkParser.soundcloud_netloc in url.netloc \
            or LinkParser.spotify_netloc in url.netloc \
            or LinkParser.tidal_netloc in url.netloc

class Music(Model):
    objects = MusicManager()

    music_type = CharField("Album or Track", max_length = 1, choices=(('A', 'Album'), ('T', 'Track')))
    name = CharField("Track Name", max_length = 200)
    artist = CharField("Artist Name", max_length = 200)
    album = CharField("Album Name", max_length = 200, blank = True)
    apple_url = URLField("Apple Music URL", null = True, unique = True)
    gpm_url = URLField("Google Play Music URL", null = True, unique = True)
    soundcloud_url = URLField("Soundcloud URL", null = True, unique = True)
    spotify_url = URLField("Spotify URL", null = True, unique = True)
    tidal_url = URLField("Tidal URL", null = True, unique = True)
    match_rating = IntegerField("Rating of the match", default = 0)
    artwork = URLField("Album art URL")

    def get_absolute_url(self):
        return "/music/{0}".format(self.id)
