#include <algorithm>
#include <chrono>
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <iomanip> // For std::setprecision

long int parseLine(const std::string& line) {
    std::size_t i = line.find_first_of("0123456789");
    std::string number_str = line.substr(i);
    number_str = number_str.substr(0, number_str.size() - 3);
    // Remove the " kB" part
    return std::stol(number_str);
}

long int getMemAvailable() {
    // MemAvailable:   703402688 kB
    std::ifstream file("/proc/meminfo");
    std::string line;
    long int result = -1;
    while (std::getline(file, line)) {
        if (line.compare(0, 13, "MemAvailable:") == 0) {
            result = parseLine(line);
            break;
        }
    }

    return result;
}

double pctg_mem_tested() {
    double mem_avail_kB = getMemAvailable();
    double four_gb_kB = (1L << 32) / 1024.;
    double pctg = (four_gb_kB / mem_avail_kB) * 100;

    return pctg;
}

double test_alloc(size_t n, char c)
{
    /* time to allocate + fill */
    auto t0 = std::chrono::high_resolution_clock::now();
    /* memory is allocated using "malloc" since
       "std::unique_ptr<char[]> ptr(new char[n])"
       also creates the objects via "new[]" */
    char* ptr = (char*)std::malloc(n);
    std::fill(ptr, ptr + n, c);
    auto t1 = std::chrono::high_resolution_clock::now();

    double t_alloc_fill =
        std::chrono::duration_cast<std::chrono::duration<double>>(t1 - t0)
        .count();
    /* prevent compiler optimizations */
    t_alloc_fill += static_cast<double>(*ptr);

    /* time to fill */
    t0 = std::chrono::high_resolution_clock::now();
    std::fill(ptr, ptr + n, c);
    t1 = std::chrono::high_resolution_clock::now();
    double t_fill =
        std::chrono::duration_cast<std::chrono::duration<double>>(t1 - t0)
        .count();
   
    /* prevent compiler optimizations */
    t_fill += static_cast<double>(*ptr);

    std::free(ptr);

    return t_alloc_fill - t_fill;
}

int main(int argc, char** argv) {
  for (size_t i = 20; i < 33; ++i) {
    std::cout << i << ": " << (1L << i) / static_cast<double>(1024.0 * 1024.0)
        << " MB, allocation time " << test_alloc(1L << i, 0)
        << " sec." << std::endl;
    if (i == 32)
        std::cout << "(last allocation is "
            << std::setprecision(2)
            << pctg_mem_tested() << "% of MemAvailable)" << std::endl;
    }

    return 0;
}
