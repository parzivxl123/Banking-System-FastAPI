from models import AuditLog

def create_audit_log(
    db,
    user_id,
    action,
    details
):
    log = AuditLog(
        UserID=user_id,
        Action=action,
        Details=details
    )

    db.add(log)
    db.commit()