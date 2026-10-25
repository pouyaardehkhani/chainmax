# Bounded integer reference model

Minimize 0 + 8 open:W0 + 23 open:W1 + 11 open:W2 + 11 ship:R_W0_M0_standard:P0:0:0 + 1 ship:R_W1_M0_standard:P0:0:0

## Variables

- `inventory:M0:P0:0:0`: integer in [0, 7], item.
- `inventory:W0:P0:0:0`: integer in [0, 7], item.
- `inventory:W1:P0:0:0`: integer in [0, 7], item.
- `inventory:W2:P0:0:0`: integer in [0, 7], item.
- `open:W0`: boolean in [0, 1], activation.
- `open:W1`: boolean in [0, 1], activation.
- `open:W2`: boolean in [0, 1], activation.
- `serve:M0:P0:0:0`: integer in [0, 5], item.
- `ship:R_W0_M0_standard:P0:0:0`: integer in [0, 7], item.
- `ship:R_W1_M0_standard:P0:0:0`: integer in [0, 6], item.

## Hard constraints

- c000000: 1 inventory:W0:P0:0:0 + 1 ship:R_W0_M0_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000001: 1 inventory:W1:P0:0:0 + 1 ship:R_W1_M0_standard:P0:0:0 eq 6. Source: balance/initial_stock/routes/recipes.
- c000002: 1 inventory:W2:P0:0:0 eq 1. Source: balance/initial_stock/routes/recipes.
- c000003: 1 inventory:M0:P0:0:0 + 1 serve:M0:P0:0:0 + -1 ship:R_W0_M0_standard:P0:0:0 + -1 ship:R_W1_M0_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000004: 1 serve:M0:P0:0:0 eq 5. Source: demands.
- c000005: 1 inventory:W0:P0:0:0 le 2. Source: locations/storage_capacity.
- c000006: 1 ship:R_W0_M0_standard:P0:0:0 le 0. Source: locations/throughput_capacity.
- c000007: 1 ship:R_W0_M0_standard:P0:0:0 le 0. Source: locations/opening_cost.
- c000008: 1 inventory:W1:P0:0:0 le 2. Source: locations/storage_capacity.
- c000009: 1 ship:R_W1_M0_standard:P0:0:0 le 8. Source: locations/throughput_capacity.
- c000010: -8 open:W1 + 1 ship:R_W1_M0_standard:P0:0:0 le 0. Source: locations/opening_cost.
- c000011: 1 inventory:W2:P0:0:0 le 1. Source: locations/storage_capacity.
- c000012: 0 le 4. Source: locations/throughput_capacity.
- c000013: -4 open:W2 le 0. Source: locations/opening_cost.
- c000014: 1 inventory:M0:P0:0:0 le 3. Source: locations/storage_capacity.
- c000015: 0 le 4. Source: locations/throughput_capacity.
- c000016: 1 ship:R_W0_M0_standard:P0:0:0 le 8. Source: routes/capacity.
- c000017: 1 ship:R_W1_M0_standard:P0:0:0 le 6. Source: routes/capacity.
