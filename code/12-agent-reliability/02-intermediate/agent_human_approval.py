from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class ActionRisk(Enum):
    READ = auto()
    WRITE = auto()


@dataclass(frozen=True)
class ProposedAction:
    name: str
    args: dict
    risk: ActionRisk
    reasoning: str


class ApprovalTimeout(Exception):
    pass


class ApprovalDenied(Exception):
    pass


def send_email_mock(to: str, subject: str, body: str) -> str:
    return f"email sent to {to}: '{subject}'"


def read_inbox_mock(folder: str) -> str:
    return f"3 unread emails in {folder}"


class HumanApprovalGate:
    def __init__(self, approver) -> None:
        # approver: callable(ProposedAction) -> bool | None (None simulates a non-response/timeout)
        self.approver = approver
        self.audit_log: list[dict] = []

    def request_approval(self, action: ProposedAction) -> bool:
        print(f"\n[APPROVAL REQUIRED] action={action.name} args={action.args}")
        print(f"  reasoning: {action.reasoning}")
        decision = self.approver(action)

        if decision is None:
            # failure mode: no response defaults to safe/no-op, never to proceeding
            self.audit_log.append({"action": action.name, "decision": "timeout->denied"})
            raise ApprovalTimeout(f"no response for '{action.name}', defaulting to deny")

        self.audit_log.append({"action": action.name, "decision": "approved" if decision else "denied"})
        if not decision:
            raise ApprovalDenied(f"human denied action '{action.name}'")
        return True


TOOLS = {"send_email": send_email_mock, "read_inbox": read_inbox_mock}


def run_agent_step(action: ProposedAction, gate: HumanApprovalGate) -> str:
    if action.risk is ActionRisk.WRITE:
        gate.request_approval(action)
    return TOOLS[action.name](**action.args)


if __name__ == "__main__":
    approve_gate = HumanApprovalGate(approver=lambda action: True)
    read_action = ProposedAction("read_inbox", {"folder": "inbox"}, ActionRisk.READ, "checking unread count")
    print(run_agent_step(read_action, approve_gate))

    write_action = ProposedAction(
        "send_email",
        {"to": "boss@example.com", "subject": "Status update", "body": "All green."},
        ActionRisk.WRITE,
        "task requires notifying the boss of completion",
    )
    print(run_agent_step(write_action, approve_gate))

    deny_gate = HumanApprovalGate(approver=lambda action: False)
    try:
        run_agent_step(write_action, deny_gate)
    except ApprovalDenied as exc:
        print(f"Blocked: {exc}")

    timeout_gate = HumanApprovalGate(approver=lambda action: None)
    try:
        run_agent_step(write_action, timeout_gate)
    except ApprovalTimeout as exc:
        print(f"Blocked: {exc}")

    print("\nAudit log:", approve_gate.audit_log + deny_gate.audit_log + timeout_gate.audit_log)
