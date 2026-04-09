"""Schema to validate user profile data"""
from typing import List, Optional
from pydantic import BaseModel

class SocialNetworkImage(BaseModel):
    """Included data"""
    id: int
    imagePath: str
    hostPath: str


class SocialNetwork(BaseModel):
    """Included data"""
    id: int
    url: str
    socialNetworkImage: SocialNetworkImage


class UserLocation(BaseModel):
    """Included data"""
    id: int
    cityEn: str
    cityUk: str
    regionEn: str
    regionUk: str
    countryEn: str
    countryUk: str
    latitude: float
    longitude: float


class NotificationPreference(BaseModel):
    """Included data"""
    id: int
    emailPreference: str
    periodicity: str


class UserProfileSchema(BaseModel):
    """Common schema for all user profile data"""
    profilePicturePath: Optional[str] = None

    name: str

    socialNetworks: List[SocialNetwork]

    showLocation: str
    showEcoPlace: str
    showToDoList: str
    rating: float
    role: str

    userLocationDto: Optional[UserLocation] = None

    notificationPreferences: List[NotificationPreference]
