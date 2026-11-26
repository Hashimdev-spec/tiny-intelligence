#include <stdio.h>
#include <time.h>
int main(){ struct timespec a,b; clock_gettime(CLOCK_MONOTONIC,&a);
 unsigned long long total=0; for(unsigned long long i=1;i<=1000000000ULL;i++) total+=i;
 clock_gettime(CLOCK_MONOTONIC,&b);
 printf("%llu in %.4fs\n", total, (b.tv_sec-a.tv_sec)+(b.tv_nsec-a.tv_nsec)/1e9); }
