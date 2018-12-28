from django.shortcuts import render


def extract_time(json):
    import datetime
    try:
        # Also convert to int since update_time will be string.  When comparing
        # strings, "10" is smaller than "2".
        print(json['released'])
        return datetime.datetime.strptime(json['released'], "%Y-%m-%d %H:%M:%S")
    except Exception:
        return datetime.datetime(1, 1, 1)


# Create your views here.
def home(request):
    import requests
    import json

    # Grab song data
    # url = 'https://musicdemons.com/api/v1/song/organic-search/all together now farm'
    # payload = {}
    # headers = {
    #     'with': 'lyrics'
    # }
    # response = requests.request('GET', url, headers = headers, data = payload, allow_redirects=False, timeout=undefined)
    # print(response.text)

    url = 'https://musicdemons.com/api/v1/song'
    payload = {}
    headers = {}
    response = requests.request('GET', url, headers = headers, data = payload, allow_redirects=False, timeout=None)
    songs = json.loads(response.text)
    songs.sort(key=extract_time, reverse=True)
    songs = songs[:12]
    youtube_thumbs = []
    youtube_urls = []
    for song in songs:
        youtube_thumbs.append('https://img.youtube.com/vi/' + song['youtube_id'] + '/0.jpg')
        youtube_urls.append('https://www.youtube.com/watch?v=' + song['youtube_id'])

    print(songs)
    return render(request, "home.html", {'songs': zip(songs, youtube_thumbs, youtube_urls)})


def lyrics(request):
    import requests
    import json

    song_id = request.POST['lyrics_req']

    url = 'https://musicdemons.com/api/v1/song/' + str(song_id)
    payload = {}
    headers = {'with': 'lyrics'}
    response = requests.request('GET', url, headers = headers, data = payload, allow_redirects=False, timeout=None)
    song_lyrics = json.loads(response.text)
    return render(request, 'lyrics.html', {'song_lyrics': song_lyrics})


def search_songs(request):
    import requests
    import json

    query = request.POST['query']

    url = "https://musicdemons.com/api/v1/person/organic_search/john"
    payload = {}
    headers = {'with': 'lyrics'}
    response = requests.get(url)
    # response = requests.request('GET', url, headers = headers, data = payload, allow_redirects=False, timeout=None)
    print(response.text)
    song_data = ''
    # song_data = json.loads(response.text)

    return render(request, 'search_songs.html', {'song': song_data})


def all_songs(request):
    import requests
    import json

    url = 'https://musicdemons.com/api/v1/song'
    payload = {}
    headers = {'with': 'artists'}
    response = requests.request('GET', url, headers = headers, data = payload, allow_redirects=False, timeout=None)
    songs = json.loads(response.text)

    youtube_urls = []
    for song in songs:
        if song['youtube_id']:
            youtube_urls.append('https://www.youtube.com/watch?v=' + song['youtube_id'])

    return render(request, 'all_songs.html', {'all_songs': zip(songs, youtube_urls)})
