"""
Pydantic модели для Food2Mood API
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# User Models
class UserResponse(BaseModel):
    user_id: int
    user_name: Optional[str] = None
    user_first_name: Optional[str] = None
    user_last_name: Optional[str] = None
    user_link: str = "tg://user?id="
    phone: Optional[str] = None
    user_reg_time: str
    first_message: int = 0
    last_message: int = 0
    mode_id: int = 0
    mode_key: str = ""
    ban: bool = False
    user_verification: Optional[float] = None
    foodToMoodCoin: int = 0
    last_recomendation_time: Optional[str] = None

    class Config:
        from_attributes = True

# Menu Models
class MenuItemResponse(BaseModel):
    id: int
    dish_name: str
    dish_category: Optional[str] = None
    dish_price: int = 0
    dish_g: Optional[str] = None
    size: Optional[str] = None
    simple_ingridients: Optional[str] = None
    additional_dishes: Optional[str] = None
    iiko_id: Optional[str] = None
    dish_rec_nutritionist: Optional[str] = None
    dish_rec_community: Optional[str] = None
    dish_rec_a_oblomov: Optional[str] = None
    dish_rec_a_ivlev: Optional[str] = None
    stat_reviews: Optional[str] = None
    stat_rating: Optional[str] = None

    class Config:
        from_attributes = True
