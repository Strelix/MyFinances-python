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
        response = self._client._get(f"/invoices/{invoice_id}/")
        return MyFinancesResponse(**response.dict())

    def delete_invoice(self, invoice_id: int) -> MyFinancesResponse[InvoiceList]:
        response = self._client._delete(f"/invoices/{invoice_id}/delete")
        return MyFinancesResponse(**response.dict())

    def search_invoices(self, customer_id: int = None, status: str = None) -> MyFinancesResponse[InvoiceList]:
        params = {
            "customer_id": customer_id,
            "status": status
        }

        params = {key: value for key, value in params.items() if value is not None}

        response = self._client._get(f"/invoices/search", params=params)
        return MyFinancesResponse(**response.dict())

    def update_invoice(self, invoice_id: int, amount: float = None, description: str = None, due_date: str = None ) -> MyFinancesResponse[CreateInvoiceResponse]:
        payload = {
            "amount": amount,
            "description": description,
            "due_date": due_date,
        }

        payload = {key: value for key, value in payload.items() if value is not None }

        response = self._client._post(f"/invoices/{invoice_id}/update", json=payload)
        return MyFinancesResponse(**response.dict())
