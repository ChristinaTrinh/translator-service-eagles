from src.translator import translate_content
import pytest
from pytest_mock import MockerFixture
import openai

def test_chinese():
    is_english, translated_content = translate_content("这是一条中文消息")
    assert is_english == False
    assert translated_content == "This is a Chinese message"

def test_llm_normal_response():
    pass

def test_llm_gibberish_response():
    pass

mock = unittest.mock.patch.object(client.chat.completions, 'create')
def test_unexpected_language(mocker):
  # we mock the model's response to return a random message

  # mock return bad language results in terms of length
  # mocker.spy_return_list.choices[0].message.content = "I don't understand your request"
  try:
    assert query_llm_robust("Hier ist dein erstes Beispiel.")==(False, "Sorry, a language detection and translation was run on your post, but due to some error, the language result contain more information than needed.")
  except AssertionError as e:
    print(f"Mock test 1 failed: {e}")
  else:
    print("Mock test 1 passed")
  # mock return bad language results in terms of return type
  # mocker.spy_return_list.choices[0].message.content = 0
  try:
    assert query_llm_robust("Il fait beau aujourd'hui.")==(False, "Sorry, a language detection and translation was run on your post, but due to some error, the language result returned something that is not a string.")
  except AssertionError as e:
    print(f"Mock test 2 failed: {e}")
  else:
    print("Mock test 2 passed!")
  # mock if errored in any OpenAI api calls
  mocker.spy_exception = OpenAIError("OpenAI Error")
  try:
    assert query_llm_robust("我要去上课。")==(False, "Sorry, a language detection and translation was run on your post, but due to some error, the calls failed.")
  except AssertionError as e:
    print(f"Mock test 3 failed: {e}")
  else:
    print("Mock test 3 passed")

  # mock if encounter any error other than OpenAI errors
  mocker.spy_exception = Exception("Some Error")
  try:
    assert query_llm_robust("À quelle heure part le train?")==(False, "Sorry, a language detection and translation was run on your post, but due to some error, the processes did not return valid response.")
  except AssertitonError as e:
    print(f"Mock test 4 failed: {e}")
  else:
    print("Mock test 4 passed!")
  # mock return bad translation results in terms of return type
  first_mock = MagicMock()
  first_mock.choices = [MagicMock()]
  first_mock.choices[0].message = MagicMock()
  first_mock.choices[0].message.content = "Chinese"

  second_mock = MagicMock()
  second_mock.choices = [MagicMock()]
  second_mock.choices[0].message = MagicMock()
  second_mock.choices[0].message.content = 0

  mocker.spy_exception = [first_mock, second_mock]
  try:
    assert query_llm_robust("C'est un exemple de message.")==(False, "Sorry, a language detection and translation was run on your post, but due to some error, the translation result returned something that is not a string.")
  except AssertionError as e:
    print(f"Mock test 5 failed: {e}")
  else:
    print("Mock test 5 passed")
