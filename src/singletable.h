#ifndef CGCF_SINGLE_TABLE_H_
#define CGCF_SINGLE_TABLE_H_

#include <cassert>
#include <cmath>
#include <cstdlib>
#include <cstring>
#include <sstream>
#include <sys/mman.h>

#include "bitsutil.h"
#include "debug.h"
#include "printutil.h"

// Huge page version of CGCF switch
#define HUGE_PAGE false

namespace cuckoofilter
{

  // the most naive table implementation: one huge bit array
  template <size_t bits_per_tag, size_t tags_per_bucket>
  class SingleTable
  {
    static constexpr size_t kBytesPerBucket =
        (bits_per_tag * tags_per_bucket + 7) >> 3;
    static constexpr uint32_t kTagMask = (1U << bits_per_tag) - 1;
    // NOTE: accomodate extra buckets if necessary to avoid overrun
    // as we always read a uint64
    static constexpr size_t kPaddingBuckets =
        ((((kBytesPerBucket + 7) / 8) * 8) - 1) / kBytesPerBucket;

    struct Bucket
    {
      char bits_[kBytesPerBucket];
    } __attribute__((__packed__));

    // using a pointer adds one more indirection
    Bucket *buckets_;
    size_t num_buckets_;

  public:
    // size_t check_slots = 0;

    explicit SingleTable(const size_t num) : num_buckets_(num)
    {
#if HUGE_PAGE
      constexpr int prot = PROT_READ | PROT_WRITE;
      constexpr int flags = MAP_ANONYMOUS | MAP_PRIVATE | MAP_HUGETLB |
                            ((21 & MAP_HUGE_MASK) << MAP_HUGE_SHIFT);
      buckets_ =
          new (mmap(nullptr, (num_buckets_ + kPaddingBuckets) * kBytesPerBucket,
                    prot, flags, -1, 0)) Bucket[num_buckets_ +
                                                kPaddingBuckets];
#else
      buckets_ = new Bucket[num_buckets_ + kPaddingBuckets];
#endif
      memset(buckets_, 0, kBytesPerBucket * (num_buckets_ + kPaddingBuckets));
    }

    ~SingleTable()
    {
#if HUGE_PAGE
      munmap(buckets_, (num_buckets_ + kPaddingBuckets) * kBytesPerBucket);
#else
      delete[] buckets_;
#endif
    }

    size_t NumBuckets() const { return num_buckets_; }

    size_t SizeInBytes() const { return kBytesPerBucket * num_buckets_; }

    size_t SizeInTags() const { return tags_per_bucket * num_buckets_; }

    std::string Info() const
    {
      std::stringstream ss;
      ss << "SingleHashtable with tag size: " << bits_per_tag << " bits \n";
      ss << "\t\tAssociativity: " << tags_per_bucket << "\n";
      ss << "\t\tTotal # of rows: " << num_buckets_ << "\n";
      ss << "\t\tTotal # slots: " << SizeInTags() << "\n";
      return ss.str();
    }

    // read tag from pos(i,j)
    inline uint32_t ReadTag(const size_t i, const size_t j) const
    {
      const char *p = buckets_[i].bits_;
      uint32_t tag;
      /* following code only works for little-endian */
      if constexpr (bits_per_tag == 2)
      {
        tag = *((uint8_t *)p) >> (j * 2);
      }
      else if constexpr (bits_per_tag == 4)
      {
        p += (j >> 1);
        tag = *((uint8_t *)p) >> ((j & 1) << 2);
      }
      else if constexpr (bits_per_tag == 8)
      {
        p += j;
        tag = *((uint8_t *)p);
      }
      else if constexpr (bits_per_tag == 12)
      {
        p += j + (j >> 1);
        tag = *((uint16_t *)p) >> ((j & 1) << 2);
      }
      else if constexpr (bits_per_tag == 16)
      {
        p += (j << 1);
        tag = *((uint16_t *)p);
      }
      else if constexpr (bits_per_tag == 32)
      {
        tag = ((uint32_t *)p)[j];
      }
      return tag & kTagMask;
    }

    // write tag to pos(i,j)
    inline void WriteTag(const size_t i, const size_t j, const uint32_t t)
    {
      char *p = buckets_[i].bits_;
      uint32_t tag = t & kTagMask;
      /* following code only works for little-endian */
      if constexpr (bits_per_tag == 2)
      {
        *((uint8_t *)p) |= tag << (2 * j);
      }
      else if constexpr (bits_per_tag == 4)
      {
        p += (j >> 1);
        if ((j & 1) == 0)
        {
          *((uint8_t *)p) &= 0xf0;
          *((uint8_t *)p) |= tag;
        }
        else
        {
          *((uint8_t *)p) &= 0x0f;
          *((uint8_t *)p) |= (tag << 4);
        }
      }
      else if constexpr (bits_per_tag == 8)
      {
        ((uint8_t *)p)[j] = tag;
      }
      else if constexpr (bits_per_tag == 12)
      {
        p += (j + (j >> 1));
        if ((j & 1) == 0)
        {
          ((uint16_t *)p)[0] &= 0xf000;
          ((uint16_t *)p)[0] |= tag;
        }
        else
        {
          ((uint16_t *)p)[0] &= 0x000f;
          ((uint16_t *)p)[0] |= (tag << 4);
        }
      }
      else if constexpr (bits_per_tag == 16)
      {
        ((uint16_t *)p)[j] = tag;
      }
      else if constexpr (bits_per_tag == 32)
      {
        ((uint32_t *)p)[j] = tag;
      }
    }

    inline bool FindTagInBuckets(const size_t i1, const size_t i2,
                                 const uint32_t tag) const
    {
      const char *p1 = buckets_[i1].bits_;
      const char *p2 = buckets_[i2].bits_;

      uint64_t v1 = *((uint64_t *)p1);
      uint64_t v2 = *((uint64_t *)p2);

      // caution: unaligned access & assuming little endian
      if constexpr (bits_per_tag == 4 && tags_per_bucket == 4)
      {
        return hasvalue4(v1, tag) || hasvalue4(v2, tag);
      }
      else if constexpr (bits_per_tag == 8 && tags_per_bucket == 4)
      {
        return hasvalue8(v1, tag) || hasvalue8(v2, tag);
      }
      else if constexpr (bits_per_tag == 12 && tags_per_bucket == 4)
      {
        return hasvalue12(v1, tag) || hasvalue12(v2, tag);
      }
      else if constexpr (bits_per_tag == 16 && tags_per_bucket == 4)
      {
        return hasvalue16(v1, tag) || hasvalue16(v2, tag);
      }
      else
      {
        for (size_t j = 0; j < tags_per_bucket; j++)
        {
          if ((ReadTag(i1, j) == tag) || (ReadTag(i2, j) == tag))
          {
            return true;
          }
        }
        return false;
      }
    }

    inline bool FindTagInBucket(const size_t i, const uint32_t tag) const
    {
      // caution: unaligned access & assuming little endian
      if constexpr (bits_per_tag == 4 && tags_per_bucket == 4)
      {
        const char *p = buckets_[i].bits_;
        uint64_t v = *(uint64_t *)p; // uint16_t may suffice
        return hasvalue4(v, tag);
      }
      else if constexpr (bits_per_tag == 8 && tags_per_bucket == 4)
      {
        const char *p = buckets_[i].bits_;
        uint64_t v = *(uint64_t *)p; // uint32_t may suffice
        return hasvalue8(v, tag);
      }
      else if constexpr (bits_per_tag == 12 && tags_per_bucket == 4)
      {
        const char *p = buckets_[i].bits_;
        uint64_t v = *(uint64_t *)p;
        return hasvalue12(v, tag);
      }
      else if constexpr (bits_per_tag == 16 && tags_per_bucket == 4)
      {
        const char *p = buckets_[i].bits_;
        uint64_t v = *(uint64_t *)p;
        return hasvalue16(v, tag);
      }
      else
      {
        for (size_t j = 0; j < tags_per_bucket; j++)
        {
          if (ReadTag(i, j) == tag)
          {
            return true;
          }
        }
        return false;
      }
    }

    inline bool DeleteTagFromBucket(const size_t i, const uint32_t tag)
    {
      for (size_t j = 0; j < tags_per_bucket; j++)
      {
        if (ReadTag(i, j) == tag)
        {
          WriteTag(i, j, 0);
          return true;
        }
      }
      return false;
    }

    inline bool GenerousInsert(const size_t i, const uint32_t tag)
    {
      for (size_t j = 0; j < tags_per_bucket - 1; ++j)
      {
        // check_slots++;

        if (ReadTag(i, j) == 0)
        {
          WriteTag(i, j, tag);
          return true;
        }
      }
      return false;
    }

    inline bool ReverseInsert(const size_t i, const uint32_t tag)
    {
      for (size_t j = tags_per_bucket; j > 0;)
      {
        // check_slots++;

        const size_t pos = --j;
        if (ReadTag(i, pos) == 0)
        {
          WriteTag(i, pos, tag);
          return true;
        }
      }
      return false;
    }

    inline bool ReadAndInsert(const size_t i, const uint32_t tag,
                              uint32_t tags[tags_per_bucket])
    {
      for (size_t j = 0; j < tags_per_bucket; ++j)
      {
        // check_slots++;

        tags[j] = ReadTag(i, j);
        if (tags[j] == 0)
        {
          WriteTag(i, j, tag);
          return true;
        }
      }
      return false;
    }

    inline void Kickout(size_t &i, uint32_t &tag, uint32_t tags[tags_per_bucket],
                        size_t alts[tags_per_bucket])
    {
      const size_t r = rand() & (tags_per_bucket - 1);
      WriteTag(i, r, tag);
      tag = tags[r];
      i = alts[r];
      for (size_t j = 0; j < tags_per_bucket; ++j)
      {
        tags[j] = ReadTag(i, j);
      }
    }

    size_t NumTagsInBucket(const size_t i) const
    {
      size_t num = 0;
      for (size_t j = 0; j < tags_per_bucket; j++)
      {
        if (ReadTag(i, j) != 0)
        {
          ++num;
        }
      }
      return num;
    }
  };
} // namespace cuckoofilter
#endif // CGCF_SINGLE_TABLE_H_
