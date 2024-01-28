import os
import logging
from openai import OpenAI

GPT_MODEL = {
    3: 'gpt-3.5-turbo',
    4: 'gpt-4',
}

SYSTEM_PROMPT_GENERAL_SUMMARY = """
You are a hisotrian. Your role is to write a brief audio guide of the nearby places.
You will be provided a list of famous places in the area.

Requirements:
- Descirbe the cultural, historical background about the place.
- If places are related to each other, describe at once with how they are related.
- Tell interesting stories/legnends behind the places only if it exists.
- Describe what the tourists can do in the place.
- Exclude the places that are not important.

Always answer in Korean.
"""

SYSTEM_PROMPT_RIGHT_INFRONT= """
You are a historian/geologist working as a tour guide. 
You will be provided cultural heritages or places that are right infront of you. 
Your role is to guide the place in detail to foreign tourist using these information.

Requirements:
- Do not try to describe all the places given. Focus on the most important one, and include others only if its context is related.
- If given place is a artefact 
    - Descirbe the cultural, historical background about the places.
    - Describe its appearance in the architectural/art hitorical perspective. It is recommended to describe the place by part in detail. (eg: If you look above the roof of the palace, you can see a table of miscellaneous objects. The number of miscellaneous objects is three or more, and there are up to 11 in Gyeonghoeru. In China, miscellaneous objects were originally made to chase away demons or fires, so they had a magical meaning, but in Korea, they symbolize a royal palace.)
- If given place is a natural scenary
    - Descirbe what you can see in the place, indicate the direction if possible.
    - Descirbe how the place was formed in the geological perspective.
- Tell interesting stories/legnends behind the places only if it exists.


Always answer in Korean.
"""

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def get_general_guide_of_places(formatted_places: list[str], gpt_version=3):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT_GENERAL_SUMMARY,
            },
            {
                "role": "user",
                "content": f'[{",".join(formatted_places)}]',
            }
        ],
        model=GPT_MODEL.get(gpt_version),
    )
    logging.debug(chat_completion.choices[0].message)
    return chat_completion.choices[0].message.content

def get_detailed_guide_of_places_right_infront(formatted_places: list[str], gpt_version=3):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT_RIGHT_INFRONT,
            },
            {
                "role": "user",
                "content": f'[{",".join(formatted_places)}]',
            }
        ],
        model=GPT_MODEL.get(gpt_version),
    )
    logging.debug(chat_completion.choices[0].message)
    return chat_completion.choices[0].message.content