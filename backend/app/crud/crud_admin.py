from sqlmodel import Session, select
from app.models.restaurant import AdminUser
from app.schemas.restaurant import AdminCreate
from app.core.security import get_password_hash

def create_admin(db: Session, admin_in: AdminCreate) -> AdminUser:
    hashed = get_password_hash(admin_in.password)
    db_admin = AdminUser(
        restaurant_id=admin_in.restaurant_id,
        username=admin_in.username,
        hashed_password=hashed
    )
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin

def get_admin_by_username(db: Session, username: str):
    return db.exec(select(AdminUser).where(AdminUser.username == username)).first()