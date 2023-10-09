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

class TestCalculateOnlineTime(unittest.TestCase):
    def test_Should_ReturnTotalSecondsOnline_When_CalculateOnlineTimeCalled(self):
        user = {'userId': '1', 'isOnline': True, 'onlinePeriods': [['2023-10-09T14:14:17', '2023-10-09T15:14:17']]}
        result = data_procession.calculate_online_time(user)
        self.assertEqual(result, 3600)

class TestCalculateDays(unittest.TestCase):
    def test_Should_ReturnTotalDays_When_CalculateDaysCalled(self):
        user = {'userId': '1', 'isOnline': True, 'onlinePeriods': [['2023-10-09T14:14:17', '2023-10-10T15:14:17']]}
        result = data_procession.calculate_days(user)
        self.assertEqual(result, 2)

class TestCalculateAverageTimes(unittest.TestCase):
    def test_Should_ReturnWeeklyAndDailyAverage_When_CalculateAverageTimesCalled(self):
        user = {'userId': '1', 'isOnline': True, 'onlinePeriods': [['2023-10-09T14:14:17', '2023-10-10T15:14:17']]}
        weekly_average, daily_average = data_procession.calculate_average_times(user)
        self.assertEqual(weekly_average, 315000.0)
        self.assertEqual(daily_average, 45000.0)

if __name__ == "__main__":
    unittest.main()
