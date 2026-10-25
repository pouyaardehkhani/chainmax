# Mathematical and business semantics

The [controlled business rules](../src/chainmax/rendering.py) are rendered in full
in every statement. The closed [domain schema](../schemas/domain.schema.json)
defines the complete input contract. Identifiers contain no colon, so grounded
decision names are unambiguous colon-separated tuples.

All quantities are nonnegative integers in items; costs are integer cents.
Product volume converts items to volume units. Inventory, shipment, and disposal
decisions have explicit finite upper bounds. Every demand is fulfilled exactly;
there are no shortages or unlisted purchases. Extra goods may remain at terminal
inventory with no salvage value, subject to storage and expiry rules. Missing
routes are unavailable. All input stock is free and initially available, distinct
from recipe output. Production costs are charged only when batches are produced.

Let I[n,p,t,a] be ending stock, X[r,p,t,a] dispatched quantity, D[n,p,t,a]
fulfilled demand, Z[n,p,t,a] disposal, and B[k,t] recipe batches. For each bucket:

```
ending inventory + dispatch + fulfillment + disposal + recipe inputs
  = initial stock (t=0) + surviving previous inventory
    + arriving shipments + recipe outputs.
```

Summed age-specific fulfillment equals each listed node/product/period demand.
Outgoing volume is bounded by node throughput; end stock volume by node storage;
route volume by route capacity. If trucks are listed, route volume also cannot
exceed truck_capacity times integer truck count. Mode eligibility is exactly the
route's product list. Truck charges supplement unit shipping costs.

Warehouse opening is once per horizon and enables outgoing shipments; initial
stock can remain at a closed location. Each route-period activation equals whether
positive shipment occurs, and positive shipment must reach its minimum lot in
items across products and ages. Upper links use the sum of finite, route-specific
shipment bounds. Maximum active suppliers counts incoming route activations at
each market; generated F08 networks contain one route per supplier/market pair.
Dependencies are directional same-period implications.

Periods are 0..T-1. Arrivals and raw stock are available, production becomes
available immediately, and demand, onward dispatch, disposal, and final stock
are accounted within the period. Zero-lead routes are a DAG. A departure in t
with lead L arrives in t+L; beyond-horizon departures have no variable and are
forbidden. Recipe inputs are nonperishable raw products, with no production chains.

Perishable ages are 0..S-1. Storage and transit age goods by elapsed periods.
Arrival at age S is forbidden. Ending inventory at age S-1 is zero: the goods
must be used, validly dispatched, or disposed of at a nonnegative item cost.
The terminal period follows the same expiry rule. Nonperishable goods stay at
age index zero. Tests include arrival at both S-1 and S.

The objective is the sum of item shipping, ending holding (including the last
period), disposal, batch production, opening, route-period, and truck costs plus
the declared constant. All coefficients are nonnegative. Multiple optimal
assignments are allowed. A feasible witness is used only to establish feasibility,
never to establish optimality.

The quantity bound Q is max(1, total initial items + sum of recipe capacity ×
output quantity × T). Inventory/disposal bounds are Q (or zero when expiring),
shipment bounds are min(Q, route capacity // product volume), fulfillment bounds
equal demand, and production/truck/Boolean bounds come from their tables.

The reference IR includes only typed bounded variables, grounded linear relations,
Boolean clauses, and Boolean-guarded linear relations. Constraints have stable IDs
and private rule-source links. It is never executed as code. CP-SAT builds its own
relations from domain tables; the checker maintains a separate event ledger.

Encoding uses binary expansion, hard domain restrictions, signed PB normalization,
and pinned Pindakaas BDD encodings through PySAT. A negative coefficient -c*b is
rewritten as c*not(b)-c. Each nonzero objective coefficient creates weighted soft
units on negated primary bits. Constants and lower-bound shifts go into the
objective offset. Hard constraints stay hard. Legacy WCNF uses integer top =
sum of all soft weights + 1. Auxiliary variables carry no business costs.

Cross-checking establishes agreement of independent implementations, not formal
proof checking or complete equivalence of every large formulation. Exhaustive
fixtures check projected semantics including auxiliary extensions.
