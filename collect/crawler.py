import requests
import json
from datetime import datetime, timedelta

BASE_URL_FB_API = "https://graph.facebook.com/v3.0"
ACCESS_TOKEN = "EAACEdEose0cBAJO7a6BVhvSBqLyruX0AG2I4UDy1RaL1ke8vhaov8yGnDGLtiyaOwlZBRQOEBbjIipojCjIj36uW0J4nob5SZAteHKMgYmRRSsBNXR2oZAcxys5PqKMnWXFOSbJ8WmaQoEdpMtd9SVLQ9R5xZCUj8tVFvgNgFgft2hcIbHJU7gDZARDR1yWQdjtImPegPZBAZDZD"
LIMIT_REQUEST = 20
pagename = "jtbcnews"
from_date = "2018-05-01"
to_date = "2018-05-24"


# json으로 데이터 리턴 해줌
def get_json_result(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()

    except Exception as e:
        return "%s : Error for request [%s]" % (datetime.now(), url)


# page이름으로 페이스북에서 id 값을 리턴해준다.
def fb_name_to_id(pagename):
    base = BASE_URL_FB_API
    node = "/" + pagename
    params = "/?access_token=%s" % ACCESS_TOKEN
    url = base + node + params

    json_result = get_json_result(url)

    return json_result["id"]


# print(fb_name_to_id("jtbcnews"))



# json 데이터 중에 필요한 데이터만 출력하는 메소드
def preprocess_post(post):
    # 작성일 +9시간 해줘야함
    created_time = post["created_time"]
    created_time = datetime.strptime(created_time, '%Y-%m-%dT%H:%M:%S+0000')
    created_time = created_time + timedelta(hours=+9)
    created_time = created_time.strftime('%Y-%m-%d %H:%M:%S')

    # 공유수
    if "shares" not in post:
        share_count = 0
    else:
        share_count = post["shares"]["count"]

    # 리액션 수
    if "reaction" not in post:
        reaction_count = 0
    else:
        reaction_count = post["reaction"]["summary"]["total_count"]

    # 댓글 수
    if "comments" not in post:
        comments_count = 0
    else:
        comments_count = post["comments"]["summary"]["total_count"]

    # 메세지
    if "message" not in post:
        message_str = ""
    else:
        message_str = post["message"]

    postVo = {
        "created_time": created_time,
        "share_count": share_count,
        "reaction_count": reaction_count,
        "comments_count": comments_count,
        "message_str": message_str
    }

    return postVo

# 페이스북 페이지넨임, 시작날자, 끝날자를 주면 json-->list 형태로 리턴
def fb_get_post_list(pagename, from_date, to_date):
    page_id = fb_name_to_id(pagename)

    base = BASE_URL_FB_API
    node = '/%s/posts' % page_id
    fields = '/?fields=id,message,link,name,type,shares,' + \
             'created_time,comments.limit(0).summary(true),' + \
             'reactions.limit(0).summary(true)'
    duration = '&since=%s&until=%s' % (from_date, to_date)
    parameters = '&limit=%s&access_token=%s' % (LIMIT_REQUEST, ACCESS_TOKEN)
    url = base + node + fields + duration + parameters

    postList = []
    isNext = True
    count = 0
    while isNext:
        tmpPostList = get_json_result(url)

        for post in tmpPostList.get("data"):
            count += 1

            postVo = preprocess_post(post)
            postList.append(postVo)
            # message_str = post["message"]
        paging = tmpPostList.get("paging").get("next")
        # paging = tmpPostList["paging"]["next"]
        if paging != None:
            url = paging
        else:
            isNext = False

    # save results to file
    with open("d:/fb/" + pagename + ".json", 'w', encoding='utf-8') as outfile:
        json_string = json.dumps(postList, indent=4, sort_keys=True, ensure_ascii=False)
        outfile.write(json_string)

    return postList

# result = fb_get_post_list(pagename, from_date, to_date)
# print(result)
