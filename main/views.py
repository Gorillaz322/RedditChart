import logging
from app import app
from flask import render_template
import re
import requests
import json
from collections import defaultdict
import main.config as config
import praw
logger = logging.getLogger(__name__)


@app.route('/line')
def line_chart():

    r = praw.Reddit(user_agent=config.USER_AGENT)
    comments = []
    words_count = []

    subreddit_obj = r.get_subreddit('news')
    for index, article in enumerate(subreddit_obj.get_hot(limit=3), start=1):
        comments_str = ' '.join([comment.body for comment in article.comments if hasattr(comment, 'body')])
        comments.append(comments_str)
        words_count.append({'words': dict(get_words_count(comments_str)), 'index': 'Article {}'.format(index)})

    popular_words = [word[0] for word in get_words_count(' '.join(comments))[:10]]

    words = []
    for b in words_count:
        info = {
            'name': b['index'],
            'data': []
        }
        for word in popular_words:
            info['data'].append(b['words'].get(word) or 0)
        words.append(info)

    data = {
        'popular_words': popular_words,
        'words_info': words
    }

    return render_template('LineChart.html', data=json.dumps(data))

@app.route('/bar')
def bar_chart():
    client = praw.Reddit(user_agent=config.USER_AGENT)

    # get popular subreddits
    r = json.loads(requests.get('https://www.reddit.com/subreddits/.json', headers=config.HEADERS).content)
    subreddits_info = []

    for s in r['data']['children'][:4]:
        subreddit_info = {}

        subreddit_name = s['data']['display_name']
        subreddit_obj = client.get_subreddit(subreddit_name)
        subreddit_info['name'] = subreddit_name
        subreddit_info['subscribers'] = s['data']['subscribers']

        comment_texts = []
        for article in subreddit_obj.get_hot(limit=1):
            comment_texts.extend([comment.body for comment in article.comments if hasattr(comment, 'body')])
        subreddit_info['words'] = get_words_count(' '.join(comment_texts))[:10]

        subreddits_info.append(subreddit_info)

    return render_template('BarChart.html', data=json.dumps(subreddits_info))


def get_words_count(text):
    regex = re.compile('[,.!?;:/"()]')
    words = regex.sub('', text).lower().split(' ')
    d = defaultdict(int)
    for word in words:
        if word not in config.BANNED_WORDS:
            d[word] += 1
    words_sorted_by_count = sorted(d.items(), key=lambda word: word[1], reverse=True)
    return words_sorted_by_count

