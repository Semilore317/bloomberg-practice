#pragma once
#include <string>
#include <map>
#include <stdexcept>

enum class OrderStatus { OPEN, PARTIAL, FILLED, CANCELLED };

struct Order {
    std::string order_id, symbol, side;
    int qty, filled;
    OrderStatus status;
};

class OrderService {
    std::map<std::string, Order> orders_;
    int seq_ = 0;
public:
    Order& place(const std::string& symbol, const std::string& side, int qty) {
        if (side != "buy" && side != "sell") throw std::invalid_argument("side must be buy or sell");
        if (qty <= 0) throw std::invalid_argument("qty must be positive");
        std::string id = "O" + std::to_string(++seq_);
        orders_[id] = Order{id, symbol, side, qty, 0, OrderStatus::OPEN};
        return orders_[id];
    }
    Order& fill(const std::string& id, int qty) {
        Order& o = get(id);
        if (qty <= 0) throw std::invalid_argument("fill qty must be positive");
        // BUG: no status guard, a cancelled (or filled) order can still be filled
        // BUG: no overfill guard, filled may exceed the original qty
        o.filled += qty;
        o.status = (o.filled == o.qty) ? OrderStatus::FILLED : OrderStatus::PARTIAL;
        return o;
    }
    Order& cancel(const std::string& id) {
        Order& o = get(id);
        // BUG: no terminal-state guard, a cancelled/filled order can be cancelled again
        o.status = OrderStatus::CANCELLED;
        return o;
    }
    int remaining(const std::string& id) { Order& o = get(id); return o.qty - o.filled; }
    int open_qty_for(const std::string& symbol) {
        int s = 0;
        // BUG: does not filter by status, so cancelled orders still count as open
        for (auto& kv : orders_) if (kv.second.symbol == symbol) s += kv.second.qty - kv.second.filled;
        return s;
    }
    Order& get(const std::string& id) {
        auto it = orders_.find(id);
        if (it == orders_.end()) throw std::invalid_argument("order not found");
        return it->second;
    }
};
