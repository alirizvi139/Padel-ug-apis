from typing import List, Optional, Type, TypeVar
from motor.motor_asyncio import AsyncIOMotorCollection
from pydantic import BaseModel
from bson import ObjectId
from app.database import get_database
from app.models.base import BaseDocument
from datetime import datetime

T = TypeVar('T', bound=BaseDocument)


class CRUDService:
    """Generic CRUD service for MongoDB operations."""
    
    def __init__(self, collection_name: str, model: Type[T]):
        self.collection_name = collection_name
        self.model = model
        self.database = get_database()
        self.collection: AsyncIOMotorCollection = self.database[collection_name]
    
    async def create(self, data: dict) -> T:
        """Create a new document."""
        result = await self.collection.insert_one(data)
        created_doc = await self.collection.find_one({"_id": result.inserted_id})
        # Convert ObjectId to string for JSON serialization
        if created_doc and "_id" in created_doc:
            created_doc["_id"] = str(created_doc["_id"])
        return self.model(**created_doc)
    
    async def get_by_id(self, id: str) -> Optional[T]:
        """Get document by ID."""
        if not ObjectId.is_valid(id):
            return None
        doc = await self.collection.find_one({"_id": ObjectId(id)})
        if doc and "_id" in doc:
            doc["_id"] = str(doc["_id"])
        return self.model(**doc) if doc else None
    
    async def get_all(self, skip: int = 0, limit: int = 100, search: str = "") -> List[T]:
        """Get all documents with pagination and optional search."""
        query = {}
        if search:
            # Search across multiple fields: name, title, status
            query = {
                "$or": [
                    {"name": {"$regex": search, "$options": "i"}},
                    {"title": {"$regex": search, "$options": "i"}},
                    {"status": {"$regex": search, "$options": "i"}},
                ]
            }
        cursor = self.collection.find(query).skip(skip).limit(limit)
        documents = await cursor.to_list(length=limit)
        # Convert ObjectId to string for JSON serialization
        for doc in documents:
            if doc and "_id" in doc:
                doc["_id"] = str(doc["_id"])
        return [self.model(**doc) for doc in documents]
    
    async def update(self, id: str, data: dict) -> Optional[T]:
        """Update document by ID."""
        if not ObjectId.is_valid(id):
            return None
        data["updated_at"] = datetime.utcnow()
        result = await self.collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if result.modified_count:
            updated_doc = await self.collection.find_one({"_id": ObjectId(id)})
            if updated_doc and "_id" in updated_doc:
                updated_doc["_id"] = str(updated_doc["_id"])
            return self.model(**updated_doc)
        return None
    
    async def delete(self, id: str) -> bool:
        """Delete document by ID."""
        if not ObjectId.is_valid(id):
            return False
        result = await self.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0
    
    async def count(self) -> int:
        """Get total count of documents."""
        return await self.collection.count_documents({})
    
    async def find_by_field(self, field: str, value: any) -> List[T]:
        """Find documents by field value."""
        cursor = self.collection.find({field: value})
        documents = await cursor.to_list(length=None)
        return [self.model(**doc) for doc in documents] 