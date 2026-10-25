# Bounded integer reference model

Minimize 0 + 5 ship:R_W1_M0_standard:P0:0:0 + 6 ship:R_W2_M0_standard:P0:0:0

## Variables

- `inventory:M0:P0:0:0`: integer in [0, 8], item.
- `inventory:W0:P0:0:0`: integer in [0, 8], item.
- `inventory:W1:P0:0:0`: integer in [0, 8], item.
- `inventory:W2:P0:0:0`: integer in [0, 8], item.
- `serve:M0:P0:0:0`: integer in [0, 3], item.
- `ship:R_W1_M0_standard:P0:0:0`: integer in [0, 4], item.
- `ship:R_W2_M0_standard:P0:0:0`: integer in [0, 2], item.

## Hard constraints

- c000000: 1 inventory:W0:P0:0:0 eq 2. Source: balance/initial_stock/routes/recipes.
- c000001: 1 inventory:W1:P0:0:0 + 1 ship:R_W1_M0_standard:P0:0:0 eq 6. Source: balance/initial_stock/routes/recipes.
- c000002: 1 inventory:W2:P0:0:0 + 1 ship:R_W2_M0_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000003: 1 inventory:M0:P0:0:0 + 1 serve:M0:P0:0:0 + -1 ship:R_W1_M0_standard:P0:0:0 + -1 ship:R_W2_M0_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000004: 1 serve:M0:P0:0:0 eq 3. Source: demands.
- c000005: 1 inventory:W0:P0:0:0 le 4. Source: locations/storage_capacity.
- c000006: 0 le 2. Source: locations/throughput_capacity.
- c000007: 1 inventory:W1:P0:0:0 le 6. Source: locations/storage_capacity.
- c000008: 1 ship:R_W1_M0_standard:P0:0:0 le 5. Source: locations/throughput_capacity.
- c000009: 1 inventory:W2:P0:0:0 le 3. Source: locations/storage_capacity.
- c000010: 1 ship:R_W2_M0_standard:P0:0:0 le 2. Source: locations/throughput_capacity.
- c000011: 1 inventory:M0:P0:0:0 le 4. Source: locations/storage_capacity.
- c000012: 0 le 1. Source: locations/throughput_capacity.
- c000013: 1 ship:R_W1_M0_standard:P0:0:0 le 4. Source: routes/capacity.
- c000014: 1 ship:R_W2_M0_standard:P0:0:0 le 2. Source: routes/capacity.
