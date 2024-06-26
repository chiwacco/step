
/*1ベストフィット検索: my_mallocのループを更新し、要求されたサイズを収容できる最小のブロックを見つけるようにしました。これにより、断片化を最小限に抑えることができます。
2割り当てと解放のロジック: 他の部分は変更せずに保持しています。これにより、プログラムがメモリを正しく割り当て、空きリストを管理し続けます。
3エッジケース: 適切なブロックが見つからない場合、mmap_from_system()を使用して新しいブロックをシステムから要求し、再度割り当てを試みます。これにより、新しい割り当てのためのスペースを常に確保できます。
*/

#include <assert.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//
// OSからメモリページを取得するインターフェース
//

void *mmap_from_system(size_t size);
void munmap_to_system(void *ptr, size_t size);

//
// 構造体の定義
//

typedef struct my_metadata_t {
  size_t size;
  struct my_metadata_t *next;
} my_metadata_t;

typedef struct my_heap_t {
  my_metadata_t *free_head;
  my_metadata_t dummy;
} my_heap_t;

//
// 静的変数 (新しい静的変数は追加しないでください！)
//
my_heap_t my_heap;

//
// ヘルパー関数（自由に追加/削除/編集してください！）
//

void my_add_to_free_list(my_metadata_t *metadata) {
  assert(!metadata->next);
  metadata->next = my_heap.free_head;
  my_heap.free_head = metadata;
}

void my_remove_from_free_list(my_metadata_t *metadata, my_metadata_t *prev) {
  if (prev) {
    prev->next = metadata->next;
  } else {
    my_heap.free_head = metadata->next;
  }
  metadata->next = NULL;
}

//
// mallocのインターフェース（次の関数の名前を変更しないでください！）
//

// これは各チャレンジの開始時に呼び出されます。
void my_initialize() {
  my_heap.free_head = &my_heap.dummy;
  my_heap.dummy.size = 0;
  my_heap.dummy.next = NULL;
}

// my_malloc()はオブジェクトが割り当てられるたびに呼び出されます。
// |size|は8の倍数で、8 <= |size| <= 4000の範囲内であることが保証されています。
// mmap_from_system() / munmap_to_system()以外のライブラリ関数の使用は許可されていません。
void *my_malloc(size_t size) {
  my_metadata_t *metadata = my_heap.free_head;
  my_metadata_t *prev = NULL;
  my_metadata_t *best_fit = NULL;
  my_metadata_t *best_fit_prev = NULL;

  // ベストフィット：オブジェクトに適合する最小の空きスロットを見つける。
  while (metadata) {
    if (metadata->size >= size) {
      if (!best_fit || metadata->size < best_fit->size) {
        best_fit = metadata;
        best_fit_prev = prev;
      }
    }
    prev = metadata;
    metadata = metadata->next;
  }

  metadata = best_fit;
  prev = best_fit_prev;

  if (!metadata) {
    // 利用可能な空きスロットがなかった場合。システムから新しいメモリ領域を要求する必要があります。
    size_t buffer_size = 4096;
    my_metadata_t *metadata = (my_metadata_t *)mmap_from_system(buffer_size);
    metadata->size = buffer_size - sizeof(my_metadata_t);
    metadata->next = NULL;
    // メモリ領域を空きリストに追加。
    my_add_to_free_list(metadata);
    // 再度my_malloc()を試みる。これで成功するはず。
    return my_malloc(size);
  }

  // |ptr|は割り当てられたオブジェクトの開始地点です。
  void *ptr = metadata + 1;
  size_t remaining_size = metadata->size - size;
  // 空きスロットを空きリストから削除。
  my_remove_from_free_list(metadata, prev);

  if (remaining_size > sizeof(my_metadata_t)) {
    // 割り当てられたオブジェクトのメタデータを縮小して、remaining_sizeに対応する領域を分離。
    metadata->size = size;
    // 残りの空きスロット用の新しいメタデータを作成。
    my_metadata_t *new_metadata = (my_metadata_t *)((char *)ptr + size);
    new_metadata->size = remaining_size - sizeof(my_metadata_t);
    new_metadata->next = NULL;
    // 残りの空きスロットを空きリストに追加。
    my_add_to_free_list(new_metadata);
  }
  return ptr;
}

// オブジェクトが解放されるたびに呼び出されます。mmap_from_system / munmap_to_system以外のライブラリ関数の使用は許可されていません。
void my_free(void *ptr) {
  // メタデータを参照。メタデータはオブジェクトの直前に配置されている。
  my_metadata_t *metadata = (my_metadata_t *)ptr - 1;
  // 空きスロットを空きリストに追加。
  my_add_to_free_list(metadata);
}

// 各チャレンジの終了時に呼び出されます。
void my_finalize() {
  // 現在は何もありません。
  // 必要に応じて追加してください！
}

void test() {
  // ここに実装してください！
  assert(1 == 1); /* 1は1です。これは常に真です！（削除しても構いません）*/
}
