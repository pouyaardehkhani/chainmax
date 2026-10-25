# Bounded integer reference model

Minimize 0 + 3 dispose:M0:P0:0:0 + 3 dispose:M0:P0:0:1 + 3 dispose:M0:P0:0:2 + 3 dispose:M0:P0:1:0 + 3 dispose:M0:P0:1:1 + 3 dispose:M0:P0:1:2 + 3 dispose:W0:P0:0:0 + 3 dispose:W0:P0:0:1 + 3 dispose:W0:P0:0:2 + 3 dispose:W0:P0:1:0 + 3 dispose:W0:P0:1:1 + 3 dispose:W0:P0:1:2 + 3 dispose:W1:P0:0:0 + 3 dispose:W1:P0:0:1 + 3 dispose:W1:P0:0:2 + 3 dispose:W1:P0:1:0 + 3 dispose:W1:P0:1:1 + 3 dispose:W1:P0:1:2 + 2 inventory:M0:P0:0:0 + 2 inventory:M0:P0:0:1 + 2 inventory:M0:P0:0:2 + 2 inventory:M0:P0:1:0 + 2 inventory:M0:P0:1:1 + 2 inventory:M0:P0:1:2 + 2 inventory:W0:P0:0:0 + 2 inventory:W0:P0:0:1 + 2 inventory:W0:P0:0:2 + 2 inventory:W0:P0:1:0 + 2 inventory:W0:P0:1:1 + 2 inventory:W0:P0:1:2 + 2 inventory:W1:P0:0:0 + 2 inventory:W1:P0:0:1 + 2 inventory:W1:P0:0:2 + 2 inventory:W1:P0:1:0 + 2 inventory:W1:P0:1:1 + 2 inventory:W1:P0:1:2 + 2 ship:R_W0_M0_standard:P0:0:0 + 2 ship:R_W0_M0_standard:P0:0:1 + 2 ship:R_W0_M0_standard:P0:0:2 + 2 ship:R_W0_M0_standard:P0:1:0 + 2 ship:R_W0_M0_standard:P0:1:1 + 2 ship:R_W0_M0_standard:P0:1:2

## Variables

- `dispose:M0:P0:0:0`: integer in [0, 3], item.
- `dispose:M0:P0:0:1`: integer in [0, 3], item.
- `dispose:M0:P0:0:2`: integer in [0, 3], item.
- `dispose:M0:P0:1:0`: integer in [0, 3], item.
- `dispose:M0:P0:1:1`: integer in [0, 3], item.
- `dispose:M0:P0:1:2`: integer in [0, 3], item.
- `dispose:W0:P0:0:0`: integer in [0, 3], item.
- `dispose:W0:P0:0:1`: integer in [0, 3], item.
- `dispose:W0:P0:0:2`: integer in [0, 3], item.
- `dispose:W0:P0:1:0`: integer in [0, 3], item.
- `dispose:W0:P0:1:1`: integer in [0, 3], item.
- `dispose:W0:P0:1:2`: integer in [0, 3], item.
- `dispose:W1:P0:0:0`: integer in [0, 3], item.
- `dispose:W1:P0:0:1`: integer in [0, 3], item.
- `dispose:W1:P0:0:2`: integer in [0, 3], item.
- `dispose:W1:P0:1:0`: integer in [0, 3], item.
- `dispose:W1:P0:1:1`: integer in [0, 3], item.
- `dispose:W1:P0:1:2`: integer in [0, 3], item.
- `inventory:M0:P0:0:0`: integer in [0, 3], item.
- `inventory:M0:P0:0:1`: integer in [0, 3], item.
- `inventory:M0:P0:0:2`: integer in [0, 0], item.
- `inventory:M0:P0:1:0`: integer in [0, 3], item.
- `inventory:M0:P0:1:1`: integer in [0, 3], item.
- `inventory:M0:P0:1:2`: integer in [0, 0], item.
- `inventory:W0:P0:0:0`: integer in [0, 3], item.
- `inventory:W0:P0:0:1`: integer in [0, 3], item.
- `inventory:W0:P0:0:2`: integer in [0, 0], item.
- `inventory:W0:P0:1:0`: integer in [0, 3], item.
- `inventory:W0:P0:1:1`: integer in [0, 3], item.
- `inventory:W0:P0:1:2`: integer in [0, 0], item.
- `inventory:W1:P0:0:0`: integer in [0, 3], item.
- `inventory:W1:P0:0:1`: integer in [0, 3], item.
- `inventory:W1:P0:0:2`: integer in [0, 0], item.
- `inventory:W1:P0:1:0`: integer in [0, 3], item.
- `inventory:W1:P0:1:1`: integer in [0, 3], item.
- `inventory:W1:P0:1:2`: integer in [0, 0], item.
- `serve:M0:P0:1:0`: integer in [0, 2], item.
- `serve:M0:P0:1:1`: integer in [0, 2], item.
- `serve:M0:P0:1:2`: integer in [0, 2], item.
- `ship:R_W0_M0_standard:P0:0:0`: integer in [0, 3], item.
- `ship:R_W0_M0_standard:P0:0:1`: integer in [0, 3], item.
- `ship:R_W0_M0_standard:P0:0:2`: integer in [0, 3], item.
- `ship:R_W0_M0_standard:P0:1:0`: integer in [0, 3], item.
- `ship:R_W0_M0_standard:P0:1:1`: integer in [0, 3], item.
- `ship:R_W0_M0_standard:P0:1:2`: integer in [0, 3], item.

## Hard constraints

- c000000: 1 dispose:W0:P0:0:0 + 1 inventory:W0:P0:0:0 + 1 ship:R_W0_M0_standard:P0:0:0 eq 3. Source: balance/initial_stock/routes/recipes.
- c000001: 1 dispose:W0:P0:0:1 + 1 inventory:W0:P0:0:1 + 1 ship:R_W0_M0_standard:P0:0:1 eq 0. Source: balance/initial_stock/routes/recipes.
- c000002: 1 dispose:W0:P0:0:2 + 1 inventory:W0:P0:0:2 + 1 ship:R_W0_M0_standard:P0:0:2 eq 0. Source: balance/initial_stock/routes/recipes.
- c000003: 1 dispose:W0:P0:1:0 + 1 inventory:W0:P0:1:0 + 1 ship:R_W0_M0_standard:P0:1:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000004: 1 dispose:W0:P0:1:1 + -1 inventory:W0:P0:0:0 + 1 inventory:W0:P0:1:1 + 1 ship:R_W0_M0_standard:P0:1:1 eq 0. Source: balance/initial_stock/routes/recipes.
- c000005: 1 dispose:W0:P0:1:2 + -1 inventory:W0:P0:0:1 + 1 inventory:W0:P0:1:2 + 1 ship:R_W0_M0_standard:P0:1:2 eq 0. Source: balance/initial_stock/routes/recipes.
- c000006: 1 dispose:W1:P0:0:0 + 1 inventory:W1:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000007: 1 dispose:W1:P0:0:1 + 1 inventory:W1:P0:0:1 eq 0. Source: balance/initial_stock/routes/recipes.
- c000008: 1 dispose:W1:P0:0:2 + 1 inventory:W1:P0:0:2 eq 0. Source: balance/initial_stock/routes/recipes.
- c000009: 1 dispose:W1:P0:1:0 + 1 inventory:W1:P0:1:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000010: 1 dispose:W1:P0:1:1 + -1 inventory:W1:P0:0:0 + 1 inventory:W1:P0:1:1 eq 0. Source: balance/initial_stock/routes/recipes.
- c000011: 1 dispose:W1:P0:1:2 + -1 inventory:W1:P0:0:1 + 1 inventory:W1:P0:1:2 eq 0. Source: balance/initial_stock/routes/recipes.
- c000012: 1 dispose:M0:P0:0:0 + 1 inventory:M0:P0:0:0 + -1 ship:R_W0_M0_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000013: 1 dispose:M0:P0:0:1 + 1 inventory:M0:P0:0:1 + -1 ship:R_W0_M0_standard:P0:0:1 eq 0. Source: balance/initial_stock/routes/recipes.
- c000014: 1 dispose:M0:P0:0:2 + 1 inventory:M0:P0:0:2 + -1 ship:R_W0_M0_standard:P0:0:2 eq 0. Source: balance/initial_stock/routes/recipes.
- c000015: 1 dispose:M0:P0:1:0 + 1 inventory:M0:P0:1:0 + 1 serve:M0:P0:1:0 + -1 ship:R_W0_M0_standard:P0:1:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000016: 1 dispose:M0:P0:1:1 + -1 inventory:M0:P0:0:0 + 1 inventory:M0:P0:1:1 + 1 serve:M0:P0:1:1 + -1 ship:R_W0_M0_standard:P0:1:1 eq 0. Source: balance/initial_stock/routes/recipes.
- c000017: 1 dispose:M0:P0:1:2 + -1 inventory:M0:P0:0:1 + 1 inventory:M0:P0:1:2 + 1 serve:M0:P0:1:2 + -1 ship:R_W0_M0_standard:P0:1:2 eq 0. Source: balance/initial_stock/routes/recipes.
- c000018: 1 serve:M0:P0:1:0 + 1 serve:M0:P0:1:1 + 1 serve:M0:P0:1:2 eq 2. Source: demands.
- c000019: 1 inventory:W0:P0:0:0 + 1 inventory:W0:P0:0:1 + 1 inventory:W0:P0:0:2 le 3. Source: locations/storage_capacity.
- c000020: 1 ship:R_W0_M0_standard:P0:0:0 + 1 ship:R_W0_M0_standard:P0:0:1 + 1 ship:R_W0_M0_standard:P0:0:2 le 5. Source: locations/throughput_capacity.
- c000021: 1 inventory:W0:P0:1:0 + 1 inventory:W0:P0:1:1 + 1 inventory:W0:P0:1:2 le 3. Source: locations/storage_capacity.
- c000022: 1 ship:R_W0_M0_standard:P0:1:0 + 1 ship:R_W0_M0_standard:P0:1:1 + 1 ship:R_W0_M0_standard:P0:1:2 le 5. Source: locations/throughput_capacity.
- c000023: 1 inventory:W1:P0:0:0 + 1 inventory:W1:P0:0:1 + 1 inventory:W1:P0:0:2 le 3. Source: locations/storage_capacity.
- c000024: 0 le 0. Source: locations/throughput_capacity.
- c000025: 1 inventory:W1:P0:1:0 + 1 inventory:W1:P0:1:1 + 1 inventory:W1:P0:1:2 le 3. Source: locations/storage_capacity.
- c000026: 0 le 0. Source: locations/throughput_capacity.
- c000027: 1 inventory:M0:P0:0:0 + 1 inventory:M0:P0:0:1 + 1 inventory:M0:P0:0:2 le 3. Source: locations/storage_capacity.
- c000028: 0 le 2. Source: locations/throughput_capacity.
- c000029: 1 inventory:M0:P0:1:0 + 1 inventory:M0:P0:1:1 + 1 inventory:M0:P0:1:2 le 3. Source: locations/storage_capacity.
- c000030: 0 le 2. Source: locations/throughput_capacity.
- c000031: 1 ship:R_W0_M0_standard:P0:0:0 + 1 ship:R_W0_M0_standard:P0:0:1 + 1 ship:R_W0_M0_standard:P0:0:2 le 6. Source: routes/capacity.
- c000032: 1 ship:R_W0_M0_standard:P0:1:0 + 1 ship:R_W0_M0_standard:P0:1:1 + 1 ship:R_W0_M0_standard:P0:1:2 le 6. Source: routes/capacity.
