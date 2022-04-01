#include "CGCF.h"

#include <cassert>
#include <iostream>
#include <vector>

using cuckoofilter::CGCF;
using namespace std;

int main(int argc, char **argv)
{
  size_t total_items = 1000000;

  // Create a CGCF where each item is of type size_t and
  // use 12 bits for each item and 4 tags for each bucket:
  CGCF<size_t, 12, 4> filter(total_items);

  // Insert items to this CGCF
  size_t num_inserted = 0;
  for (size_t i = 0; i < total_items; i++, num_inserted++)
  {
    if (filter.Add(i) != cuckoofilter::Ok)
    {
      break;
    }
  }

  // Check if previously inserted items are in the filter, expected
  // true for all items
  for (size_t i = 0; i < num_inserted; i++)
  {
    assert(filter.Contain(i) == cuckoofilter::Ok);
  }

  // Check non-existing items, a few false positive expected
  size_t total_queries = 0;
  size_t false_queries = 0;
  for (size_t i = total_items; i < 2 * total_items; i++)
  {
    if (filter.Contain(i) == cuckoofilter::Ok)
    {
      false_queries++;
    }
    total_queries++;
  }

  cout << "false positive rate is "
       << 100.0 * false_queries / total_queries << "%\n";

  return 0;
}
