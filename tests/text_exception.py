import unittest
from adapters.onebot_qq_extension.exception import *


class TestException(unittest.TestCase):
    def test_all(self):
        raise_data = {"retcode": "10000"}

        raise_data["retcode"] = "10000"
        with self.assertRaises(RequestError):
            raise_action_error(**raise_data)
        with self.assertRaises(ActionFailed):
            raise_action_error(**raise_data)

        raise_data["retcode"] = "32004"
        with self.assertRaises(FileWriteErrorActionFailed):
            raise_action_error(**raise_data)
        with self.assertRaises(FilesystemError):
            raise_action_error(**raise_data)

        raise_data["retcode"] = "30000"
        with self.assertRaises(ExecutionError):
            raise_action_error(**raise_data)
        with self.assertRaises(ActionFailed):
            raise_action_error(**raise_data)

        raise_data["retcode"] = "31000"
        with self.assertRaises(DatabaseError):
            raise_action_error(**raise_data)
        with self.assertRaises(ExecutionError):
            raise_action_error(**raise_data)
        with self.assertRaises(ActionFailed):
            raise_action_error(**raise_data)

        raise_data["retcode"] = "32587"
        with self.assertRaises(FilesystemError):
            raise_action_error(**raise_data)
        with self.assertRaises(ExecutionError):
            raise_action_error(**raise_data)
        with self.assertRaises(ActionFailed):
            raise_action_error(**raise_data)

        raise_data["retcode"] = "20002"
        with self.assertRaises(InternalHandlerErrorActionFailed):
            raise_action_error(**raise_data)

        raise_data["retcode"] = "99999"
        with self.assertRaises(ActionFailed):
            raise_action_error(**raise_data)
