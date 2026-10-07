from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import json
from hashlib import sha256


@dataclass
class DiagnosticReport:
    vehicle_id: str | None = None
    vin: str | None = None
    ecu_identities: list[dict] = field(default_factory=list)
    dtcs: list[dict] = field(default_factory=list)
    measurements: list[dict] = field(default_factory=list)
    evidence: list[dict] = field(default_factory=list)

    def add_evidence(self, record: dict) -> None:
        required = {"source", "observed_at", "evidence_state"}
        missing = required - record.keys()
        if missing:
            raise ValueError(f"evidence record missing fields: {sorted(missing)}")
        if record["evidence_state"] not in {"observed", "verified", "inferred", "unknown"}:
            raise ValueError("invalid evidence state")
        self.evidence.append(dict(record))

    def snapshot(self) -> dict:
        return {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "vehicle_id": self.vehicle_id,
            "vin": self.vin,
            "ecu_identities": self.ecu_identities,
            "dtcs": self.dtcs,
            "measurements": self.measurements,
            "evidence": self.evidence,
        }

    def digest(self) -> str:
        canonical = json.dumps(
            self.snapshot(), sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode()
        return sha256(canonical).hexdigest()
