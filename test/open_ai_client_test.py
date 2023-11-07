import unittest
from unittest.mock import patch
from open_ai_client import open_ai_client

class TestOpenAPIClient(unittest.TestCase):

    def setUp(self):
        self.api_key = 1.0# "TEST_API_KEY"
        self.client = open_ai_client.OpenAIClient(api_key = self.api_key, model =  "das model")

    @patch('requests.post')
    def test_generate_chat_completion_success(self, mock_post):
        mock_response = {
            "status_code": 200,
            "json.return_value": {
                "choices": [{"message": {"content": "Mocked response"}}]
            }
        }
        mock_post.return_value = unittest.mock.Mock(**mock_response)

        prompt = "What is the nutricional value of a Banana 🍌?"
        response = self.client.generate_chat_completion(prompt)

       
        _, kwargs = mock_post.call_args
        
        self.assertTrue('Banana' in kwargs["data"], "The prompt should be passed to the API")
        self.assertTrue('"temperature": 0.7' in kwargs["data"], "Temperature should be passed to the API")
        self.assertTrue('"model": "das model"' in kwargs["data"], "Model should be passed to the API")

        self.assertEqual(response, "Mocked response")


if __name__ == '__main__':
    unittest.main()