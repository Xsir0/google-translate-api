import os
import base64
import requests
from dotenv import load_dotenv


load_dotenv()

key = os.getenv('TRANSLATE_KEY')

if not key:
    raise Exception('set key first!')


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
}


def translate(text: str, target_language: str, display_language: str, source_language: str = "auto"):
    """
    Response Example:
    {
    "translation": "How is the weather today? Do you like the weather today?",
    "sentences": [
        {
            "trans": "How is the weather today? Do you like the weather today?",
            "orig": "今天天气如何，你喜欢今天的天气吗",
            "backend": "NMT",
            "modelSpecification": [
                {
                    "modelNamespace": "lf"
                }
            ],
            "translationEngineDebugInfo": [
                {
                    "modelTracking": {
                        "checkpointMd5": "1e810531b645c06de4d778dc66657aca",
                        "launchDoc": "leapfrog_zh_en_2024q1.md"
                    },
                    "featuresApplied": [
                        "BLOB_TRANSLATION"
                    ]
                }
            ]
        }
    ],
    "detectedLanguages": {
        "srclangs": [
            "zh-CN"
        ],
        "srclangsConfidences": [
            1
        ],
        "extendedSrclangs": [
            "zh-CN"
        ]
    },
    "sourceLanguage": "zh-CN"
}
    """
    url = f"https://translate-pa.googleapis.com/v1/translate?params.client=gtx&query.source_language={source_language}&query.target_language={target_language}&query.display_language={display_language}&query.text={text}&key={key}&data_types=TRANSLATION&data_types=SENTENCE_SPLITS&data_types=BILINGUAL_DICTIONARY_FULL"
    print('url: ', url)
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        result = response.json()['translation']
        return result
    print(
        f"Request error, status_code: {response.status_code}, reason: {response.text}")
    return None


def get_audio_info(language: str, text: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "Content-Type": "application/json+protobuf"
    }
    url = f"https://translate-pa.googleapis.com/v1/textToSpeech?client=gtx&language={language}&text={text}&voice_speed=1&key={key}"
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        return response.json()[0]
    print(
        f'get audio info fail, status_code: {response.status_code}, reason: {response.text}')
    return None


def base64_to_audio(base64str: str):

    audio_data = base64.b64decode(base64str)
    with open('assets/output.mp3', 'wb') as audio_file:
        audio_file.write(audio_data)


if __name__ == '__main__':
    text = "今天天气怎么样？"
    translated_content = translate(
        text=text, target_language="en-US", display_language="zh-CN")
    print('translated text: ', translated_content)
    if translate:
        audio_base64str = get_audio_info(
            language="en", text=translated_content)
        if audio_base64str:
            base64_to_audio(audio_base64str)
