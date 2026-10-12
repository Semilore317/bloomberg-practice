#include <iostream>
#include <functional>
#include "orders.hpp"
static int total=0, failures=0;
static void check(const char* n, bool c){ ++total; std::cout<<(c?"PASS ":(++failures,"FAIL "))<<n<<"\n"; }
static bool throws(std::function<void()> f){ try{ f(); return false; } catch(...) { return true; } }
int main(){
    { OrderService s; auto& o=s.place("AAPL","buy",10); check("place_creates_open_order", o.status==OrderStatus::OPEN && s.remaining(o.order_id)==10); }
    { OrderService s; auto& o=s.place("AAPL","buy",10); s.fill(o.order_id,4); check("partial_fill_sets_partial_and_remaining", o.status==OrderStatus::PARTIAL && s.remaining(o.order_id)==6); }
    { OrderService s; auto& o=s.place("AAPL","buy",10); s.fill(o.order_id,10); check("full_fill_sets_filled", o.status==OrderStatus::FILLED && s.remaining(o.order_id)==0); }
    { OrderService s; auto& o=s.place("AAPL","buy",10); s.fill(o.order_id,4); s.fill(o.order_id,6); check("two_fills_accumulate", o.status==OrderStatus::FILLED); }
    { OrderService s; auto& o=s.place("AAPL","buy",10); check("overfill_rejected", throws([&]{ s.fill(o.order_id,11); })); }
    { OrderService s; auto& o=s.place("AAPL","buy",10); s.cancel(o.order_id); check("fill_cancelled_order_rejected", throws([&]{ s.fill(o.order_id,1); })); }
    { OrderService s; auto& o=s.place("AAPL","buy",10); s.cancel(o.order_id); check("cancel_open_order", o.status==OrderStatus::CANCELLED); }
    { OrderService s; auto& o=s.place("AAPL","buy",10); s.cancel(o.order_id); check("double_cancel_rejected", throws([&]{ s.cancel(o.order_id); })); }
    { OrderService s; auto& o=s.place("AAPL","buy",10); s.cancel(o.order_id); check("open_qty_excludes_cancelled", s.open_qty_for("AAPL")==0); }
    { OrderService s; auto& a=s.place("AAPL","buy",10); s.place("AAPL","buy",5); s.fill(a.order_id,4); check("open_qty_sums_remaining", s.open_qty_for("AAPL")==11); }
    std::cout<<(failures?"FAILED ":"OK ")<<(total-failures)<<"/"<<total<<"\n"; return failures?1:0;
}
