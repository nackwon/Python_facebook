import json
import re
from konlpy.tag import Twitter
from collections import Counter

def json_to_str(filename, key):
    jsonfile = open(filename, 'r', encoding='utf-8')
    json_string = jsonfile.read()
    jsondata = json.loads(json_string)

    # print(type(json_string)) str 형
    # print(json_string)

    # print(type(jsondata)) list형
    # print(jsondata)

    data = ''

    for item in jsondata:
        value = item.get(key)

        if value is None:
            continue

        data += re.sub(r'[^\w]', '', value)
        # 글자안에는 우리가 원하지 않는 문자들이 들어간다 개행문자라던지 . , 공백 등 이러한 것을 모두 없애야 한다 그때 정규표현식 사용
    return data

def count_wordfreq(data):
    twitter = Twitter()
    nonus = twitter.nouns(data)

    count = Counter(nonus)
    print(type(count))
    return count

