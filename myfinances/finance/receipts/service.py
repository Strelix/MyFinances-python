from typing import Optional

from pydantic import FilePath

from myfinances.base_service import BaseService
from myfinances.finance.receipts.models import Receipt, ReceiptList, ReceiptIDResponse
from myfinances.models import MyFinancesResponse


class ReceiptService(BaseService):
    def create_receipt(self,
                       name: str,
                       image: Optional[FilePath] = None,
                       date: Optional[str] = None,
                       merchant_store: Optional[str] = None,
                       purchase_category: Optional[str] = None,
                       total_amount: float = None,
                       owner: Optional[str] = None
    ) -> MyFinancesResponse[ReceiptIDResponse]:

        params = {
            "name": name,
            "image": image,
            "date": date,
            "merchant_store": merchant_store,
            "purchase_category": purchase_category,
            "total_amount": total_amount,
            "owner": owner
        }

        response = self._client._post("/receipts/create/", json=params)

        return MyFinancesResponse(**response.dict())

    def list_receipts(self) -> MyFinancesResponse[ReceiptList]:
        response = self._client._get("/receipts/")
        return MyFinancesResponse(**response.dict())

    def delete_receipt(self, receipt_id: int) -> MyFinancesResponse[ReceiptIDResponse]:
        response = self._client._delete(f"/receipts/{receipt_id}/delete")
        return MyFinancesResponse(**response.dict())

    def search_receipts(self, receipt_id: int = None, name: str = None, merchant_store: str = None,
                        image: Optional[FilePath] = None,  date: Optional[str] = None, purchase_category: Optional[str] = None,
                       total_amount: float = None, owner: Optional[str] = None ) -> MyFinancesResponse[ReceiptList]:
        params = {}

        if receipt_id is not None:
            params["id"] = receipt_id

        if name is not None:
            params["name"] = name

        if merchant_store is not None:
            params["merchant_store"] = merchant_store

        if image is not None:
            params["image"] = image

        if date is not None:
            params["date"] = date

        if purchase_category is not None:
            params["purchase_category"] = purchase_category

        if total_amount is not None:
            params["total_amount"] = total_amount

        if owner is not None:
            params["owner"] = owner

        response = self._client._get("/receipts/search/", params=params)
        return MyFinancesResponse(**response.dict())
