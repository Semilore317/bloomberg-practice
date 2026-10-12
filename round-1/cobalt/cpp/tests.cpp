#include <iostream>
#include <functional>
static int total=0, failures=0;
static void check(const char* n, bool c){ ++total; std::cout<<(c?"PASS ":(++failures,"FAIL "))<<n<<"\n"; }
static bool throws(std::function<void()> f){ try{ f(); return false; } catch(...) { return true; } }
#include "wallet.hpp"
static WalletService acct(){ WalletService s; s.open_account("a1",500); return s; }
int main(){
    { auto s=acct(); check("open_sets_balance", s.balance("a1")==500 && s.available("a1")==500); }
    { auto s=acct(); s.authorize("a1",300); check("authorize_reduces_available", s.balance("a1")==500 && s.available("a1")==200); }
    { auto s=acct(); s.authorize("a1",300); check("authorize_keeps_balance", s.balance("a1")==500); }
    { auto s=acct(); auto& h=s.authorize("a1",300); s.capture(h.hold_id); check("capture_reduces_balance", s.balance("a1")==200); }
    { auto s=acct(); auto& h=s.authorize("a1",300); s.capture(h.hold_id); check("capture_frees_hold", s.available("a1")==200); }
    { auto s=acct(); auto& h=s.authorize("a1",300); s.voidHold(h.hold_id); check("void_restores_available", s.available("a1")==500 && s.balance("a1")==500); }
    { auto s=acct(); auto& h=s.authorize("a1",300); s.voidHold(h.hold_id); bool a=throws([&]{ s.voidHold(h.hold_id); }); auto& h2=s.authorize("a1",100); s.capture(h2.hold_id); bool b=throws([&]{ s.voidHold(h2.hold_id); }); check("void_non_held_rejected", a && b); }
    { auto s=acct(); auto& h=s.authorize("a1",300); s.voidHold(h.hold_id); check("capture_non_held_rejected", throws([&]{ s.capture(h.hold_id); })); }
    { auto s=acct(); check("unknown_hold_raises", throws([&]{ s.voidHold("nope"); })); }
    { auto s=acct(); check("authorize_rejects_nonpositive", throws([&]{ s.authorize("a1",0); })); }
    std::cout<<(failures?"FAILED ":"OK ")<<(total-failures)<<"/"<<total<<"\n"; return failures?1:0;
}
