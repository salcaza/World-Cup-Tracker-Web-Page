import unittest
from unittest.mock import mock_open, patch
import json
from football_api import find_stadium, get_team_schedule
from news_api import get_news


class TestSchedule(unittest.TestCase):

    # Patch is used to prevent real API call
    @patch('football_api.save_stadium_json')
    def test_find_stadium(self, mock_json):

        fake_stadium_data = {
            "stadiums": [
                {"id": "1", "name_en": "Azteca Stadium", "city_en": "Mexico City"},
                {"id": "2", "name_en": "MetLife Stadium", "city_en": "New York"}
            ]
        }

        # fake data that copies the same structure as real
        fake_file_content = json.dumps(fake_stadium_data)

        # mock the open function
        with patch('football_api.open', mock_open(read_data=fake_file_content)):
            result = find_stadium("1")
            self.assertEqual(result, ("Azteca Stadium", "Mexico City"))

    # use patch to prevent real save_news api call
    @patch("news_api.save_news")
    def test_get_news(self, mock_save):
        # dump empty article data into a file for testing
        fake_file_data = json.dumps({"articles": []})

        # mock the open function and reads the fake data instead of real file
        with patch("news_api.open", mock_open(read_data=fake_file_data)):
            result = get_news("Haiti")
        
        self.assertEqual(result, [])

    
    @patch("football_api.save_schedule_json")
    def test_get_team_schedule(self, mock_save_schedule):

        fake_schedule = json.dumps({"games" : []})

        with patch("football_api.open", mock_open(read_data = fake_schedule)):
            result = get_team_schedule("Mexico")

            self.assertEqual(result, [])




if __name__ == "__main__":
    unittest.main()



