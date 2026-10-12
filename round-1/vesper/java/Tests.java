public class Tests {
    static int total=0, failures=0;
    static void check(String n, boolean c){ total++; if(c) System.out.println("PASS "+n); else { failures++; System.out.println("FAIL "+n);} }
    interface R { void run(); }
    static boolean throwsEx(R r){ try{ r.run(); return false; } catch(RuntimeException e){ return true; } }
    public static void main(String[] a){
        { Pool p=new Pool(2); p.acquire(); check("acquire_marks_in_use", p.inUseCount()==1); }
        { Pool p=new Pool(2); Pool.Connection c=p.acquire(); p.release(c.connId); check("release_returns_to_idle", p.idleCount()==1 && p.inUseCount()==0); }
        { Pool p=new Pool(2); Pool.Connection c=p.acquire(); p.release(c.connId); p.acquire(); check("reacquire_reuses_idle", p.size()==1); }
        { Pool p=new Pool(2); Pool.Connection a1=p.acquire(); Pool.Connection b=p.acquire(); check("two_acquires_distinct", !a1.connId.equals(b.connId) && p.inUseCount()==2); }
        { Pool p=new Pool(2); p.acquire(); p.acquire(); check("capacity_enforced", throwsEx(()->p.acquire())); }
        { Pool p=new Pool(2); Pool.Connection c=p.acquire(); p.release(c.connId); check("release_requires_in_use", throwsEx(()->p.release(c.connId))); }
        { Pool p=new Pool(2); p.close(); check("no_acquire_after_close", throwsEx(()->p.acquire())); }
        { Pool p=new Pool(2); check("release_unknown_raises", throwsEx(()->p.release("nope"))); }
        { Pool p=new Pool(1); Pool.Connection a1=p.acquire(); p.release(a1.connId); p.acquire(); check("release_frees_capacity", p.inUseCount()==1); }
        System.out.println((failures>0?"FAILED ":"OK ")+(total-failures)+"/"+total); System.exit(failures>0?1:0);
    }
}
