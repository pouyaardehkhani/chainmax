# Bounded integer reference model

Minimize 0 + 2 inventory:M0:P0:0:0 + 2 inventory:M0:P0:1:0 + 2 inventory:W0:P0:0:0 + 2 inventory:W0:P0:1:0 + 2 inventory:W1:P0:0:0 + 2 inventory:W1:P0:1:0 + 2 ship:R_W0_M0_standard:P0:0:0

## Variables

- `inventory:M0:P0:0:0`: integer in [0, 5], item.
- `inventory:M0:P0:1:0`: integer in [0, 5], item.
- `inventory:W0:P0:0:0`: integer in [0, 5], item.
- `inventory:W0:P0:1:0`: integer in [0, 5], item.
- `inventory:W1:P0:0:0`: integer in [0, 5], item.
- `inventory:W1:P0:1:0`: integer in [0, 5], item.
- `serve:M0:P0:1:0`: integer in [0, 4], item.
- `ship:R_W0_M0_standard:P0:0:0`: integer in [0, 5], item.

## Hard constraints

- c000000: 1 inventory:W0:P0:0:0 + 1 ship:R_W0_M0_standard:P0:0:0 eq 4. Source: balance/initial_stock/routes/recipes.
- c000001: -1 inventory:W0:P0:0:0 + 1 inventory:W0:P0:1:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000002: 1 inventory:W1:P0:0:0 eq 1. Source: balance/initial_stock/routes/recipes.
- c000003: -1 inventory:W1:P0:0:0 + 1 inventory:W1:P0:1:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000004: 1 inventory:M0:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000005: -1 inventory:M0:P0:0:0 + 1 inventory:M0:P0:1:0 + 1 serve:M0:P0:1:0 + -1 ship:R_W0_M0_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000006: 1 serve:M0:P0:1:0 eq 4. Source: demands.
- c000007: 1 inventory:W0:P0:0:0 le 0. Source: locations/storage_capacity.
- c000008: 1 ship:R_W0_M0_standard:P0:0:0 le 6. Source: locations/throughput_capacity.
- c000009: 1 inventory:W0:P0:1:0 le 0. Source: locations/storage_capacity.
- c000010: 0 le 6. Source: locations/throughput_capacity.
- c000011: 1 inventory:W1:P0:0:0 le 2. Source: locations/storage_capacity.
- c000012: 0 le 3. Source: locations/throughput_capacity.
- c000013: 1 inventory:W1:P0:1:0 le 2. Source: locations/storage_capacity.
- c000014: 0 le 3. Source: locations/throughput_capacity.
- c000015: 1 inventory:M0:P0:0:0 le 0. Source: locations/storage_capacity.
- c000016: 0 le 0. Source: locations/throughput_capacity.
- c000017: 1 inventory:M0:P0:1:0 le 0. Source: locations/storage_capacity.
- c000018: 0 le 0. Source: locations/throughput_capacity.
- c000019: 1 ship:R_W0_M0_standard:P0:0:0 le 5. Source: routes/capacity.
- c000020: 0 le 5. Source: routes/capacity.
