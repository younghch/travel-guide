import os
from openai import OpenAI

GPT_MODEL = {
    3: 'gpt-3.5-turbo',
    4: 'gpt-4',
}

SYSTEM_PROMPT_GENERAL_SUMMARY = """
You are a hisotrian. Your role is to write a brief audio guide of the nearby places.
You will be given a list of famous places in the area.

Requirements:
- Include historical facts about the place.
- Include interesting stories about the place.
- If the places are related to each other, explain the relationship.
- Describe what the tourists can do in the place.
- Exclude the places that are not historically important.

Always answer in Korean.
"""

SYSTEM_PROMPT_DETAIL= """
You are a historian. You will be provided a place user want to be guided. 
Your role is to write audio tour guide of the place.

Always answer in Korean.
"""

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def get_general_guide_of_places(places: list[str], model=3):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT_GENERAL_SUMMARY,
            },
            {
                "role": "user",
                "content": ', '.join(places),
            }
        ],
        model=GPT_MODEL.get(model),
    )
    print(chat_completion.choices[0].message)
    return chat_completion.choices[0].message.content

def get_detailed_guide_of_a_place(place: str, model=3):
    print("running detailed guide")
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT_DETAIL,
            },
            {
                "role": "user",
                "content": place,
            }
        ],
        model=GPT_MODEL.get(model),
    )
    print(chat_completion.choices[0].message)
    return chat_completion.choices[0].message.content