public class Tests {
    static int total=0, failures=0;
    static void check(String n, boolean c){ total++; if(c) System.out.println("PASS "+n); else { failures++; System.out.println("FAIL "+n);} }
    interface R { void run(); }
    static boolean throwsEx(R r){ try{ r.run(); return false; } catch(RuntimeException e){ return true; } }
    static Wallet acct(){ Wallet s=new Wallet(); s.openAccount("a1",500); return s; }
    public static void main(String[] a){
        { Wallet s=acct(); check("open_sets_balance", s.balance("a1")==500 && s.available("a1")==500); }
        { Wallet s=acct(); s.authorize("a1",300); check("authorize_reduces_available", s.balance("a1")==500 && s.available("a1")==200); }
        { Wallet s=acct(); s.authorize("a1",300); check("authorize_keeps_balance", s.balance("a1")==500); }
        { Wallet s=acct(); Wallet.Hold h=s.authorize("a1",300); s.capture(h.holdId); check("capture_reduces_balance", s.balance("a1")==200); }
        { Wallet s=acct(); Wallet.Hold h=s.authorize("a1",300); s.capture(h.holdId); check("capture_frees_hold", s.available("a1")==200); }
        { Wallet s=acct(); Wallet.Hold h=s.authorize("a1",300); s.voidHold(h.holdId); check("void_restores_available", s.available("a1")==500 && s.balance("a1")==500); }
        { Wallet s=acct(); Wallet.Hold h=s.authorize("a1",300); s.voidHold(h.holdId); boolean x=throwsEx(()->s.voidHold(h.holdId)); Wallet.Hold h2=s.authorize("a1",100); s.capture(h2.holdId); boolean y=throwsEx(()->s.voidHold(h2.holdId)); check("void_non_held_rejected", x && y); }
        { Wallet s=acct(); Wallet.Hold h=s.authorize("a1",300); s.voidHold(h.holdId); check("capture_non_held_rejected", throwsEx(()->s.capture(h.holdId))); }
        { Wallet s=acct(); check("unknown_hold_raises", throwsEx(()->s.voidHold("nope"))); }
        { Wallet s=acct(); check("authorize_rejects_nonpositive", throwsEx(()->s.authorize("a1",0))); }
        System.out.println((failures>0?"FAILED ":"OK ")+(total-failures)+"/"+total); System.exit(failures>0?1:0);
    }
}
