import csv
import json
from facebook_scraper import get_posts

nrOfPages = 10000
filename = 'SophieLÃ¸hdez'
facebookId = 'SophieLoehde'

with open('data/' + filename + '.csv', 'w', encoding="utf-8", newline="") as f:
    headers = ['postId', 'originalPost', 'likes', 'numberOfCommentsInPost', 'postCreatedAt']
    writer = csv.DictWriter(f, headers, quoting=csv.QUOTE_ALL)
    writer.writeheader()

    count = 0
    skipCount = 0
    for post in get_posts(facebookId, pages=nrOfPages, credentials=("","")):
        try:
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