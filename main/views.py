import logging
from app import app
from flask import render_template
import re
import json
from collections import defaultdict
import main.config as config
import praw
logger = logging.getLogger(__name__)


@app.route('/')
def get_most_popular_words_dict():

    r = praw.Reddit(user_agent=config.USER_AGENT)
    comments = []
    words_count = []

    subreddit_obj = r.get_subreddit('news')
    for index, article in enumerate(subreddit_obj.get_hot(limit=4), start=1):
        comments_str = ' '.join([comment.body for comment in article.comments if hasattr(comment, 'body')])
        comments.append(comments_str)
        words_count.append({'words': dict(get_words_count(comments_str)), 'index': index})

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

    return render_template('chart.html', data=json.dumps(data))


def get_words_count(text):
    regex = re.compile('[,.!?;:/"()]')
    words = regex.sub('', text).lower().split(' ')
    d = defaultdict(int)
    for word in words:
        if word not in config.BANNED_WORDS:
            d[word] += 1
    words_sorted_by_count = sorted(d.items(), key=lambda word: word[1], reverse=True)
    return words_sorted_by_count

