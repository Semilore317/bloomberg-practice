#include <iostream>
#include <functional>
static int total=0, failures=0;
static void check(const char* n, bool c){ ++total; std::cout<<(c?"PASS ":(++failures,"FAIL "))<<n<<"\n"; }
static bool throws(std::function<void()> f){ try{ f(); return false; } catch(...) { return true; } }
#include "pool.hpp"
int main(){
    { ConnectionPool p(2); p.acquire(); check("acquire_marks_in_use", p.in_use_count()==1); }
    { ConnectionPool p(2); auto& c=p.acquire(); p.release(c.conn_id); check("release_returns_to_idle", p.idle_count()==1 && p.in_use_count()==0); }
    { ConnectionPool p(2); auto& c=p.acquire(); p.release(c.conn_id); p.acquire(); check("reacquire_reuses_idle", p.size()==1); }
    { ConnectionPool p(2); auto& a=p.acquire(); auto& b=p.acquire(); check("two_acquires_distinct", a.conn_id!=b.conn_id && p.in_use_count()==2); }
    { ConnectionPool p(2); p.acquire(); p.acquire(); check("capacity_enforced", throws([&]{ p.acquire(); })); }
    { ConnectionPool p(2); auto& c=p.acquire(); p.release(c.conn_id); check("release_requires_in_use", throws([&]{ p.release(c.conn_id); })); }
    { ConnectionPool p(2); p.close(); check("no_acquire_after_close", throws([&]{ p.acquire(); })); }
    { ConnectionPool p(2); check("release_unknown_raises", throws([&]{ p.release("nope"); })); }
    { ConnectionPool p(1); auto& a=p.acquire(); p.release(a.conn_id); p.acquire(); check("release_frees_capacity", p.in_use_count()==1); }
    std::cout<<(failures?"FAILED ":"OK ")<<(total-failures)<<"/"<<total<<"\n"; return failures?1:0;
}
