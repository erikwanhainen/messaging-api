def test_send_message(client):
    message_data = {
        "recipient": "user@example.com",
        "content": "Hello",
    }

    response = client.post("/messages/", json=message_data)

    assert response.status_code == 200
    data = response.json()
    assert data["recipient"] == "user@example.com"
    assert data["content"] == "Hello"
    assert data["read"] is False
    assert "id" in data
    assert "created_at" in data


def test_get_unread_messages(client, create_message):
    recipient = "user@example.com"
    msg1 = create_message(recipient=recipient, content="Message 1", read=False)
    msg2 = create_message(recipient=recipient, content="Message 2", read=False)
    msg3 = create_message(recipient=recipient, content="Message 3", read=True)

    response = client.get(
        "/messages/unread/", params={"recipient": recipient, "offset": 0, "limit": 3}
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["id"] == str(msg2.id)
    assert data[0]["recipient"] == recipient
    assert data[0]["content"] == "Message 2"
    assert data[1]["id"] == str(msg1.id)
    assert data[1]["recipient"] == recipient
    assert data[1]["content"] == "Message 1"


def test_mark_messages_as_read(client, create_message):
    recipient = "user@example.com"
    message = create_message(
        recipient="user@example.com",
        content="Message to be marked as read",
        read=False,
    )

    response = client.patch(
        "/messages/mark-read", json={"message_ids": [str(message.id)]}
    )

    assert response.status_code == 204

    unread_response = client.get(
        "/messages/unread/", params={"recipient": recipient, "offset": 0, "limit": 3}
    )
    unread_messages = unread_response.json()
    assert len(unread_messages) == 0


def test_get_messages_with_pagination(client, create_message):
    recipient = "user@example.com"
    msg1 = create_message(recipient=recipient, content="Message 1")
    msg2 = create_message(recipient=recipient, content="Message 2")
    msg3 = create_message(recipient=recipient, content="Message 3")

    response = client.get(
        "/messages/", params={"recipient": recipient, "offset": 0, "limit": 2}
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["id"] == str(msg3.id)
    assert data[0]["recipient"] == recipient
    assert data[0]["content"] == "Message 3"
    assert data[1]["id"] == str(msg2.id)
    assert data[1]["recipient"] == recipient
    assert data[1]["content"] == "Message 2"


def test_delete_single_message(client, create_message):
    recipient = "user@example.com"
    message = create_message(recipient=recipient, content="Message to be deleted")

    response = client.delete(f"/messages/{message.id}")

    assert response.status_code == 204

    get_response = client.get("/messages/", params={"recipient": recipient})
    messages = get_response.json()
    assert len(messages) == 0


def test_delete_multiple_messages(client, create_message):
    recipient = "user@example.com"
    message1 = create_message(recipient=recipient, content="Message to delete 1")
    message2 = create_message(recipient=recipient, content="Message to delete 2")
    message_ids = [str(message1.id), str(message2.id)]

    response = client.request(
        "DELETE", "/messages/bulk", json={"message_ids": message_ids}
    )

    assert response.status_code == 204

    get_response = client.get("/messages/", params={"recipient": recipient})
    remaining_messages = get_response.json()
    assert len(remaining_messages) == 0


def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"
