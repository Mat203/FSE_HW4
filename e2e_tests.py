import unittest
import data_procession
from datetime import datetime, timedelta

class TestEndToEnd(unittest.TestCase):
    def test_ShouldTest_AllFunctions_When_MultipleUsers(self):
        data = [
            {'userId': '1', 'isOnline': True, 'onlinePeriods': [['2023-10-09T14:14:17', '2023-10-09T15:14:17']]},
            {'userId': '2', 'isOnline': True, 'onlinePeriods': [['2023-10-09T16:14:17', '2023-10-10T16:14:17']]}
        ]
        for user in data:
            total_time = data_procession.calculate_online_time(user)
            if user['userId'] == '1':
                self.assertEqual(total_time, 3600.0)
            elif user['userId'] == '2':
                self.assertEqual(total_time, 86400.0)

            weekly_avg, daily_avg = data_procession.calculate_average_times(user)
            if user['userId'] == '1':
                self.assertEqual(weekly_avg, 3600.0 * 7)
                self.assertEqual(daily_avg, 3600.0)
            elif user['userId'] == '2':
                self.assertEqual(weekly_avg, 43200.0 * 7)
                self.assertEqual(daily_avg, 43200)

        for user in data:
            data_procession.delete_user_data(user['userId'])
            self.assertNotIn(user['userId'], data_procession.previous_state)

    def test_ShouldTest_AllFunctions_When_MultipleUsersAndMultipleOnlinePeriodds(self):
        data = [
            {'userId': '1', 'isOnline': True, 'onlinePeriods': [['2023-10-09T14:14:17', '2023-10-09T15:14:17'], ['2023-10-10T14:14:17', '2023-10-10T15:14:17']]},
            {'userId': '2', 'isOnline': True, 'onlinePeriods': [['2023-10-09T16:14:17', '2023-10-10T16:14:17'], ['2023-10-11T16:14:17', '2023-10-12T16:14:17']]}
        ]
        for user in data:
            total_time = data_procession.calculate_online_time(user)
            if user['userId'] == '1':
                self.assertEqual(total_time, 3600.0 * 2)
            elif user['userId'] == '2':
                self.assertEqual(total_time, 86400.0 * 2)

            weekly_avg, daily_avg = data_procession.calculate_average_times(user)
            if user['userId'] == '1':
                self.assertEqual(weekly_avg, 3600.0 * 7)
                self.assertEqual(daily_avg, 3600.0)
            elif user['userId'] == '2':
                self.assertEqual(weekly_avg, 43200.0 * 7)
                self.assertEqual(daily_avg, 43200.0)

        for user in data:
            data_procession.delete_user_data(user['userId'])
            self.assertNotIn(user['userId'], data_procession.previous_state)


if __name__ == '__main__':
    unittest.main()
