#１辞書の各単語をソート→ソート
#２入力と同じものを見つけてソート前の単語を返す
#(辞書にない単語がを探そうとした場合もつける？)

def sort_word(word): #入力文字列のソート
    return ''.join(sorted(word))

def sort_dictionary(dictionary):
    return sorted(dictionary, key=lambda x: x[0]) #key=lamdaでソート基準を指定。それは要素xの0番目

def create_new_dictionary(dictionary):
    new_dictionary = [] #配列を定義
    for word in dictionary:
        new_dictionary.append((sort_word(word), word)) #並べ替えしたwordとwordのペアを新しい辞書に入れる
    return new_dictionary

def binary_search(sorted_word, dictionary): #act, (act, cat)
    left = 0
    right = len(dictionary) - 1
    anagram_list = []


    while left <= right:
        mid = (left + right) // 2
        if dictionary[mid][0] == sorted_word:
            while mid > 0 and dictionary[mid-1][0] == sorted_word:
                mid -= 1
            while mid < len(dictionary) and dictionary[mid][0] == sorted_word:
                anagram_list.append(dictionary[mid][1])
                mid += 1
            return anagram_list  # 元の単語を返す
        elif dictionary[mid][0] < sorted_word:
            left = mid + 1
        else:
            right = mid - 1
    return []  # 見つからなかった場合


# テキストファイルを開いて各行を配列に格納する
with open('words.txt', 'r') as file:
    words_data = [line.strip() for line in file]

#main
search_word = input("input: ")

new_dictionary = create_new_dictionary(words_data)
sorted_new_dictionary = sort_dictionary(new_dictionary)

result = binary_search(sort_word(search_word), sorted_new_dictionary)

if result != -1:
    print(f"{search_word}'s anagram = {result}.")
else:
    print(f"{search_word} is not found.")


test1 =bool((binary_search(sort_word('act'), sorted_new_dictionary)) == ['act', 'cat']) #複数個
print(test1)
test2 =bool((binary_search(sort_word(' '), sorted_new_dictionary)) == []) #空文字
print(test2)
test3 = bool(binary_search(sort_word('abbuct'), sorted_new_dictionary) == []) #not found
print(test3)
test4 = bool(binary_search(sort_word('baduct'), sorted_new_dictionary) == ['abduct']) #普通
print(test4)
