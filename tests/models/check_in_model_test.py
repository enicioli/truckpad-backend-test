import json
import pytest
import unittest
from bson import ObjectId

from tests import setup
from api.models.check_in import CheckInModel
from api.odm.check_in import CheckInDocument
from api.odm.trucker import TruckerDocument

app = setup.create_flask_app()


class CheckInModelTest(unittest.TestCase):

    @pytest.mark.usefixtures('fixture_check_in_post_body', 'fixture_trucker_document')
    def test_1_create_check_in(self):
        data = json.loads(self.check_in_post_body)
        check_in = CheckInModel.create_check_in(data, trucker=self.trucker)

        self.assertIsInstance(check_in, CheckInDocument)
        self.assertIsNotNone(check_in._id)

    @pytest.mark.usefixtures('fixture_check_in_document')
    def test_2_get_check_in_by_id(self):
        check_in = CheckInModel.get_check_in_by_id(str(self.check_in._id))
        check_in_not_exists = CheckInModel.get_check_in_by_id(str(ObjectId()))

        self.assertEqual(check_in, self.check_in)
        self.assertIsNone(check_in_not_exists)

    @pytest.mark.usefixtures('fixture_check_in_document')
    def test_3_checkout(self):
        check_in = CheckInModel.checkout(self.check_in)
        self.assertIsNotNone(check_in.checkedOut)

        check_in_already_checked_out = CheckInModel.checkout(check_in)
        self.assertIsNone(check_in_already_checked_out)

    @pytest.fixture(scope="function")
    def fixture_check_in_post_body(request):
        request.check_in_post_body = setup.read_fixture_file('check_in_post_body.json')

    @pytest.fixture(scope="function")
    def fixture_trucker_document(request):
        trucker = TruckerDocument(**json.loads(setup.read_fixture_file('trucker_post_body.json')))
        trucker._id = ObjectId()
        request.trucker = trucker

    @pytest.fixture(scope="function")
    def fixture_check_in_document(request):
        trucker = TruckerDocument(**json.loads(setup.read_fixture_file('trucker_post_body.json')))
        trucker._id = ObjectId()

        check_in_data = json.loads(setup.read_fixture_file('check_in_post_body.json'))

        request.check_in = CheckInModel.create_check_in(check_in_data, trucker=trucker)


if __name__ == '__main__':
    unittest.main()
