from myfinances.base_service import BaseService
from myfinances.finance.invoices.models import InvoiceList, CreateInvoiceResponse, Invoice
from myfinances.models import MyFinancesResponse


class InvoicesService(BaseService):
    def create_invoice(self,
                       customer_id: int, amount: float, description: str = None, due_date: str = None) -> MyFinancesResponse[CreateInvoiceResponse]:
        payload = {
            "customer_id": customer_id,
            "amount": amount,
            "description": description,
            "due_date": due_date,
        }

        response = self._client._post("/invoices/create", json=payload)
        return MyFinancesResponse(**response.dict())

    def list_invoices(self) -> MyFinancesResponse[InvoiceList]:
        response = self._client._get(f"/invoices/")
        return MyFinancesResponse(**response.dict())

    def get_invoice(self, invoice_id: int) -> MyFinancesResponse[Invoice]:
        """
        Gathering a specific Invoice by ID

        Args:
            invoice_id (int): Invoice ID

        Returns:
                MyFinancesResponse[Client]: Invoice details
        """
        response = self._client._get(f"/invoices/{invoice_id}/")
        return MyFinancesResponse(**response.dict())

    def delete_invoice(self, invoice_id: int) -> MyFinancesResponse[Invoice]:
        """
        Delete a specific Invoice by ID

        Args:
            invoice_id (int): Invoice ID

        Returns:
            MyFinancesResponse[Invoice]: Deleting the specified Invoice
        """
        response = self._client._delete(f"/invoices/{invoice_id}/delete")
        return MyFinancesResponse(**response.dict())

    def search_invoices(self, customer_id: int = None, status: str = None) -> MyFinancesResponse[InvoiceList]:
        """
        Search for a specific Invoice by use of filters

        Args:
            customer_id (int): Customer ID
            status (str): Invoice status

        Returns:
            MyFinancesResponse[InvoiceList]: invoice list with the specified filters
        """
        params = {}

        if customer_id is not None:
            params["customer_id"] = customer_id

        if status is not None:
            params["status"] = status

        response = self._client._get(f"/invoices/search", params=params)
        return MyFinancesResponse(**response.dict())

    def update_invoice(self, customer_id: int, amount: float = None, description: str = None, due_date: str = None, status: str = None ) -> MyFinancesResponse[Invoice]:
        """
        Updating an existing Invoice

        Args:
            customer_id (int): customer's ID
            amount (float): Invoice total amount to be change
            description (str): Invoice description to be change
            due_date (str): due date of the invoice to be changed
            status (str): Invoice status to be changed

        Returns:
            MyFinancesResponse[Invoice]: updating an existing invoice's details
        """
        params = {
            key: value for key, value in{
                "amount": amount,
                "description": description,
                "due_date": due_date,
                "status": status,
            }.items() if value is not None
        }

        response = self._client._patch(f"/invoices/{customer_id}/update", json=params)
        return MyFinancesResponse(**response.dict())
