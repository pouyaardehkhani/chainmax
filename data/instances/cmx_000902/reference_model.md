# Bounded integer reference model

Minimize 0 + 11 ship:R_W0_M0_standard:P0:0:0 + 11 ship:R_W0_M0_standard:P0:1:0 + 4 ship:R_W1_M0_standard:P0:0:0 + 4 ship:R_W2_M0_standard:P0:0:0

## Variables

- `inventory:M0:P0:0:0`: integer in [0, 10], item.
- `inventory:M0:P0:1:0`: integer in [0, 10], item.
- `inventory:M0:P0:2:0`: integer in [0, 10], item.
- `inventory:W0:P0:0:0`: integer in [0, 10], item.
- `inventory:W0:P0:1:0`: integer in [0, 10], item.
- `inventory:W0:P0:2:0`: integer in [0, 10], item.
- `inventory:W1:P0:0:0`: integer in [0, 10], item.
- `inventory:W1:P0:1:0`: integer in [0, 10], item.
- `inventory:W1:P0:2:0`: integer in [0, 10], item.
- `inventory:W2:P0:0:0`: integer in [0, 10], item.
- `inventory:W2:P0:1:0`: integer in [0, 10], item.
- `inventory:W2:P0:2:0`: integer in [0, 10], item.
- `serve:M0:P0:2:0`: integer in [0, 3], item.
- `ship:R_W0_M0_standard:P0:0:0`: integer in [0, 3], item.
- `ship:R_W0_M0_standard:P0:1:0`: integer in [0, 3], item.
- `ship:R_W1_M0_standard:P0:0:0`: integer in [0, 3], item.
- `ship:R_W2_M0_standard:P0:0:0`: integer in [0, 4], item.

## Hard constraints

- c000000: 1 inventory:W0:P0:0:0 + 1 ship:R_W0_M0_standard:P0:0:0 eq 6. Source: balance/initial_stock/routes/recipes.
- c000001: -1 inventory:W0:P0:0:0 + 1 inventory:W0:P0:1:0 + 1 ship:R_W0_M0_standard:P0:1:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000002: -1 inventory:W0:P0:1:0 + 1 inventory:W0:P0:2:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000003: 1 inventory:W1:P0:0:0 + 1 ship:R_W1_M0_standard:P0:0:0 eq 3. Source: balance/initial_stock/routes/recipes.
- c000004: -1 inventory:W1:P0:0:0 + 1 inventory:W1:P0:1:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000005: -1 inventory:W1:P0:1:0 + 1 inventory:W1:P0:2:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000006: 1 inventory:W2:P0:0:0 + 1 ship:R_W2_M0_standard:P0:0:0 eq 1. Source: balance/initial_stock/routes/recipes.
- c000007: -1 inventory:W2:P0:0:0 + 1 inventory:W2:P0:1:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000008: -1 inventory:W2:P0:1:0 + 1 inventory:W2:P0:2:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000009: 1 inventory:M0:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000010: -1 inventory:M0:P0:0:0 + 1 inventory:M0:P0:1:0 + -1 ship:R_W0_M0_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000011: -1 inventory:M0:P0:1:0 + 1 inventory:M0:P0:2:0 + 1 serve:M0:P0:2:0 + -1 ship:R_W0_M0_standard:P0:1:0 + -1 ship:R_W1_M0_standard:P0:0:0 + -1 ship:R_W2_M0_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000012: 1 serve:M0:P0:2:0 eq 3. Source: demands.
- c000013: 1 inventory:W0:P0:0:0 le 9. Source: locations/storage_capacity.
- c000014: 1 ship:R_W0_M0_standard:P0:0:0 le 3. Source: locations/throughput_capacity.
- c000015: 1 inventory:W0:P0:1:0 le 9. Source: locations/storage_capacity.
- c000016: 1 ship:R_W0_M0_standard:P0:1:0 le 3. Source: locations/throughput_capacity.
- c000017: 1 inventory:W0:P0:2:0 le 9. Source: locations/storage_capacity.
- c000018: 0 le 3. Source: locations/throughput_capacity.
- c000019: 1 inventory:W1:P0:0:0 le 3. Source: locations/storage_capacity.
- c000020: 1 ship:R_W1_M0_standard:P0:0:0 le 1. Source: locations/throughput_capacity.
- c000021: 1 inventory:W1:P0:1:0 le 3. Source: locations/storage_capacity.
- c000022: 0 le 1. Source: locations/throughput_capacity.
- c000023: 1 inventory:W1:P0:2:0 le 3. Source: locations/storage_capacity.
- c000024: 0 le 1. Source: locations/throughput_capacity.
- c000025: 1 inventory:W2:P0:0:0 le 2. Source: locations/storage_capacity.
- c000026: 1 ship:R_W2_M0_standard:P0:0:0 le 2. Source: locations/throughput_capacity.
- c000027: 1 inventory:W2:P0:1:0 le 2. Source: locations/storage_capacity.
- c000028: 0 le 2. Source: locations/throughput_capacity.
- c000029: 1 inventory:W2:P0:2:0 le 2. Source: locations/storage_capacity.
- c000030: 0 le 2. Source: locations/throughput_capacity.
- c000031: 1 inventory:M0:P0:0:0 le 4. Source: locations/storage_capacity.
- c000032: 0 le 1. Source: locations/throughput_capacity.
- c000033: 1 inventory:M0:P0:1:0 le 4. Source: locations/storage_capacity.
- c000034: 0 le 1. Source: locations/throughput_capacity.
- c000035: 1 inventory:M0:P0:2:0 le 4. Source: locations/storage_capacity.
- c000036: 0 le 1. Source: locations/throughput_capacity.
- c000037: 1 ship:R_W0_M0_standard:P0:0:0 le 3. Source: routes/capacity.
- c000038: 1 ship:R_W0_M0_standard:P0:1:0 le 3. Source: routes/capacity.
- c000039: 0 le 3. Source: routes/capacity.
- c000040: 1 ship:R_W1_M0_standard:P0:0:0 le 3. Source: routes/capacity.
- c000041: 0 le 3. Source: routes/capacity.
- c000042: 0 le 3. Source: routes/capacity.
- c000043: 1 ship:R_W2_M0_standard:P0:0:0 le 4. Source: routes/capacity.
- c000044: 0 le 4. Source: routes/capacity.
- c000045: 0 le 4. Source: routes/capacity.
