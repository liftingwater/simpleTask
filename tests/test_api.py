def test_hello_world(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Hello, World!' in response.data


def test_create_ticket(client):
    response = client.post('/tickets', json={
        'title': 'Test Ticket',
        'description': 'Test Description',
        'status': 'todo'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == 'Test Ticket'
    assert data['description'] == 'Test Description'
    assert data['status'] == 'todo'
    assert 'id' in data
    assert 'created_at' in data


def test_get_tickets(client):
    # Create a ticket first
    client.post('/tickets', json={
        'title': 'Test Ticket',
        'description': 'Test Description',
        'status': 'todo'
    })
    
    response = client.get('/tickets')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_single_ticket(client):
    # Create a ticket first
    create_response = client.post('/tickets', json={
        'title': 'Test Ticket',
        'description': 'Test Description',
        'status': 'todo'
    })
    ticket_id = create_response.get_json()['id']
    
    response = client.get(f'/tickets/{ticket_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == ticket_id
    assert data['title'] == 'Test Ticket'


def test_update_ticket(client):
    # Create a ticket first
    create_response = client.post('/tickets', json={
        'title': 'Test Ticket',
        'description': 'Test Description',
        'status': 'todo'
    })
    ticket_id = create_response.get_json()['id']
    
    response = client.put(f'/tickets/{ticket_id}', json={
        'title': 'Updated Ticket',
        'status': 'done'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'Updated Ticket'
    assert data['status'] == 'done'


def test_delete_ticket(client):
    # Create a ticket first
    create_response = client.post('/tickets', json={
        'title': 'Test Ticket',
        'description': 'Test Description',
        'status': 'todo'
    })
    ticket_id = create_response.get_json()['id']
    
    response = client.delete(f'/tickets/{ticket_id}')
    assert response.status_code == 204
    
    # Verify it's deleted
    get_response = client.get(f'/tickets/{ticket_id}')
    assert get_response.status_code == 404


def test_get_nonexistent_ticket(client):
    response = client.get('/tickets/999')
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data

