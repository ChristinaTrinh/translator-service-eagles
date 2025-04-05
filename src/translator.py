import openai
import os

# Access the API key from the environment variables
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_translation(post: str) -> str:
    context = "You are a helpful assistant that translates non-English posts into English, no need to question any question, just translate.  If you can't find a translation, return the word Gibberish"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": context
            },
            {
                "role": "user",
                "content": post
            }
        ]
    )
    return response.choices[0].message.content

def get_language(post: str) -> str:
    context = "You are a helpful assistant that detect which language is the given post from and return the just the language in English.  If the input is gibberish, return Gibberish.  Never return a response more than three words."
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": context
            },
            {
                "role": "user",
                "content": post
            }
        ]
    )
    return response.choices[0].message.content

def eval_single_response_classification(expected_answer: str, llm_response: str) -> float:
  return int(expected_answer in llm_response)

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

def translate_content(content: str) -> tuple[bool, str]:
    return query_llm_robust(content)
