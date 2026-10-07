# IADP Architecture

UI -> Diagnostic Core -> Protocol Session -> Transport -> Adapter -> Vehicle

Layers:
1. Application: Android/Desktop/Web
2. Diagnostic Core: workflows and domain models
3. Protocols: OBD-II, CAN, ISO-TP, UDS, KWP2000
4. Transport: abstract frame/byte transport
5. Adapters: ELM327, SocketCAN, J2534, Bluetooth, Wi-Fi, USB
6. Knowledge Base: vehicle/ECU/protocol records with provenance
7. Simulation & Replay: virtual ECU and deterministic fixtures

The core never depends directly on a physical adapter.

Initial hardware-facing scope is read-only identification and data collection. Write, routine-control, actuator and programming functions require explicit capability declarations, session rules and tests.
