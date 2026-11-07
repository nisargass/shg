from enum import Enum
from typing import List, Callable
from fastapi import HTTPException, status


class UserRole(str, Enum):
    SHG_LEADER = "SHG_LEADER"
    SHG_MEMBER = "SHG_MEMBER"
    BUYER = "BUYER"
    FEDERATION_OFFICER = "FEDERATION_OFFICER"
    CUSTOMER = "CUSTOMER"


def check_role_access(user_role: str, allowed_roles: List[UserRole]) -> bool:
    """Verifies if the user's role is in the list of allowed roles."""
    allowed_values = [r.value for r in allowed_roles]
    return user_role in allowed_values


def enforce_role(user_role: str, allowed_roles: List[UserRole]) -> None:
    """Raises 403 Forbidden if user role is not authorized."""
    if not check_role_access(user_role, allowed_roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Operation not permitted for role '{user_role}'. Required one of: {[r.value for r in allowed_roles]}"
        )
