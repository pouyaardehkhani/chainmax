# Bounded integer reference model

Minimize 0 + 14 open:W0 + 3 open:W1 + 3 open:W2 + 6 ship:R_W0_M0_standard:P0:0:0 + 10 ship:R_W2_M0_standard:P0:0:0 + 12 ship:R_W2_M1_standard:P0:0:0

## Variables

- `inventory:M0:P0:0:0`: integer in [0, 9], item.
- `inventory:M1:P0:0:0`: integer in [0, 9], item.
- `inventory:W0:P0:0:0`: integer in [0, 9], item.
- `inventory:W1:P0:0:0`: integer in [0, 9], item.
- `inventory:W2:P0:0:0`: integer in [0, 9], item.
- `open:W0`: boolean in [0, 1], activation.
- `open:W1`: boolean in [0, 1], activation.
- `open:W2`: boolean in [0, 1], activation.
- `serve:M0:P0:0:0`: integer in [0, 3], item.
- `serve:M1:P0:0:0`: integer in [0, 4], item.
- `ship:R_W0_M0_standard:P0:0:0`: integer in [0, 6], item.
- `ship:R_W0_M1_standard:P0:0:0`: integer in [0, 5], item.
- `ship:R_W2_M0_standard:P0:0:0`: integer in [0, 4], item.
- `ship:R_W2_M1_standard:P0:0:0`: integer in [0, 6], item.

## Hard constraints

- c000000: 1 inventory:W0:P0:0:0 + 1 ship:R_W0_M0_standard:P0:0:0 + 1 ship:R_W0_M1_standard:P0:0:0 eq 4. Source: balance/initial_stock/routes/recipes.
- c000001: 1 inventory:W1:P0:0:0 eq 2. Source: balance/initial_stock/routes/recipes.
- c000002: 1 inventory:W2:P0:0:0 + 1 ship:R_W2_M0_standard:P0:0:0 + 1 ship:R_W2_M1_standard:P0:0:0 eq 3. Source: balance/initial_stock/routes/recipes.
- c000003: 1 inventory:M0:P0:0:0 + 1 serve:M0:P0:0:0 + -1 ship:R_W0_M0_standard:P0:0:0 + -1 ship:R_W2_M0_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000004: 1 inventory:M1:P0:0:0 + 1 serve:M1:P0:0:0 + -1 ship:R_W0_M1_standard:P0:0:0 + -1 ship:R_W2_M1_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000005: 1 serve:M0:P0:0:0 eq 3. Source: demands.
- c000006: 1 serve:M1:P0:0:0 eq 4. Source: demands.
- c000007: 1 inventory:W0:P0:0:0 le 3. Source: locations/storage_capacity.
- c000008: 1 ship:R_W0_M0_standard:P0:0:0 + 1 ship:R_W0_M1_standard:P0:0:0 le 4. Source: locations/throughput_capacity.
- c000009: -4 open:W0 + 1 ship:R_W0_M0_standard:P0:0:0 + 1 ship:R_W0_M1_standard:P0:0:0 le 0. Source: locations/opening_cost.
- c000010: 1 inventory:W1:P0:0:0 le 5. Source: locations/storage_capacity.
- c000011: 0 le 3. Source: locations/throughput_capacity.
- c000012: -3 open:W1 le 0. Source: locations/opening_cost.
- c000013: 1 inventory:W2:P0:0:0 le 3. Source: locations/storage_capacity.
- c000014: 1 ship:R_W2_M0_standard:P0:0:0 + 1 ship:R_W2_M1_standard:P0:0:0 le 3. Source: locations/throughput_capacity.
- c000015: -3 open:W2 + 1 ship:R_W2_M0_standard:P0:0:0 + 1 ship:R_W2_M1_standard:P0:0:0 le 0. Source: locations/opening_cost.
- c000016: 1 inventory:M0:P0:0:0 le 1. Source: locations/storage_capacity.
- c000017: 0 le 1. Source: locations/throughput_capacity.
- c000018: 1 inventory:M1:P0:0:0 le 1. Source: locations/storage_capacity.
- c000019: 0 le 3. Source: locations/throughput_capacity.
- c000020: 1 ship:R_W0_M0_standard:P0:0:0 le 6. Source: routes/capacity.
- c000021: 1 ship:R_W0_M1_standard:P0:0:0 le 5. Source: routes/capacity.
- c000022: 1 ship:R_W2_M0_standard:P0:0:0 le 4. Source: routes/capacity.
- c000023: 1 ship:R_W2_M1_standard:P0:0:0 le 6. Source: routes/capacity.
