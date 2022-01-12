import requests
import bs4
import sys

def send_request(first_language, second_language, translated_word):
    url = f"https://context.reverso.net/translation/{first_language}-{second_language}/{translated_word}"

    request = requests.get(url=url, headers={'User-Agent': 'Mozila/5.0'})
    print("Context examples:\n")

    request_result = bs4.BeautifulSoup(request.text, 'html.parser')
    word_translations_html = request_result.find_all('a', 'translation', limit=6)
    translate_examples_html = request_result.find_all('div', class_='example', limit=5)

    word_translations = []
    translate_examples = []

    for translation in word_translations_html:
        string = translation.text
        string = string.replace('\n', '')
        string = string.replace(' ', '')
        word_translations.append(string)
        
    for example in translate_examples_html:
        string = example.text
        string = string.replace('\n', "")
        string = string.replace('\r', "\t")
        string = string.replace('  ', "")
        translate_examples.append(string)
    
    return word_translations, translate_examples


def all_languages():
    for language in languages:
        try:
            if first_language != language:
            
                word_translations, translate_examples = send_request(first_language, language, translated_word)
                
                myfile = open(f'./{translated_word}.txt', 'a+', encoding='utf-8')
                
                print(f"{language.capitalize()} Translations:")
                myfile.write(f"{language.capitalize()} Translations:\n")

                for i in range(1, 6):
                    print(word_translations[i], '\n')
                    myfile.write(f'{word_translations[i]}\n')

                print(f"{language.capitalize()} Examples:")
                myfile.write(f"{language.capitalize()} Examples:\n")
                
                for j in range(5):
                    print(translate_examples[j], "\n")
                    myfile.write(f'{translate_examples[j]}\n')
                
                myfile.close()
        except  IndexError:
            print("Unable to translate to the current language")
            myfile.write("Unable to translate to the current language\n")
            myfile.close()
        


languages = ("arabic", "german", "english",
            "spanish", "french", "hebrew",
            "japanese", "dutch", "polish",
            "portuguese", "romanian", "russian", "turkish")

arguments = sys.argv
first_language = arguments[1].lower()
second_language = arguments[2].lower()
translated_word = arguments[3]

try:
    if second_language == 'all':
        all_languages()
    else:
        
        word_translations, translate_examples = send_request(first_language, second_language, translated_word)
        
        print(f"{second_language.capitalize()} Translations:")
        
        for i in range(len(word_translations) - 1):
            print(word_translations[i], "\n")
        
        print(f"{second_language.capitalize()} Examples:")
        
        for i in range(5):
            print(translate_examples[i], "\n")

except ConnectionError:
        print("Something wrong with your internet connection")
except IndexError:
        all_languages = languages
        if first_language not in all_languages:
            print(f"Sorry, the program doesn't support {first_language}")
        elif second_language not in all_languages:
            print(f"Sorry, the program doesn't support {second_language}")
        else:
            print(f"Sorry, unable to find {translated_word}")