import json
import os
from matplotlib import pyplot as plt


def get_avg_price(json_data):
    sum = 0
    for item in json_data:
        sum += int(item['price'])
    return sum/len(json_data)


def main():
    json_files = [f for f in os.listdir('json')
                  if os.path.isfile(os.path.join('json', f)) and f.endswith('.json')]

    avg_prices_momo = dict()
    avg_prices_pchome = dict()

    for json_file in json_files:
        with open(os.path.join('json', json_file), 'r', encoding='UTF-8') as file:
            data = json.load(file)
            date = data['date']
            if data['store'] == 'momo':
                avg_prices_momo[date] = get_avg_price(data['items'])
            elif data['store'] == 'pchome':
                avg_prices_pchome[date] = get_avg_price(data['items'])

    keys = avg_prices_momo.keys()
    dates = sorted(keys)
    print('momo')
    for date in dates:
        print(date, int(avg_prices_momo[date]))
    print('pchome')
    for date in dates:
        print(date, int(avg_prices_pchome[date]))

    # x-axis
    x = [int(i) for i in range(len(dates))]
    plt.xticks(x, dates)  # 將 x-axis 用字串標註
    price_momo = [avg_prices_momo[d] for d in dates]  # y1-axis
    price_pchome = [avg_prices_pchome[d] for d in dates]  # y2-axis
    plt.plot(x, price_momo, marker='o', linestyle='solid')
    plt.plot(x, price_pchome, marker='o', linestyle='solid')
    plt.legend(['momo', 'pchome'])
    # specify values on ys
    for a, b in zip(x, price_momo):
        plt.text(a, b, str(int(b)))
    for a, b in zip(x, price_pchome):
        plt.text(a, b, str(int(b)))
    plt.show()


if __name__ == '__main__':
    main()

