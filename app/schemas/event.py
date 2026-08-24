from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID

class EventCreateRequest(BaseModel):
    title: str = Field(min_length=3, max_length=100, description="Title of the event")
    description: str = Field(min_length=10, max_length=1000, description="Description of the event")
    venue_name: str = Field(min_length=2, max_length=100, description="Name of the venue")
    venue_address: str = Field(min_length=5, max_length=200, description="Address of the venue")
    start_time: datetime = Field(description="Start time of the event in ISO 8601 format")
    end_time: datetime = Field(description="End time of the event in ISO 8601 format")

class EventCreateResponse(BaseModel):
    organizer_id: UUID = Field(description="ID of the user creating the event")
    title: str = Field(min_length=3, max_length=100, description="Title of the event")
    description: str = Field(min_length=10, max_length=1000, description="Description of the event")
    venue_name: str = Field(min_length=2, max_length=100, description="Name of the venue")
    venue_address: str = Field(min_length=5, max_length=200, description="Address of the venue")
    start_time: datetime = Field(description="Start time of the event in ISO 8601 format")
    end_time: datetime = Field(description="End time of the event in ISO 8601 format")
    