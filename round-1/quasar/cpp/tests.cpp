#include <iostream>
#include <functional>
static int total=0, failures=0;
static void check(const char* n, bool c){ ++total; std::cout<<(c?"PASS ":(++failures,"FAIL "))<<n<<"\n"; }
static bool throws(std::function<void()> f){ try{ f(); return false; } catch(...) { return true; } }
#include "ratelimit.hpp"
int main(){
    { double t=1000; RateLimiter r(3,10,[&]{return t;}); bool ok=r.allow("k")&&r.allow("k")&&r.allow("k"); check("allows_under_limit", ok); }
    { double t=1000; RateLimiter r(3,10,[&]{return t;}); for(int i=0;i<3;i++) r.allow("k"); check("blocks_at_limit", r.allow("k")==false); }
    { double t=1000; RateLimiter r(3,10,[&]{return t;}); r.allow("k"); check("remaining_counts_down", r.remaining("k")==2); }
    { double t=1000; RateLimiter r(3,10,[&]{return t;}); for(int i=0;i<3;i++) r.allow("k"); check("remaining_zero_at_limit", r.remaining("k")==0); }
    { double t=1000; RateLimiter r(3,10,[&]{return t;}); for(int i=0;i<3;i++) r.allow("a"); check("separate_keys_independent", r.allow("b")==true); }
    { double t=1000; RateLimiter r(3,10,[&]{return t;}); for(int i=0;i<3;i++) r.allow("k"); bool blocked=(r.allow("k")==false); t+=11; check("window_resets_after_window", blocked && r.allow("k")==true); }
    { double t=1000; RateLimiter r(3,10,[&]{return t;}); r.allow("k"); r.allow("k"); t+=11; check("remaining_resets_after_window", r.remaining("k")==3); }
    { double t=1000; RateLimiter r(3,10,[&]{return t;}); for(int i=0;i<3;i++) r.allow("k"); r.reset("k"); check("reset_clears_the_window", r.allow("k")==true); }
    std::cout<<(failures?"FAILED ":"OK ")<<(total-failures)<<"/"<<total<<"\n"; return failures?1:0;
}
