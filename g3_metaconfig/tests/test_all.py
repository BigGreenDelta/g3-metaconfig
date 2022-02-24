import logging
import sys
import unittest
from typing import Optional, Dict

import configargparse

from g3_metaconfig import G3ConfigMeta, Param

log = logging.getLogger(__name__)

sys.argv = [
    *sys.argv,
    "--count=55",
    "--count2=99",
    "--count3=333",
    "--number=999.0",
    "--text=test_text",
]


class G3Config(metaclass=G3ConfigMeta):
    class Config:
        env_prefix = "G3_"

    class ArgParserConfig:
        default_config_files = ["config.yml"]
        description = "Test"
        argument_parser_class = configargparse.ArgParser

    count: int = Param("--count", help="Help yuorself", default=33)
    count2: int = Param()
    count3: int = Param(default=100)
    condition: bool = Param("-c", "--cond", env_var="TEST_COND")
    text: str = None
    number: float = 3.52
    array: list = ["asdsssssss"]
    optional_unset: Optional[str] = None
    optional_with_value: Optional[str] = "asdsssssss"
    other_types: Dict[str, str] = None


class MyConfigs(metaclass=G3ConfigMeta):
    Test1 = None
    Test2 = None


class DefaultTestCases(unittest.TestCase):
    def test_default(self):
        self.assertEqual(MyConfigs.Test1, None)
        self.assertEqual(MyConfigs().Test1, None)

        self.assertEqual(MyConfigs.Test2, None)
        self.assertEqual(MyConfigs().Test2, None)

    def test_full(self):
        log.debug(f"{G3Config.count=} {G3Config().count=}")
        self.assertEqual(G3Config.count, 55)
        self.assertEqual(G3Config().count, 55)

        log.debug(f"{G3Config.count2=} {G3Config().count2=}")
        self.assertEqual(G3Config.count2, 99)
        self.assertEqual(G3Config().count2, 99)

        log.debug(f"{G3Config.count3=} {G3Config().count3=}")
        self.assertEqual(G3Config.count3, 333)
        self.assertEqual(G3Config().count3, 333)

        log.debug(f"{G3Config.condition=} {G3Config().condition=}")
        self.assertEqual(G3Config.condition, None)
        self.assertEqual(G3Config().condition, None)

        log.debug(f"{G3Config.text=} {G3Config().text=}")
        self.assertEqual(G3Config.text, "test_text")
        self.assertEqual(G3Config().text, "test_text")

        log.debug(f"{G3Config.number=} {G3Config().number=}")
        self.assertEqual(G3Config.number, 999.0)
        self.assertEqual(G3Config().number, 999.0)

        log.debug(f"{G3Config.array=} {G3Config().array=}")
        self.assertEqual(G3Config.array, ["asdsssssss"])
        self.assertEqual(G3Config().array, ["asdsssssss"])

        log.debug(f"{G3Config.optional_unset=} {G3Config().optional_unset=}")
        self.assertEqual(G3Config.optional_unset, None)
        self.assertEqual(G3Config().optional_unset, None)

        log.debug(f"{G3Config.optional_with_value=} {G3Config().optional_with_value=}")
        self.assertEqual(G3Config.optional_with_value, "asdsssssss")
        self.assertEqual(G3Config().optional_with_value, "asdsssssss")

        log.debug(f"{G3Config.other_types=} {G3Config().other_types=}")
        self.assertEqual(G3Config.other_types, None)
        self.assertEqual(G3Config().other_types, None)


if __name__ == "__main__":
    unittest.main()
