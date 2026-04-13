# E1-PR2 Implementation Plan

Plan for **PR 2: Add Inventory Reservation & Stock Validation**.
Based on `docs/E1_PR2_ticket.md`.

---

## Step 1: [domain/entities] Define `StockItem` Entity & Config Fields (R1)

Pure data-model changes.
Adds the `StockItem` entity and new inventory fields to `WarehouseConfig`.
All existing tests pass because new fields carry temporary defaults.

### Changes

**`app/domain/entities/stock_item.py`** _(new)_
- Immutable Pydantic model: `sku: str`, `quantity: int`, `reserved: int = 0`.
- Computed property `available` → `quantity - reserved`.

**`app/application/config/warehouse_config.py`**
- Add `low_stock_threshold: int = 10` and `max_reservation_ttl_minutes: int = 30`.
- Each `Field(...)` includes a `description` with calibration rationale.

### Tests

**`tests/domain/entities/test_stock_item.py`** _(new)_
- `available` returns correct value.
- Immutability: assigning a field raises `ValidationError`.

**`tests/application/config/test_warehouse_config.py`**
- New tests for default values of `low_stock_threshold`
  and `max_reservation_ttl_minutes`.

---

## Step 2: [domain/services] Add `InventoryService` Business Logic (R2)

Stateless domain service with reservation and validation rules.

### Changes

**`app/domain/services/inventory/inventory_service.py`** _(new)_
- `reserve(item: StockItem, qty: int) -> StockItem`:
  raises `InsufficientStockError` when `qty > item.available`.
- `release(item: StockItem, qty: int) -> StockItem`:
  releases reserved stock; clamps to zero.

### Tests

**`tests/domain/services/inventory/test_inventory_service.py`** _(new)_
- Reserve reduces `available`.
- Reserve raises `InsufficientStockError` when over-reserving.
- Release restores availability.
- Release clamps to zero on excess.

---

## Step 3: [application/use_cases] Add `ReserveStockUseCase` (R3)

Orchestrates `InventoryService` with `StockRepository`.

### Changes

**`app/application/use_cases/reserve_stock_use_case.py`** _(new)_
- Injects `InventoryService` and `StockRepository`.
- `execute(sku, qty)`: fetches item, delegates to service, persists result.

**`app/domain/repositories/stock_repository.py`** _(new)_
- ABC with `get_by_sku(sku: str) -> StockItem` and `save(item: StockItem) -> None`.

### Tests

**`tests/application/use_cases/test_reserve_stock_use_case.py`** _(new)_
- Happy path with mocked repository.
- Propagates `InsufficientStockError` from service.

---

## Step 4: [adapters/outbound] Implement `InMemoryStockRepository` (R4)

### Changes

**`app/adapters/outbound/inventory/in_memory_stock_repository.py`** _(new)_
- Dict-based implementation of `StockRepository`.

**`app/adapters/container.py`**
- Register `InMemoryStockRepository`, `InventoryService`,
  and `ReserveStockUseCase`.

### Tests

**`tests/adapters/outbound/inventory/test_in_memory_stock_repository.py`** _(new)_
- Round-trip: save then get returns same item.
- `get_by_sku` raises `KeyError` for missing SKU.

**`tests/adapters/test_container.py`**
- Smoke test: container builds without errors.

---

## Step 5: [docs] Update Documentation (R5)

No code changes.

### Changes

**`docs/architecture.md`**
- Add **§ Inventory Reservation** section with entity fields,
  service rules, and config parameters table.

---

## Dependency Graph

```
Step 1 ─── StockItem Entity & Config
   │
   ├──► Step 2 ─── InventoryService
   │         │
   │         └──► Step 3 ─── ReserveStockUseCase
   │                   │
   │                   └──► Step 4 ─── InMemoryStockRepository & DI
   │
   └──────────────────────► Step 5 ─── Documentation
```

Steps 2–4 form a dependency chain.
Step 5 depends only on Step 1
(documents the final entity shape; service details are stable).

---

## Files Changed Summary

| Step | New Files | Modified Files | Deleted Files |
|------|-----------|----------------|---------------|
| 1 | `stock_item.py`, `test_stock_item.py` | `warehouse_config.py`, `test_warehouse_config.py` | — |
| 2 | `inventory_service.py`, `test_inventory_service.py` | — | — |
| 3 | `reserve_stock_use_case.py`, `stock_repository.py`, test | — | — |
| 4 | `in_memory_stock_repository.py`, test | `container.py`, `test_container.py` | — |
| 5 | — | `docs/architecture.md` | — |

## Verification Notes

No issues found.

