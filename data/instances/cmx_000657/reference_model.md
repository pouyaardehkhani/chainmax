# Bounded integer reference model

Minimize 0 + 3 ship:R_W0_M0_standard:P0:0:0

## Variables

- `inventory:M0:P0:0:0`: integer in [0, 5], item.
- `inventory:W0:P0:0:0`: integer in [0, 5], item.
- `inventory:W1:P0:0:0`: integer in [0, 5], item.
- `serve:M0:P0:0:0`: integer in [0, 2], item.
- `ship:R_W0_M0_standard:P0:0:0`: integer in [0, 3], item.

## Hard constraints

- c000000: 1 inventory:W0:P0:0:0 + 1 ship:R_W0_M0_standard:P0:0:0 eq 3. Source: balance/initial_stock/routes/recipes.
- c000001: 1 inventory:W1:P0:0:0 eq 2. Source: balance/initial_stock/routes/recipes.
- c000002: 1 inventory:M0:P0:0:0 + 1 serve:M0:P0:0:0 + -1 ship:R_W0_M0_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000003: 1 serve:M0:P0:0:0 eq 2. Source: demands.
- c000004: 2 inventory:W0:P0:0:0 le 2. Source: locations/storage_capacity.
- c000005: 2 ship:R_W0_M0_standard:P0:0:0 le 5. Source: locations/throughput_capacity.
- c000006: 2 inventory:W1:P0:0:0 le 5. Source: locations/storage_capacity.
- c000007: 0 le 2. Source: locations/throughput_capacity.
- c000008: 2 inventory:M0:P0:0:0 le 1. Source: locations/storage_capacity.
- c000009: 0 le 2. Source: locations/throughput_capacity.
- c000010: 2 ship:R_W0_M0_standard:P0:0:0 le 6. Source: routes/capacity.
