# Bounded integer reference model

Minimize 0 + 3 produce:B_W0:0 + 5 produce:B_W1:0 + 4 produce:B_W2:0 + 8 produce:B_W3:0 + 9 ship:R_W0_M0_standard:P0:0:0 + 6 ship:R_W0_M1_standard:P0:0:0 + 11 ship:R_W1_M0_standard:P0:0:0 + 11 ship:R_W1_M1_standard:P0:0:0 + 7 ship:R_W2_M0_standard:P0:0:0 + 11 ship:R_W2_M1_standard:P0:0:0 + 10 ship:R_W3_M0_standard:P0:0:0 + 6 ship:R_W3_M1_standard:P0:0:0

## Variables

- `inventory:M0:P0:0:0`: integer in [0, 31], item.
- `inventory:M0:RAW:0:0`: integer in [0, 31], item.
- `inventory:M1:P0:0:0`: integer in [0, 31], item.
- `inventory:M1:RAW:0:0`: integer in [0, 31], item.
- `inventory:W0:P0:0:0`: integer in [0, 31], item.
- `inventory:W0:RAW:0:0`: integer in [0, 31], item.
- `inventory:W1:P0:0:0`: integer in [0, 31], item.
- `inventory:W1:RAW:0:0`: integer in [0, 31], item.
- `inventory:W2:P0:0:0`: integer in [0, 31], item.
- `inventory:W2:RAW:0:0`: integer in [0, 31], item.
- `inventory:W3:P0:0:0`: integer in [0, 31], item.
- `inventory:W3:RAW:0:0`: integer in [0, 31], item.
- `produce:B_W0:0`: integer in [0, 7], batch.
- `produce:B_W1:0`: integer in [0, 4], batch.
- `produce:B_W2:0`: integer in [0, 2], batch.
- `produce:B_W3:0`: integer in [0, 1], batch.
- `serve:M0:P0:0:0`: integer in [0, 5], item.
- `serve:M1:P0:0:0`: integer in [0, 4], item.
- `ship:R_W0_M0_standard:P0:0:0`: integer in [0, 5], item.
- `ship:R_W0_M1_standard:P0:0:0`: integer in [0, 5], item.
- `ship:R_W1_M0_standard:P0:0:0`: integer in [0, 6], item.
- `ship:R_W1_M1_standard:P0:0:0`: integer in [0, 5], item.
- `ship:R_W2_M0_standard:P0:0:0`: integer in [0, 3], item.
- `ship:R_W2_M1_standard:P0:0:0`: integer in [0, 9], item.
- `ship:R_W3_M0_standard:P0:0:0`: integer in [0, 6], item.
- `ship:R_W3_M1_standard:P0:0:0`: integer in [0, 5], item.

## Hard constraints

- c000000: 1 inventory:W0:P0:0:0 + -1 produce:B_W0:0 + 1 ship:R_W0_M0_standard:P0:0:0 + 1 ship:R_W0_M1_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000001: 1 inventory:W0:RAW:0:0 + 1 produce:B_W0:0 eq 7. Source: balance/initial_stock/routes/recipes.
- c000002: 1 inventory:W1:P0:0:0 + -1 produce:B_W1:0 + 1 ship:R_W1_M0_standard:P0:0:0 + 1 ship:R_W1_M1_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000003: 1 inventory:W1:RAW:0:0 + 2 produce:B_W1:0 eq 9. Source: balance/initial_stock/routes/recipes.
- c000004: 1 inventory:W2:P0:0:0 + -1 produce:B_W2:0 + 1 ship:R_W2_M0_standard:P0:0:0 + 1 ship:R_W2_M1_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000005: 1 inventory:W2:RAW:0:0 + 3 produce:B_W2:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000006: 1 inventory:W3:P0:0:0 + -2 produce:B_W3:0 + 1 ship:R_W3_M0_standard:P0:0:0 + 1 ship:R_W3_M1_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000007: 1 inventory:W3:RAW:0:0 + 3 produce:B_W3:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000008: 1 inventory:M0:P0:0:0 + 1 serve:M0:P0:0:0 + -1 ship:R_W0_M0_standard:P0:0:0 + -1 ship:R_W1_M0_standard:P0:0:0 + -1 ship:R_W2_M0_standard:P0:0:0 + -1 ship:R_W3_M0_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000009: 1 inventory:M0:RAW:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000010: 1 inventory:M1:P0:0:0 + 1 serve:M1:P0:0:0 + -1 ship:R_W0_M1_standard:P0:0:0 + -1 ship:R_W1_M1_standard:P0:0:0 + -1 ship:R_W2_M1_standard:P0:0:0 + -1 ship:R_W3_M1_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000011: 1 inventory:M1:RAW:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000012: 1 serve:M0:P0:0:0 eq 5. Source: demands.
- c000013: 1 serve:M1:P0:0:0 eq 4. Source: demands.
- c000014: 1 inventory:W0:P0:0:0 + 1 inventory:W0:RAW:0:0 le 3. Source: locations/storage_capacity.
- c000015: 1 ship:R_W0_M0_standard:P0:0:0 + 1 ship:R_W0_M1_standard:P0:0:0 le 7. Source: locations/throughput_capacity.
- c000016: 1 inventory:W1:P0:0:0 + 1 inventory:W1:RAW:0:0 le 3. Source: locations/storage_capacity.
- c000017: 1 ship:R_W1_M0_standard:P0:0:0 + 1 ship:R_W1_M1_standard:P0:0:0 le 6. Source: locations/throughput_capacity.
- c000018: 1 inventory:W2:P0:0:0 + 1 inventory:W2:RAW:0:0 le 2. Source: locations/storage_capacity.
- c000019: 1 ship:R_W2_M0_standard:P0:0:0 + 1 ship:R_W2_M1_standard:P0:0:0 le 0. Source: locations/throughput_capacity.
- c000020: 1 inventory:W3:P0:0:0 + 1 inventory:W3:RAW:0:0 le 0. Source: locations/storage_capacity.
- c000021: 1 ship:R_W3_M0_standard:P0:0:0 + 1 ship:R_W3_M1_standard:P0:0:0 le 2. Source: locations/throughput_capacity.
- c000022: 1 inventory:M0:P0:0:0 + 1 inventory:M0:RAW:0:0 le 0. Source: locations/storage_capacity.
- c000023: 0 le 1. Source: locations/throughput_capacity.
- c000024: 1 inventory:M1:P0:0:0 + 1 inventory:M1:RAW:0:0 le 2. Source: locations/storage_capacity.
- c000025: 0 le 1. Source: locations/throughput_capacity.
- c000026: 1 ship:R_W0_M0_standard:P0:0:0 le 5. Source: routes/capacity.
- c000027: 1 ship:R_W0_M1_standard:P0:0:0 le 5. Source: routes/capacity.
- c000028: 1 ship:R_W1_M0_standard:P0:0:0 le 6. Source: routes/capacity.
- c000029: 1 ship:R_W1_M1_standard:P0:0:0 le 5. Source: routes/capacity.
- c000030: 1 ship:R_W2_M0_standard:P0:0:0 le 3. Source: routes/capacity.
- c000031: 1 ship:R_W2_M1_standard:P0:0:0 le 9. Source: routes/capacity.
- c000032: 1 ship:R_W3_M0_standard:P0:0:0 le 6. Source: routes/capacity.
- c000033: 1 ship:R_W3_M1_standard:P0:0:0 le 5. Source: routes/capacity.
