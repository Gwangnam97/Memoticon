# %%
from instagrapi import Client
import os
from dotenv import load_dotenv
load_dotenv()


USERNAME = os.getenv("instagram_username")
PASSWORD = os.getenv("instagram_password")


cl = Client()
cl.login(USERNAME, PASSWORD)


def send_message():
    send_to = cl.user_id_from_username(username="g.h.nee")
    cl.direct_send(text="Hello", user_ids=[send_to])


for i in cl.hashtag_medias_top(name="밈", amount=2):
    print(i)
    a = i


# %%

# hashtag = cl.hashtag_info('meme')
# print(f'hashtag.dict() : {hashtag.dict()}')

# medias = cl.hashtag_medias_top('meme', amount=2)
# print(f'medias[0].dict() : {medias[0].dict()}')

# medias = cl.hashtag_medias_recent('meme', amount=2)
# print(f'medias[0].dict() : {medias[0].dict()}')

# medias = cl.hashtag_medias_top_a1('meme', amount=2)
# print(medias)

# a = {'step_name': 'select_contact_point_recovery',
#      'step_data': {'choice': '1', 'email': 'j*******0@gmail.com', 'hl_co_enabled': False, 'sigp_to_hl': False},
#      'flow_render_type': 3,
#      'bloks_action': 'com.instagram.challenge.navigation.take_challenge',
#      'nonce_code': 'AfyJyaaTQ1O-vJAb3CHW9-eJH9DQyvP-ECSOLW7wLwHT0cNjajrZXWQiyeDZgAS2RBxXCtPTNSd9Qg', 'user_id': 3993897174, 'cni': 18280987276129175,
#      'challenge_context': '{"step_name": "select_contact_point_recovery", "nonce_code": "AfyJyaaTQ1O-vJAb3CHW9-eJH9DQyvP-ECSOLW7wLwHT0cNjajrZXWQiyeDZgAS2RBxXCtPTNSd9Qg", "user_id": 3993897174, "cni": 18280987276129175, "first_factor_code": "0wBaztBZzhmLzdt7PYgfjhR6itXrtiibsUkwdFhHmtYHn3nenak5BTJIKDsNV4bH", "is_stateless": false, "challenge_type_enum": "HACKED_LOCK", "present_as_modal": false}',
#      'challenge_type_enum_str': 'HACKED_LOCK',
#      'status': 'ok'}
# b = a['step_data']
