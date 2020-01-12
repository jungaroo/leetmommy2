from app import app
import unittest


class IntegrationAppTest(unittest.TestCase):
    """Tests Flask app routes"""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_ping(self):
        """Make sure that we can ping"""
        result = self.client.get('/')

        self.assertEqual(result.status_code, 200)

    def test_scraper(self):
        """Make sure that we can scrape data into test database"""

        result = self.client.post('/scrape', data={
            'cohort': 'r11',
        })

        self.assertEqual(result.status_code, 200)

    def test_search(self):
        """Make sure that we can search for fake data"""
        
        result = self.client.post('/search', data={
            'cohort': 'r11',
        })

        self.assertEqual(result.status_code, 200)

    def test_autocomplete(self):
        """Make sure we get autocomplete """

        result = self.client.post('/autocomplete', data={
            'cohort': 'r11',
        })

        self.assertEqual(result.status_code, 200)
