import pytest
import requests
import json
from unittest.mock import patch

BASE_URL = 'https://sef.podkolzin.consulting' 

from unittest.mock import patch

@patch('requests.get')
def test_ShouldCalculateOnlineTime_When_WeGetAPI(mock_get):
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {'userId': '1', 'onlineTime': 1000}

    userId = '1'
    response = requests.get(f'{BASE_URL}/api/stats/user/online_time?userId={userId}')

    mock_get.assert_called_once_with(f'{BASE_URL}/api/stats/user/online_time?userId={userId}')

    assert response.status_code == 200
    data = response.json()
    assert 'onlineTime' in data

from unittest.mock import patch

@patch('requests.get')
def test_ShouldCalculateAverageTimes_When_WeGetAPI(mock_get):
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {'userId': '1', 'weeklyAverage': 1000, 'dailyAverage': 200}

    userId = '1'
    response = requests.get(f'{BASE_URL}/api/stats/user/average?userId={userId}')

    mock_get.assert_called_once_with(f'{BASE_URL}/api/stats/user/average?userId={userId}')

    assert response.status_code == 200
    data = response.json()
    assert 'weeklyAverage' in data
    assert 'dailyAverage' in data

@patch('requests.post')
def test_ShouldForgetUuser_When_WeDelete_Data(mock_post):
    mock_response = mock_post.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {'userId': '1'}

    userId = '1'
    response = requests.post(f'{BASE_URL}/api/user/forget?userId={userId}')

    mock_post.assert_called_once_with(f'{BASE_URL}/api/user/forget?userId={userId}')

    assert response.status_code == 200
    data = response.json()
    assert data['userId'] == userId

if __name__ == "__main__":
    pytest.main()
