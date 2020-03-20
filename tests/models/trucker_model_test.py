import json
import pytest
import unittest
from bson import ObjectId

from tests import setup
from api.models.trucker import TruckerModel
from api.odm.trucker import TruckerDocument

app = setup.create_flask_app()


class TruckerModelTest(unittest.TestCase):

    @pytest.mark.usefixtures('fixture_trucker_post_body')
    def test_1_create_trucker(self):
        data = json.loads(self.trucker_post_body)
        trucker = TruckerModel.create_trucker(data)

        self.assertIsInstance(trucker, TruckerDocument)
        self.assertIsNotNone(trucker._id)

    @pytest.mark.usefixtures('fixture_trucker_document')
    def test_2_get_trucker_by_id(self):
        trucker = TruckerModel.get_trucker_by_id(str(self.trucker._id))
        trucker_not_exists = TruckerModel.get_trucker_by_id(str(ObjectId()))

        self.assertEqual(trucker, self.trucker)
        self.assertIsNone(trucker_not_exists)

    @pytest.mark.usefixtures('fixture_trucker_document', 'fixture_trucker_update_body')
    def test_3_update_trucker(self):
        update_trucker = json.loads(self.trucker_update_body)
        trucker = TruckerModel.update_trucker(self.trucker, update_trucker)

        for key in update_trucker:
            self.assertEqual(trucker.get(key), update_trucker[key])

    @pytest.mark.usefixtures('fixture_trucker_document')
    def test_4_delete_trucker(self):
        TruckerModel.delete_trucker(self.trucker)
        self.assertIsNone(TruckerModel.get_trucker_by_id(str(self.trucker._id)))

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
