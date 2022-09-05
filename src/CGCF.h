#ifndef CGCF_H_
#define CGCF_H_

#include <cassert>

#include "debug.h"
#include "hashutil.h"
#include "printutil.h"
#include "singletable.h"

namespace cuckoofilter
{
  // status returned by a cuckoo filter operation
  enum Status
  {
    Ok = 0,
    NotFound = 1,
    NotEnoughSpace = 2,
    NotSupported = 3,
  };

  // A cuckoo filter class exposes a Bloomier filter interface,
  // providing methods of Add, Delete, Contain. It takes three
  // template parameters:
  //   ItemType:  the type of item you want to insert
  //   bits_per_item: how many bits each item is hashed into
  //   TableType: the storage of table, SingleTable by default, and
  // PackedTable to enable semi-sorting
  template <typename ItemType, size_t bits_per_item, size_t tags_per_bucket,
            template <size_t, size_t> class TableType = SingleTable,
            typename HashFamily = TwoIndependentMultiplyShift>
  class CGCF
  {
    // Storage of items
    TableType<bits_per_item, tags_per_bucket> *table_;

    // Number of items stored
    size_t num_items_;

    // Number of chunks and buckets in a chunk
    size_t num_chunks_, num_buckets_;

    // maximum number of cuckoo kicks before claiming failure
    size_t max_kickout_;

    typedef struct
    {
      size_t index;
      uint32_t tag;
      bool used;
    } VictimCache;

    VictimCache victim_;

    HashFamily hasher_;

    double Log_b(const double n) const
    {
      const double a = std::log(n * (tags_per_bucket - 1) + 1.0);
      const double b = std::log(tags_per_bucket);
      return a / b;
    }

    size_t MaxKickout(const size_t chunks, const size_t buckets) const
    {
      const double c = std::log(chunks);
      const double b = Log_b(buckets);
      return (size_t)std::ceil(2 * tags_per_bucket * c * b);
    }

    double BallsInBinsMaxLoad(const double balls, const double bins) const
    {
      return balls / bins + 1.5 * std::sqrt(2.0 * balls / bins * std::log(bins));
    }

    inline size_t IndexHash(const uint32_t hv) const
    {
      return (num_buckets_ * num_chunks_ * hv) >> 32;
    }

    inline uint32_t TagHash(const uint32_t hv) const
    {
      uint32_t tag;
      tag = hv & ((1ULL << bits_per_item) - 1);
      tag += (tag == 0);
      return tag;
    }

    inline void GenerateIndexTagHash(const ItemType &item,
                                     size_t *__restrict index,
                                     uint32_t *__restrict tag) const
    {
      const uint64_t hash = hasher_(item);
      *index = IndexHash(hash >> 32);
      *tag = TagHash(hash);
    }

    inline size_t AltIndex(const size_t index, const uint32_t tag) const
    {
      // 0x5bd1e995 is the hash constant from MurmurHash2
      uint32_t t = tag * 0x5bd1e995;
      t &= num_buckets_ - 1;
      return index ^ t;
    }

    inline Status AddImpl(const size_t i, const uint32_t tag)
    {
      size_t curindex = i;
      uint32_t curtag = tag;

      uint32_t tags[tags_per_bucket];
      size_t alts[tags_per_bucket];

      // check_buckets++;

      if (table_->GenerousInsert(curindex, curtag))
      {
        num_items_++;
        return Ok;
      }
      curindex = AltIndex(curindex, curtag);

      // check_buckets++;

      if (table_->ReadAndInsert(curindex, curtag, tags))
      {
        num_items_++;
        return Ok;
      }

      for (size_t count = 1; count < max_kickout_; ++count)
      {
        for (size_t j = 0; j < tags_per_bucket; j++)
        {
          alts[j] = AltIndex(curindex, tags[j]);

          // check_buckets++;

          if (table_->ReverseInsert(alts[j], tags[j]))
          {
            table_->WriteTag(curindex, j, curtag);
            // time[count]++;
            ++num_items_;
            return Ok;
          }
        }

        table_->Kickout(curindex, curtag, tags, alts);
      }

      victim_.index = curindex;
      victim_.tag = curtag;
      victim_.used = true;
      return Ok;
    }

    // load factor is the fraction of occupancy
    double LoadFactor() const { return 1.0 * Size() / table_->SizeInTags(); }

    double BitsPerItem() const { return 8.0 * table_->SizeInBytes() / Size(); }

  public:
    // size_t time[kMaxCuckooCount] = {0}, check_buckets = 0;

    explicit CGCF(const size_t max_num_keys)
        : num_items_(0), victim_(), hasher_()
    {
      size_t keys = max_num_keys;
      double buckets = (double)keys / tags_per_bucket / 0.95, chunks = 1, num;

      do
      {
        for (size_t tmp = 1; tmp <= buckets; tmp <<= 1)
        {
          num = buckets / tmp;
          if (BallsInBinsMaxLoad(keys, num) <= 0.96 * tags_per_bucket * tmp)
          {
            keys /= num;
            chunks *= num;
            buckets = tmp;
            break;
          }
        }
      } while (num >= 2);

      num_chunks_ = (size_t)std::ceil(chunks);
      num_buckets_ = upperpower2((size_t)std::ceil(buckets));

      max_kickout_ = MaxKickout(num_chunks_, num_buckets_);
      victim_.used = false;
      table_ = new TableType<bits_per_item, tags_per_bucket>(num_buckets_ *
                                                             num_chunks_);
    }

    ~CGCF() { delete table_; }

    // Add an item to the filter.
    Status Add(const ItemType &item)
    {
      size_t i;
      uint32_t tag;

      if (__builtin_expect(victim_.used, 0))
      {
        return NotEnoughSpace;
      }

      GenerateIndexTagHash(item, &i, &tag);

      return AddImpl(i, tag);
    }

    // Report if the item is inserted, with false positive rate.
    Status Contain(const ItemType &item) const
    {
      size_t i1, i2;
      uint32_t tag;

      GenerateIndexTagHash(item, &i1, &tag);
      i2 = AltIndex(i1, tag);

      if (table_->FindTagInBuckets(i1, i2, tag))
      {
        return Ok;
      }

      if (__builtin_expect(victim_.used && tag == victim_.tag &&
                               (i1 == victim_.index || i2 == victim_.index),
                           0))
      {
        return Ok;
      }

      return NotFound;
    }

    // Delete an key from the filter
    Status Delete(const ItemType &item)
    {
      size_t i1, i2;
      uint32_t tag;

      GenerateIndexTagHash(item, &i1, &tag);
      i2 = AltIndex(i1, tag);

      if (table_->DeleteTagFromBucket(i1, tag))
      {
        num_items_--;
        goto TryEliminateVictim;
      }
      else if (table_->DeleteTagFromBucket(i2, tag))
      {
        num_items_--;
        goto TryEliminateVictim;
      }
      else if (victim_.used && tag == victim_.tag &&
               (i1 == victim_.index || i2 == victim_.index))
      {
        // num_items_--;
        victim_.used = false;
        return Ok;
      }
      else
      {
        return NotFound;
      }
    TryEliminateVictim:
      if (__builtin_expect(victim_.used, 0))
      {
        victim_.used = false;
        size_t i = victim_.index;
        uint32_t tag = victim_.tag;
        AddImpl(i, tag);
      }
      return Ok;
    }

    /* methods for providing stats  */
    // summary infomation
    std::string Info() const
    {
      std::stringstream ss;
      ss << "CuckooFilter Status:\n"
         << "\t\t" << table_->Info() << "\n"
         << "\t\tKeys stored: " << Size() << "\n"
         << "\t\tLoad factor: " << LoadFactor() << "\n"
         << "\t\tHashtable size: " << (table_->SizeInBytes() >> 10) << " KB\n";
      if (Size() > 0)
      {
        ss << "\t\tbit/key:   " << BitsPerItem() << "\n";
      }
      else
      {
        ss << "\t\tbit/key:   N/A\n";
      }
      return ss.str();
    }

    // number of current inserted items;
    size_t Size() const { return num_items_; }

    // size of the filter in bytes.
    size_t SizeInBytes() const { return table_->SizeInBytes(); }

    // number of chunks
    size_t NumChunks() const { return num_chunks_; }

    // number of buckes in a chunk
    size_t NumBuckets() const { return num_buckets_; }

    // size_t CheckSlots() const { return table_->check_slots; }
  };
} // namespace cuckoofilter
#endif // CGCF_H_
