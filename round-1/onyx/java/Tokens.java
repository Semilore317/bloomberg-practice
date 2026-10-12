import java.util.*;
import java.util.function.DoubleSupplier;
public class Tokens {
    public enum TokenStatus { ACTIVE, REVOKED }
    public static class Token { public String tokenId,userId; public TokenStatus status; double expiresAt; boolean hasExpiry;
        Token(String id,String u,double e){tokenId=id;userId=u;status=TokenStatus.ACTIVE;expiresAt=e;hasExpiry=true;} }
    private final Map<String,Token> tokens=new LinkedHashMap<>();
    private final double ttl; private final DoubleSupplier clock; private int seq=0;
    public Tokens(double ttl, DoubleSupplier clock){ this.ttl=ttl; this.clock=clock; }
    public Token issue(String user){ String id="T"+(++seq); Token t=new Token(id,user,clock.getAsDouble()+ttl); tokens.put(id,t); return t; }
    public boolean validate(String id){
        Token t=tokens.get(id); if(t==null) return false;
        return t.status==TokenStatus.ACTIVE;
    }
    public Token refresh(String id){
        Token t=get(id);
        if(t.status!=TokenStatus.ACTIVE) throw new IllegalArgumentException("cannot refresh a revoked token");
        t.expiresAt=clock.getAsDouble()+ttl; return t;
    }
    public Token revoke(String id){
        Token t=get(id);
        t.status=TokenStatus.REVOKED; t.hasExpiry=false; return t;
    }
    public Token get(String id){ Token t=tokens.get(id); if(t==null) throw new IllegalArgumentException("token not found"); return t; }
}
