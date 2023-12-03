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
- Descirbe the cultural, historical background about the place.
- If places are related to each other, make a story with related places, describe at once.
- Tell interesting stories behind the place.
- Describe what the tourists can do in the place.
- Exclude the places that are not important.

Always answer in Korean.
"""

SYSTEM_PROMPT_RIGHT_INFRONT= """
You are a historian working as a tour guide. 
You will be provided a cultural heritage or place where you are standing infront of. 
Your role is to guide the place in detail to foreign tourist.

Requirements:
- Descirbe the cultural, historical background about the places.
- Describe how the place looks, characteristic and meanings of each part.
- Tell interesting stories behind the places.

Always answer in Korean.
"""

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def get_general_guide_of_places(places: list[str], gpt_version=3):
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
        model=GPT_MODEL.get(gpt_version),
    )
    print(chat_completion.choices[0].message)
    return chat_completion.choices[0].message.content

def get_detailed_guide_of_places_right_infront(places: list[str], gpt_version=3):
    print("running detailed guide")
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT_RIGHT_INFRONT,
            },
            {
                "role": "user",
                "content": ', '.join(places),
            }
        ],
        model=GPT_MODEL.get(gpt_version),
    )
    print(chat_completion.choices[0].message)
    return chat_completion.choices[0].message.content