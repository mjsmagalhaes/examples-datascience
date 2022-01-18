# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 11:11:46 2022

@author: PICHAU
"""

from ibm_watson import SpeechToTextV1
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

api = {
       'speech-to-text': {
           "apikey": "xncxj93v08IHYklo0peZF-aGcLDXo0bM7ldb9LbH-uAN",
           "url": "https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/0a1494ff-ed7c-4330-b8d6-a11c2a7751fe"
},
       'language-translator': {
           "apikey": "gmybI3wJ3cRd2qK_ijR5JlIFdX4Vf2zMi8WkfnJ8bhvy",
           "url": "https://api.us-south.language-translator.watson.cloud.ibm.com/instances/dc5611b3-ca80-496d-97c6-0935538301ee"
       }
}

# %%

speech_auth = IAMAuthenticator(api['speech-to-text']['apikey'])

speech_to_text = SpeechToTextV1(
    authenticator=speech_auth
)

speech_to_text.set_service_url(api['speech-to-text']['url'])

with open("PolynomialRegressionandPipelines.mp3","rb") as audio:
    response = speech_to_text.recognize(audio=audio, content_type='audio/mp3')

# %%

lines=response.result['results']
text = []
for i, line in enumerate(lines):
    text_line = line['alternatives'][0]['transcript']
    text.append(text_line)

    print('{:d}: {:s}'.format(i, text_line))
    print('----')

with open("audio_en.txt","w") as txt:
    txt.writelines(map(lambda t: t + '\n', text))

# %%

translator_auth = IAMAuthenticator(api['language-translator']['apikey'])

version_lt='2018-05-01'

language_translator = LanguageTranslatorV3(
    version=version_lt,
    authenticator=translator_auth
)

language_translator.set_service_url(api['language-translator']['url'])

# %%

# from pandas import json_normalize
# lang = json_normalize(language_translator.list_identifiable_languages().get_result(), "languages")

# %%

translation_response = language_translator.translate(text=text, model_id='en-pt').get_result()

# %%

translated_lines=translation_response['translations']
translated_text = []
for i, line in enumerate(translated_lines):
    text_line = line['translation']
    translated_text.append(text_line)

    print('{:d}: {:s}'.format(i, text_line))
    print('----')

with open("audio_pt.txt","w") as txt:
    txt.writelines(map(lambda t: t + '\n', translated_text))