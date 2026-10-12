#include <iostream>
#include <functional>
static int total=0, failures=0;
static void check(const char* n, bool c){ ++total; std::cout<<(c?"PASS ":(++failures,"FAIL "))<<n<<"\n"; }
static bool throws(std::function<void()> f){ try{ f(); return false; } catch(...) { return true; } }
#include "inventory.hpp"
int main(){
    { double t=1000; InventoryService s({{"A",5},{"B",8}},60,[&]{return t;}); auto& r=s.reserve("A",2); check("reserve_reduces_available", r.status==ResStatus::HELD && s.available("A")==3); }
    { double t=1000; InventoryService s({{"A",5},{"B",8}},60,[&]{return t;}); auto& r=s.reserve("A",2); s.commit(r.reservation_id); check("commit_keeps_stock_consumed", s.available("A")==3); }
    { double t=1000; InventoryService s({{"A",5},{"B",8}},60,[&]{return t;}); auto& r=s.reserve("A",2); s.release(r.reservation_id); check("release_restores_stock", s.available("A")==5); }
    { double t=1000; InventoryService s({{"A",5},{"B",8}},60,[&]{return t;}); auto& r=s.reserve("A",2); s.release(r.reservation_id);
      bool a=throws([&]{ s.release(r.reservation_id); }); auto& r2=s.reserve("A",2); s.commit(r2.reservation_id); bool b=throws([&]{ s.release(r2.reservation_id); });
      check("release_non_held_rejected", a && b && s.available("A")==3); }
    { double t=1000; InventoryService s({{"A",5},{"B",8}},60,[&]{return t;}); s.reserve("A",2); t+=61; check("expired_hold_restores_stock", s.available("A")==5); }
    { double t=1000; InventoryService s({{"A",5},{"B",8}},60,[&]{return t;}); auto& r=s.reserve("A",2); t+=61; check("expired_hold_cannot_be_committed", throws([&]{ s.commit(r.reservation_id); })); }
    { double t=1000; InventoryService s({{"A",5},{"B",8}},60,[&]{return t;}); auto& r=s.reserve("A",2); s.commit(r.reservation_id); t+=1000; check("committed_survives_ttl", s.available("A")==3 && s.reserved_units("A")==2); }
    { double t=1000; InventoryService s({{"A",5},{"B",8}},60,[&]{return t;}); s.reserve("A",2); t+=61; check("reserved_units_reflects_expiry", s.reserved_units("A")==0); }
    { double t=1000; InventoryService s({{"A",5},{"B",8}},60,[&]{return t;}); check("reserve_rejects_oversell", throws([&]{ s.reserve("A",6); })); }
    { double t=1000; InventoryService s({{"A",5},{"B",8}},60,[&]{return t;}); s.reserve("A",2); s.reserve("A",1); check("reserve_sums_reduce", s.available("A")==2); }
    std::cout<<(failures?"FAILED ":"OK ")<<(total-failures)<<"/"<<total<<"\n"; return failures?1:0;
}
