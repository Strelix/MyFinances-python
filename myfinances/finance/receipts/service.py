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
