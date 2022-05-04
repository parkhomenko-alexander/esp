def test_user_bp_index_with_fixture(test_client):
    response = test_client.get('/user/')
    data = response.data.decode("utf-8")
    assert response.status_code == 200
    assert 'Система мониторинга параметров воздуха' in data

def test_user_bp_login_with_fixture(test_client):
    response = test_client.get('/user/login')
    data = response.data.decode("utf-8")
    assert response.status_code == 200
    assert 'Войти' in data


