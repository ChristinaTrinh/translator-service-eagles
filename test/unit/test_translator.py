from src.translator import translate_content, client
from mock import patch, MagicMock
import openai
from openai import OpenAIError

def test_chinese():
    is_english, translated_content = translate_content("这是一条中文消息")
    assert is_english == False
    assert translated_content in ["This is a Chinese message.", "This is a message in Chinese."]

def test_llm_normal_response():
    is_english, translated_content = translate_content("This is a test for normal response.")
    assert is_english == True
    assert translated_content == "This is a test for normal response."
    is_english1, translated_content1 = translate_content("Il fait beau aujourd'hui.")
    assert is_english1 == False
    assert translated_content1 in ["The weather is nice today.", "It is nice today.", "It’s nice today."]

def test_llm_gibberish_response():
    is_english, translated_content = translate_content("asdgkjasndgo;98i43qwtoishfjn")
    assert is_english == True
    assert translated_content == "Post is just gibberish, no need to translate."

@patch.object(client.chat.completions, 'create')
def test_unexpected_language(mocker):
  # we mock the model's response to return a random message

  # mock return bad language results in terms of length
  mocker.return_value.choices[0].message.content = "I don't understand your request"
  assert translate_content("Hier ist dein erstes Beispiel.")==(False, "Sorry, a language detection and translation was run on your post, but due to some error, the language result contain more information than needed.")
 
  # mock return bad language results in terms of return type
  mocker.return_value.choices[0].message.content = 0
  assert translate_content("Il fait beau aujourd'hui.")==(False, "Sorry, a language detection and translation was run on your post, but due to some error, the language result returned something that is not a string.")
 
  # mock if errored in any OpenAI api calls
  mocker.side_effect = OpenAIError("OpenAI Error")
  assert translate_content("我要去上课。")==(False, "Sorry, a language detection and translation was run on your post, but due to some error, the calls failed.")

  # mock if encounter any error other than OpenAI errors
  mocker.side_effect = Exception("Some Error")
  assert translate_content("À quelle heure part le train?")==(False, "Sorry, a language detection and translation was run on your post, but due to some error, the processes did not return valid response.")
  
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
  assert translate_content("C'est un exemple de message.")==(False, "Sorry, a language detection and translation was run on your post, but due to some error, the translation result returned something that is not a string.")

