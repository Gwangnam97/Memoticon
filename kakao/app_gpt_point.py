#%%
import openai

openai.api_key = "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"


input_sentence = "잘생긴 옆집 아저씨"
# Extract key words from sentences using the GPT-3 model
messages = [
    {"role": "user",
        "content": f"1. 고양이 - 3 2. 귀여운 - 2 3. 잠자는 - 1 \n위와 같은 형식으로 아래 문장에서 핵심단어를 3개를 추출하고, 각 단어를 가중치와 함께 (단어-정수) 형태로 나타내주세요. \n\n {input_sentence}"}
]
completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", messages=messages, temperature=0.2
)
category_name = completion.choices[0].message.content

# Convert the extracted words into a list
category_lists = category_name.split(", ")
category_list = [category.rstrip(".") for category in category_lists]

print(category_name)
#%%