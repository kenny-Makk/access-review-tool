from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Base, Account, Role, Permission, AccountRole, RolePermission

engine = create_engine("sqlite:///review.db")
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

with Session(engine) as session:
    now = datetime.now()

    # 権限
    view_contact = Permission(name="view_contact_info", sensitivity_category="contact_info")
    view_qual = Permission(name="view_qualifications", sensitivity_category="qualifications")
    view_hours = Permission(name="generate_raw_reports", sensitivity_category="raw_hours_data")
    view_email = Permission(name="view_email_history", sensitivity_category="email_history")

    # ロール
    team_leader = Role(name="team_leader")
    volunteer_support = Role(name="volunteer_support")
    recruitment_it = Role(name="recruitment_it")

    # アカウント
    acct1 = Account(label="acct-001", last_login_at=now - timedelta(days=200))
    acct2 = Account(label="acct-002", last_login_at=now - timedelta(days=3))
    acct3 = Account(label="acct-003", last_login_at=now - timedelta(days=5))
    acct4 = Account(label="acct-004", last_login_at=now - timedelta(days=160))
    acct5 = Account(label="acct-005", last_login_at=now - timedelta(days=10))
    acct6 = Account(label="acct-006", last_login_at=now - timedelta(days=400))

    session.add_all([view_contact, view_qual, view_hours, view_email,
                     team_leader, volunteer_support, recruitment_it,
                     acct1, acct2, acct3, acct4, acct5, acct6])
    session.flush()

    role_perms = [
        (team_leader, view_hours),
        (volunteer_support, view_contact),
        (volunteer_support, view_qual),
        (volunteer_support, view_hours),
        (recruitment_it, view_email),
    ]
    for role, perm in role_perms:
        session.add(RolePermission(role_id=role.id, permission_id=perm.id))

    account_roles = [
        (acct1, team_leader),
        (acct2, team_leader),
        (acct3, volunteer_support),
        (acct4, volunteer_support),
        (acct5, recruitment_it),
        (acct6, recruitment_it),
    ]
    for acct, role in account_roles:
        session.add(AccountRole(account_id=acct.id, role_id=role.id))

    session.commit()

print("seeded")