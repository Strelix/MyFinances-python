from typing import Optional

from pydantic import EmailStr

from myfinances.base_service import BaseService
from myfinances.clients.models import ClientIdResponse, ClientData, Client
from myfinances.models import MyFinancesResponse


class ClientsService(BaseService):
    def list_clients(
            self,
            order_by: Optional[str] = None,
            search: Optional[str] = None
    ) -> MyFinancesResponse[ClientData]:
        """List clients under the specified team."""
        params = {}
        if order_by:
            params["order_by"] = order_by
        if search:
            params["search"] = search

        response = self._client._get("/clients/", params=params)
        return MyFinancesResponse(**response.dict())

    def create_client(
            self,
            name: str,
            phone_number: Optional[str] = None,
            email: Optional[EmailStr] = None,
            company: Optional[str] = None,
            contact_method: Optional[str] = None,
            is_representative: bool = False,
            address: Optional[str] = None,
            city: Optional[str] = None,
            country: Optional[str] = None
    ) -> MyFinancesResponse[ClientIdResponse]:
        """List clients under the specified team."""
        params = {
            "name": name,
            "phone_number": phone_number,
            "email": email,
            "company": company,
            "contact_method": contact_method,
            "is_representative": is_representative,
            "address": address,
            "city": city,
            "country": country,
        }

        response = self._client._post("/clients/create/", json=params)

        return MyFinancesResponse(**response.dict())

    def get_client(self, client_id: int) -> MyFinancesResponse[Client]:
        response = self._client._get(f"/clients/{client_id}")
        return MyFinancesResponse(**response.dict())

    def update_client(self,
                      name: str = None,
                      phone_number: Optional[str] = None,
                      email: Optional[EmailStr] = None,
                      company: Optional[str] = None,
                      contact_method: Optional[str] = None,
                      is_representative: bool = None,
                      address: Optional[str] = None,
                      city: Optional[str] = None,
                      country: Optional[str] = None) -> MyFinancesResponse[Client]:
        params = {}

        if name is not None:
            params["name"] = name

        if phone_number is not None:
            params["phone_number"] = phone_number

        if email is not None:
            params["email"] = email

        if company is not None:
            params["company"] = company

        if contact_method is not None:
            params["contact_method"] = contact_method

        if is_representative is not None:
            params["is_representative"] = is_representative

        if address is not None:
            params["address"] = address

        if city is not None:
            params["city"] = city

        if country is not None:
            params["country"] = country

        response = self._client._patch("/clients/update/", json=params)
        return MyFinancesResponse(**response.dict())

    def delete_client(self, client_id: int) -> MyFinancesResponse[Client]:
        response = self._client._delete(f"/clients/{client_id}/delete")
        return MyFinancesResponse(**response.dict())
