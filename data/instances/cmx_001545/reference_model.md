# Bounded integer reference model

Minimize 0 + 6 ship:R_W0_M0_rail:P0:0:0 + 8 ship:R_W0_M0_road:P0:0:0 + 4 ship:R_W1_M0_rail:P0:0:0 + 7 ship:R_W1_M0_road:P0:0:0 + 5 trucks:R_W0_M0_rail:0 + 5 trucks:R_W0_M0_road:0 + 4 trucks:R_W1_M0_rail:0 + 9 trucks:R_W1_M0_road:0

## Variables

- `inventory:M0:P0:0:0`: integer in [0, 7], item.
- `inventory:W0:P0:0:0`: integer in [0, 7], item.
- `inventory:W1:P0:0:0`: integer in [0, 7], item.
- `serve:M0:P0:0:0`: integer in [0, 3], item.
- `ship:R_W0_M0_rail:P0:0:0`: integer in [0, 3], item.
- `ship:R_W0_M0_road:P0:0:0`: integer in [0, 7], item.
- `ship:R_W1_M0_rail:P0:0:0`: integer in [0, 6], item.
- `ship:R_W1_M0_road:P0:0:0`: integer in [0, 3], item.
- `trucks:R_W0_M0_rail:0`: integer in [0, 1], truck.
- `trucks:R_W0_M0_road:0`: integer in [0, 3], truck.
- `trucks:R_W1_M0_rail:0`: integer in [0, 2], truck.
- `trucks:R_W1_M0_road:0`: integer in [0, 1], truck.

## Hard constraints

- c000000: 1 inventory:W0:P0:0:0 + 1 ship:R_W0_M0_rail:P0:0:0 + 1 ship:R_W0_M0_road:P0:0:0 eq 3. Source: balance/initial_stock/routes/recipes.
- c000001: 1 inventory:W1:P0:0:0 + 1 ship:R_W1_M0_rail:P0:0:0 + 1 ship:R_W1_M0_road:P0:0:0 eq 4. Source: balance/initial_stock/routes/recipes.
- c000002: 1 inventory:M0:P0:0:0 + 1 serve:M0:P0:0:0 + -1 ship:R_W0_M0_rail:P0:0:0 + -1 ship:R_W0_M0_road:P0:0:0 + -1 ship:R_W1_M0_rail:P0:0:0 + -1 ship:R_W1_M0_road:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000003: 1 serve:M0:P0:0:0 eq 3. Source: demands.
- c000004: 1 inventory:W0:P0:0:0 le 6. Source: locations/storage_capacity.
- c000005: 1 ship:R_W0_M0_rail:P0:0:0 + 1 ship:R_W0_M0_road:P0:0:0 le 4. Source: locations/throughput_capacity.
- c000006: 1 inventory:W1:P0:0:0 le 3. Source: locations/storage_capacity.
- c000007: 1 ship:R_W1_M0_rail:P0:0:0 + 1 ship:R_W1_M0_road:P0:0:0 le 7. Source: locations/throughput_capacity.
- c000008: 1 inventory:M0:P0:0:0 le 3. Source: locations/storage_capacity.
- c000009: 0 le 3. Source: locations/throughput_capacity.
- c000010: 1 ship:R_W0_M0_rail:P0:0:0 le 3. Source: routes/capacity.
- c000011: 1 ship:R_W0_M0_rail:P0:0:0 + -3 trucks:R_W0_M0_rail:0 le 0. Source: routes/truck_capacity.
- c000012: 1 ship:R_W0_M0_road:P0:0:0 le 7. Source: routes/capacity.
- c000013: 1 ship:R_W0_M0_road:P0:0:0 + -3 trucks:R_W0_M0_road:0 le 0. Source: routes/truck_capacity.
- c000014: 1 ship:R_W1_M0_rail:P0:0:0 le 6. Source: routes/capacity.
- c000015: 1 ship:R_W1_M0_rail:P0:0:0 + -4 trucks:R_W1_M0_rail:0 le 0. Source: routes/truck_capacity.
- c000016: 1 ship:R_W1_M0_road:P0:0:0 le 3. Source: routes/capacity.
- c000017: 1 ship:R_W1_M0_road:P0:0:0 + -5 trucks:R_W1_M0_road:0 le 0. Source: routes/truck_capacity.
