# Bounded integer reference model

Minimize 0 + 17 open:W0 + 19 open:W1 + 8 open:W2 + 10 ship:R_W0_M0_standard:P0:0:0 + 9 ship:R_W2_M0_standard:P0:0:0

## Variables

- `inventory:M0:P0:0:0`: integer in [0, 9], item.
- `inventory:W0:P0:0:0`: integer in [0, 9], item.
- `inventory:W1:P0:0:0`: integer in [0, 9], item.
- `inventory:W2:P0:0:0`: integer in [0, 9], item.
- `open:W0`: boolean in [0, 1], activation.
- `open:W1`: boolean in [0, 1], activation.
- `open:W2`: boolean in [0, 1], activation.
- `serve:M0:P0:0:0`: integer in [0, 5], item.
- `ship:R_W0_M0_standard:P0:0:0`: integer in [0, 5], item.
- `ship:R_W2_M0_standard:P0:0:0`: integer in [0, 9], item.

## Hard constraints

- c000000: 1 inventory:W0:P0:0:0 + 1 ship:R_W0_M0_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000001: 1 inventory:W1:P0:0:0 eq 2. Source: balance/initial_stock/routes/recipes.
- c000002: 1 inventory:W2:P0:0:0 + 1 ship:R_W2_M0_standard:P0:0:0 eq 7. Source: balance/initial_stock/routes/recipes.
- c000003: 1 inventory:M0:P0:0:0 + 1 serve:M0:P0:0:0 + -1 ship:R_W0_M0_standard:P0:0:0 + -1 ship:R_W2_M0_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000004: 1 serve:M0:P0:0:0 eq 5. Source: demands.
- c000005: 1 inventory:W0:P0:0:0 le 1. Source: locations/storage_capacity.
- c000006: 1 ship:R_W0_M0_standard:P0:0:0 le 0. Source: locations/throughput_capacity.
- c000007: 1 ship:R_W0_M0_standard:P0:0:0 le 0. Source: locations/opening_cost.
- c000008: 1 inventory:W1:P0:0:0 le 5. Source: locations/storage_capacity.
- c000009: 0 le 3. Source: locations/throughput_capacity.
- c000010: -3 open:W1 le 0. Source: locations/opening_cost.
- c000011: 1 inventory:W2:P0:0:0 le 2. Source: locations/storage_capacity.
- c000012: 1 ship:R_W2_M0_standard:P0:0:0 le 9. Source: locations/throughput_capacity.
- c000013: -9 open:W2 + 1 ship:R_W2_M0_standard:P0:0:0 le 0. Source: locations/opening_cost.
- c000014: 1 inventory:M0:P0:0:0 le 3. Source: locations/storage_capacity.
- c000015: 0 le 0. Source: locations/throughput_capacity.
- c000016: 1 ship:R_W0_M0_standard:P0:0:0 le 5. Source: routes/capacity.
- c000017: 1 ship:R_W2_M0_standard:P0:0:0 le 9. Source: routes/capacity.
