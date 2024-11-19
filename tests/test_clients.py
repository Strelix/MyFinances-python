import pytest
from unittest.mock import Mock

from myfinances import MyFinancesClient
from myfinances.clients.service import ClientsService


@pytest.fixture
def mock_client():
    mock = Mock(spec=MyFinancesClient)
    mock.session = Mock()
    return mock


@pytest.fixture
def clients_service(mock_client):
    return ClientsService(mock_client)


def test_create_client(clients_service, mock_client):
    clients_data = {
        "name": "John Doe",
        "phone_number": "1234567890",
        "email": "john.doe@example.com",
        "company": "Example Inc",
        "contact_method": "email",
        "is_representative": True,
        "address": "123 Main St",
        "city": "Sample City",
        "country": "Sample Country"
    }

    mock_response_data = {
        "meta": {
            "success": True,
            "status_code": 200,
            "message": "Success"
        },
        "data": {"client_id": 123}
    }

    mock_post = Mock()
    mock_post.dict.return_value = mock_response_data
    mock_client._post.return_value = mock_post

    response = clients_service.create_client(**clients_data)

    mock_client._post.assert_called_once_with("/clients/create/", clients_data)
    assert response.data["client_id"] == 123
    assert response.meta.success is True
    assert response.meta.status_code == 200
    assert response.meta.message == "Success"


def test_list_clients(clients_service, mock_client):
    clients_data = [
        {"id": 1, "name": "Client 1", "company": "Company 1", "phone_number": "1234567890",
         "email": "company1@company1.com", "contact_method": "phone", "is_representative": True, "address": "123 Main",
         "city": "Sample City", "country": "Australia"},
        {"id": 2, "name": "Client 2", "company": "Company 2", "phone_number": "0987654321",
         "email": "company2@company2.com", "contact_method": "email", "is_representative": True,
         "address": "321 Main", "city": "Sample City", "country": "South America"},
    ]

    mock_response_data = {
        "meta": {
            "success": True,
            "status_code": 200,
            "message": "Success"
        },
        "data": clients_data
    }

    mock_response = Mock()
    mock_response.dict.return_value = mock_response_data
    mock_client._get.return_value = mock_response

    response = clients_service.list_clients()

    mock_client._get.assert_called_once_with("/clients/", params={})
    assert response.meta.success is True
    assert response.meta.status_code == 200
    assert response.meta.message == "Success"

    assert isinstance(response.data, list)
    assert len(response.data) == 2
    assert response.data[0]["id"] == clients_data[0]["id"]


def test_client_by_id(clients_service, mock_client):
    clients_data = {
        "id": 1,
        "name": "Client 1",
        "company": "Company 1",
        "phone_number": "1234567890",
        "email": "company1@company1.com",
        "contact_method": "phone",
        "is_representative": True,
        "address": "123 Main",
        "city": "Sample City",
        "country": "Australia"
    }

    mock_response_data = {
        "meta": {
            "success": True,
            "status_code": 200,
            "message": "Success"
        },
        "data": clients_data
    }

    mock_response = Mock()
    mock_response.dict.return_value = mock_response_data
    mock_client._get.return_value = mock_response

    clients_id = 1
    response = clients_service.get_client(clients_id)

    mock_client._get.assert_called_once_with(f"/clients/{clients_id}")
    assert response.meta.success is True
    assert response.meta.status_code == 200
    assert response.meta.message == "Success"

    assert response.data["id"] == clients_data["id"]
    assert response.data["name"] == clients_data["name"]
    assert response.data["company"] == clients_data["company"]
    assert response.data == clients_data


def test_delete_clients(clients_service, mock_client):
    clients_data = [
        {"id": 1, "name": "Client 1", "company": "Company 1", "phone_number": "1234567890",
         "email": "company1@company1.com", "contact_method": "phone", "is_representative": True, "address": "123 Main",
         "city": "Sample City", "country": "Australia"},
        {"id": 2, "name": "Client 2", "company": "Company 2", "phone_number": "0987654321",
         "email": "company2@company2.com", "contact_method": "email", "is_representative": True,
         "address": "321 Main", "city": "Sample City", "country": "South America"},
    ]

    mock_response_data = {
        "meta": {
            "success": True,
            "status_code": 200,
            "message": "Success"
        },
        "data": clients_data
    }

    mock_response = Mock()
    mock_response.dict.return_value = mock_response_data
    mock_client._delete.return_value = mock_response

    Client_Id = 1
    response = clients_service.delete_client(Client_Id)

    mock_client._delete.assert_called_once_with(f"/clients/{Client_Id}/delete")
    assert response.meta.success is True
    assert response.meta.status_code == 200
    assert response.meta.message == "Success"

    remaining_clients = [clients for clients in clients_data if clients["id"] == Client_Id]
    assert len(remaining_clients) == 1
    assert remaining_clients[0]["id"] == Client_Id


def test_update_clients_name(clients_service, mock_client):
    clients_data = {
        "id": 1,
        "name": "Client 1",
        "company": "Company 1",
        "phone_number": "1234567890",
        "email": "company1@company1.com",
        "contact_method": "phone",
        "is_representative": True,
        "address": "123 Main",
        "city": "Sample City",
        "country": "Australia"
    }

    mock_response_data = {
        "meta": {
            "success": True,
            "status_code": 200,
            "message": "Success"
        },
        "data": clients_data
    }

    mock_response = Mock()
    mock_response.dict.return_value = mock_response_data
    mock_client._patch.return_value = mock_response

    new_name = "Client 3"
    response = clients_service.update_client(name=new_name)

    mock_client._patch.assert_called_once_with(f"/clients/update/", json={"name": new_name})
    assert response.meta.success is True
    assert response.meta.status_code == 200
    assert response.meta.message == "Success"

    # Updated Version
    updated_clients_data = {
        "id": 1,
        "name": "Client 3",
        "company": "Company 1",
        "phone_number": "1234567890",
        "email": "company1@company1.com",
        "contact_method": "phone",
        "is_representative": True,
        "address": "123 Main",
        "city": "Sample City",
        "country": "Australia"
    }

    mock_get_response_data = {
        "meta": {
            "success": True,
            "status_code": 200,
            "message": "Success"
        },
        "data": updated_clients_data
    }

    mock_get_response = Mock()
    mock_get_response.dict.return_value = mock_get_response_data
    mock_client._get.return_value = mock_get_response

    get_response = clients_service.get_client(1)
    mock_client._get.assert_called_once_with(f"/clients/1")
    assert get_response.data["name"] == "Client 3"
