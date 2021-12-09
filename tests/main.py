import unittest

from g3_config import G3ConfigMeta, Param


class G3Config(metaclass=G3ConfigMeta):
    class Config:
        env_prefix = "G3_"

    class ArgParserConfig:
        default_config_files = ["config.yml"]
        description = "Test"

    count: int = Param("--count", help="Help yuorself", default=33)
    condition: bool = Param("-c", "--cond", env_var="TEST_COND")
    text: str = None
    array: list = ["asdsssssss"]


class MyConfigs(G3Config):
    Test1 = None
    Test2 = None


class MyTestCase(unittest.TestCase):
    def test_fail_check(self):
        self.assertEqual(G3Config.count, 33)
        self.assertEqual(G3Config.condition, None)
        self.assertEqual(G3Config.text, None)
        self.assertEqual(G3Config.array, ["asdsssssss"])


if __name__ == '__main__':
    unittest.main()
