import re
import spacy
import nltk
from nltk.corpus import stopwords
from raw_data import contraction_mapping, removeJunk, replace_encode, replace_string
nlp = spacy.load('en_core_web_lg')
nltk.download('stopwords')
stopWords = set(stopwords.words('english'))


def clean(text):
    text = re.sub(r"\n|\t|\r", " ", text)
    text = re.sub('"', '', text)
    text = re.sub("'", "", text)
    text = re.sub(r"\s+", " ", text)
    text = text.replace(" . ", ". ")
    text = text.replace('..', '.')
    text = ' '.join([contraction_mapping[t] if t in contraction_mapping else t for t in text.split(" ")])
    re.sub('[\(\)\{\}\[\]]', '', text)
    text = re.sub(r"\s+", " ", text)
    text = ' '.join(["" if t in removeJunk else t for t in text.split(" ")])
    text = ' '.join([replace_string[word] if word in replace_string else word for word in text.split(" ")])
    text = re.sub(r"\s+", " ", text)
    text = text.replace(" . ",". ")
    text = text.replace(" , ",", ")
    return text


encoding_patterns = [
        r'[\u0080-\uFFFF]',  # match any non-ASCII characters
        r'â€.',  # match UTF-8 encoding for non-ASCII characters
        r'\\x..',  # match escaped hexadecimal encoding
        r'&.{2,6};',  # match HTML/XML entity encoding
    ]


def search_text(pattern, text):
    return re.findall(pattern, text)


def is_encoded(s):
    for pattern in encoding_patterns:
        if re.search(pattern, s):
            return True
    return False


def removeEncoding(text):
    encoding_regex = '|'.join(encoding_patterns)
    text = re.sub(encoding_regex, ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def is_roman_number(num):
    #this function is to match the roman integers.
    num = num.upper()
    pattern = re.compile(
        r"""^M{0,3}(CM|CD|D?C{0,3})?(XC|XL|L?X{0,3})?(IX|IV|V?I{0,3})?$""", re.VERBOSE)
    if re.match(pattern, num):
        return True
    return False


def capitalize_first_letter(sentence):
    if not sentence:
        return ""
    first_alpha_index = None
    for index, char in enumerate(sentence):
        if char.isalpha():
            first_alpha_index = index
            break
    if first_alpha_index is None:
        return sentence
    return sentence[:first_alpha_index] + sentence[first_alpha_index].upper() + sentence[first_alpha_index + 1:]


def cleanEncoding(text, original_text):
    for key, value in replace_encode.items():
        text = text.replace(key, value)
    text = re.sub(r'\s+', ' ', text)
    doc = nlp(text)
    cleaned_text = ""
    for token in doc:
        text = token.text
        if is_encoded(text) and not search_text(text, original_text):
            text = removeEncoding(text)
        cleaned_text += text + token.whitespace_
    for key, value in replace_encode.items():
        cleaned_text = cleaned_text.replace(key, value)
    cleaned_text = re.sub(r"\s+", " ", cleaned_text)
    return cleaned_text


def capitalize_proper_nouns(text):
    doc = nlp(text)
    capitalized_text = ""
    for token in doc:
        if token.pos_ == 'PROPN' or token.ent_type_ != "":
            text = token.text
            temp = re.sub(r"\W|\s",'',text).strip()
            if is_roman_number(text) or (len(temp) < 3 and len(temp) > 0 and text[0].isalpha() and text.lower() not in stopWords):
                text = text.upper()
            else:
                text = text.capitalize()
            capitalized_text += text + token.whitespace_
        else:
            capitalized_text += token.text_with_ws
    capitalized_text = re.sub(r"\s+", " ", capitalized_text)
    capitalized_text = capitalize_first_letter(capitalized_text)
    return capitalized_text


def afterClean(text, original_text):
    # brio can some times give some encoding issues. so you can clean them.
    text = text.replace("\n", ' ')
    text = text.replace("\t", ' ')
    while len(text) > 0 and (text[0] in ['.', ' ', ';', ':', '.', '-', ')', '^', '~', '=', '/', '>', '?', '|']):
        text = text[1:]
    text = re.sub(r"\s+", " ", text)
    text = cleanEncoding(text, original_text)
    text = capitalize_proper_nouns(text)
    while len(text) > 0 and (text[0] in ['.', ' ', ';', ':', '.', '-', ')', '^', '~', '=', '/', '>', '?', '|']):
        text = text[1:]
    return text.strip()


def sentenceTokenizer(text):
    sentences = []
    doc = nlp(text)
    for sent in doc.sents:
        sentences.append(str(sent))
    return sentences


if __name__ == '__main__':
    text = """The top foreign policy aide to Turkish presidential challenger Kemal Kılıçdaroğlu believes an opposition victory in next month’s elections could unlock a new era of defense cooperation between Ankara and the U.S. \n\nÜnal Çeviköz told Newsweek in an interview that a new, opposition-led government will look to conclude a stalled $20 billion deal for American-made F-16s and rejoin the F-35 fighter jet program from which Turkey was removed in 2019 after purchasing Russian-made S-400 anti-aircraft systems. \n\n“With the democratization processes in domestic politics, and with a new vision of the foreign policy implementation of Turkey after the elections with the new government, we believe that Turkish-U.S. relations will also have a better openings and horizons,” Çeviköz said. \n\nKılıçdaroğlu is standing as the opposition candidate for the May 14 election, representing the six-party Nation Alliance which was formed with the singular intention of unseating President Recep Tayyip Erdoğan and ending his 20 years in power. Kılıçdaroğlu—a veteran bureaucrat and long-time leader of the social democratic CHP party—slightly ahead of the incumbent. \n\nÇeviköz said the opposition grouping is “quite confident” of success and said a new Kılıçdaroğlu-led administration will be looking to repair some of the damage done to Turkey’s foreign relations over 20 years of Erdogan, particularly to Turkish-U.S. defense-industrial cooperation. \n\nA proposed $20 billion deal for 40 Lockheed Martin Block 70 F-16 fighter jets as well as upgrades to Turkey’s current F-16 fleet, has been stuck in limbo amid a range of U.S.-Turkish disputes, including Ankara’s continued block on Swedish NATO accession.  \n\nThis week, the U.S. approved an F-16 modernization package worth some $259 million, a decision Çeviköz said he hopes is a good sign for the future, and recognition of the Turkish parliament’s recent approval for Finland to join NATO. \n\n"It’s a very marginal part of the whole project, which is still pending.” Çeviköz said. “The overall big project is more than $20 billion. So, we expect that after the elections, these reciprocal encouraging steps will probably continue, and we will achieve further progress.”  \n\nThe F-35 problem is more challenging. Rejoining the fifth-generation jet program “is a goal, and it is already present in our common position paper which has been signed by the six leaders of the nation alliance,” Çeviköz said. \n\n“But I have to admit that we have lost two years,” he added, noting that the elements of development and production that were once Turkey’s responsibility have now been taken over “by other producers.”  \n\n“So, it will be difficult to enter into the F-35 project per se,” he said. “But the idea here is it\'s a matter of continuing key defense-industrial cooperation between Turkey and the U.S. The F-35 is only the fifth-generation project. There will be further technological development in the future, for the formation of the sixth generation, perhaps.” \n\n“The idea that we have in our mind is that we want to show our determination to continue the development of Turkish defense-industrial production in coordination and cooperation with the U.S. And that is what we mean when we say we want to return to the F-35 project.” \n\nAnkara was kicked out of the F-35 program for purchasing S-400 Russian surface-to-air missile platforms, ignoring warnings from fellow NATO nations including the U.S. that the systems could compromise allied security and classified information about the F-35 aircraft. \n\nÇeviköz said a new opposition-led government would be willing to work with NATO allies to nullify any dangers posed by the S-400s. \n\n“We understand that one of the main hurdles in front of Turkey’s reengagement in the F-35 project or further defense-industrial cooperation with the U.S. is, of course, the procurement of S-400s from the Russians,” he said.  \n\n“I understand that the future government will be of course willing to find a solution to that problem. I can\'t make any judgement now as to how this solution is going to be reached. But it will be a kind of understanding which will satisfy the two parties, both Turkey and the U.S. And with the resolution of this S-400 hurdle, I\'m sure the reintroduction of Turkey into the defense-industrial cooperation with the U.S. will continue.” \n\nPressed on whether a future Kılıçdaroğlu administration would be willing to give up the Russian systems, Çeviköz responded: “\'Giving up\' can be defined in different terms. Certainly, Turkey is not going to throw them away, because we paid for them, and we have installed them.” \n\n“But there could be several mechanisms or options which can be satisfactory for the security perception that our NATO allies have about the presence of S-400s in Turkish territory. I think there will be a lot of possibilities to overcome those concerns.” \n\nNewsweek has contacted the State Department by email to request comment. """
    print(clean(text))
