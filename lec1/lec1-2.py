#文字列の一部を使って単語が作れるか？
#１inputファイルと辞書をソート
#２入力と同じものを見つけてソート前の単語を返す

import sys
DICT_FILE = "words.txt"

def count_alphabet(word):
    count = [0] * 26

    for i in word:
        count[ord(i) - ord('a')] += 1
    return count

#アルファベットの出現頻度
def is_anagram(w_cnt, dic_cnt):
    for i in range(26):
        if w_cnt[i] < dic_cnt[i]:
            return False
    return True


def find_anagram(words, dictionary):
    new_dictionary = [] #配列を定義
    for word in dictionary:
        new_dictionary.append((word, count_alphabet(word)))
    anagrams = []

    for word in words:
        word_cnt = (word, count_alphabet(word))
        anagram = []
        for word, count in new_dictionary:
            if is_anagram(word_cnt[1], count):
                anagram.append(word)
        anagrams.append(anagram)
    return anagrams



def calculate_score(word):
    SCORES = [1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2, 2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4]
    score = 0
    for character in list(word):
        score += SCORES[ord(character) - ord('a')]
    return score


def main(words_path):
    dict_path = 'words.txt'
    dictionary, words = [], []
    with open(dict_path, 'r', encoding='utf-8') as dict_file:
        for line in dict_file:
            dictionary.append(line.strip())

    with open(words_path, 'r', encoding='utf-8') as words_file:
        for line in words_file:
            words.append(line.strip())

    anagrams = find_anagram(words, dictionary)

    max_scores = []
    for anagram_list in anagrams:
        max_score = (0, None)
        for anagram in anagram_list:
            current_score = calculate_score(anagram)
            if max_score[0] < current_score:
                max_score = (current_score, anagram)
        max_scores.append(max_score)

    with open(f"answer_{words_path}", 'w', encoding='utf-8') as file:
        for (_, anagram) in max_scores:
            file.write(f"{anagram}\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: %s data_file" % sys.argv[0])
        exit(1)
    main(sys.argv[1])

    



