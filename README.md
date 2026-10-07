# Iran AutoDiag Platform (IADP)

> Evidence-first automotive diagnostic platform foundation for vehicles commonly encountered in Iran.

This repository was previously a historical experimental trading-dashboard artifact. That artifact remains in Git history for provenance; the active codebase is now IADP.

## Current implementation
- OBD-II request builders and core live-data decoders
- CAN frame validation and in-memory transport
- Classic-CAN ISO-TP framing, flow control, sequence validation and reassembly
- UDS session control, TesterPresent, ReadDataByIdentifier and negative-response handling
- VIN identification helpers for OBD-II Mode 09 and a generic UDS DID path
- deterministic virtual ECU
- deterministic replay engine with evidence digest
- conservative ELM327 command boundary
- JSON schemas for diagnostic records and vehicle knowledge
- unit-test coverage for protocol and simulator paths

## Scope
- OBD-II / SAE J1979
- CAN / CAN-FD abstraction
- ISO-TP / ISO 15765-2
- UDS / ISO 14229
- KWP2000 and legacy transport boundaries
- ELM327, SocketCAN, J2534 and future adapters
- ECU identification, VIN, DTC, live data and diagnostic sessions
- Vehicle/ECU knowledge base with evidence provenance
- deterministic simulation and replay before hardware

## Safety boundary
The current implementation is deliberately read-oriented and simulator-first. Write-capable ECU operations, security access, programming, actuator control and vehicle-specific service procedures are not presented as production-ready.

## Engineering rule
Protocol implementations are separated from adapters and vehicle-specific data. No vehicle-specific CAN IDs, DIDs, security algorithms or service behavior are accepted as facts without provenance and verification status.

See ARCHITECTURE.md, docs/ROADMAP.md and docs/DATA-PROVENANCE.md.
