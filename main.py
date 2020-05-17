from deezerapp import DeezerApp

if __name__ == '__main__':
    deez = DeezerApp()
    x = deez.track_names(deez.search('Imagine dragons'))
    #print(*x, sep='\n')

    tracks = deez.chart_tracks(region='Russia', limit=1000)

    print('id\ttitle\tartist\talbum\tfans\trelease_date\tgenre')

    print(*deez.track_names(tracks), sep='\n')