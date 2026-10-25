# Bounded integer reference model

Minimize 0 + 7 active:R_W0_M0_standard:0 + 7 active:R_W0_M1_standard:0 + 2 active:R_W1_M0_standard:0 + 15 active:R_W1_M1_standard:0 + 13 active:R_W2_M0_standard:0 + 15 active:R_W2_M1_standard:0 + 12 ship:R_W0_M0_standard:P0:0:0 + 10 ship:R_W0_M1_standard:P0:0:0 + 11 ship:R_W1_M0_standard:P0:0:0 + 10 ship:R_W1_M1_standard:P0:0:0

## Variables

- `active:R_W0_M0_standard:0`: boolean in [0, 1], activation.
- `active:R_W0_M1_standard:0`: boolean in [0, 1], activation.
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
- `serve:M1:P0:0:0`: integer in [0, 5], item.
- `ship:R_W0_M0_standard:P0:0:0`: integer in [0, 8], item.
- `ship:R_W0_M1_standard:P0:0:0`: integer in [0, 7], item.
- `ship:R_W1_M0_standard:P0:0:0`: integer in [0, 5], item.
- `ship:R_W1_M1_standard:P0:0:0`: integer in [0, 6], item.
- `ship:R_W2_M0_standard:P0:0:0`: integer in [0, 4], item.
- `ship:R_W2_M1_standard:P0:0:0`: integer in [0, 6], item.

## Hard constraints

- c000000: 1 inventory:W0:P0:0:0 + 1 ship:R_W0_M0_standard:P0:0:0 + 1 ship:R_W0_M1_standard:P0:0:0 eq 7. Source: balance/initial_stock/routes/recipes.
- c000001: 1 inventory:W1:P0:0:0 + 1 ship:R_W1_M0_standard:P0:0:0 + 1 ship:R_W1_M1_standard:P0:0:0 eq 4. Source: balance/initial_stock/routes/recipes.
- c000002: 1 inventory:W2:P0:0:0 + 1 ship:R_W2_M0_standard:P0:0:0 + 1 ship:R_W2_M1_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000003: 1 inventory:M0:P0:0:0 + 1 serve:M0:P0:0:0 + -1 ship:R_W0_M0_standard:P0:0:0 + -1 ship:R_W1_M0_standard:P0:0:0 + -1 ship:R_W2_M0_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000004: 1 inventory:M1:P0:0:0 + 1 serve:M1:P0:0:0 + -1 ship:R_W0_M1_standard:P0:0:0 + -1 ship:R_W1_M1_standard:P0:0:0 + -1 ship:R_W2_M1_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000005: 1 serve:M0:P0:0:0 eq 4. Source: demands.
- c000006: 1 serve:M1:P0:0:0 eq 5. Source: demands.
- c000007: 1 inventory:W0:P0:0:0 le 4. Source: locations/storage_capacity.
- c000008: 1 ship:R_W0_M0_standard:P0:0:0 + 1 ship:R_W0_M1_standard:P0:0:0 le 5. Source: locations/throughput_capacity.
- c000009: 1 inventory:W1:P0:0:0 le 3. Source: locations/storage_capacity.
- c000010: 1 ship:R_W1_M0_standard:P0:0:0 + 1 ship:R_W1_M1_standard:P0:0:0 le 7. Source: locations/throughput_capacity.
- c000011: 1 inventory:W2:P0:0:0 le 0. Source: locations/storage_capacity.
- c000012: 1 ship:R_W2_M0_standard:P0:0:0 + 1 ship:R_W2_M1_standard:P0:0:0 le 1. Source: locations/throughput_capacity.
- c000013: 1 inventory:M0:P0:0:0 le 3. Source: locations/storage_capacity.
- c000014: 0 le 2. Source: locations/throughput_capacity.
- c000015: 1 inventory:M1:P0:0:0 le 2. Source: locations/storage_capacity.
- c000016: 0 le 2. Source: locations/throughput_capacity.
- c000017: 1 ship:R_W0_M0_standard:P0:0:0 le 8. Source: routes/capacity.
- c000018: -8 active:R_W0_M0_standard:0 + 1 ship:R_W0_M0_standard:P0:0:0 le 0. Source: routes/activation.
- c000019: -2 active:R_W0_M0_standard:0 + 1 ship:R_W0_M0_standard:P0:0:0 ge 0. Source: routes/minimum_lot.
- c000020: 1 ship:R_W0_M1_standard:P0:0:0 le 7. Source: routes/capacity.
- c000021: -7 active:R_W0_M1_standard:0 + 1 ship:R_W0_M1_standard:P0:0:0 le 0. Source: routes/activation.
- c000022: -2 active:R_W0_M1_standard:0 + 1 ship:R_W0_M1_standard:P0:0:0 ge 0. Source: routes/minimum_lot.
- c000023: 1 ship:R_W1_M0_standard:P0:0:0 le 5. Source: routes/capacity.
- c000024: -5 active:R_W1_M0_standard:0 + 1 ship:R_W1_M0_standard:P0:0:0 le 0. Source: routes/activation.
- c000025: -1 active:R_W1_M0_standard:0 + 1 ship:R_W1_M0_standard:P0:0:0 ge 0. Source: routes/minimum_lot.
- c000026: 1 ship:R_W1_M1_standard:P0:0:0 le 6. Source: routes/capacity.
- c000027: -6 active:R_W1_M1_standard:0 + 1 ship:R_W1_M1_standard:P0:0:0 le 0. Source: routes/activation.
- c000028: -2 active:R_W1_M1_standard:0 + 1 ship:R_W1_M1_standard:P0:0:0 ge 0. Source: routes/minimum_lot.
- c000029: 1 ship:R_W2_M0_standard:P0:0:0 le 4. Source: routes/capacity.
- c000030: -4 active:R_W2_M0_standard:0 + 1 ship:R_W2_M0_standard:P0:0:0 le 0. Source: routes/activation.
- c000031: -2 active:R_W2_M0_standard:0 + 1 ship:R_W2_M0_standard:P0:0:0 ge 0. Source: routes/minimum_lot.
- c000032: 1 ship:R_W2_M1_standard:P0:0:0 le 6. Source: routes/capacity.
- c000033: -6 active:R_W2_M1_standard:0 + 1 ship:R_W2_M1_standard:P0:0:0 le 0. Source: routes/activation.
- c000034: -1 active:R_W2_M1_standard:0 + 1 ship:R_W2_M1_standard:P0:0:0 ge 0. Source: routes/minimum_lot.
- c000035: 1 active:R_W0_M0_standard:0 + 1 active:R_W1_M0_standard:0 + 1 active:R_W2_M0_standard:0 le 2. Source: sourcing/max_active_suppliers.
- c000036: 1 active:R_W0_M1_standard:0 + 1 active:R_W1_M1_standard:0 + 1 active:R_W2_M1_standard:0 le 2. Source: sourcing/max_active_suppliers.
- c000037: -1 active:R_W0_M1_standard:0 + 1 active:R_W1_M0_standard:0 le 0. Source: sourcing/dependencies.
