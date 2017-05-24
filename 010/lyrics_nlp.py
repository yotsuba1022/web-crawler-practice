import json
import jieba
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud


MAYDAY_LYRICS_LIB = 'MayDay.json'
AIMER_ENGLISH_LIB = 'Aimer-eng.json'


def analyze_lyrics(lyrics_file):
    print('Analyzing %s...' % lyrics_file)
    with open('./lyrics_lib/%s' % lyrics_file, 'r', encoding='UTF-8') as lyrics:
        data = json.load(lyrics)
    words = list()
    for song in data.values():
        words += [word for word in jieba.cut(song) if word.split() and len(word) > 1]

    counter = Counter(words)
    print(counter.most_common(10))

    word_cloud = WordCloud(font_path='./fonts/NotoSansMonoCJKtc-Regular.otf').generate(' '.join(words))
    plt.imshow(word_cloud)
    plt.axis('off')
    plt.show()
    print('Analyze finished.')


if __name__ == '__main__':
    jieba.set_dictionary('./dictionary/dict.txt.big')
    analyze_lyrics(MAYDAY_LYRICS_LIB)
    analyze_lyrics(AIMER_ENGLISH_LIB)
