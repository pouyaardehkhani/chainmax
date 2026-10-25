# Bounded integer reference model

Minimize 0 + 24 open:W0 + 24 open:W1 + 22 open:W2 + 20 open:W3 + 8 ship:R_W0_M0_standard:P0:0:0 + 8 ship:R_W0_M1_standard:P0:0:0 + 11 ship:R_W1_M0_standard:P0:0:0 + 8 ship:R_W1_M1_standard:P0:0:0 + 5 ship:R_W2_M0_standard:P0:0:0 + 4 ship:R_W2_M1_standard:P0:0:0 + 5 ship:R_W3_M0_standard:P0:0:0

## Variables

- `inventory:M0:P0:0:0`: integer in [0, 10], item.
- `inventory:M1:P0:0:0`: integer in [0, 10], item.
- `inventory:W0:P0:0:0`: integer in [0, 10], item.
- `inventory:W1:P0:0:0`: integer in [0, 10], item.
- `inventory:W2:P0:0:0`: integer in [0, 10], item.
- `inventory:W3:P0:0:0`: integer in [0, 10], item.
- `open:W0`: boolean in [0, 1], activation.
- `open:W1`: boolean in [0, 1], activation.
- `open:W2`: boolean in [0, 1], activation.
- `open:W3`: boolean in [0, 1], activation.
- `serve:M0:P0:0:0`: integer in [0, 2], item.
- `serve:M1:P0:0:0`: integer in [0, 3], item.
- `ship:R_W0_M0_standard:P0:0:0`: integer in [0, 6], item.
- `ship:R_W0_M1_standard:P0:0:0`: integer in [0, 5], item.
- `ship:R_W1_M0_standard:P0:0:0`: integer in [0, 5], item.
- `ship:R_W1_M1_standard:P0:0:0`: integer in [0, 7], item.
- `ship:R_W2_M0_standard:P0:0:0`: integer in [0, 9], item.
- `ship:R_W2_M1_standard:P0:0:0`: integer in [0, 5], item.
- `ship:R_W3_M0_standard:P0:0:0`: integer in [0, 4], item.

## Hard constraints

- c000000: 1 inventory:W0:P0:0:0 + 1 ship:R_W0_M0_standard:P0:0:0 + 1 ship:R_W0_M1_standard:P0:0:0 eq 2. Source: balance/initial_stock/routes/recipes.
- c000001: 1 inventory:W1:P0:0:0 + 1 ship:R_W1_M0_standard:P0:0:0 + 1 ship:R_W1_M1_standard:P0:0:0 eq 1. Source: balance/initial_stock/routes/recipes.
- c000002: 1 inventory:W2:P0:0:0 + 1 ship:R_W2_M0_standard:P0:0:0 + 1 ship:R_W2_M1_standard:P0:0:0 eq 5. Source: balance/initial_stock/routes/recipes.
- c000003: 1 inventory:W3:P0:0:0 + 1 ship:R_W3_M0_standard:P0:0:0 eq 2. Source: balance/initial_stock/routes/recipes.
- c000004: 1 inventory:M0:P0:0:0 + 1 serve:M0:P0:0:0 + -1 ship:R_W0_M0_standard:P0:0:0 + -1 ship:R_W1_M0_standard:P0:0:0 + -1 ship:R_W2_M0_standard:P0:0:0 + -1 ship:R_W3_M0_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000005: 1 inventory:M1:P0:0:0 + 1 serve:M1:P0:0:0 + -1 ship:R_W0_M1_standard:P0:0:0 + -1 ship:R_W1_M1_standard:P0:0:0 + -1 ship:R_W2_M1_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000006: 1 serve:M0:P0:0:0 eq 2. Source: demands.
- c000007: 1 serve:M1:P0:0:0 eq 3. Source: demands.
- c000008: 1 inventory:W0:P0:0:0 le 3. Source: locations/storage_capacity.
- c000009: 1 ship:R_W0_M0_standard:P0:0:0 + 1 ship:R_W0_M1_standard:P0:0:0 le 0. Source: locations/throughput_capacity.
- c000010: 1 ship:R_W0_M0_standard:P0:0:0 + 1 ship:R_W0_M1_standard:P0:0:0 le 0. Source: locations/opening_cost.
- c000011: 1 inventory:W1:P0:0:0 le 3. Source: locations/storage_capacity.
- c000012: 1 ship:R_W1_M0_standard:P0:0:0 + 1 ship:R_W1_M1_standard:P0:0:0 le 1. Source: locations/throughput_capacity.
- c000013: -1 open:W1 + 1 ship:R_W1_M0_standard:P0:0:0 + 1 ship:R_W1_M1_standard:P0:0:0 le 0. Source: locations/opening_cost.
- c000014: 1 inventory:W2:P0:0:0 le 3. Source: locations/storage_capacity.
- c000015: 1 ship:R_W2_M0_standard:P0:0:0 + 1 ship:R_W2_M1_standard:P0:0:0 le 5. Source: locations/throughput_capacity.
- c000016: -5 open:W2 + 1 ship:R_W2_M0_standard:P0:0:0 + 1 ship:R_W2_M1_standard:P0:0:0 le 0. Source: locations/opening_cost.
- c000017: 1 inventory:W3:P0:0:0 le 1. Source: locations/storage_capacity.
- c000018: 1 ship:R_W3_M0_standard:P0:0:0 le 2. Source: locations/throughput_capacity.
- c000019: -2 open:W3 + 1 ship:R_W3_M0_standard:P0:0:0 le 0. Source: locations/opening_cost.
- c000020: 1 inventory:M0:P0:0:0 le 0. Source: locations/storage_capacity.
- c000021: 0 le 1. Source: locations/throughput_capacity.
- c000022: 1 inventory:M1:P0:0:0 le 2. Source: locations/storage_capacity.
- c000023: 0 le 0. Source: locations/throughput_capacity.
- c000024: 1 ship:R_W0_M0_standard:P0:0:0 le 6. Source: routes/capacity.
- c000025: 1 ship:R_W0_M1_standard:P0:0:0 le 5. Source: routes/capacity.
- c000026: 1 ship:R_W1_M0_standard:P0:0:0 le 5. Source: routes/capacity.
- c000027: 1 ship:R_W1_M1_standard:P0:0:0 le 7. Source: routes/capacity.
- c000028: 1 ship:R_W2_M0_standard:P0:0:0 le 9. Source: routes/capacity.
- c000029: 1 ship:R_W2_M1_standard:P0:0:0 le 5. Source: routes/capacity.
- c000030: 1 ship:R_W3_M0_standard:P0:0:0 le 4. Source: routes/capacity.
