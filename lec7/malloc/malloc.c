#include <assert.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//
// Interfaces to get memory pages from OS
//

#define NUM_BINS 10
#define BIN_SIZE_MULTIPLIER 2

void *mmap_from_system(size_t size);
void munmap_to_system(void *ptr, size_t size);

//
// Struct definitions
//

typedef struct my_metadata_t {
  size_t size;
  struct my_metadata_t *next;
} my_metadata_t;

typedef struct my_heap_t {
  my_metadata_t *free_bins[NUM_BINS];
} my_heap_t;

//
// Static variables (DO NOT ADD ANOTHER STATIC VARIABLES!)
//
my_heap_t my_heap;

//
// Helper functions (feel free to add/remove/edit!)
//

void my_add_to_free_list(my_metadata_t *metadata) {
  assert(!metadata->next);

  int bin_index = 0;
  size_t bin_size = 8;

  while (bin_index < NUM_BINS - 1 && metadata->size > bin_size) {
    bin_size = (size_t)(bin_size * BIN_SIZE_MULTIPLIER);
    bin_index++;
  }

  metadata->next = my_heap.free_bins[bin_index];
  my_heap.free_bins[bin_index] = metadata;
}

void my_remove_from_free_list(my_metadata_t *metadata, my_metadata_t *prev, int bin_index) {
  if (prev) {
    prev->next = metadata->next;
  } else {
    my_heap.free_bins[bin_index] = metadata->next;
  }
  metadata->next = NULL;
}

//
// Interfaces of malloc (DO NOT RENAME FOLLOWING FUNCTIONS!)
//

//メモリ管理システムの初期化
void my_initialize() {
  for (int i = 0; i < NUM_BINS; i++) {
    //フリーブロックリストをNULLで初期化
    my_heap.free_bins[i] = NULL;
  }
}

// my_malloc() is called every time an object is allocated.
// |size| is guaranteed to be a multiple of 8 bytes and meets 8 <= |size| <=
// 4000. You are not allowed to use any library functions other than

//指定されたサイズのメモリを割り当てる
void *my_malloc(size_t size) {
  int bin_index = 0;
  size_t bin_size = 8;
  //サイズに応じて適切なbinを選択する
  while (bin_index < NUM_BINS - 1 && size > bin_size) {
    bin_size = (size_t)(bin_size * BIN_SIZE_MULTIPLIER);
    bin_index++;
  }


  my_metadata_t *metadata = NULL;
  my_metadata_t *prev = NULL;
  my_metadata_t *best_fit = NULL;
  my_metadata_t *best_fit_prev = NULL;

  //選択されたbinから最適なフリーブロックを探す
  for (int i = bin_index; i < NUM_BINS; i++) {
    metadata = my_heap.free_bins[i];
    prev = NULL;

    while (metadata) {
      if (metadata->size >= size) {
	//適切なフリーブロックを探す
        if (!best_fit || metadata->size < best_fit->size) {
          best_fit = metadata;
          best_fit_prev = prev;
          if (metadata->size == size) break; //サイズがちょうど一致したら探索終了
        }
      }
      prev = metadata;
      metadata = metadata->next;
    }

    if (best_fit) break;//最適なフリーブロックが見つかれば探索終了
  }
  // now, metadata points to the first free slot
  // and prev is the previous entry.

  metadata = best_fit;
  prev = best_fit_prev;
  
  //最適なフリーブロックがなければ新たにメモリ確保
  if (!metadata) {
    size_t buffer_size = 4096;
    metadata = (my_metadata_t *)mmap_from_system(buffer_size);
    metadata->size = buffer_size - sizeof(my_metadata_t);
    metadata->next = NULL;
    my_add_to_free_list(metadata);
    return my_malloc(size);
  }

  // |ptr| is the beginning of the allocated object.
  //
  // ... | metadata | object | ...
  //     ^          ^
  //     metadata   ptr

  //メモリを確保してポインタを返す
  void *ptr = metadata + 1;
  size_t remaining_size = metadata->size - size;
  int best_fit_bin_index = 0;
  size_t best_fit_bin_size = 8;

  while (best_fit_bin_index < NUM_BINS - 1 && best_fit->size > best_fit_bin_size) {
    best_fit_bin_size = (size_t)(best_fit_bin_size * BIN_SIZE_MULTIPLIER);
    best_fit_bin_index++;
  }
  //フリーブロックリストから削除する
  my_remove_from_free_list(metadata, prev, best_fit_bin_index);

  //フリーブロックを分割して余った部分を新たなフリーブロックとして追加する
  if (remaining_size > sizeof(my_metadata_t)) {
    metadata->size = size;
    
    // Create a new metadata for the remaining free slot.
    //
    // ... | metadata | object | metadata | free slot | ...
    //     ^          ^        ^
    //     metadata   ptr      new_metadata
    //                 <------><---------------------->
    //                   size       remaining size

    //残りの空き容量のために新しいメタデータを作成
    my_metadata_t *new_metadata = (my_metadata_t *)((char *)ptr + size);
    new_metadata->size = remaining_size - sizeof(my_metadata_t);
    new_metadata->next = NULL;
    my_add_to_free_list(new_metadata);
  }
  return ptr; //確保したメモリのポインタを返す
}

//指定されたメモリを解放する
void my_free(void *ptr) {
  // Look up the metadata. The metadata is placed just prior to the object.
  //
  // ... | metadata | object | ...
  //     ^          ^
  //     metadata   ptr
  //メモリのメタデータを取得する（メモリブロックの直前にある）
  my_metadata_t *metadata = (my_metadata_t *)ptr - 1;
  //フリーブロックリストに追加する
  my_add_to_free_list(metadata);
}

// This is called at the end of each challenge.
void my_finalize() {
  // Nothing is here for now.
  // feel free to add something if you want!
}

void test() {
  // Implement here!
  assert(1 == 1);/* 1 is 1. That's always true! (You can remove this.) */
}
