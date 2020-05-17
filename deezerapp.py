import deezer
import time


class DeezerApp:
    def __init__(self):
        self.full_cool_down_time = time.clock()
        self.track_info = {}
        self.album_info = {}
        self.artist_info = {}
        self.playlist_info = {}
        self.genre_info = {}

        self.chart_id = {}
        with open('.charts', 'r') as f:
            output = f.read()
            lines = output.split('\n')
            for line in lines:
                c_name, c_id = line.split()
                self.chart_id[c_name] = c_id

        with open('.deezerapp', 'r') as f:
            app_id, app_secret = f.read().split('\n')
        self.client = deezer.Client(app_id=app_id, app_secret=app_secret)

    def search(self, s): # returns list of tracks
        return self.client.search(s)

    def chart_tracks(self, region='Worldwide', limit=10): # returns list of tracks
        if region not in self.chart_id.keys():
            return ["I don't know this region"]
        ids = self.tracks_from_playlist(self.chart_id[region], limit=limit)
        return ids

    def tracks_from_playlist(self, playlist_id, limit=10):
        tracks = self.client.get_playlist(playlist_id).tracks
        return tracks[:min(limit, len(tracks))]

    def track_names(self, tracks):
        if type(tracks) == deezer.Track:
            tracks = [tracks]
        res = []
        for t in tracks:
            self.update_track(t.id)
            self.update_album(t.album.id)
            genre_id = self.album_info[t.album.id].genre_id
            self.update_genre(genre_id)
            res.append('{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(
                    t.id, # deezer id
                    self.track_info[t.id].title, # track title
                    self.track_info[t.id].artist.name, # artist
                    self.album_info[t.album.id].title, # album
                    self.album_info[t.album.id].fans, # album fans
                    self.track_info[t.id].release_date, # release date
                    self.genre_info[genre_id].name # genre
                ))
        return res

    def get_options(self, deezer_obj):
        if type(deezer_obj) == deezer.Artist:
            self.update_artist(deezer_obj.id)
            return set(self.artist_info[deezer_obj.id].__dict__['_fields']) & self.artist_opts
        elif type(deezer_obj) == deezer.Album:
            self.update_album(deezer_obj.id)
            return set(self.album_info[deezer_obj.id].__dict__['_fields']) & self.album_opts
        elif type(deezer_obj) == deezer.Track:
            self.update_track(deezer_obj.id)
            res = set(self.track_info[deezer_obj.id].__dict__['_fields']) & self.track_opts
            res.add('download')
            return res
        elif type(deezer_obj) == deezer.Playlist:
            self.update_playlist(deezer_obj.id)
            return set(self.playlist_info[deezer_obj.id].__dict__['_fields']) & self.playlist_opts
        else:
            return []

    def update_genre(self, genre_id):
        if genre_id not in self.genre_info.keys():
            self.genre_info[genre_id] = self.client.get_genre(genre_id)
        return self.genre_info[genre_id]

    def update_artist(self, artist_id):
        if artist_id not in self.artist_info.keys():
            self.artist_info[artist_id] = self.client.get_artist(artist_id)
        return self.artist_info[artist_id]

    def update_album(self, album_id):
        if album_id not in self.album_info.keys():
            self.album_info[album_id] = self.client.get_album(album_id)
        return self.album_info[album_id]

    def update_track(self, track_id):
        if track_id not in self.track_info.keys():
            self.track_info[track_id] = self.client.get_track(track_id)
        return self.track_info[track_id]

    def update_playlist(self, playlist_id):
        if playlist_id not in self.playlist_info.keys():
            self.playlist_info[playlist_id] = self.client.get_playlist(playlist_id)
        return self.playlist_info[playlist_id]
