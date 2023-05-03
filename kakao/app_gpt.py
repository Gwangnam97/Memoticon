# %%
import openai
import os
from dotenv import load_dotenv

load_dotenv()


api_key = os.getenv("api_key")
question = "안녕하십니까? 학교 문법은 각 학교 교육 과정(교과서)으로 확인하셔야 하므로, 온라인 가나다에서 문의하신 바에 대하여 논하기 어렵습니다. 다만, '있어라(명령형)', '있는다(현재형)'와 같이 활용하는 '있다'가 있고, 이는 동사로 처리할 수 있습니다. 사전에서 동사 '있다'의 쓰임을 확인하실 수 있습니다."
# question = "분신 건설노동자 유서 먹고 살려고 노조 했는데... 윤석열 독재의 제물돼"

# Set OpenAI API Key
openai.api_key = api_key

messages = [
    {
        "role": "user",
        "content": f"아래 문장에서 핵심단어를 1개만 추출해주세요. \n\n {question}",
    }
]

completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", messages=messages, temperature=0.2
)

# GPT's response
category_name = completion["choices"][0]["message"]["content"]
print(f"답변 : {category_name}")
category_lists = category_name.split(", ")


# `.`로 시작하는 row를 삭제하는 함수
def remove_dot_ending_value(row):
    if row.endswith("."):
        return row[:-1]
    else:
        return row


category_list = []
for category_str in category_lists:
    category_list.append(remove_dot_ending_value(category_str))
print(f"전처리 답변 : {type(category_list)} , {category_list}")
