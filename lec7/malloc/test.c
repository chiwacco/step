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
  my_metadata_t *free_head;
  my_metadata_t dummy;
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
// Interfaces of malloc (DO NOT RENAME FOLLOWING FUNCTIONS!)
//

// This is called at the beginning of each challenge.
void my_initialize() {
  my_heap.free_head = &my_heap.dummy;
  my_heap.dummy.size = 0;
  my_heap.dummy.next = NULL;
}

// my_malloc() is called every time an object is allocated.
// |size| is guaranteed to be a multiple of 8 bytes and meets 8 <= |size| <=
// 4000. You are not allowed to use any library functions other than
// mmap_from_system() / munmap_to_system().

void *my_malloc(size_t size) {
  my_metadata_t *best_fit = NULL;
  my_metadata_t *best_fit_prev = NULL;
  my_metadata_t *metadata = my_heap.free_head;
  my_metadata_t *prev = NULL;

  // Find the best-fit block
  while (metadata) {
    if (metadata->size >= size && (!best_fit || metadata->size < best_fit->size)) {
      best_fit = metadata;
      best_fit_prev = prev;
    }
    prev = metadata;
    metadata = metadata->next;
  }
  
  if (!best_fit) {
    // No suitable free slot found, request a new memory region
    size_t buffer_size = 4096;
    my_metadata_t *new_metadata = (my_metadata_t *)mmap_from_system(buffer_size);
    new_metadata->size = buffer_size - sizeof(my_metadata_t);
    new_metadata->next = NULL;
    // Add the memory region to the free list.
    my_add_to_free_list(new_metadata);
    // Retry my_malloc()
    return my_malloc(size);
  }

  // |ptr| is the beginning of the allocated object
  void *ptr = (void *)(best_fit + 1);
  size_t remaining_size = best_fit->size - size;

  // Remove the best-fit block from the free list
  my_remove_from_free_list(best_fit, best_fit_prev);

  if (remaining_size > sizeof(my_metadata_t)) {
    // Create a new metadata for the remaining free slot
    my_metadata_t *new_metadata = (my_metadata_t *)((char *)ptr + size);
    new_metadata->size = remaining_size - sizeof(my_metadata_t);
    new_metadata->next = NULL;
    // Add the remaining free slot to the free list
    my_add_to_free_list(new_metadata);
    // Update the size of the allocated block
    best_fit->size = size;
  }

  return ptr;
}

// This is called every time an object is freed. You are not allowed to
// use any library functions other than mmap_from_system / munmap_to_system.
void my_free(void *ptr) {
  // Look up the metadata. The metadata is placed just prior to the object.
  my_metadata_t *metadata = (my_metadata_t *)ptr - 1;
  // Add the free block to the free list.
  my_add_to_free_list(metadata);
}

// This is called at the end of each challenge.
void my_finalize() {
  // Nothing needed here for now.
}

void test() {
  // Implement test cases if needed.
  assert(1 == 1); // Placeholder assertion
}
