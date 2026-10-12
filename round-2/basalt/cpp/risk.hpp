#pragma once
#include <string>
#include <map>
#include <set>
#include <cstdlib>
struct RiskService {
    std::map<std::string, long> net;
    std::set<std::string> seen;
    std::string key(const std::string&, const std::string& symbol) const { return symbol; }
    void add_trade(const std::string& trade_id, const std::string& cp, const std::string& symbol, long qty) {
        net[key(cp, symbol)] += std::labs(qty);
    }
    long net_position(const std::string& cp, const std::string& symbol) {
        auto it = net.find(key(cp, symbol)); return it == net.end() ? 0 : it->second;
    }
};
