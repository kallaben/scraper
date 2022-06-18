import csv
import json
import datetime
from facebook_scraper import get_posts
from os.path import exists

filename = 'PernilleVermund'
facebookId = 'PernilleVermundNB'
credentials = ("", "")

# The program will fetch posts from now until the date given below.
year = 2021
month = 1
day = 1





















getPostUntilDate = datetime.datetime(year, month, day)
postFilePath = 'data/' + filename + '_post_ids.csv'
if not exists(postFilePath):
    with open(postFilePath, 'w+', encoding="utf-8", newline="") as f:
        headers = ['postId', 'postUrl', 'postCreatedAt']
        writer = csv.DictWriter(f, headers, quoting=csv.QUOTE_ALL)
        writer.writeheader()

        count = 0
        for post in get_posts(facebookId, options={"allow_extra_requests": False}, credentials=credentials):
            postUrl = post['post_url']
            postCreatedAt = post['time']

            if postCreatedAt < getPostUntilDate:
                break

            row = {
                'postUrl': postUrl,
                'postId': post['post_id'],
                'postCreatedAt': postCreatedAt.strftime("%m/%d/%Y, %H:%M:%S")
            }

            writer.writerow(row)


postsToFetch = []
with open(postFilePath) as postFile:
    csvReader = csv.DictReader(postFile)
    for row in csvReader:
        postsToFetch.append({'postUrl': row['postUrl'], 'postId': row['postId']})

commentFileHeaders = ['postId', 'originalPost', 'likes', 'numberOfCommentsInPost', 'postCreatedAt']
commentFilePath = 'data/' + filename + '_posts.csv'
if not exists(commentFilePath):
    with open(commentFilePath, 'w+', encoding="utf-8", newline="") as commentFile:
        headers = commentFileHeaders
        writer = csv.DictWriter(commentFile, headers, quoting=csv.QUOTE_ALL)
        writer.writeheader()

alreadyFetchedPostIds = []
with open(commentFilePath, encoding="utf-8", newline="") as commentFile:
    csvReader = csv.DictReader(commentFile)
    for row in csvReader:
        alreadyFetchedPostIds.append(row['postId'])
alreadyFetchedPostIds = list(set(alreadyFetchedPostIds))

remainingPostUrlsToFetch = [post['postUrl'] for post in postsToFetch if post['postId'] not in alreadyFetchedPostIds]
with open(commentFilePath, 'a', encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, commentFileHeaders, quoting=csv.QUOTE_ALL)
    count = 0
    skipCount = 0
    for post in get_posts(post_urls=remainingPostUrlsToFetch, credentials=credentials):
        try:
            print('Attempting to fetch', post['post_url'])
            row = {
                'postId': post['post_id'],
                'originalPost': post['text'].replace('\n', '\\n'),
                'numberOfCommentsInPost': post['comments'],
                'postCreatedAt': post['time'],
                'likes': post['likes']
            }
            writer.writerow(row)
            count += 1
        except Exception as e:
            print('Skipping post due to error:', e)
            skipCount += 1
        print('Posts fetched:', count, 'Skipped posts:', skipCount)
