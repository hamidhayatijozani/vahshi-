# Diagnostic Data Provenance

Every vehicle/ECU/protocol fact must carry source, observation time, identity scope, protocol/transport, raw evidence where appropriate, verification state, confidence, and contributor.

Verification states:
- observed
- verified
- inferred
- unknown

Inferred data must never silently become verified data.
