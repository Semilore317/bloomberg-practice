public class Tests {
    static int total=0, failures=0;
    static void check(String n, boolean c){ total++; if(c) System.out.println("PASS "+n); else { failures++; System.out.println("FAIL "+n);} }
    interface R { void run(); }
    static boolean throwsEx(R r){ try{ r.run(); return false; } catch(RuntimeException e){ return true; } }
    static class Clk implements java.util.function.DoubleSupplier { double v=1000; public double getAsDouble(){return v;} }
    public static void main(String[] a){
        { Clk c=new Clk(); Subscriptions s=new Subscriptions(60,c); Subscriptions.Subscription x=s.startTrial("u1"); check("trial_is_entitled", x.status==Subscriptions.SubStatus.TRIAL && s.isEntitled(x.subId)); }
        { Clk c=new Clk(); Subscriptions s=new Subscriptions(60,c); Subscriptions.Subscription x=s.startTrial("u1"); s.activate(x.subId); check("activate_makes_active", x.status==Subscriptions.SubStatus.ACTIVE && s.isEntitled(x.subId)); }
        { Clk c=new Clk(); Subscriptions s=new Subscriptions(60,c); Subscriptions.Subscription x=s.startTrial("u1"); s.activate(x.subId); s.suspend(x.subId); check("suspend_removes_entitlement", !s.isEntitled(x.subId)); }
        { Clk c=new Clk(); Subscriptions s=new Subscriptions(60,c); Subscriptions.Subscription x=s.startTrial("u1"); s.activate(x.subId); s.suspend(x.subId); s.resume(x.subId); check("resume_restores_entitlement", s.isEntitled(x.subId)); }
        { Clk c=new Clk(); Subscriptions s=new Subscriptions(60,c); Subscriptions.Subscription x=s.startTrial("u1"); s.activate(x.subId); s.cancel(x.subId); check("cancel_removes_entitlement", !s.isEntitled(x.subId)); }
        { Clk c=new Clk(); Subscriptions s=new Subscriptions(60,c); Subscriptions.Subscription x=s.startTrial("u1"); s.cancel(x.subId); check("cancelled_cannot_be_reactivated", throwsEx(()->s.activate(x.subId))); }
        { Clk c=new Clk(); Subscriptions s=new Subscriptions(60,c); Subscriptions.Subscription x=s.startTrial("u1"); s.cancel(x.subId); check("double_cancel_rejected", throwsEx(()->s.cancel(x.subId))); }
        { Clk c=new Clk(); Subscriptions s=new Subscriptions(60,c); Subscriptions.Subscription x=s.startTrial("u1"); c.v+=61; check("expired_trial_not_entitled", !s.isEntitled(x.subId)); }
        { Clk c=new Clk(); Subscriptions s=new Subscriptions(60,c); Subscriptions.Subscription x=s.startTrial("u1"); s.activate(x.subId); c.v+=1000; check("active_survives_trial_ttl", s.isEntitled(x.subId)); }
        { Clk c=new Clk(); Subscriptions s=new Subscriptions(60,c); Subscriptions.Subscription x=s.startTrial("u1"); c.v+=61; check("expired_trial_cannot_be_activated", throwsEx(()->s.activate(x.subId))); }
        System.out.println((failures>0?"FAILED ":"OK ")+(total-failures)+"/"+total); System.exit(failures>0?1:0);
    }
}
