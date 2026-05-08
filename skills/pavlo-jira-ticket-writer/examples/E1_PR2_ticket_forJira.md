## Objective

Introduce stock reservation logic so that concurrent order fulfilment
does not over-commit inventory.
This is the foundation for the pick-and-pack pipeline planned in PR 3.

## Background & Motivation

| Module | Current State | Limitation |
|--------|--------------|------------|
| `StockItem` entity | ❌ Missing | No domain model for inventory quantities |
| `InventoryService` | ❌ Missing | No reservation or validation logic |
| `StockRepository` | ❌ Missing | No persistence contract for stock data |
| `WarehouseConfig` | ⚠️ Exists | Lacks low-stock threshold and reservation TTL parameters |

The warehouse module currently handles inbound receiving
but has no concept of reserving stock against outbound orders.
Without reservation, two orders can claim the same unit.

## Scope

### In Scope

1. **`StockItem` entity** — immutable domain model with quantity, reserved, and available fields.
2. **`InventoryService`** — stateless domain service for reserve / release operations.
3. **`ReserveStockUseCase`** — application-layer orchestration of service + repository.
4. **`InMemoryStockRepository`** — adapter implementation and DI wiring.
5. **Documentation** — update `docs/architecture.md` with new inventory section.

### Out of Scope

- Persistent (database-backed) stock repository — deferred to E1-PR4.
- Reservation expiry / TTL enforcement — deferred to E1-PR3.
- UI / dashboard changes — deferred to E1-PR5.

---

## Requirements

### R1 — `StockItem` Entity & Config Fields

**Current:** No domain model for stock quantities.

**Target:** Immutable `StockItem` entity with `sku`, `quantity`,
`reserved`, and computed `available` property.
`WarehouseConfig` gains `low_stock_threshold` and `max_reservation_ttl_minutes`.

### R2 — `InventoryService`

**Current:** No reservation logic.

**Target:** Stateless domain service with `reserve` and `release` methods.

### R3 — `ReserveStockUseCase`

**Current:** No orchestration layer for inventory.

**Target:** Use case that fetches a `StockItem` by SKU,
delegates to `InventoryService.reserve`, and persists the result.

### R4 — `InMemoryStockRepository` & DI Wiring

**Current:** No `StockRepository` contract.

**Target:** ABC in `domain/repositories/` with `get_by_sku` and `save`.
In-memory dict adapter in `adapters/outbound/inventory/`.
Registered in DI container.

### R5 — Documentation

**Current:** `docs/architecture.md` has no inventory section.

**Target:** New **§ Inventory Reservation** section documenting
entity fields, service rules, and config parameters.

---

## Acceptance Criteria

- [ ] `StockItem` is an immutable model with `sku`, `quantity`,
  `reserved`, and computed `available`.
- [ ] `WarehouseConfig` has `low_stock_threshold` and `max_reservation_ttl_minutes`
  with sensible defaults.
- [ ] Reserving stock returns an updated item
  and raises an error when available stock is insufficient.
- [ ] Releasing more than the reserved amount clamps to zero.
- [ ] `ReserveStockUseCase` orchestrates fetch → reserve → persist.
- [ ] `InMemoryStockRepository` is implemented and wired into the DI container.
- [ ] `docs/architecture.md` contains an Inventory Reservation section.
- [ ] All new code has corresponding unit tests; test suite passes.

