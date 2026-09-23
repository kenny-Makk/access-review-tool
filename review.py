from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from models import Finding, Account, Role


def describe(finding, session):
    if finding.rule_type == "B":
        acct = session.get(Account, finding.account_id)
        return f"[Rule B] {acct.label} has been dormant since {acct.last_login_at}"
    else:
        role = session.get(Role, finding.role_id)
        return f"[Rule C] Role '{role.name}' has a risky permission combination"


def review_findings(session):
    stmt = select(Finding).where(Finding.status == "pending")
    findings = session.scalars(stmt).all()

    if not findings:
        print("No pending findings.")
        return

    for f in findings:
        print(describe(f, session))
        choice = input("Approve or reject? [a/r/skip]: ").strip().lower()
        if choice == "a":
            f.status = "approved"
        elif choice == "r":
            f.status = "rejected"
        else:
            continue
        session.commit()
        print(f"-> marked as {f.status}\n")


if __name__ == "__main__":
    engine = create_engine("sqlite:///review.db")
    with Session(engine) as session:
        review_findings(session)