from pydantic import BaseModel, FilePath, condecimal
from typing import Optional, List


class Receipt(BaseModel):
    id: int
    name: str
    image: FilePath
    date: Optional[str] = None
    merchant_store: Optional[str] = None
    purchase_category: Optional[str] = None
    total_price: condecimal(gt=0)
    owner: Optional[str] = None


class ReceiptList(BaseModel):
    receipts: List[Receipt]


class ReceiptIDResponse(BaseModel):
    receipt_id: int
