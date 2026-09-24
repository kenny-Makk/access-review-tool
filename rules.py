from datetime import datetime, timedelta
from sqlalchemy import create_engine, select, distinct
from sqlalchemy.orm import Session
from models import Account, Role, Permission, RolePermission, Finding


def find_dormant(session, days=90):
    cutoff = datetime.now() - timedelta(days=days)
    stmt = select(Account).where(
        Account.is_active == True,
        Account.last_login_at < cutoff,
    )
    return session.scalars(stmt).all()


def find_risky_combinations(session, risky_categories={"contact_info", "qualifications", "raw_hours_data"}):
    results = []
    roles = session.scalars(select(Role)).all()
    for role in roles:
        stmt = (
            select(distinct(Permission.sensitivity_category))
            .join(RolePermission, RolePermission.permission_id == Permission.id)
            .where(RolePermission.role_id == role.id)
        )
        categories = set(session.scalars(stmt).all())
        if risky_categories.issubset(categories):
            results.append(role)
    return results


def run_rules_and_save(session):
    for acct in find_dormant(session):
        session.add(Finding(rule_type="B", account_id=acct.id))
        print(f"[Rule B] {acct.label} flagged as dormant")

    for role in find_risky_combinations(session):
        session.add(Finding(rule_type="C", role_id=role.id))
        print(f"[Rule C] {role.name} flagged for risky permission combination")

        for role, extra_categories in find_over_permissioned(session):
            session.add(Finding(rule_type="A", role_id=role.id))
            print(f"[Rule A] {role.name} has extra access: {extra_categories}")

    session.commit()

EXPECTED_CATEGORIES = {
    "team_leader": {"raw_hours_data"},
    "volunteer_support": {"contact_info", "qualifications"},
    "recruitment_it": {"email_history"},
}


def find_over_permissioned(session):
    results = []
    roles = session.scalars(select(Role)).all()
    for role in roles:
        stmt = (
            select(distinct(Permission.sensitivity_category))
            .join(RolePermission, RolePermission.permission_id == Permission.id)
            .where(RolePermission.role_id == role.id)
        )
        actual_categories = set(session.scalars(stmt).all())
        expected = EXPECTED_CATEGORIES.get(role.name, set())
        extra = actual_categories - expected
        if extra:
            results.append((role, extra))
    return results

if __name__ == "__main__":
    engine = create_engine("sqlite:///review.db")
    with Session(engine) as session:
        run_rules_and_save(session)