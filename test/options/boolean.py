from itertools import chain
import os
import unittest

from nativeconfig.exceptions import InitializationError, DeserializationError, ValidationError
from nativeconfig.options import BooleanOption

from test import DummyMemoryConfig
from test import all_casings
from test.options import TestOptionMixin


class MyConfig(DummyMemoryConfig):
    boolean_true = BooleanOption('BooleanTrue', env_name='BOOLEAN_TRUE', default=True)
    boolean_false = BooleanOption('BooleanFalse', default=False)


class TestBooleanOption(unittest.TestCase, TestOptionMixin):
    @classmethod
    def setUpClass(cls):
        cls.OPTION_TYPE = BooleanOption

    def tearDown(self):
        c = MyConfig.get_instance()
        del c.boolean_true
        del c.boolean_false
        os.unsetenv('BOOLEAN_TRUE')

#{ Custom

    def test_cannot_be_empty(self):
        c = MyConfig.get_instance()

        c.set_value('BooleanTrue', "")
        self.assertEqual(c.boolean_true, True)

        c.set_value('BooleanFalse', "")
        self.assertEqual(c.boolean_false, False)

    def test_non_bool_raises_exception(self):
        c = MyConfig.get_instance()

        with self.assertRaises(ValidationError):
            c.boolean_true = '42'

    def test_true_serialized_to_1(self):
        c = MyConfig.get_instance()
        c.boolean_false = True
        self.assertEqual(c.get_value('BooleanFalse'), '1')

    def test_false_serialized_to_0(self):
        c = MyConfig.get_instance()
        c.boolean_true = False
        self.assertEqual(c.get_value('BooleanTrue'), '0')

    def test_can_be_deleted(self):
        c = MyConfig.get_instance()

        c.boolean_true = False
        self.assertEqual(c.boolean_true, False)
        del c.boolean_true
        self.assertEqual(c.boolean_true, True)

        c.boolean_true = False
        self.assertEqual(c.boolean_true, False)
        c.boolean_true = None
        self.assertEqual(c.boolean_true, True)

    def test_json_serialization_deserialization(self):
        c = MyConfig.get_instance()

        self.assertEqual(c.get_value_for_option_name('BooleanTrue'), 'true')
        self.assertEqual(c.get_value_for_option_name('BooleanFalse'), 'false')

        c.set_value_for_option_name('BooleanFalse', 'true')
        self.assertEqual(c.boolean_false, True)

        c.set_value_for_option_name('BooleanTrue', 'false')
        self.assertEqual(c.boolean_true, False)

    def test_deserialization_of_allowed_true_values(self):
        c = MyConfig.get_instance()

        for v in chain.from_iterable([all_casings(v) for v in BooleanOption.TRUE_RAW_VALUES]):
            c.set_value('BooleanFalse', v)
            self.assertEqual(c.boolean_false, True)

    def test_deserialization_of_allowed_false_values(self):
        c = MyConfig.get_instance()

        for v in chain.from_iterable([all_casings(v) for v in BooleanOption.FALSE_RAW_VALUES]):
            c.set_value('BooleanTrue', v)
            self.assertEqual(c.boolean_true, False)

    def test_deserialization_of_disallowed_values(self):
        c = MyConfig.get_instance()
        c.set_value('BooleanFalse', 'foobar')
        with self.assertRaises(DeserializationError):
            c.boolean_false

#{ TestOptionMixin

    def test_choices_cannot_be_empty(self):
        pass  # choices are hardcoded

    def test_default_value_must_be_one_of_choices_if_any(self):
        with self.assertRaises(ValidationError):
            class MyConfig(DummyMemoryConfig):
                boolean = self.OPTION_TYPE('Boolean', default=42)

        class MyConfig(DummyMemoryConfig):
            boolean = self.OPTION_TYPE('Boolean', default=True)

        class MyConfig(DummyMemoryConfig):
            boolean = self.OPTION_TYPE('Boolean', default=False)

    def test_all_choices_must_be_valid(self):
        pass  # choices are hardcoded

    def test_default_must_be_valid(self):
        self.test_default_value_must_be_one_of_choices_if_any()

    def test_value_must_be_one_of_choices_if_any(self):
        class MyConfig(DummyMemoryConfig):
            boolean = self.OPTION_TYPE('Boolean', default=True)

        with self.assertRaises(ValidationError):
            MyConfig.get_instance().boolean = 42

        MyConfig.get_instance().boolean = True
        MyConfig.get_instance().boolean = False

    def test_serialize_json(self):
        c = MyConfig.get_instance()
        c.boolean_true = False
        self.assertEqual(c.get_value_for_option_name('BooleanTrue'), 'false')

    def test_deserialize_json(self):
        c = MyConfig.get_instance()
        c.set_value_for_option_name('BooleanTrue', 'false')
        c.boolean_true = False

    def test_value_can_be_overridden_by_env(self):
        os.environ['BOOLEAN_TRUE'] = '\"0\"'
        c = MyConfig.get_instance()
        self.assertEqual(c.boolean_true, False)

    def test_value_can_be_overridden_by_one_shot_value(self):
        c = MyConfig.get_instance()


    def test_value_that_cannot_be_deserialized_during_get_calls_resolver(self):
        pass

    def test_invalid_deserialized_value_during_get_calls_resolver(self):
        pass

    def test_setting_value_resets_one_shot_value(self):
        pass

    def test_setting_invalid_value_raises_exception(self):
        pass

    def test_setting_none_deletes_value(self):
        pass

    def test_deleting_value(self):
        pass

#}
