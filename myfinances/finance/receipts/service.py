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
        """
        Creates a new receipt

        Args:
            name(str): The name of the client
            image(Optional[FilePath]): file path of the image of the receipt.
            date(Optional[str]): date of the receipt (format: YYYY-MM-DD)
            merchant_store(Optional[str]): The names store or merchant
            purchase_category(Optional[str]): Category of the purchase
            total_amount(float): The total of the purchase
            owner(Optional[str]): Owner of the store

        Returns:
            MyFinancesResponse[ReceiptIDResponse]: Creation of the receipt
        """

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
        """
        Lists all the receipts

        Returns:
            MyFinancesResponse[ReceiptList]: lists of all the receipts in the system
        """
        response = self._client._get("/receipts/")
        return MyFinancesResponse(**response.dict())

    def delete_receipt(self, receipt_id: int) -> MyFinancesResponse[ReceiptIDResponse]:
        """
        Deletes a receipt by its ID.

        Args:
            receipt_id(int): Receipt ID's to delete the receipt

        Returns:
            MyFinancesResponse[ReceiptIDResponse]: Deletion of the receipt
        """
        response = self._client._delete(f"/receipts/{receipt_id}/delete")
        return MyFinancesResponse(**response.dict())

    def search_receipts(self,
                        receipt_id: int = None,
                        name: str = None,
                        merchant_store: str = None,
                        image: Optional[FilePath] = None,
                        date: Optional[str] = None,
                        purchase_category: Optional[str] = None,
                        total_amount: float = None,
                        owner: Optional[str] = None) -> MyFinancesResponse[ReceiptList]:
        """
        Searching for the receipts for a specific receipt by using filters

        Args:
            receipt_id(Optional[int]): Receipt ID's
            name(str): The name of the client
            image(Optional[FilePath]): file path of the image of the receipt.
            date(Optional[str]): date of the receipt (format: YYYY-MM-DD)
            merchant_store(Optional[str]): The names store or merchant
            purchase_category(Optional[str]): Category of the purchase
            total_amount(float): The total of the purchase
            owner(Optional[str]): Owner of the store

        Returns:
            MyFinancesResponse[ReceiptList]: List of receipts returning base the filter
        """
        params = {
            key: value for key, value in {
                "id": receipt_id,
                "name": name,
                "merchant_store": merchant_store,
                "image": image,
                "date": date,
                "purchase_category": purchase_category,
                "total_amount": total_amount,
                "owner": owner
            }.items() if value is not None
        }
        response = self._client._get("/receipts/search/", params=params)
        return MyFinancesResponse(**response.dict())
