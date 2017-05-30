import xml.etree.ElementTree as ET


if __name__ == '__main__':
    tree = ET.parse('example.xml')
    root = tree.getroot()
    print(root.attrib)
    total = root.attrib['totalResults']
    movies = list()
    for tag in root.findall('result'):
        print(tag.attrib)
        movies.append(tag.attrib['title'])
    print('-----')
    print('There are', total, 'results in the xml file.')
    print('Top 10 record:')
    print('\n'.join(movies))