# Bounded integer reference model

Minimize 0 + 7 ship:R_W0_M0_standard:P0:0:0 + 7 ship:R_W0_M0_standard:P1:0:0 + 5 ship:R_W2_M0_standard:P0:0:0 + 5 ship:R_W2_M0_standard:P1:0:0

## Variables

- `inventory:M0:P0:0:0`: integer in [0, 20], item.
- `inventory:M0:P1:0:0`: integer in [0, 20], item.
- `inventory:W0:P0:0:0`: integer in [0, 20], item.
- `inventory:W0:P1:0:0`: integer in [0, 20], item.
- `inventory:W1:P0:0:0`: integer in [0, 20], item.
- `inventory:W1:P1:0:0`: integer in [0, 20], item.
- `inventory:W2:P0:0:0`: integer in [0, 20], item.
- `inventory:W2:P1:0:0`: integer in [0, 20], item.
- `serve:M0:P0:0:0`: integer in [0, 4], item.
- `serve:M0:P1:0:0`: integer in [0, 4], item.
- `ship:R_W0_M0_standard:P0:0:0`: integer in [0, 13], item.
- `ship:R_W0_M0_standard:P1:0:0`: integer in [0, 6], item.
- `ship:R_W2_M0_standard:P0:0:0`: integer in [0, 15], item.
- `ship:R_W2_M0_standard:P1:0:0`: integer in [0, 7], item.

## Hard constraints

- c000000: 1 inventory:W0:P0:0:0 + 1 ship:R_W0_M0_standard:P0:0:0 eq 3. Source: balance/initial_stock/routes/recipes.
- c000001: 1 inventory:W0:P1:0:0 + 1 ship:R_W0_M0_standard:P1:0:0 eq 2. Source: balance/initial_stock/routes/recipes.
- c000002: 1 inventory:W1:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000003: 1 inventory:W1:P1:0:0 eq 3. Source: balance/initial_stock/routes/recipes.
- c000004: 1 inventory:W2:P0:0:0 + 1 ship:R_W2_M0_standard:P0:0:0 eq 5. Source: balance/initial_stock/routes/recipes.
- c000005: 1 inventory:W2:P1:0:0 + 1 ship:R_W2_M0_standard:P1:0:0 eq 7. Source: balance/initial_stock/routes/recipes.
- c000006: 1 inventory:M0:P0:0:0 + 1 serve:M0:P0:0:0 + -1 ship:R_W0_M0_standard:P0:0:0 + -1 ship:R_W2_M0_standard:P0:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000007: 1 inventory:M0:P1:0:0 + 1 serve:M0:P1:0:0 + -1 ship:R_W0_M0_standard:P1:0:0 + -1 ship:R_W2_M0_standard:P1:0:0 eq 0. Source: balance/initial_stock/routes/recipes.
- c000008: 1 serve:M0:P0:0:0 eq 4. Source: demands.
- c000009: 1 serve:M0:P1:0:0 eq 4. Source: demands.
- c000010: 1 inventory:W0:P0:0:0 + 2 inventory:W0:P1:0:0 le 8. Source: locations/storage_capacity.
- c000011: 1 ship:R_W0_M0_standard:P0:0:0 + 2 ship:R_W0_M0_standard:P1:0:0 le 2. Source: locations/throughput_capacity.
- c000012: 1 inventory:W1:P0:0:0 + 2 inventory:W1:P1:0:0 le 9. Source: locations/storage_capacity.
- c000013: 0 le 3. Source: locations/throughput_capacity.
- c000014: 1 inventory:W2:P0:0:0 + 2 inventory:W2:P1:0:0 le 10. Source: locations/storage_capacity.
- c000015: 1 ship:R_W2_M0_standard:P0:0:0 + 2 ship:R_W2_M0_standard:P1:0:0 le 15. Source: locations/throughput_capacity.
- c000016: 1 inventory:M0:P0:0:0 + 2 inventory:M0:P1:0:0 le 4. Source: locations/storage_capacity.
- c000017: 0 le 3. Source: locations/throughput_capacity.
- c000018: 1 ship:R_W0_M0_standard:P0:0:0 + 2 ship:R_W0_M0_standard:P1:0:0 le 13. Source: routes/capacity.
- c000019: 1 ship:R_W2_M0_standard:P0:0:0 + 2 ship:R_W2_M0_standard:P1:0:0 le 15. Source: routes/capacity.
