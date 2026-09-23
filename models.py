from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass


@event.listens_for(Engine,"connect")
def enable_sqlite_fk(dbapi_conn, _):
    dbapi_conn.execute("PRAGMA foreign_keys=ON")


class Account(Base):
    __tablename__= "accounts"

    id: Mapped[int]=mapped_column(primary_key=True)
    label: Mapped[str]=mapped_column(String(100))
    last_login_at: Mapped[datetime | None]=mapped_column(DateTime)
    is_active: Mapped[bool]=mapped_column(default=True)


class Role(Base):
    __tablename__="roles"

    id: Mapped[int]=mapped_column(primary_key=True)
    name: Mapped[str]=mapped_column(String(50), unique=True)


class Permission(Base):
    __tablename__="permissions"

    id: Mapped[int]=mapped_column(primary_key=True)
    name: Mapped[str]=mapped_column(String(50), unique=True)
    sensitivity_category: Mapped[str]=mapped_column(String(50))


class AccountRole(Base):
    __tablename__ = "account_roles"

    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), primary_key=True)

class RolePermission(Base):
    __tablename__="role_permissions"
    role_id:Mapped[int]=mapped_column(ForeignKey("roles.id"),primary_key=True)
    permission_id:Mapped[int]=mapped_column(ForeignKey("permissions.id"),primary_key=True)


class Finding(Base):
    __tablename__ = "findings"

    id: Mapped[int] = mapped_column(primary_key=True)
    rule_type: Mapped[str] = mapped_column(String(20))  # "B" または "C"
    account_id: Mapped[int | None] = mapped_column(ForeignKey("accounts.id"), nullable=True)
    role_id: Mapped[int | None] = mapped_column(ForeignKey("roles.id"), nullable=True)
    detected_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending / approved / rejected
