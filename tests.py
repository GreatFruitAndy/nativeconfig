import sys
import unittest

from nativeconfig import *


class MyBaseConfig(object):
    single_value = Option('Single')
    single_value_default = Option('SingleDefault', default='a')
    single_value_default_no_empty = Option('SingleDefaultNoEmpty', default='a', default_if_empty=True)

    single_value_int = IntOption('SingleInt')
    single_value_int_default = IntOption('SingleIntDefault', default=1)

    choice_value = ChoiceOption('Choice', ['a', 'b'], default='a')
    choice_value_int = ChoiceOption('ChoiceInt', [1, 2], default=1, deserializer=int)

    array_value = ArrayOption('Array')
    array_value_default = ArrayOption('ArrayDefault', default=['a', 'b'])

    dict_value = DictOption('Dict')
    dict_value_default = DictOption('DictDefault', default={'a': '1', 'b': '2'})



# TODO: validate
# TODO: snapshot
# TODO: base methods


class TestBaseConfig(object):
    MyConfig = None

    def test_del_without_default_sets_none(self):
        c = self.MyConfig.instance()

        c.single_value = 'a'
        self.assertEqual(c.single_value, 'a')
        del c.single_value
        self.assertEqual(c.single_value, None)
        c.single_value = 'b'
        self.assertEqual(c.single_value, 'b')
        c.single_value = None
        self.assertEqual(c.single_value, None)

        c.single_value_int = 1
        self.assertEqual(c.single_value_int, 1)
        del c.single_value_int
        self.assertEqual(c.single_value_int, None)
        c.single_value_int = 2
        self.assertEqual(c.single_value_int, 2)
        c.single_value_int = None
        self.assertEqual(c.single_value_int, None)

        c.choice_value = 'b'
        self.assertEqual(c.choice_value, 'b')
        del c.choice_value
        self.assertEqual(c.choice_value, 'a')
        c.choice_value = 'b'
        self.assertEqual(c.choice_value, 'b')
        c.choice_value = None
        self.assertEqual(c.choice_value, 'a')

        c.choice_value_int = 2
        self.assertEqual(c.choice_value_int, 2)
        del c.choice_value_int
        self.assertEqual(c.choice_value_int, 1)
        c.choice_value_int = 2
        self.assertEqual(c.choice_value_int, 2)
        c.choice_value_int = None
        self.assertEqual(c.choice_value_int, 1)

        c.array_value = ['a', 'b']
        self.assertEqual(c.array_value, ['a', 'b'])
        del c.array_value
        self.assertEqual(c.array_value, None)
        c.array_value = ['b', 'c']
        self.assertEqual(c.array_value, ['b', 'c'])
        c.array_value = None
        self.assertEqual(c.array_value, None)

        c.dict_value = {'c': '3'}
        self.assertEqual(c.dict_value, {'c': '3'})
        del c.dict_value
        self.assertEqual(c.dict_value, None)
        c.dict_value = {'d': '4'}
        self.assertEqual(c.dict_value, {'d': '4'})
        c.dict_value = None
        self.assertEqual(c.dict_value, None)

    def test_del_with_default_sets_default(self):
        c = self.MyConfig.instance()

        c.single_value_default = 'b'
        self.assertEqual(c.single_value_default, 'b')
        del c.single_value_default
        self.assertEqual(c.single_value_default, 'a')
        c.single_value_default = 'c'
        self.assertEqual(c.single_value_default, 'c')
        c.single_value_default = None
        self.assertEqual(c.single_value_default, 'a')

        c.single_value_default_no_empty = 'b'
        self.assertEqual(c.single_value_default_no_empty, 'b')
        del c.single_value_default_no_empty
        self.assertEqual(c.single_value_default_no_empty, 'a')
        c.single_value_default_no_empty = 'c'
        self.assertEqual(c.single_value_default_no_empty, 'c')
        c.single_value_default_no_empty = None
        self.assertEqual(c.single_value_default_no_empty, 'a')

        c.single_value_int_default = 2
        self.assertEqual(c.single_value_int_default, 2)
        del c.single_value_int_default
        self.assertEqual(c.single_value_int_default, 1)
        c.single_value_int_default = 3
        self.assertEqual(c.single_value_int_default, 3)
        c.single_value_int_default = None
        self.assertEqual(c.single_value_int_default, 1)

        c.array_value_default = ['b', 'c']
        self.assertEqual(c.array_value_default, ['b', 'c'])
        del c.array_value_default
        self.assertEqual(c.array_value_default, ['a', 'b'])
        c.array_value_default = ['c', 'd']
        self.assertEqual(c.array_value_default, ['c', 'd'])
        c.array_value_default = None
        self.assertEqual(c.array_value_default, ['a', 'b'])

        c.dict_value_default = {'c': '3'}
        self.assertEqual(c.dict_value_default, {'c': '3'})
        del c.dict_value_default
        self.assertEqual(c.dict_value_default, {'a': '1', 'b': '2'})
        c.dict_value_default = {'d': '4'}
        self.assertEqual(c.dict_value_default, {'d': '4'})
        c.dict_value_default = None
        self.assertEqual(c.dict_value_default, {'a': '1', 'b': '2'})

    def test_values_can_be_get_by_option_name(self):
        c = self.MyConfig.instance()

        c.single_value = 'a'
        self.assertEqual('"a"', c.get_value_for_option_name('Single'))

        self.assertEqual('"a"', c.get_value_for_option_name('SingleDefault'))
        c.single_value_default = 'b'
        self.assertEqual('"b"', c.get_value_for_option_name('SingleDefault'))

        c.single_value_int = 1
        self.assertEqual('"1"', c.get_value_for_option_name('SingleInt'))

        self.assertEqual('"1"', c.get_value_for_option_name('SingleIntDefault'))
        c.single_value_int_default = 2
        self.assertEqual('"2"', c.get_value_for_option_name('SingleIntDefault'))

        self.assertEqual('"a"', c.get_value_for_option_name('Choice'))
        c.choice_value = 'b'
        self.assertEqual('"b"', c.get_value_for_option_name('Choice'))

        self.assertEqual('"1"', c.get_value_for_option_name('ChoiceInt'))
        c.choice_value_int = 2
        self.assertEqual('"2"', c.get_value_for_option_name('ChoiceInt'))

        c.array_value = ['c', 'd']
        self.assertEqual('["c", "d"]', c.get_value_for_option_name('Array'))

        c.dict_value = {'d': '1'}
        self.assertEqual('{"d": "1"}', c.get_value_for_option_name('Dict'))

    def test_values_can_be_set_by_option_name(self):
        c = self.MyConfig.instance()

        c.set_value_for_option_name('Single', '"b"')
        self.assertEqual(c.single_value, 'b')

        c.set_value_for_option_name('SingleDefault', '"c"')
        self.assertEqual(c.single_value_default, 'c')

        c.set_value_for_option_name('SingleDefaultNoEmpty', '"d"')
        self.assertEqual(c.single_value_default_no_empty, 'd')

        c.set_value_for_option_name('SingleInt', '"5"')
        self.assertEqual(c.single_value_int, 5)

        c.set_value_for_option_name('SingleIntDefault', '"6"')
        self.assertEqual(c.single_value_int_default, 6)

        c.set_value_for_option_name('Choice', '"b"')
        self.assertEqual(c.choice_value, 'b')

        c.set_value_for_option_name('ChoiceInt', '"5"')
        self.assertEqual(c.choice_value_int, 5)

        c.set_value_for_option_name('Array', '["x", "z"]')
        self.assertEqual(c.array_value, ['x', 'z'])

        c.set_value_for_option_name('ArrayDefault', '["x", "z"]')
        self.assertEqual(c.array_value_default, ['x', 'z'])

        c.set_value_for_option_name('Dict', '{"f": "7"}')
        self.assertEqual(c.dict_value, {'f': '7'})

        c.set_value_for_option_name('DictDefault', '{"f": "8"}')
        self.assertEqual(c.dict_value_default, {'f': '8'})

    def test_values_can_be_del_by_option_name(self):
        c = self.MyConfig.instance()
        c.set_value_for_option_name('Single', '"b"')
        c.remove_value_for_option_name('Single')
        self.assertEqual(c.single_value, None)

        c.set_value_for_option_name('SingleDefault', '"b"')
        c.remove_value_for_option_name('SingleDefault')
        self.assertEqual(c.single_value_default, 'a')

        c.set_value_for_option_name('SingleDefaultNoEmpty', '"b"')
        c.remove_value_for_option_name('SingleDefaultNoEmpty')
        self.assertEqual(c.single_value_default_no_empty, 'a')

        c.set_value_for_option_name('SingleInt', '"5"')
        c.remove_value_for_option_name('SingleInt')
        self.assertEqual(c.single_value_int, None)

        c.set_value_for_option_name('SingleIntDefault', '"2"')
        c.remove_value_for_option_name('SingleIntDefault')
        self.assertEqual(c.single_value_int_default, 1)

        c.set_value_for_option_name('Choice', '"b"')
        c.remove_value_for_option_name('Choice')
        self.assertEqual(c.choice_value, 'a')

        c.set_value_for_option_name('ChoiceInt', '"5"')
        c.remove_value_for_option_name('ChoiceInt')
        self.assertEqual(c.choice_value_int, 1)

        c.set_value_for_option_name('Array', '["x", "z"]')
        c.remove_value_for_option_name('Array')
        self.assertEqual(c.array_value, None)

        c.set_value_for_option_name('ArrayDefault', '["c", "d"]')
        c.remove_value_for_option_name('ArrayDefault')
        self.assertEqual(c.array_value_default, ['a', 'b'])

        c.set_value_for_option_name('Dict', '{"f": "7"}')
        c.remove_value_for_option_name('Dict')
        self.assertEqual(c.dict_value, None)

        c.set_value_for_option_name('DictDefault', '{"f": "7"}')
        c.remove_value_for_option_name('DictDefault')
        self.assertEqual(c.dict_value_default, {'a': '1', 'b': '2'})

    def test_setting_to_empty_string(self):
        c = self.MyConfig.instance()

        c.single_value = ''
        self.assertEqual(c.single_value, '')

        c.single_value_default = ''
        self.assertEqual(c.single_value_default, '')

        c.single_value_default_no_empty = ''
        self.assertEqual(c.single_value_default_no_empty, 'a')

        with self.assertRaises(ValueError):
            c.single_value_int = ''

        with self.assertRaises(ValueError):
            c.single_value_int_default = ''

    def test_validate(self):
        # duplicate
        # wrong choice
        # wrong default type
        pass

    def test_snapshot_returns_empty_and_none_values(self):
        c = self.MyConfig.instance()

        c.single_value_default = ''
        c.array_value_default = []
        c.dict_value_default = {}

        snapshot = c.snapshot()

        self.assertEqual(snapshot['Single'], 'null')
        self.assertEqual(snapshot['SingleDefault'], '""')
        self.assertEqual(snapshot['SingleDefaultNoEmpty'], '"a"')
        self.assertEqual(snapshot['SingleInt'], 'null')
        self.assertEqual(snapshot['SingleIntDefault'], '"1"')
        self.assertEqual(snapshot['Choice'], '"a"')
        self.assertEqual(snapshot['ChoiceInt'], '"1"')
        self.assertEqual(snapshot['Array'], 'null')
        self.assertEqual(snapshot['ArrayDefault'], '[]')
        self.assertEqual(snapshot['Dict'], 'null')
        self.assertEqual(snapshot['DictDefault'], '{}')

    def test_set_choice_to_wrong_option_causes_exception(self):
        c = self.MyConfig.instance()

        with self.assertRaises(ValueError):
            c.choice_value = 'c'

        with self.assertRaises(ValueError):
            c.choice_value_int = 10

    def tearDown(self):
        c = self.MyConfig.instance()

        del c.single_value
        del c.single_value_default
        del c.single_value_default_no_empty

        del c.single_value_int
        del c.single_value_int_default

        del c.choice_value
        del c.choice_value_int

        del c.array_value
        del c.array_value_default

        del c.dict_value
        del c.dict_value_default


if sys.platform.startswith('win32'):
    class TestRegistryConfig(TestBaseConfig, unittest.TestCase):
        class MyConfig(MyBaseConfig, RegistryConfig):
            REGISTRY_PATH = r'Software\NativeConfigTest'

        @classmethod
        def tearDownClass(cls):
            super(TestRegistryConfig, cls).tearDownClass()
            try:
                import winreg
            except ImportError:
                import _winreg as winreg

            for k in _traverse_registry_key(cls.MyConfig.REGISTRY_KEY, cls.MyConfig.REGISTRY_PATH):
                winreg.DeleteKey(cls.MyConfig.REGISTRY_KEY, k)
elif sys.platform.startswith('darwin'):
    class TestNSUserDefaultsConfig(TestBaseConfig, unittest.TestCase):
        class MyConfig(MyBaseConfig, NSUserDefaultsConfig):
            pass


class TestJSONConfig(TestBaseConfig, unittest.TestCase):
    class MyConfig(MyBaseConfig, JSONConfig):
        JSON_PATH = '.nativeconfig'

    @classmethod
    def tearDownClass(cls):
        super(TestJSONConfig, cls).tearDownClass()
        os.remove(cls.MyConfig.JSON_PATH)


class TestInMemoryConfig(TestBaseConfig, unittest.TestCase):
    class MyConfig(MyBaseConfig, InMemoryConfig):
        pass