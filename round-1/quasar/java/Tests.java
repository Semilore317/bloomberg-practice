public class Tests {
    static int total=0, failures=0;
    static void check(String n, boolean c){ total++; if(c) System.out.println("PASS "+n); else { failures++; System.out.println("FAIL "+n);} }
    static class Clk implements java.util.function.DoubleSupplier { double v=1000; public double getAsDouble(){return v;} }
    public static void main(String[] a){
        { Clk c=new Clk(); RateLimit r=new RateLimit(3,10,c); check("allows_under_limit", r.allow("k")&&r.allow("k")&&r.allow("k")); }
        { Clk c=new Clk(); RateLimit r=new RateLimit(3,10,c); for(int i=0;i<3;i++) r.allow("k"); check("blocks_at_limit", r.allow("k")==false); }
        { Clk c=new Clk(); RateLimit r=new RateLimit(3,10,c); r.allow("k"); check("remaining_counts_down", r.remaining("k")==2); }
        { Clk c=new Clk(); RateLimit r=new RateLimit(3,10,c); for(int i=0;i<3;i++) r.allow("k"); check("remaining_zero_at_limit", r.remaining("k")==0); }
        { Clk c=new Clk(); RateLimit r=new RateLimit(3,10,c); for(int i=0;i<3;i++) r.allow("a"); check("separate_keys_independent", r.allow("b")==true); }
        { Clk c=new Clk(); RateLimit r=new RateLimit(3,10,c); for(int i=0;i<3;i++) r.allow("k"); boolean blocked=(r.allow("k")==false); c.v+=11; check("window_resets_after_window", blocked && r.allow("k")==true); }
        { Clk c=new Clk(); RateLimit r=new RateLimit(3,10,c); r.allow("k"); r.allow("k"); c.v+=11; check("remaining_resets_after_window", r.remaining("k")==3); }
        { Clk c=new Clk(); RateLimit r=new RateLimit(3,10,c); for(int i=0;i<3;i++) r.allow("k"); r.reset("k"); check("reset_clears_the_window", r.allow("k")==true); }
        System.out.println((failures>0?"FAILED ":"OK ")+(total-failures)+"/"+total); System.exit(failures>0?1:0);
    }
}
