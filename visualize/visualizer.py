import matplotlib.pyplot as plt
from matplotlib import font_manager
import webbrowser
import pytagcloud

# 일반 그래프로 나타내는 함수
def show_graph_bar(dictWords, pagename):

    font_filename = 'c:/Windows/fonts/malgun.ttf'
    font_name = font_manager.FontProperties(fname=font_filename).get_name()
    print(font_name) # 폰트 이름

    plt.rc('font', family=font_name)

    plt.xlabel("주요 단어")
    plt.ylabel("빈도수")
    plt.grid(True)

    dict_keys = dictWords.keys()
    dict_values = dictWords.values()

    plt.bar(range(len(dictWords)), dict_values, align='center')
    plt.xticks(range(len(dictWords)), list(dict_keys), rotation=70)

    save_filename = "D:/fb/%s_bar_graph.png" % pagename
    plt.savefig(save_filename, dpi=400, bbox_inches='tight')

    plt.show()

# 워드크라우드 그래프
def wordcloud(dictWords, pagename):
    print(type(dictWords))
    print(dictWords)

    taglist = pytagcloud.make_tags(dictWords.items(), maxsize=80)

    save_filename = "D:/fb/%s_wordcloud.jpg" % pagename

    pytagcloud.create_tag_image(
        taglist,
        save_filename,
        size=(800, 600),
        fontname='korean',
        rectangular=False
    )
    webbrowser.open(save_filename)