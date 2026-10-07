# Roadmap

## Phase 0 — Foundation — implemented
- repository and package structure
- protocol boundaries
- provenance schemas
- deterministic simulator
- initial CI workflow

## Phase 1 — Core protocols — implemented in this branch
- OBD-II request builders and core PID decoders
- OBD/UDS VIN identification helpers
- ISO-TP classic-CAN framing, validation and reassembly
- CAN transport abstraction and deterministic memory transport
- UDS session control, TesterPresent, DID reads and NRC handling
- deterministic replay engine with SHA-256 evidence digest
- ELM327 command boundary

## Phase 2 — Integration hardening — in progress
- complete ISO-TP sender/receiver state machine with production timeout policy
- CAN-FD addressing and payload rules
- response matching and ECU discovery
- DTC normalization across OBD-II and UDS
- fixture corpus and negative-path coverage
- CI execution evidence and package quality gates

## Phase 3 — Vehicle knowledge — planned
- Android Bluetooth/Wi-Fi adapters
- desktop SocketCAN/J2534 adapters
- evidence-bound vehicle/ECU database for Iran
- observed/verified/inferred/unknown provenance enforcement
- workshop scan/report format

## Phase 4 — Advanced diagnostics — gated
- actuator tests
- service functions
- advanced UDS
- write-capable operations only behind explicit safety/capability gates

## Phase 5 — Production hardening
- hardware matrix
- interoperability testing
- performance/reliability testing
- signed release artifacts
- diagnostic knowledge engine
