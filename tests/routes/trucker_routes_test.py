import json
import pytest
import unittest
from bson import ObjectId

from tests import setup
from api.models.trucker import TruckerModel

app = setup.create_flask_app()


class TruckerRoutesTest(unittest.TestCase):

    @pytest.mark.usefixtures('fixture_trucker_post_body')
    def test_1_route_create_trucker(self):
        with app.test_client() as c:
            response = c.post('/trucker', json=json.loads(self.trucker_post_body))
            response_bad_request = c.post('/trucker', json={})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_bad_request.status_code, 400)

    @pytest.mark.usefixtures('fixture_trucker_document', 'fixture_trucker_update_body')
    def test_2_route_update_trucker(self):
        with app.test_client() as c:
            response = c.patch('/trucker/{}'.format(self.trucker._id), json=json.loads(self.trucker_update_body))
            response_bad_request_due_to_invalid_id = c.put('/trucker/{}'.format('0'), json={})
            response_not_found = c.put('/trucker/{}'.format(str(ObjectId())), json={})
            response_bad_request_due_to_invalid_body = c.put('/trucker/{}'.format(self.trucker._id), json={'name': 1})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_bad_request_due_to_invalid_id.status_code, 400)
        self.assertEqual(response_not_found.status_code, 404)
        self.assertEqual(response_bad_request_due_to_invalid_body.status_code, 400)

    @pytest.mark.usefixtures('fixture_trucker_document')
    def test_3_route_get_trucker(self):
        with app.test_client() as c:
            response = c.get('/trucker/{}'.format(self.trucker._id))
            response_bad_request_due_to_invalid_id = c.get('/trucker/{}'.format('0'))
            response_not_found = c.get('/trucker/{}'.format(str(ObjectId())), json={})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_bad_request_due_to_invalid_id.status_code, 400)
        self.assertEqual(response_not_found.status_code, 404)

    @pytest.mark.usefixtures('fixture_trucker_document')
    def test_4_route_delete_trucker(self):
        with app.test_client() as c:
            response = c.delete('/trucker/{}'.format(self.trucker._id))
            response_bad_request_due_to_invalid_id = c.delete('/trucker/{}'.format('0'))
            response_not_found = c.delete('/trucker/{}'.format(str(ObjectId())), json={})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_bad_request_due_to_invalid_id.status_code, 400)
        self.assertEqual(response_not_found.status_code, 404)

    @pytest.fixture(scope="function")
    def fixture_trucker_post_body(request):
        request.trucker_post_body = setup.read_fixture_file('trucker_post_body.json')

    @pytest.fixture(scope="function")
    def fixture_trucker_update_body(request):
        request.trucker_update_body = setup.read_fixture_file('trucker_update_body.json')

    @pytest.fixture(scope="function")
    def fixture_trucker_document(request):
        request.trucker = TruckerModel.create_trucker(json.loads(setup.read_fixture_file('trucker_post_body.json')))


if __name__ == '__main__':
    unittest.main()
