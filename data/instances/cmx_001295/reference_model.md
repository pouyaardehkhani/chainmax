# Bounded integer reference model

Minimize 0 + 5 active:R_W1_M0_standard:0 + 14 active:R_W1_M1_standard:0 + 17 active:R_W2_M0_standard:0 + 11 active:R_W2_M1_standard:0 + 9 ship:R_W1_M0_standard:P0:0:0 + 1 ship:R_W1_M1_standard:P0:0:0 + 5 ship:R_W2_M0_standard:P0:0:0 + 12 ship:R_W2_M1_standard:P0:0:0

## Variables

- `active:R_W1_M0_standard:0`: boolean in [0, 1], activation.
- `active:R_W1_M1_standard:0`: boolean in [0, 1], activation.
- `active:R_W2_M0_standard:0`: boolean in [0, 1], activation.
- `active:R_W2_M1_standard:0`: boolean in [0, 1], activation.
- `inventory:M0:P0:0:0`: integer in [0, 11], item.
- `inventory:M1:P0:0:0`: integer in [0, 11], item.
- `inventory:W0:P0:0:0`: integer in [0, 11], item.
- `inventory:W1:P0:0:0`: integer in [0, 11], item.
- `inventory:W2:P0:0:0`: integer in [0, 11], item.
- `serve:M0:P0:0:0`: integer in [0, 4], item.
- `serve:M1:P0:0:0`: integer in [0, 2], item.
- `ship:R_W1_M0_standard:P0:0:0`: integer in [0, 7], item.
- `ship:R_W1_M1_standard:P0:0:0`: integer in [0, 5], item.
- `ship:R_W2_M0_standard:P0:0:0`: integer in [0, 5], item.
- `ship:R_W2_M1_standard:P0:0:0`: integer in [0, 4], item.

## Hard constraints

- c000000: 1 inventory:W0:P0:0:0 eq 2. Source: balance/initial_stock/routes/recipes.
- c000001: 1 inventory:W1:P0:0:0 + 1 ship:R_W1_M0_standard:P0:0:0 + 1 ship:R_W1_M1_standard:P0:0:0 eq 1. Source: balance/initial_stock/routes/recipes.
- c000002: 1 inventory:W2:P0:0:0 + 1 ship:R_W2_M0_standard:P0:0:0 + 1 ship:R_W2_M1_standard:P0:0:0 eq 8. Source: balance/initial_stock/routes/recipes.
- c000003: 1 inventory:M0:P0:0:0 + 1 serve:M0:P0:0:0 + -1 ship:R_W1_M0_standard:P0:0:0 + -1 ship:R_W2_M0_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000004: 1 inventory:M1:P0:0:0 + 1 serve:M1:P0:0:0 + -1 ship:R_W1_M1_standard:P0:0:0 + -1 ship:R_W2_M1_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000005: 1 serve:M0:P0:0:0 eq 4. Source: demands.
- c000006: 1 serve:M1:P0:0:0 eq 2. Source: demands.
- c000007: 1 inventory:W0:P0:0:0 le 4. Source: locations/storage_capacity.
- c000008: 0 le 3. Source: locations/throughput_capacity.
- c000009: 1 inventory:W1:P0:0:0 le 1. Source: locations/storage_capacity.
- c000010: 1 ship:R_W1_M0_standard:P0:0:0 + 1 ship:R_W1_M1_standard:P0:0:0 le 3. Source: locations/throughput_capacity.
- c000011: 1 inventory:W2:P0:0:0 le 2. Source: locations/storage_capacity.
- c000012: 1 ship:R_W2_M0_standard:P0:0:0 + 1 ship:R_W2_M1_standard:P0:0:0 le 7. Source: locations/throughput_capacity.
- c000013: 1 inventory:M0:P0:0:0 le 2. Source: locations/storage_capacity.
- c000014: 0 le 2. Source: locations/throughput_capacity.
- c000015: 1 inventory:M1:P0:0:0 le 1. Source: locations/storage_capacity.
- c000016: 0 le 3. Source: locations/throughput_capacity.
- c000017: 1 ship:R_W1_M0_standard:P0:0:0 le 7. Source: routes/capacity.
- c000018: -7 active:R_W1_M0_standard:0 + 1 ship:R_W1_M0_standard:P0:0:0 le 0. Source: routes/activation.
- c000019: -1 active:R_W1_M0_standard:0 + 1 ship:R_W1_M0_standard:P0:0:0 ge 0. Source: routes/minimum_lot.
- c000020: 1 ship:R_W1_M1_standard:P0:0:0 le 5. Source: routes/capacity.
- c000021: -5 active:R_W1_M1_standard:0 + 1 ship:R_W1_M1_standard:P0:0:0 le 0. Source: routes/activation.
- c000022: -1 active:R_W1_M1_standard:0 + 1 ship:R_W1_M1_standard:P0:0:0 ge 0. Source: routes/minimum_lot.
- c000023: 1 ship:R_W2_M0_standard:P0:0:0 le 5. Source: routes/capacity.
- c000024: -5 active:R_W2_M0_standard:0 + 1 ship:R_W2_M0_standard:P0:0:0 le 0. Source: routes/activation.
- c000025: -1 active:R_W2_M0_standard:0 + 1 ship:R_W2_M0_standard:P0:0:0 ge 0. Source: routes/minimum_lot.
- c000026: 1 ship:R_W2_M1_standard:P0:0:0 le 4. Source: routes/capacity.
- c000027: -4 active:R_W2_M1_standard:0 + 1 ship:R_W2_M1_standard:P0:0:0 le 0. Source: routes/activation.
- c000028: -1 active:R_W2_M1_standard:0 + 1 ship:R_W2_M1_standard:P0:0:0 ge 0. Source: routes/minimum_lot.
