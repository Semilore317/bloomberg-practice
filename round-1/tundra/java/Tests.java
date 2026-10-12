public class Tests {
    static int total=0, failures=0;
    static void check(String n, boolean c){ total++; if(c) System.out.println("PASS "+n); else { failures++; System.out.println("FAIL "+n);} }
    static class Clk implements java.util.function.DoubleSupplier { double v=1000; public double getAsDouble(){return v;} }
    public static void main(String[] a){
        { Clk c=new Clk(); Cache ch=new Cache(2,60,c); ch.put("a",1); Integer r=ch.get("a"); check("put_get", r!=null && r==1); }
        { Clk c=new Clk(); Cache ch=new Cache(2,60,c); check("missing_returns_none", ch.get("x")==null); }
        { Clk c=new Clk(); Cache ch=new Cache(2,60,c); ch.put("a",1); ch.put("a",2); Integer r=ch.get("a"); check("update_existing", r!=null && r==2); }
        { Clk c=new Clk(); Cache ch=new Cache(2,60,c); ch.put("a",1); ch.put("b",2); ch.put("c",3); check("capacity_evicts_oldest", ch.get("a")==null && ch.get("c")!=null && ch.get("c")==3); }
        { Clk c=new Clk(); Cache ch=new Cache(3,60,c); ch.put("a",1); ch.put("b",2); check("size_counts_live", ch.size()==2); }
        { Clk c=new Clk(); Cache ch=new Cache(2,60,c); ch.put("a",1); ch.put("b",2); Integer ga=ch.get("a"); ch.put("c",3); check("lru_evicts_least_recently_used", ga!=null && ga==1 && ch.get("b")==null && ch.get("a")!=null && ch.get("a")==1); }
        { Clk c=new Clk(); Cache ch=new Cache(2,60,c); ch.put("a",1); c.v+=61; check("expired_get_returns_none", ch.get("a")==null); }
        { Clk c=new Clk(); Cache ch=new Cache(2,60,c); ch.put("a",1); c.v+=61; check("expired_not_counted_in_size", ch.size()==0); }
        System.out.println((failures>0?"FAILED ":"OK ")+(total-failures)+"/"+total); System.exit(failures>0?1:0);
    }
}
