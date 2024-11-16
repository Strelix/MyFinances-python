import pytest
from unittest.mock import Mock

from myfinances import MyFinancesClient
from myfinances.clients.service import ClientsService
from myfinances.clients.models import ClientIdResponse, ClientData


@pytest.fixture
def mock_client():
    mock = Mock(spec=MyFinancesClient)
    mock.session = Mock()
    return mock


@pytest.fixture
def clients_service(mock_client):
    return ClientsService(mock_client)


def test_create_client(clients_service, mock_client):
    # Arrange: Prepare the client data and mock the response
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

    # Updated mock response structure with both `meta` and `data` fields
    mock_response_data = {
        "meta": {
            "success": True,
            "status_code": 200,
            "message": "Success"
        },  # Include the meta field
        "data": {"client_id": 123}
    }

    # Mock the _post method to return a mock response object
    mock_post = Mock()
    mock_post.dict.return_value = mock_response_data
    mock_client._post.return_value = mock_post

    # Act: Call the method you're testing
    response = clients_service.create_client(**clients_data)

    # Assert: Ensure the correct API call was made
    mock_client._post.assert_called_once_with("/clients/create/", clients_data)
    assert response.data["client_id"] == 123
    assert response.meta.success is True
    assert response.meta.status_code == 200
    assert response.meta.message == "Success"
