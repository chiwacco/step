import random, sys, time

# Hash function.
#
# |key|: string
# Return value: a hash value

#ハッシュ関数（not good）
def calculate_hash(key):
    assert type(key) == str
    hash = 0
    for i in key:
        hash += ord(i)
    return hash


class Item:
    def __init__(self, key, value, next):
        assert type(key) == str # key is str?
        self.key = key
        self.value = value
        self.next = next


class HashTable: #HashTableの定義，(key, value)を格納

    def __init__(self):
        self.bucket_size = 97 #素数
        self.buckets = [None] * self.bucket_size
        self.item_count = 0 #ハッシュに入っているアイテム数をカウント

    
    def put(self, key, value):
        assert type(key) == str
        self.check_size() #Don't remove this code.　再ハッシュが必要か判断し再サイズする
        bucket_index = calculate_hash(key) % self.bucket_size
        item = self.buckets[bucket_index] #itemは[]番目の要素だよ
        while item: #ハッシュテーブルから繋がるリスト内を検索（見つかるまでrepeat）
            if item.key == key:
                item.value = value
                return False
            item = item.next #終わったら次のハッシュテーブルに移動

        new_item = Item(key, value, self.buckets[bucket_index])
        self.buckets[bucket_index] = new_item
        self.item_count += 1
        return True

    #keyが存在するか
    def get(self, key):
        assert type(key) == str
        self.check_size() # Note: Don't remove this code.
        bucket_index = calculate_hash(key) % self.bucket_size
        item = self.buckets[bucket_index]
        while item:
            if item.key == key:
                return (item.value, True)
            item = item.next
        return (None, False)


    def delete(self, key):
        assert type(key) == str
        self.check_size()

        bucket_index = calculate_hash(key) % self.bucket_size
        current_item = self.buckets[bucket_index] #bucket内の最初のアイテム
        previous_item = None #前のアイテムを保持する変数を初期化

        while current_item: #itemを探す
            if current_item.key == key:
                if previous_item is None: #bucket内の最初のアイテムを削除したい
                    self.buckets[bucket_index] = current_item.next
                else:
                    previous_item.next = current_item.next #A->B->C を A->Cに付け替え
                self.item_count -= 1
                return True
        
            previous_item = current_item
            current_item = current_item.next

        return False # Not found

        pass

    # Return the total number of items in the hash table.
    def size(self):
        return self.item_count

    # Note: Don't change this function.
    def check_size(self): #サイズが条件を満たすかチェック
        assert (self.bucket_size < 100 or
                self.item_count >= self.bucket_size * 0.3)


# Test the functional behavior of the hash table.
def functional_test():
    hash_table = HashTable()

    assert hash_table.put("aaa", 1) == True
    assert hash_table.get("aaa") == (1, True)
    assert hash_table.size() == 1

    assert hash_table.put("bbb", 2) == True
    assert hash_table.put("ccc", 3) == True
    assert hash_table.put("ddd", 4) == True
    assert hash_table.get("aaa") == (1, True)
    assert hash_table.get("bbb") == (2, True)
    assert hash_table.get("ccc") == (3, True)
    assert hash_table.get("ddd") == (4, True)
    assert hash_table.get("a") == (None, False)
    assert hash_table.get("aa") == (None, False)
    assert hash_table.get("aaaa") == (None, False)
    assert hash_table.size() == 4

    assert hash_table.put("aaa", 11) == False
    assert hash_table.get("aaa") == (11, True)
    assert hash_table.size() == 4

    assert hash_table.delete("aaa") == True
    assert hash_table.get("aaa") == (None, False)
    assert hash_table.size() == 3

    assert hash_table.delete("a") == False
    assert hash_table.delete("aa") == False
    assert hash_table.delete("aaa") == False
    assert hash_table.delete("aaaa") == False

    assert hash_table.delete("ddd") == True
    assert hash_table.delete("ccc") == True
    assert hash_table.delete("bbb") == True
    assert hash_table.get("aaa") == (None, False)
    assert hash_table.get("bbb") == (None, False)
    assert hash_table.get("ccc") == (None, False)
    assert hash_table.get("ddd") == (None, False)
    assert hash_table.size() == 0

    assert hash_table.put("abc", 1) == True
    assert hash_table.put("acb", 2) == True
    assert hash_table.put("bac", 3) == True
    assert hash_table.put("bca", 4) == True
    assert hash_table.put("cab", 5) == True
    assert hash_table.put("cba", 6) == True
    assert hash_table.get("abc") == (1, True)
    assert hash_table.get("acb") == (2, True)
    assert hash_table.get("bac") == (3, True)
    assert hash_table.get("bca") == (4, True)
    assert hash_table.get("cab") == (5, True)
    assert hash_table.get("cba") == (6, True)
    assert hash_table.size() == 6

    assert hash_table.delete("abc") == True
    assert hash_table.delete("cba") == True
    assert hash_table.delete("bac") == True
    assert hash_table.delete("bca") == True
    assert hash_table.delete("acb") == True
    assert hash_table.delete("cab") == True
    assert hash_table.size() == 0
    print("Functional tests passed!")


def performance_test():
    hash_table = HashTable()

    for iteration in range(100):
        begin = time.time()
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.put(str(rand), str(rand))
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.get(str(rand))
        end = time.time()
        print("%d %.6f" % (iteration, end - begin))

    for iteration in range(100):
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.delete(str(rand))

    assert hash_table.size() == 0
    print("Performance tests passed!")


if __name__ == "__main__":
    functional_test()
    performance_test()