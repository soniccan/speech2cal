
#Todo 出てきた文章を解析して
#・予定の内容
#・時間(s)
#・繰返しがあるのかないのか
#　をとりだす。
#method　mecab?機械学習？

import parse_speech as parser
import json


def parse2cal(file_name)->str:

    # transcript = parser.parse_speech(filename')
    transcript ='今日3時にゲームセンター'


if __name__ == " __main__":
    
    parse2cal("temp.mp3")