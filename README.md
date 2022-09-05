CPCF: A Flexible Chunking and Proactive Insertion Cuckoo Filter
============

Overview
--------
CPCF is a type of approximate set-membership query data structure based on cuckoo filter. CGCF requires smaller space and provides better operational performance in most cases, compared to other cuckoo filter variants.



API
--------
A CPCF supports following operations:

*  `Add(item)`: insert an item to the filter
*  `Contain(item)`: return if item is already in the filter. Note that this method may return false positive results like cuckoo filters
*  `Delete(item)`: delete the given item from the filter. Note that to use this method, it must be ensured that this item is in the filter (e.g., based on records on external storage); otherwise, a false item may be deleted.
*  `Size()`: return the total number of items currently in the filter
*  `SizeInBytes()`: return the filter size in bytes
*  `NumChunks()`: return the number of sub-filters
*  `NumBuckets()`: return the number of buckets in a sub-filter

Here is a simple example in C++ for the basic usage of CGCF.
More examples can be found in `example/` directory.

```cpp
// Create a CPCF where each item is of type size_t and
// use 12 bits for each item and 4 tags for each bucket,
// with capacity of total_items
CPCF<size_t, 12, 4> filter(total_items);
// Insert item 12 to this CPCF
filter.Add(12);
// Check if previously inserted items are in the filter
assert(filter.Contain(12) == cuckoofilter::Ok);
```

Repository structure
--------------------
*  `src/`: the C++ header and implementation of CPCF
*  `example/test.cc`: an example of using CPCF


Build
-------
This libray depends on openssl library. Note that on MacOS 10.12, the header
files of openssl are not available by default. It may require to install openssl
and pass the path to `lib` and `include` directories to gcc, for example:

```bash
$ brew install openssl
# Replace 1.0.2j with the actual version of the openssl installed
$ export LDFLAGS="-L/usr/local/Cellar/openssl/1.0.2j/lib"
$ export CFLAGS="-I/usr/local/Cellar/openssl/1.0.2j/include"
```

To build the example (`example/test.cc`):
```bash
$ make test
```
