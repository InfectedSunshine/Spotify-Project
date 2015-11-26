import sys
import spotipy
import spotipy.util as util
scope = 'user-library-read'
scope = 'playlist-modify-public'
user_list=[]
target_list=[]
if len(sys.argv) > 3:
    username = sys.argv[1]
    target = sys.argv[2]
    playlist_name=sys.argv[3]
else:
    print "Usage: %s username" % (sys.argv[0],)
    sys.exit()

token = util.prompt_for_user_token(username, scope)

sp=spotipy.Spotify(auth=token)

if token:

    def current_user_saved_artists(username):
	artist_list=[]
        results = sp.current_user_saved_tracks()
	user_tracks=results['items']
	while results['next']:
    	    results=sp.next(results)
	    user_tracks.extend(results['items'])
        for items in user_tracks:
       	    artist_list.append(items['track']['artists'][0]['uri'])
	return sorted(set(artist_list))

    def get_artist_list_from_playlists(target):
	def store_tracks(results):	
	    for i, item in enumerate(artist_uri['items']):
			track = item['track']['artists'][0]['uri']
			artist_list.append(track)
	target_playlist_list = sp.user_playlists(target)
	artist_list=[]
	for playlist in target_playlist_list['items']:
	     if playlist['owner']['id'] == target:
	        playlist_tracks=sp.user_playlist(target, playlist['uri'], fields="tracks,next")
	        artist_uri= playlist_tracks['tracks']
		store_tracks(artist_uri)
		while artist_uri['next']:
		    artist_uri=sp.next(artist_uri)
		    store_tracks(artist_uri)
	return sorted(set(artist_list))
	    

    def make_similar_artist_list(user_list, target_list):
	return list(set(target_list) & set(user_list))

    def make_difference_artist_list(user_list, target_list):
	return list(set(target_list) - set(user_list))
 
    def add_to_playlist(username, track_list, playlist_id):
		sp.user_playlist_add_tracks(username, playlist_id, track_list)
    
    def get_track_list(artist_list):
	playlist=[]
	counter=1
	for item in artist_list:
	    top_tracks= sp.artist_top_tracks(item)
	    if len(top_tracks['tracks']) != 0 :
	    	add_track=top_tracks['tracks'][0]['uri']
	   	playlist.append(add_track)
		counter=counter+1
	    if counter>100:
		return playlist
		break
	
    	return playlist
    def create_playlist(username):
	playlist_info=sp.user_playlist_create(username, playlist_name)['id']
	return playlist_info

user_tracks=current_user_saved_artists(username)

target_tracks=get_artist_list_from_playlists(target)

similar_list=make_similar_artist_list(user_tracks, target_tracks)

new_playlist_id= create_playlist(username)

similar_playlist_list=get_track_list(similar_list)

add_to_playlist(username, similar_playlist_list, new_playlist_id)

print target_tracks
print similar_list

