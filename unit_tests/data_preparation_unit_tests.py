import unittest
from unittest.mock import patch, MagicMock
import data_procession
from datetime import datetime

class TestUpdateUserData(unittest.TestCase):
    def test_Should_UpdateUserData_When_UserIsOnline(self):
        user = {'userId': '1', 'isOnline': True}
        previous_state = {'1': {'userId': '1', 'isOnline': False, 'onlinePeriods': []}}
        result = data_procession.update_user_data(user, previous_state)
        self.assertIsNotNone(result['onlinePeriods'][0][0])
        self.assertIsNone(result['onlinePeriods'][0][1])

    def test_Should_UpdateUserData_When_UserIsOffline(self):
        user = {'userId': '1', 'isOnline': False}
        previous_state = {'1': {'userId': '1', 'isOnline': True, 'onlinePeriods': [['2023-10-09T14:14:17', None]]}}
        result = data_procession.update_user_data(user, previous_state)
        self.assertIsNotNone(result['onlinePeriods'][0][1])

    def test_Should_KeepOnlinePeriods_When_UserStaysOnline(self):
        user = {'userId': '1', 'isOnline': True}
        previous_state = {'1': {'userId': '1', 'isOnline': True, 'onlinePeriods': [['2023-10-09T14:14:17', None]]}}
        result = data_procession.update_user_data(user, previous_state)
        self.assertEqual(result['onlinePeriods'], previous_state['1']['onlinePeriods'])

    def test_Should_KeepOnlinePeriods_When_UserStaysOffline(self):
        user = {'userId': '1', 'isOnline': False}
        previous_state = {'1': {'userId': '1', 'isOnline': False, 'onlinePeriods': [['2023-10-09T14:14:17', '2023-10-09T15:14:17']]}}
        result = data_procession.update_user_data(user, previous_state)
        self.assertEqual(result['onlinePeriods'], previous_state['1']['onlinePeriods'])

    @patch('data_procession.get_data')
    def test_ShouldFetch_and_update_data_When_MultipleUsers(self, mock_get_data):
        user1_id = '1'
        user1 = {'userId': user1_id, 'isOnline': True, 'lastSeenDate': datetime.now().isoformat()}
        user2_id = '2'
        user2 = {'userId': user2_id, 'isOnline': True, 'lastSeenDate': datetime.now().isoformat()}
        mock_get_data.return_value = [user1, user2]

        data_procession.fetch_and_update_data()

        self.assertEqual(len(data_procession.previous_state), 2)
        self.assertIn(user1_id, data_procession.previous_state)
        self.assertIn(user2_id, data_procession.previous_state)


unittest.main()