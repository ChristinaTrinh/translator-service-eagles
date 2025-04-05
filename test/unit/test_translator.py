from src.translator import translate_content, query_llm_robust
from unittest.mock import patch, MagicMock
import openai
from openai import OpenAIError
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if OPENAI_API_KEY is None:
    raise ValueError("API key not found in environment variables")

client = openai.OpenAI(api_key = OPENAI_API_KEY)

def test_chinese():
    is_english, translated_content = translate_content("这是一条中文消息")
    assert is_english == False
    assert translated_content in ["This is a Chinese message.", "This is a message in Chinese."]

def test_llm_normal_response():
    pass

def test_llm_gibberish_response():
    pass

@patch.object(client.chat.completions, 'create')
def test_unexpected_language(mocker):
  # we mock the model's response to return a random message

  # mock return bad language results in terms of length
  mocker.return_value.choices[0].message.content = "I don't understand your request"
  assert query_llm_robust("Hier ist dein erstes Beispiel.")==(False, "Sorry, a language detection and translation was run on your post, but due to some error, the language result contain more information than needed.")
 
  # mock return bad language results in terms of return type
  mocker.return_value.choices[0].message.content = 0
  assert query_llm_robust("Il fait beau aujourd'hui.")==(False, "Sorry, a language detection and translation was run on your post, but due to some error, the language result returned something that is not a string.")
 
  # mock if errored in any OpenAI api calls
  mocker.side_effect = OpenAIError("OpenAI Error")
  assert query_llm_robust("我要去上课。")==(False, "Sorry, a language detection and translation was run on your post, but due to some error, the calls failed.")

  # mock if encounter any error other than OpenAI errors
  mocker.side_effect = Exception("Some Error")
  assert query_llm_robust("À quelle heure part le train?")==(False, "Sorry, a language detection and translation was run on your post, but due to some error, the processes did not return valid response.")
  
  # mock return bad translation results in terms of return type
  first_mock = MagicMock()
  first_mock.choices = [MagicMock()]
  first_mock.choices[0].message = MagicMock()
  first_mock.choices[0].message.content = "Chinese"

  second_mock = MagicMock()
  second_mock.choices = [MagicMock()]
  second_mock.choices[0].message = MagicMock()
  second_mock.choices[0].message.content = 0

  mocker.side_effect = [first_mock, second_mock]
  assert query_llm_robust("C'est un exemple de message.")==(False, "Sorry, a language detection and translation was run on your post, but due to some error, the translation result returned something that is not a string.")

