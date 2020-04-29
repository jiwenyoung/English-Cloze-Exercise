import re
import random

class Helper:
    def separate_text(self, rawtext):
        """ split raw text into a list of sentences """
        spliters = {".", "?", ":", "!", "..."}
        for spliter in spliters:
            rawtext = rawtext.replace(spliter, "{}|".format(spliter))
        rawtext = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", rawtext)
        resultArr = rawtext.split("|")
        return resultArr

    def clean_each_sentence(self, sentences, limit_words_number_lower, limit_words_number_upper):
        """ clean each sentence and filter out sentence shorter than 10 words"""
        data = set()
        for sub in sentences:
            # get rid of exta charactar unnecessary
            trimers = {"*", "\n", "<", ">"}
            for trimer in trimers:
                sub = sub.replace(trimer, "")
            sub = sub.strip()
            sub = " ".join(sub.split())
            words = len(sub.split(" "))

            # if sentence is less than 10 words, we don't need it
            if words > int(limit_words_number_lower) and words < int(limit_words_number_upper):
                data.add(sub)
        return data

    def transform_sentenses_to_tuples(self, sentences_list, keywords):
        """ transform data from sentence list to list of Tuples """

        def full2half(sentence):
            """ full unicode char switch to half unicode char """
            chars = []
            for char in sentence:
                num = ord(char)
                if num == 0x3000:
                    num = 32
                elif 0xFF01 <= num <= 0xFF5E:
                    num -= 0xfee0
                num = chr(num)
                chars.append(num)
            return ''.join(chars)

        def separate_sentence_to_list(sentence, keyword):
            """
            replace space inside phrase with |
            so we can splice them as normal word
            as last, in word list, change | back to space
            """
            sentence_undersocre = ""
            sentence_wordlist = []
            if keyword != "".join(keyword.split()):
                keyword_underscore = keyword.replace(" ", "|")
                sentence_undersocre = sentence.replace(
                    keyword, keyword_underscore)
                sentence_wordlist = sentence_undersocre.split(" ")
                for index, word in enumerate(sentence_wordlist):
                    if "|" in word:
                        word = word.replace("|", " ")
                        sentence_wordlist[index] = word
            else:
                sentence_wordlist = sentence.split(" ")
            return sentence_wordlist

        def compose_choices(keyword):
            """ choose other three word to compose choices """
            choices = random.sample(keywords, 4)
            if keyword not in choices:
                change_index = random.randint(0, 3)
                choices[change_index] = keyword
            return choices

        def replace_by_underscore(sentence_wordlist, keyword):
            """ replace the keyword to ____ in sentence """
            placeholder_len = len(keyword) + 2
            placeholder = "_" * placeholder_len
            words = sentence_wordlist
            for index, word in enumerate(words):
                if word.lower() == keyword.lower():
                    words[index] = placeholder
                    break
            sentence = " ".join(words)
            return sentence

        def main(sentences_list, keywords):
            filtered = []
            for sentence in sentences_list:
                random.shuffle(keywords)
                for keyword in keywords:
                    keyword = keyword.lower().strip()
                    sentence = full2half(sentence)
                    sentence_wordlist = separate_sentence_to_list(
                        sentence, keyword)

                    # loop every word start
                    if keyword in sentence_wordlist:
                        choices = compose_choices(keyword)
                        sentence = replace_by_underscore(
                            sentence_wordlist, keyword)
                        filtered.append((sentence, keyword, set(choices)))
                        break
            return filtered

        return main(sentences_list, keywords)
