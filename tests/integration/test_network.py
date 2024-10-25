import unittest
import requests
from unittest.mock import patch

class TestNetworkInteractions(unittest.TestCase):
    BASE_URL = "http://localhost:5000/api"  # Example API base URL

    @patch('requests.get')
    def test_get_data(self, mock_get):
        """Test the GET request to fetch data."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"data": "sample data"}

        response = requests.get(f"{self.BASE_URL}/data")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"data": "sample data"})

    @patch('requests.post')
    def test_post_data(self, mock_post):
        """Test the POST request to send data."""
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {"message": "Data created"}

        response = requests.post(f"{self.BASE_URL}/data", json={"data": "new data"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"message": "Data created"})

if __name__ == '__main__':
    unittest.main()
