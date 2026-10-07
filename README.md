# Iran AutoDiag Platform (IADP)

> Automotive diagnostic platform foundation for vehicles commonly encountered in Iran.

This repository was previously a historical experimental trading-dashboard artifact. That artifact remains in Git history; the active development branch is being repurposed for IADP.

## Scope
- OBD-II / SAE J1979
- CAN / CAN-FD abstraction
- ISO-TP / ISO 15765-2
- UDS / ISO 14229
- KWP2000 and legacy transport boundaries
- ELM327, SocketCAN, J2534 and future adapters
- ECU identification, VIN, DTC, live data and diagnostic sessions
- Vehicle/ECU knowledge base with evidence provenance
- Deterministic simulation and replay before hardware

## Engineering rule
Protocol implementations are separated from adapters and vehicle-specific data. No vehicle-specific CAN IDs, DIDs, security algorithms or service behavior are accepted as facts without provenance and verification status.

See ARCHITECTURE.md and docs/ROADMAP.md.
