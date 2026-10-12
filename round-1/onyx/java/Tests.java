public class Tests {
    static int total=0, failures=0;
    static void check(String n, boolean c){ total++; if(c) System.out.println("PASS "+n); else { failures++; System.out.println("FAIL "+n);} }
    interface R { void run(); }
    static boolean throwsEx(R r){ try{ r.run(); return false; } catch(RuntimeException e){ return true; } }
    static class Clk implements java.util.function.DoubleSupplier { double v=1000; public double getAsDouble(){return v;} }
    public static void main(String[] a){
        { Clk c=new Clk(); Tokens s=new Tokens(60,c); Tokens.Token x=s.issue("u1"); check("issued_token_validates", s.validate(x.tokenId)); }
        { Clk c=new Clk(); Tokens s=new Tokens(60,c); Tokens.Token x=s.issue("u1"); s.revoke(x.tokenId); check("revoke_invalidates", s.validate(x.tokenId)==false); }
        { Clk c=new Clk(); Tokens s=new Tokens(60,c); Tokens.Token x=s.issue("u1"); c.v+=40; s.refresh(x.tokenId); c.v+=40; check("refresh_extends_lifetime", s.validate(x.tokenId)); }
        { Clk c=new Clk(); Tokens s=new Tokens(60,c); check("unknown_token_invalid", s.validate("nope")==false); }
        { Clk c=new Clk(); Tokens s=new Tokens(60,c); Tokens.Token x=s.issue("u1"); Tokens.Token r=s.refresh(x.tokenId); check("refresh_returns_active", r.status==Tokens.TokenStatus.ACTIVE); }
        { Clk c=new Clk(); Tokens s=new Tokens(60,c); Tokens.Token x=s.issue("u1"); s.revoke(x.tokenId); check("revoked_cannot_refresh", throwsEx(()->s.refresh(x.tokenId))); }
        { Clk c=new Clk(); Tokens s=new Tokens(60,c); Tokens.Token x=s.issue("u1"); s.revoke(x.tokenId); check("double_revoke_rejected", throwsEx(()->s.revoke(x.tokenId))); }
        { Clk c=new Clk(); Tokens s=new Tokens(60,c); Tokens.Token x=s.issue("u1"); c.v+=61; check("expired_token_invalid", s.validate(x.tokenId)==false); }
        { Clk c=new Clk(); Tokens s=new Tokens(60,c); Tokens.Token x=s.issue("u1"); c.v+=61; check("expired_token_cannot_refresh", throwsEx(()->s.refresh(x.tokenId))); }
        System.out.println((failures>0?"FAILED ":"OK ")+(total-failures)+"/"+total); System.exit(failures>0?1:0);
    }
}
