import requests
import time
import random
from googletrans import Translator  # Для Google Translate
from bs4 import BeautifulSoup  # Для парсинга с Reverso Context


# Функция для перевода с Google Translate
def google_translate(text, target_language='en'):
    translator = Translator()
    try:
        translation = translator.translate(text, dest=target_language)
        return translation.text
    except Exception as e:
        print(f"Ошибка Google Translate: {e}")
        return None  # Возвращаем None при ошибке


# Функция для перевода с LibreTranslate
def libre_translate(text, target_language='en'):
    try:
        url = "https://libretranslate.com/translate"
        payload = {'q': text, 'source': 'en', 'target': target_language}
        response = requests.post(url, data=payload)
        return response.json()['translatedText']
    except Exception as e:
        print(f"Ошибка LibreTranslate: {e}")
        return None


# Функция для перевода с MyMemory
def mymemory_translate(text, target_language='en'):
    try:
        url = f"https://api.mymemory.translated.net/get?q={text}&langpair=en|{target_language}"
        response = requests.get(url)
        return response.json()['responseData']['translatedText']
    except Exception as e:
        print(f"Ошибка MyMemory: {e}")
        return None


# Функция для перевода с Reverso Context
def reverso_translate(text, target_language='en'):
    try:
        url = f"https://context.reverso.net/translation/english-{target_language}/{text.replace(' ', '%20')}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        translation = soup.find('a', {'class': 'translation'}).text.strip()
        return translation
    except Exception as e:
        print(f"Ошибка Reverso Context: {e}")
        return None


# Список переводчиков для round-robin
translators = [google_translate, libre_translate, mymemory_translate, reverso_translate]


# Функция для перевода одного предложения через несколько переводчиков
def translate_with_fallback(sentence, target_language='en'):
    for translator in translators:
        translation = translator(sentence, target_language)
        if translation:  # Если перевод успешен
            return translation
    return sentence  # Если все переводчики не сработали, возвращаем оригинал


# Функция для перевода книги
def translate_book(input_file, output_file, target_language='en'):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Разбиваем текст на предложения (можно доработать, если нужно лучшее разделение)
    sentences = content.split('. ')

    translated_sentences = []

    for i, sentence in enumerate(sentences):
        print(f"Перевод предложения {i + 1}...")

        # Переводим предложение с попыткой использовать все переводчики по очереди
        translated_sentence = translate_with_fallback(sentence, target_language)
        translated_sentences.append(f"{sentence} ( {translated_sentence})")

        # Задержка перед следующим запросом
        time.sleep(random.uniform(0, 1))  # 1-2 секунды задержки

    # Записываем результат в файл
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('. '.join(translated_sentences))

    print(f"Перевод завершён. Результат сохранён в {output_file}")


# Пример использования
input_file = "C:/Users/ponom/Downloads/Azimov_A._Ya_Robot.txt"
output_file = "C:/Users/ponom/Downloads/tests/output.txt"-
translate_book(input_file, output_file, target_language='en')
