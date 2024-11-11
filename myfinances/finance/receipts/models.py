from pydantic import BaseModel, FilePath, condecimal
from typing import Optional, List


class Receipt(BaseModel):
    id: int
    name: str
    imgae: FilePath
    date: Optional[str] = None
    merchant_store: Optional[str] = None
    purchase_category: Optional[str] = None
    total_price: condecimal(gt=0)
    owner: Optional[str] = None


class ReceiptList(BaseModel):
    receipts: List[Receipt]


class CreateReceiptResponse(BaseModel):
    receipt_id: int
    message: Optional[str] == "Receipt successfully created"
