from src.translator import translate_content
import mock
from mock import patch, MagicMock
from openai import OpenAIError


def query_llm_robust(post: str) -> tuple[bool, str]:
  try:
    llm_language_result = get_language(post)
    if not isinstance(llm_language_result, str): raise ValueError("Sorry, a language detection and translation was run on your post, but due to some error, the language result returned something that is not a string.")
    if len(llm_language_result.split())>3 : raise ValueError("Sorry, a language detection and translation was run on your post, but due to some error, the language result contain more information than needed.")
    if_english = eval_single_response_classification("English", llm_language_result)
    if_gibberish = eval_single_response_classification("Gibberish", llm_language_result)
    if if_gibberish : return (True, "Post is just gibberish, no need to translate.")
    if not if_english :
      llm_translated_result = get_translation(post)
      if not isinstance(llm_translated_result, str): raise ValueError("Sorry, a language detection and translation was run on your post, but due to some error, the translation result returned something that is not a string.")
      return (False, llm_translated_result)
    return (True, post)
  except ValueError as e:
    return (False, str(e))
  except OpenAIError as e:
    return (False, "Sorry, a language detection and translation was run on your post, but due to some error, the calls failed.")
  except Exception as e:
    return (False, "Sorry, a language detection and translation was run on your post, but due to some error, the processes did not return valid response.")

  # mock return bad language results in terms of length
  mocker.return_value.choices[0].message.content = "I don't understand your request"
  try:
    assert query_llm_robust("Hier ist dein erstes Beispiel.")==(False, "Sorry, a language detection and translation was run on your post, but due to some error, the language result contain more information than needed.")
  except AssertionError as e:
    print(f"Mock test 1 failed: {e}")
  else:
    print("Mock test 1 passed")
  # mock return bad language results in terms of return type
  mocker.return_value.choices[0].message.content = 0
  try:
    assert query_llm_robust("Il fait beau aujourd'hui.")==(False, "Sorry, a language detection and translation was run on your post, but due to some error, the language result returned something that is not a string.")
  except AssertionError as e:
    print(f"Mock test 2 failed: {e}")
  else:
    print("Mock test 2 passed!")
  # mock if errored in any OpenAI api calls
  mocker.side_effect = OpenAIError("OpenAI Error")
  try:
    assert query_llm_robust("我要去上课。")==(False, "Sorry, a language detection and translation was run on your post, but due to some error, the calls failed.")
  except AssertionError as e:
    print(f"Mock test 3 failed: {e}")
  else:
    print("Mock test 3 passed")

  # mock if encounter any error other than OpenAI errors
  mocker.side_effect = Exception("Some Error")
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

  mocker.side_effect = [first_mock, second_mock]
  try:
    assert query_llm_robust("C'est un exemple de message.")==(False, "Sorry, a language detection and translation was run on your post, but due to some error, the translation result returned something that is not a string.")
  except AssertionError as e:
    print(f"Mock test 5 failed: {e}")
  else:
    print("Mock test 5 passed")
