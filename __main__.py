from collect import crawler
from analysis import analizer
from visualize import visualizer

pagename = "jtbcnews"
from_date = "2018-05-01"
to_date = "2018-05-24"

if __name__ == "__main__":
   # postList = crawler.fb_get_post_list(pagename, from_date, to_date)
   # print(postList)

   dataString = analizer.json_to_str("D:/fb/jtbcnews.json", 'comments_str')
   count_data = analizer.count_wordfreq(dataString)
   print(count_data.most_common(20)) # most_common(20) 상위 20위까지만 표시하게끔 해줌

   # dictWords = dict(count_data.most_common(20))
   # visualizer.show_graph_bar(dictWords, pagename)

   dictWords = dict(count_data.most_common(20))
   visualizer.wordcloud(dictWords, pagename)