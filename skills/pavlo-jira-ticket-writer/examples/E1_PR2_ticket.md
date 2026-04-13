<!--
  Notes for AI agent:
  This ticket is based on the following documents:
  - docs/E1_epic.md — Warehouse Management epic overview
  - docs/architecture.md — Current module documentation
-->

```json
{
  "ticket": "TBD",
  "epic": "E1 — Warehouse Management",
  "type": "Story",
  "priority": "Medium",
  "labels": ["inventory", "backend"],
  "components": ["warehouse"],
  "story_points": null,
  "sprint": null
}
```

# PR 2: Add Inventory Reservation & Stock Validation

**Epic:** E1 — Warehouse Management

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

## Current State (Code References)

### `WarehouseConfig`

- **File:** `app/application/config/warehouse_config.py`
- Contains `warehouse_name` and `max_capacity` fields.
- No inventory-specific parameters (threshold, TTL).

### Stock persistence

- No `StockRepository` interface or implementation exists.
- Inbound receiving writes directly to an in-memory dict inside the adapter
  with no domain contract.

---

## Requirements

### R1 — `StockItem` Entity & Config Fields

**Current:** No domain model for stock quantities.

**Target:** Immutable `StockItem` entity with `sku`, `quantity`,
`reserved`, and computed `available` property.
`WarehouseConfig` gains `low_stock_threshold` and `max_reservation_ttl_minutes`.

**Details:**
- `StockItem` uses `ConfigDict(frozen=True)`.
- `available` is a `@computed_field`: `quantity - reserved`.
- `reserved` defaults to `0`; `quantity` must be `≥ 0` (`Field(ge=0)`).
- `low_stock_threshold` defaults to `10`.
- `max_reservation_ttl_minutes` defaults to `30`.

### R2 — `InventoryService`

**Current:** No reservation logic.

**Target:** Stateless domain service with `reserve` and `release` methods.

**Details:**
- `reserve(item, qty)`: returns new `StockItem` with `reserved += qty`.
  Raises `InsufficientStockError` if `qty > item.available`.
- `release(item, qty)`: returns new `StockItem` with `reserved -= qty`,
  clamped to `0`.
- No repository or adapter dependencies — pure domain logic.

### R3 — `ReserveStockUseCase`

**Current:** No orchestration layer for inventory.

**Target:** Use case that fetches a `StockItem` by SKU,
delegates to `InventoryService.reserve`, and persists the result.

**Details:**
- Constructor-injected: `InventoryService`, `StockRepository`.
- `execute(sku: str, qty: int) -> StockItem`.

### R4 — `InMemoryStockRepository` & DI Wiring

**Current:** No `StockRepository` contract.

**Target:** ABC in `domain/repositories/` with `get_by_sku` and `save`.
In-memory dict adapter in `adapters/outbound/inventory/`.
Registered in DI container.

**Details:**
- `get_by_sku(sku)` raises `KeyError` if SKU not found.
- `save(item)` upserts by `sku`.

### R5 — Documentation

**Current:** `docs/architecture.md` has no inventory section.

**Target:** New **§ Inventory Reservation** section documenting
entity fields, service rules, and config parameters.

---

## Acceptance Criteria

- [ ] `StockItem` is an immutable Pydantic model with `sku`, `quantity`,
  `reserved`, and computed `available`.
- [ ] `reserved` defaults to `0`; `quantity` is validated `≥ 0`.
- [ ] `WarehouseConfig` has `low_stock_threshold` (default `10`)
  and `max_reservation_ttl_minutes` (default `30`).
- [ ] `InventoryService.reserve` returns updated item
  and raises `InsufficientStockError` on over-reservation.
- [ ] `InventoryService.release` clamps reserved to zero on excess.
- [ ] `ReserveStockUseCase` orchestrates fetch → reserve → persist.
- [ ] `InMemoryStockRepository` passes round-trip and missing-SKU tests.
- [ ] DI container builds without errors with default config.
- [ ] `docs/architecture.md` contains an Inventory Reservation section.
- [ ] All new code has corresponding unit tests; test suite passes.

