# Bounded integer reference model

Minimize 0 + 6 ship:R_W0_M0_rail:P0:0:0 + 7 ship:R_W0_M0_road:P0:0:0 + 5 ship:R_W1_M0_road:P0:0:0 + 2 trucks:R_W0_M0_rail:0 + 8 trucks:R_W0_M0_road:0 + 4 trucks:R_W1_M0_road:0

## Variables

- `inventory:M0:P0:0:0`: integer in [0, 9], item.
- `inventory:W0:P0:0:0`: integer in [0, 9], item.
- `inventory:W1:P0:0:0`: integer in [0, 9], item.
- `inventory:W2:P0:0:0`: integer in [0, 9], item.
- `serve:M0:P0:0:0`: integer in [0, 5], item.
- `ship:R_W0_M0_rail:P0:0:0`: integer in [0, 5], item.
- `ship:R_W0_M0_road:P0:0:0`: integer in [0, 6], item.
- `ship:R_W1_M0_road:P0:0:0`: integer in [0, 9], item.
- `trucks:R_W0_M0_rail:0`: integer in [0, 2], truck.
- `trucks:R_W0_M0_road:0`: integer in [0, 2], truck.
- `trucks:R_W1_M0_road:0`: integer in [0, 3], truck.

## Hard constraints

- c000000: 1 inventory:W0:P0:0:0 + 1 ship:R_W0_M0_rail:P0:0:0 + 1 ship:R_W0_M0_road:P0:0:0 eq 1. Source: balance/initial_stock/routes/recipes.
- c000001: 1 inventory:W1:P0:0:0 + 1 ship:R_W1_M0_road:P0:0:0 eq 5. Source: balance/initial_stock/routes/recipes.
- c000002: 1 inventory:W2:P0:0:0 eq 3. Source: balance/initial_stock/routes/recipes.
- c000003: 1 inventory:M0:P0:0:0 + 1 serve:M0:P0:0:0 + -1 ship:R_W0_M0_rail:P0:0:0 + -1 ship:R_W0_M0_road:P0:0:0 + -1 ship:R_W1_M0_road:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000004: 1 serve:M0:P0:0:0 eq 5. Source: demands.
- c000005: 1 inventory:W0:P0:0:0 le 5. Source: locations/storage_capacity.
- c000006: 1 ship:R_W0_M0_rail:P0:0:0 + 1 ship:R_W0_M0_road:P0:0:0 le 3. Source: locations/throughput_capacity.
- c000007: 1 inventory:W1:P0:0:0 le 3. Source: locations/storage_capacity.
- c000008: 1 ship:R_W1_M0_road:P0:0:0 le 7. Source: locations/throughput_capacity.
- c000009: 1 inventory:W2:P0:0:0 le 4. Source: locations/storage_capacity.
- c000010: 0 le 4. Source: locations/throughput_capacity.
- c000011: 1 inventory:M0:P0:0:0 le 2. Source: locations/storage_capacity.
- c000012: 0 le 4. Source: locations/throughput_capacity.
- c000013: 1 ship:R_W0_M0_rail:P0:0:0 le 5. Source: routes/capacity.
- c000014: 1 ship:R_W0_M0_rail:P0:0:0 + -4 trucks:R_W0_M0_rail:0 le 0. Source: routes/truck_capacity.
- c000015: 1 ship:R_W0_M0_road:P0:0:0 le 6. Source: routes/capacity.
- c000016: 1 ship:R_W0_M0_road:P0:0:0 + -3 trucks:R_W0_M0_road:0 le 0. Source: routes/truck_capacity.
- c000017: 1 ship:R_W1_M0_road:P0:0:0 le 9. Source: routes/capacity.
- c000018: 1 ship:R_W1_M0_road:P0:0:0 + -3 trucks:R_W1_M0_road:0 le 0. Source: routes/truck_capacity.
