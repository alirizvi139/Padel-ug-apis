from typing import List, Optional, Type, TypeVar
from fastapi import APIRouter, HTTPException, Query, Path
from pydantic import BaseModel
from app.services.crud_service import CRUDService
from app.models.base import BaseDocument
from app.models.user import User
import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

T = TypeVar('T', bound=BaseDocument)

# Create user router
user_router = APIRouter(prefix="/users", tags=["users"])

# Initialize user service (will be created when needed)
def get_user_service():
    return CRUDService("users", User)


@user_router.post("/", response_model=dict)
async def create_user(user: User):
    """Create a new user."""
    try:
        user_service = get_user_service()
        data = user.dict(exclude={"id", "created_at", "updated_at"})
        created_user = await user_service.create(data)
        return {
            "success": True,
            "message": "User created successfully",
            "data": created_user.dict()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@user_router.get("/{user_id}", response_model=dict)
async def get_user(user_id: str = Path(..., description="User ID")):
    """Get user by ID."""
    user_service = get_user_service()
    user = await user_service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "success": True,
        "message": "User retrieved successfully",
        "data": user.dict()
    }


@user_router.get("/", response_model=dict)
async def get_users(
    skip: int = Query(0, ge=0, description="Number of users to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of users to return"),
    search: Optional[str] = Query(None, description="Search term for filtering users")
):
    """Get all users with pagination."""
    user_service = get_user_service()
    users = await user_service.get_all(skip=skip, limit=limit, search=search)
    total = await user_service.count()
    pages = (total + limit - 1) // limit
    
    pagination = {
        "page": skip // limit + 1,
        "size": limit,
        "total": total,
        "pages": pages
    }
    
    return {
        "success": True,
        "message": "Users retrieved successfully",
        "data": [user.dict() for user in users],
        "pagination": pagination
    }


@user_router.put("/{user_id}", response_model=dict)
async def update_user(
    user: User,
    user_id: str = Path(..., description="User ID")
):
    """Update user by ID."""
    user_service = get_user_service()
    data = user.dict(exclude={"id", "created_at"})
    updated_user = await user_service.update(user_id, data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "success": True,
        "message": "User updated successfully",
        "data": updated_user.dict()
    }


@user_router.delete("/{user_id}", response_model=dict)
async def delete_user(user_id: str = Path(..., description="User ID")):
    """Delete user by ID."""
    user_service = get_user_service()
    deleted = await user_service.delete(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "success": True,
        "message": "User deleted successfully"
    } 

client = AsyncIOMotorClient(settings.mongodb_url)
db = client[settings.database_name]
