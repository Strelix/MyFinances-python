import pytest
from unittest.mock import Mock
from myfinances import MyFinancesClient
from myfinances.finance.receipts.service import ReceiptService


@pytest.fixture
def mock_client():
    mock = Mock(spec=MyFinancesClient)
    mock.session = Mock()
    return mock


@pytest.fixture
def receipts_service(mock_client):
    return ReceiptService(mock_client)


def test_create_receipt(receipts_service, mock_client):
    receipts_data = {
        "name": "Client  1",
        "image": "file_example",
        "date": "2024-05-21",
        "merchant_store": "Store 1",
        "purchase_category": "Purchase 1",
        "total_amount": 500,
        "owner": "Client  2"
    }

    mock_response_data = {
        "meta": {
            "success": True,
            "status_code": 200,
        },
        "data": receipts_data
    }

    mock_post = Mock()
    mock_post.dict.return_value = mock_response_data
    mock_client._post.return_value = mock_post

    response = receipts_service.create_receipt(**receipts_data)

    mock_client._post.assert_called_once_with("/receipts/create/", json=receipts_data)
    assert response.meta.success is True
    assert response.meta.status_code == 200

    assert response.data["name"] == receipts_data["name"]
    assert response.data["image"] == receipts_data["image"]


def test_list_receipts(receipts_service, mock_client):
    list_of_receipts = [
        {"id": 1, "name": "Client  1", "image": "file_example", "date": "2024-05-21",
         "merchant_store": "Store 1", "purchase_category": "Purchase 1", "total_amount": 100, "owner": "Owner 1"},
        {"id": 2, "name": "Client  2", "image": "file1_example", "date": "2024-03-21",
         "merchant_store": "Store 2", "purchase_category": "Purchase 2", "total_amount": 245, "owner": "Owner 2"}
    ]

    mock_response_data = {
        "meta": {
            "success": True,
            "status_code": 200,
        },
        "data": list_of_receipts
    }

    mock_response = Mock()
    mock_response.dict.return_value = mock_response_data
    mock_client._get.return_value = mock_response

    response = receipts_service.list_receipts()
    mock_client._get.assert_called_once_with("/receipts/")
    assert response.meta.success is True
    assert response.meta.status_code == 200

    assert isinstance(response.data, list)
    assert len(response.data) == 2


def test_delete_receipt(receipts_service, mock_client):
    list_of_receipts = [
        {"id": 1, "name": "Client  1", "image": "file_example", "date": "2024-05-21",
         "merchant_store": "Store 1", "purchase_category": "Purchase 1", "total_amount": 100, "owner": "Owner 1"},
        {"id": 2, "name": "Client  2", "image": "file1_example", "date": "2024-03-21",
         "merchant_store": "Store 2", "purchase_category": "Purchase 2", "total_amount": 245, "owner": "Owner 2"}
    ]

    mock_response_data = {
        "meta": {
            "success": True,
            "status_code": 200,
        },
        "data": list_of_receipts
    }

    mock_response = Mock()
    mock_response.dict.return_value = mock_response_data

    mock_client._delete = Mock(return_value=mock_response)

    receipt_id = 2

    response = receipts_service.delete_receipt(receipt_id)

    mock_client._delete.assert_called_once_with(f"/receipts/{receipt_id}/delete")

    assert response.meta.success is True
    assert response.meta.status_code == 200

    remaining_receipts = [receipt for receipt in list_of_receipts if receipt["id"] != receipt_id]
    assert len(remaining_receipts) == 1
    assert remaining_receipts[0]["id"] == 1


def test_update_receipt(receipts_service, mock_client):
    list_of_receipts = [
        {"id": 1, "name": "Client  1", "image": "file_example", "date": "2024-05-21",
         "merchant_store": "Store 1", "purchase_category": "Purchase 1", "total_amount": 100, "owner": "Owner 1"},
        {"id": 2, "name": "Client 2", "image": "file1_example", "date": "2024-03-21",
         "merchant_store": "Store 2", "purchase_category": "Purchase 2", "total_amount": 245, "owner": "Owner 2"}
    ]

    mock_response_data = {
        "meta": {
            "success": True,
            "status_code": 200,
        },
        "data": list_of_receipts
    }

    mock_response = Mock()
    mock_response.dict.return_value = mock_response_data
    mock_client._get.return_value = mock_response

    search_name = "Client 2"
    response = receipts_service.search_receipts(name=search_name)
    mock_client._get.assert_called_once_with("/receipts/search/", params={"name": search_name})

    assert response.meta.success is True
    assert response.meta.status_code == 200

    assert response.data[1]["name"] == search_name
