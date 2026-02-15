from pydantic import BaseModel

class CostOut(BaseModel): 
    id: int | None 
    name: str | None

    model_config = {
        "from_attributes": True
    }