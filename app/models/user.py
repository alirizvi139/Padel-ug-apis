from typing import Literal, Optional
from pydantic import Field, BaseModel
from app.models.base import BaseDocument


class Attack(BaseModel):
    pistol: int = Field(..., ge=0, description="Number of pistols")
    bomb: int = Field(..., ge=0, description="Number of bombs")
    dynamite: int = Field(..., ge=0, description="Number of dynamites")


class User(BaseDocument):
    og_code: int = Field(..., description="OG Code number")
    name: str = Field(..., description="User name")
    title: str = Field(..., description="User title")
    rank: int = Field(..., ge=0, description="Rank number")
    points: int = Field(..., ge=0, description="User points")
    attack: Attack = Field(..., description="Attack weapons")
    defence: int = Field(..., ge=0, description="Defence number")
    status: Literal["Scull", "Ripple", "Jail"] = Field(..., description="User status")
    matches: int = Field(..., ge=0, description="Number of matches")
    won: int = Field(..., ge=0, description="Number of matches won")
    approval: Literal["Approved", "Pending", "Rejected"] = Field(
        ..., description="Approval status"
    )
    profile_image: str = Field(..., description="Profile image URL")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
