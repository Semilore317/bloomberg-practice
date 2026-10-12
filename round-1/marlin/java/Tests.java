import java.util.*;
public class Tests {
    static int total=0, failures=0;
    static void check(String n, boolean c){ total++; if(c) System.out.println("PASS "+n); else { failures++; System.out.println("FAIL "+n);} }
    interface R { void run(); }
    static boolean throwsEx(R r){ try{ r.run(); return false; } catch(RuntimeException e){ return true; } }
    static class Clk implements java.util.function.DoubleSupplier { double v=1000; public double getAsDouble(){return v;} }
    static Map<String,Integer> stock(){ Map<String,Integer> m=new HashMap<>(); m.put("A",5); m.put("B",8); return m; }
    public static void main(String[] a){
        { Clk c=new Clk(); Inventory s=new Inventory(stock(),60,c); Inventory.Reservation r=s.reserve("A",2); check("reserve_reduces_available", r.status==Inventory.ResStatus.HELD && s.available("A")==3); }
        { Clk c=new Clk(); Inventory s=new Inventory(stock(),60,c); Inventory.Reservation r=s.reserve("A",2); s.commit(r.reservationId); check("commit_keeps_stock_consumed", s.available("A")==3); }
        { Clk c=new Clk(); Inventory s=new Inventory(stock(),60,c); Inventory.Reservation r=s.reserve("A",2); s.release(r.reservationId); check("release_restores_stock", s.available("A")==5); }
        { Clk c=new Clk(); Inventory s=new Inventory(stock(),60,c); Inventory.Reservation r=s.reserve("A",2); s.release(r.reservationId);
          boolean x=throwsEx(()->s.release(r.reservationId)); Inventory.Reservation r2=s.reserve("A",2); s.commit(r2.reservationId); boolean y=throwsEx(()->s.release(r2.reservationId));
          check("release_non_held_rejected", x && y && s.available("A")==3); }
        { Clk c=new Clk(); Inventory s=new Inventory(stock(),60,c); s.reserve("A",2); c.v+=61; check("expired_hold_restores_stock", s.available("A")==5); }
        { Clk c=new Clk(); Inventory s=new Inventory(stock(),60,c); Inventory.Reservation r=s.reserve("A",2); c.v+=61; check("expired_hold_cannot_be_committed", throwsEx(()->s.commit(r.reservationId))); }
        { Clk c=new Clk(); Inventory s=new Inventory(stock(),60,c); Inventory.Reservation r=s.reserve("A",2); s.commit(r.reservationId); c.v+=1000; check("committed_survives_ttl", s.available("A")==3 && s.reservedUnits("A")==2); }
        { Clk c=new Clk(); Inventory s=new Inventory(stock(),60,c); s.reserve("A",2); c.v+=61; check("reserved_units_reflects_expiry", s.reservedUnits("A")==0); }
        { Clk c=new Clk(); Inventory s=new Inventory(stock(),60,c); check("reserve_rejects_oversell", throwsEx(()->s.reserve("A",6))); }
        { Clk c=new Clk(); Inventory s=new Inventory(stock(),60,c); s.reserve("A",2); s.reserve("A",1); check("reserve_sums_reduce", s.available("A")==2); }
        System.out.println((failures>0?"FAILED ":"OK ")+(total-failures)+"/"+total); System.exit(failures>0?1:0);
    }
}
