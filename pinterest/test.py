import random
import time
import os
from py3pin.Pinterest import Pinterest

# 로그인
pinterest = Pinterest(email='leejw228@naver.com', 
                      password='ljw813-2813',
                      username="leejw0029",
                      cred_root='./pinterest_test/')
pinterest.login()

user_profile = pinterest.get_user_overview()
board = pinterest.boards(username='username')
print(user_profile, board)
pins = pinterest.board_feed(board_id='board_id')
print(pins)