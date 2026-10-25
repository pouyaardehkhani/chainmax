# Bounded integer reference model

Minimize 0 + 8 active:R_W0_M0_standard:0 + 17 active:R_W1_M0_standard:0 + 15 active:R_W2_M0_standard:0 + 1 ship:R_W0_M0_standard:P0:0:0 + 1 ship:R_W1_M0_standard:P0:0:0 + 2 ship:R_W2_M0_standard:P0:0:0

## Variables

- `active:R_W0_M0_standard:0`: boolean in [0, 1], activation.
- `active:R_W1_M0_standard:0`: boolean in [0, 1], activation.
- `active:R_W2_M0_standard:0`: boolean in [0, 1], activation.
- `inventory:M0:P0:0:0`: integer in [0, 11], item.
- `inventory:W0:P0:0:0`: integer in [0, 11], item.
- `inventory:W1:P0:0:0`: integer in [0, 11], item.
- `inventory:W2:P0:0:0`: integer in [0, 11], item.
- `serve:M0:P0:0:0`: integer in [0, 3], item.
- `ship:R_W0_M0_standard:P0:0:0`: integer in [0, 3], item.
- `ship:R_W1_M0_standard:P0:0:0`: integer in [0, 7], item.
- `ship:R_W2_M0_standard:P0:0:0`: integer in [0, 5], item.

## Hard constraints

- c000000: 1 inventory:W0:P0:0:0 + 1 ship:R_W0_M0_standard:P0:0:0 eq 3. Source: balance/initial_stock/routes/recipes.
- c000001: 1 inventory:W1:P0:0:0 + 1 ship:R_W1_M0_standard:P0:0:0 eq 2. Source: balance/initial_stock/routes/recipes.
- c000002: 1 inventory:W2:P0:0:0 + 1 ship:R_W2_M0_standard:P0:0:0 eq 6. Source: balance/initial_stock/routes/recipes.
- c000003: 1 inventory:M0:P0:0:0 + 1 serve:M0:P0:0:0 + -1 ship:R_W0_M0_standard:P0:0:0 + -1 ship:R_W1_M0_standard:P0:0:0 + -1 ship:R_W2_M0_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000004: 1 serve:M0:P0:0:0 eq 3. Source: demands.
- c000005: 1 inventory:W0:P0:0:0 le 5. Source: locations/storage_capacity.
- c000006: 1 ship:R_W0_M0_standard:P0:0:0 le 4. Source: locations/throughput_capacity.
- c000007: 1 inventory:W1:P0:0:0 le 5. Source: locations/storage_capacity.
- c000008: 1 ship:R_W1_M0_standard:P0:0:0 le 4. Source: locations/throughput_capacity.
- c000009: 1 inventory:W2:P0:0:0 le 5. Source: locations/storage_capacity.
- c000010: 1 ship:R_W2_M0_standard:P0:0:0 le 6. Source: locations/throughput_capacity.
- c000011: 1 inventory:M0:P0:0:0 le 2. Source: locations/storage_capacity.
- c000012: 0 le 0. Source: locations/throughput_capacity.
- c000013: 1 ship:R_W0_M0_standard:P0:0:0 le 3. Source: routes/capacity.
- c000014: -3 active:R_W0_M0_standard:0 + 1 ship:R_W0_M0_standard:P0:0:0 le 0. Source: routes/activation.
- c000015: -1 active:R_W0_M0_standard:0 + 1 ship:R_W0_M0_standard:P0:0:0 ge 0. Source: routes/minimum_lot.
- c000016: 1 ship:R_W1_M0_standard:P0:0:0 le 7. Source: routes/capacity.
- c000017: -7 active:R_W1_M0_standard:0 + 1 ship:R_W1_M0_standard:P0:0:0 le 0. Source: routes/activation.
- c000018: -1 active:R_W1_M0_standard:0 + 1 ship:R_W1_M0_standard:P0:0:0 ge 0. Source: routes/minimum_lot.
- c000019: 1 ship:R_W2_M0_standard:P0:0:0 le 5. Source: routes/capacity.
- c000020: -5 active:R_W2_M0_standard:0 + 1 ship:R_W2_M0_standard:P0:0:0 le 0. Source: routes/activation.
- c000021: -1 active:R_W2_M0_standard:0 + 1 ship:R_W2_M0_standard:P0:0:0 ge 0. Source: routes/minimum_lot.
