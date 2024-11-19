import pytest
from unittest.mock import Mock
from myfinances import MyFinancesClient
from myfinances.finance.invoices import InvoicesService


@pytest.fixture
def mock_client():
    mock = Mock(spec=MyFinancesClient)
    mock.session = Mock()
    return mock

@pytest.fixture
def invoices_service(mock_client):
    return InvoicesService(mock_client)


def test_create_invoice(invoices_service, mock_client):
    new_invoice_data ={
        "customer_id": 123,
        "amount": 100,
        "description": "Data Analytics service",
        "due_date": "2020-05-21"
    }

    mock_response_data = {
        "meta": {
            "success": True,
            "status_code": 200,
            "message": "Successfully created"
        },
        "data": {
            "invoice_id": 102,
        }
    }

    mock_post = Mock()
    mock_post.dict.return_value = mock_response_data
    mock_client._post.return_value = mock_post

    response = invoices_service.create_invoice(**new_invoice_data)

    mock_client._post.assert_called_once_with("/invoices/create", json=new_invoice_data)
    assert response.data["invoice_id"] == 102
    assert response.meta.success is True
    assert response.meta.status_code == 200
    assert response.meta.message == "Successfully created"


def test_list_invoices(invoices_service, mock_client):

    invoice_list = [
        {"id": 1, "customer_id": 123, "amount": 250.0, "description": "Service Fee", "status": "pending"},
        {"id": 2, "customer_id": 124, "amount": 300.0, "description": "Consulting Fee", "status": "pending"}
    ]

    mock_response_data = {
        "meta": {
            "success": True,
            "status_code": 200,
            "message": "Successfully fetched invoices"
        },
        "data": invoice_list
    }

    mock_response = Mock()
    mock_response.dict.return_value = mock_response_data
    mock_client._get.return_value = mock_response

    response = invoices_service.list_invoices()

    mock_client._get.assert_called_once_with("/invoices/")

    assert response.meta.success is True
    assert response.meta.status_code == 200
    assert response.meta.message == "Successfully fetched invoices"

    assert isinstance(response.data, list)
    assert len(response.data) == 2
    assert response.data[0]["id"] == 1
    assert response.data[1]["amount"] == 300.0
    assert response.data[0]["status"] == "pending"
    assert response.data[1]["status"] == "pending"


def test_delete_invoice(invoices_service, mock_client):
    invoice_list = [
        {"id": 1, "customer_id": 123, "amount": 250.0, "description": "Service Fee", "status": "pending"},
        {"id": 2, "customer_id": 124, "amount": 300.0, "description": "Consulting Fee", "status": "pending"}
    ]

    mock_response_data = {
        "meta": {
            "success": True,
            "status_code": 200,
            "message": "Successfully deleted invoice"
        },
        "data": invoice_list
    }

    mock_response = Mock()
    mock_response.dict.return_value = mock_response_data

    mock_client._delete.return_value = mock_response

    invoice_id = 1

    response = invoices_service.delete_invoice(invoice_id)

    mock_client._delete.assert_called_once_with(f"/invoices/{invoice_id}/delete")

    assert response.meta.success is True
    assert response.meta.status_code == 200
    assert response.meta.message == "Successfully deleted invoice"

    remaining_invoices = [invoice for invoice in invoice_list if invoice['id'] != invoice_id]

    assert len(remaining_invoices) == 1
    assert remaining_invoices[0]['id'] == 2


def test_get_invoice(invoices_service, mock_client):
    invoice_data = {
        "id": 2,
        "customer_id": 124,
        "amount": 300.0,
        "description": "Consulting Fee",
        "status": "pending"
    }

    mock_response_data = {
        "meta": {
            "success": True,
            "status_code": 200,
            "message": "Successfully deleted invoice"
        },
        "data": invoice_data
    }

    mock_response = Mock()
    mock_response.dict.return_value = mock_response_data
    mock_client._get.return_value = mock_response

    invoice_id = 2
    response = invoices_service.get_invoice(invoice_id)

    mock_client._get.assert_called_once_with(f"/invoices/{invoice_id}/")

    assert response.meta.success is True
    assert response.meta.status_code == 200
    assert response.meta.message == "Successfully deleted invoice"

    assert response.data["id"] == invoice_data["id"]
    assert response.data["customer_id"] == invoice_data["customer_id"]
    assert response.data["amount"] == invoice_data["amount"]
    assert response.data["description"] == invoice_data["description"]
    assert response.data["status"] == invoice_data["status"]


def test_search_invoices_by_id(invoices_service, mock_client):
    invoice_data = [
        {"id": 1, "customer_id": 123, "amount": 300.0, "description": "Analytics Consultant", "status": "pending"},
        {"id": 2, "customer_id": 124, "amount": 150.0, "description": "Service fee", "status": "paid"}
    ]

    mock_response_data = {
        "meta": {
            "success": True,
            "status_code": 200,
            "message": "Invoices fetched successfully"
        },
        "data": invoice_data
    }

    mock_response = Mock()
    mock_response.dict.return_value = mock_response_data
    mock_client._get.return_value = mock_response

    customer_id = 124

    response = invoices_service.search_invoices(customer_id)
    mock_client._get.assert_called_once_with(f"/invoices/search", params={"customer_id": customer_id})

    assert response.meta.success is True
    assert response.meta.status_code == 200
    assert response.meta.message == "Invoices fetched successfully"

    assert response.data[1]["id"] == 2
    assert response.data[1]["customer_id"] == 124


def test_update_invoice(invoices_service, mock_client):
    invoice_data = {
        "id": 1,
        "customer_id": "125",
        "amount": 100,
        "description": "Service fees",
        "due_date": "2024-12-31",
        "status": "pending"
    }

    mock_response_data = {
        "meta": {
            "success": True,
            "status_code": 200,
            "message": "Invoices successfully updated"
        },
        "data": invoice_data
    }

    mock_response = Mock()
    mock_response.dict.return_value = mock_response_data
    mock_client._patch.return_value = mock_response

    new_status = "paid"

    response = invoices_service.update_invoice(1, status=new_status)

    mock_client._patch.assert_called_once_with(f"/invoices/1/update", json={"status": new_status})

    assert response.meta.success is True
    assert response.meta.status_code == 200
    assert response.meta.message == "Invoices successfully updated"

    # updated version
    updated_invoice_data = {
        "id": 1,
        "customer_id": "125",
        "amount": 100,
        "description": "Service fees",
        "due_date": "2024-12-31",
        "status": "paid"
    }

    mock_get_response_data = {
        "meta": {
            "success": True,
            "status_code": 200,
            "message": "Invoice fetched successfully"
        },
        "data": updated_invoice_data
    }

    mock_get_response = Mock()
    mock_get_response.dict.return_value = mock_get_response_data
    mock_client._get.return_value = mock_get_response

    get_response = invoices_service.get_invoice(1)
    mock_client._get.assert_called_once_with(f"/invoices/1/")
    assert get_response.data["status"] == "paid"
