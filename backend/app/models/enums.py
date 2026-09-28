import enum

class OrderStatus(str, enum.Enum):
    PENDING = "PENDING"
    PREPARING = "PREPARING"
    SERVED = "SERVED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class TableStatus(str, enum.Enum):
    AVAILABLE = "available"
    OCCUPIED = "occupied"

class PartyType(str, enum.Enum):
    SOLO = "solo"
    FRIENDS = "friends"
    FAMILY = "family"

class CustomerType(str, enum.Enum):
    TOURIST = "tourist"
    REGULAR = "regular"