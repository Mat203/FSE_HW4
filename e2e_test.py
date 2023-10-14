import pytest
import requests
import json
from unittest.mock import patch

BASE_URL = 'http://127.0.0.1:5000' 

from unittest.mock import patch

@patch('data_procession.calculate_online_time')
@patch('data_procession.update_user_data')
def test_ShouldCalculateOnlineTime_When_WeGetAPI(mock_update_user_data, mock_calculate_online_time):
    user = {'userId': '1', 'onlinePeriods': [['2023-10-14T18:27:57', None]]}
    previous_state = {}
    mock_update_user_data.return_value = user, previous_state
    mock_calculate_online_time.return_value = 1000

    userId = '1'
    response = requests.get(f'{BASE_URL}/api/stats/user/online_time?userId={userId}')

    assert response.status_code == 200
    data = response.json()
    assert 'onlineTime' in data
    assert data['onlineTime'] == 1000


if __name__ == "__main__":
    pytest.main()
