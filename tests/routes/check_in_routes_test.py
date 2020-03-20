import json
import pytest
import unittest
from bson import ObjectId

from tests import setup
from api.models.trucker import TruckerModel
from api.models.check_in import CheckInModel

app = setup.create_flask_app()


class CheckInRoutesTest(unittest.TestCase):

    @pytest.mark.usefixtures('fixture_trucker_document', 'fixture_check_in_post_body')
    def test_1_route_create_check_in(self):
        with app.test_client() as c:
            body = json.loads(self.check_in_post_body)
            response = c.post('/check-in/trucker/{}'.format(self.trucker._id), json=body)
            response_bad_request_due_to_invalid_id = c.post('/check-in/trucker/{}'.format('0'), json={})
            response_not_found = c.post('/check-in/trucker/{}'.format(str(ObjectId())), json=body)
            response_bad_request_due_to_invalid_body = c.post('/check-in/trucker/{}'.format(self.trucker._id),
                                                              json={'isLoaded': 1})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_bad_request_due_to_invalid_id.status_code, 400)
        self.assertEqual(response_not_found.status_code, 404)
        self.assertEqual(response_bad_request_due_to_invalid_body.status_code, 400)

    @pytest.mark.usefixtures('fixture_check_in_document')
    def test_2_route_get_check_in(self):
        with app.test_client() as c:
            response = c.get('/check-in/{}'.format(self.check_in._id))
            response_bad_request_due_to_invalid_id = c.get('/check-in/{}'.format('0'))
            response_not_found = c.get('/check-in/{}'.format(str(ObjectId())))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_bad_request_due_to_invalid_id.status_code, 400)
        self.assertEqual(response_not_found.status_code, 404)

    @pytest.mark.usefixtures('fixture_check_in_document')
    def test_3_route_checkout(self):
        with app.test_client() as c:
            response = c.patch('/check-in/{}/checkout'.format(self.check_in._id))
            response_bad_request_due_to_invalid_id = c.patch('/check-in/{}/checkout'.format('0'))
            response_not_found = c.patch('/check-in/{}/checkout'.format(str(ObjectId())))
            response_bad_request_due_to_already_checked_out = c.patch('/check-in/{}/checkout'.format(self.check_in._id))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_bad_request_due_to_invalid_id.status_code, 400)
        self.assertEqual(response_not_found.status_code, 404)
        self.assertEqual(response_bad_request_due_to_already_checked_out.status_code, 400)

    @pytest.fixture(scope="function")
    def fixture_check_in_post_body(request):
        request.check_in_post_body = setup.read_fixture_file('check_in_post_body.json')

    @pytest.fixture(scope="function")
    def fixture_trucker_document(request):
        request.trucker = TruckerModel.create_trucker(json.loads(setup.read_fixture_file('trucker_post_body.json')))

    @pytest.fixture(scope="function")
    def fixture_check_in_document(request):
        trucker = TruckerModel.create_trucker(json.loads(setup.read_fixture_file('trucker_post_body.json')))
        request.check_in = CheckInModel.create_check_in(json.loads(setup.read_fixture_file('check_in_post_body.json')),
                                                        trucker)


if __name__ == '__main__':
    unittest.main()
