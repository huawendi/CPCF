#include <chrono>
#include <iostream>
#include <random>
#include <vector>

using namespace std;

void random_gen(const size_t n, vector<uint32_t> &store, mt19937 &rd)
{
    store.resize(n);
    for (size_t i = 0; i < n; i++)
    {
        store[i] = rd();
    }
}

uint32_t fun_and(const uint32_t x, const uint32_t s)
{
    return x & (s - 1);
}

uint32_t fun_move(const uint32_t x, const uint32_t s)
{
    uint64_t tmp = x * s;
    return tmp >> 32;
}

uint32_t fun_mod(const uint32_t x, const uint32_t s)
{
    return x % s;
}

int main()
{
    auto start = chrono::system_clock::now();
    auto end = chrono::system_clock::now();

    unsigned seed = chrono::system_clock::now().time_since_epoch().count();
    mt19937 rd(seed);

    vector<uint32_t> nums;
    random_gen(100, nums, rd);

    // for (size_t i = 0; i < nums.size(); i++)
    // {
    //     cout << nums[i] << endl;
    // }

    chrono::duration<double> and_time, move_time, mod_time;

    for (size_t i = 10; i < 31; i++)
    {
        cout << i << ":\n";

        start = chrono::system_clock::now();
        for (size_t j = 0; j < nums.size(); j++)
        {
            fun_and(nums[j], (1 << i));
        }
        end = chrono::system_clock::now();
        and_time = end - start;
        cout << and_time.count() * 1e+6 << endl;

        start = chrono::system_clock::now();
        for (size_t j = 0; j < nums.size(); j++)
        {
            fun_move(nums[j], (1 << i));
        }
        end = chrono::system_clock::now();
        move_time = end - start;
        cout << move_time.count() * 1e+6 << endl;

        start = chrono::system_clock::now();
        for (size_t j = 0; j < nums.size(); j++)
        {
            fun_mod(nums[j], (1 << i));
        }
        end = chrono::system_clock::now();
        mod_time = end - start;
        cout << mod_time.count() * 1e+6 << endl;
    }


    return 0;
}