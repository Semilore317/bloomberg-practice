#include <iostream>
static int total=0, failures=0;
static void check(const char* n, bool c){ ++total; std::cout<<(c?"PASS ":(++failures,"FAIL "))<<n<<"\n"; }
#include "cache.hpp"
int main(){
    { double t=1000; LRUCache c(2,60,[&]{return t;}); c.put("a",1); auto r=c.get("a"); check("put_get", r.first && r.second==1); }
    { double t=1000; LRUCache c(2,60,[&]{return t;}); check("missing_returns_none", c.get("x").first==false); }
    { double t=1000; LRUCache c(2,60,[&]{return t;}); c.put("a",1); c.put("a",2); auto r=c.get("a"); check("update_existing", r.first && r.second==2); }
    { double t=1000; LRUCache c(2,60,[&]{return t;}); c.put("a",1); c.put("b",2); c.put("c",3); check("capacity_evicts_oldest", c.get("a").first==false && c.get("c").second==3); }
    { double t=1000; LRUCache c(3,60,[&]{return t;}); c.put("a",1); c.put("b",2); check("size_counts_live", c.size()==2); }
    { double t=1000; LRUCache c(2,60,[&]{return t;}); c.put("a",1); c.put("b",2); auto ga=c.get("a"); c.put("c",3); check("lru_evicts_least_recently_used", ga.first && ga.second==1 && c.get("b").first==false && c.get("a").second==1); }
    { double t=1000; LRUCache c(2,60,[&]{return t;}); c.put("a",1); t+=61; check("expired_get_returns_none", c.get("a").first==false); }
    { double t=1000; LRUCache c(2,60,[&]{return t;}); c.put("a",1); t+=61; check("expired_not_counted_in_size", c.size()==0); }
    std::cout<<(failures?"FAILED ":"OK ")<<(total-failures)<<"/"<<total<<"\n"; return failures?1:0;
}
