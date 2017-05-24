import jieba


jieba.set_dictionary('./dictionary/dict.txt.big')  # 對繁體中文斷詞較準確的字典檔


def main():
    s = '啥小?我點的蚵仔煎裡面沒有蚵仔也沒有蛋啊!!!幹你娘!!好人你幫幫人民的啦 為基金福利會設護叫天主善的啦 聯合國把雞爆加你們聯合國 洨敬白布雞使喚唷際甘草精華雄沒醉不女人'
    print([word for word in jieba.cut(s)])


if __name__ == '__main__':
    main()
