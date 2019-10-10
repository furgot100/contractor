from unittest import TestCase, main as unittest_main, mock
from app import app
from bson.objectid import ObjectId

sample_player_id = ObjectId('5d9cf5a7a2e0b9c1dbdc5d59')
sample_player = {
    'name' : 'Cam newton',
    'position' : 'QB',
    'image_url' : 'https://i.kym-cdn.com/photos/images/facebook/001/281/636/d84.jpg'
}

sample_form_data = {
    'name' : sample_player['name'],
    'position' : sample_player['position'],
    'image_url' : sample_player['image_url']
}

class ConstructorTests(TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
    
    def test_index(self):
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Player', result.data)

    def test_new(self):
        result = self.client.get('/new')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'New Player', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_player(self, mock_find):
        mock_find.return_value = sample_player

        result = self.client.get(f'/player/{sample_player_id}')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Cam newton', result.data)
    
    @mock.patch('pymongo.collection.Collection.find_one')
    def test_edit_player(self, mock_find):
        mock_find.return_value = sample_player

        result = self.client.get(f'/edit/{sample_player_id}')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Cam newton', result.data)

    @mock.patch('pymongo.collection.Collection.insert_one')
    def test_submit_player(self, mock_insert):
        result = self.client.post('/new', data=sample_form_data)
        self.assertEqual(result.status, '302 FOUND')
        mock_insert.assert_called_with(sample_player)

    @mock.patch('pymongo.collection.Collection.delete_one')
    def test_delete_player(self, mock_delete):
        form_data = {'_method': 'DELETE'}
        result = self.client.post(f'/delete/{sample_player_id}', data=form_data)
        self.assertEqual(result.status, '302 FOUND')
        mock_delete.assert_called_with({'_id': sample_player_id})


if __name__ == '__main__':
    unittest_main()