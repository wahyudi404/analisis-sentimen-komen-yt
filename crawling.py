import pandas as pd
from googleapiclient.discovery import build

# fungsi crawling
def video_comments(video_id):
	# empty list for storing reply
	replies = []

	# creating youtube resource object
	youtube = build('youtube', 'v3', developerKey=api_key)

	# retrieve youtube video results
	video_response = youtube.commentThreads().list(part='snippet,replies', videoId=video_id).execute()

	# iterate video response
	while video_response:
		
		# extracting required info
		# from each result object
		for item in video_response['items']:
			
			# Extracting comments ()
			published = item['snippet']['topLevelComment']['snippet']['publishedAt']
			user = item['snippet']['topLevelComment']['snippet']['authorDisplayName']

			# Extracting comments
			comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
			likeCount = item['snippet']['topLevelComment']['snippet']['likeCount']

			replies.append([published, user, comment, likeCount])
			
			# counting number of reply of comment
			replycount = item['snippet']['totalReplyCount']

			# if reply is there
			if replycount>0:
				# iterate through all reply
				for reply in item['replies']['comments']:
					
					# Extract reply
					published = reply['snippet']['publishedAt']
					user = reply['snippet']['authorDisplayName']
					repl = reply['snippet']['textDisplay']
					likeCount = reply['snippet']['likeCount']
					
					# Store reply is list
					#replies.append(reply)
					replies.append([published, user, repl, likeCount])

			# print comment with list of reply
			#print(comment, replies, end = '\n\n')

			# empty reply list
			#replies = []

		# Again repeat
		if 'nextPageToken' in video_response:
			video_response = youtube.commentThreads().list(
					part = 'snippet,replies',
					pageToken = video_response['nextPageToken'], 
					videoId = video_id
				).execute()
		else:
			break
	#endwhile
	return replies

# Jalankan Proses Crawling
# isikan dengan api key Anda
api_key = 'API_KEY'

# Enter video id
# contoh url video = https://www.youtube.com/watch?v=5tucmKjOGi8
video_id = "bkRuRfjNQr4" #isikan dengan kode / ID video

# Call function
comments = video_comments(video_id)

# print(comments)

dataComments = []
for comment in comments:
    dataComments.append(comment[2])

# print(dataComments)

# Ubah Hasil Crawling ke Dataframe
# df = pd.DataFrame(comments, columns=['publishedAt', 'authorDisplayName', 'textDisplay', 'likeCount'])
df = pd.DataFrame(dataComments, columns=['komentar'])
# print(df)

# Simpan Hasil Crawling ke file CSV
df.to_csv('youtube-comments.csv', index=False)

print('Successfully Saved')
