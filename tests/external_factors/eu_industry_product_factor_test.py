import unittest

from pandas import DataFrame

from timeseries_generator.external_factors import (
    EUIndustryProductFactorEurostat,
    EUIndustryProductFactor,
)


class TestEUIndustryProductFactor(unittest.TestCase):

    def test_loading(self):
        euipf: EUIndustryProductFactor = EUIndustryProductFactor()
        df: DataFrame = euipf.generate("01-01-2018", "01-01-2020")
        self.assertAlmostEqual(1.059, df.head(1)[euipf.col_name].values[0])

    def test_loading_eurostat(self):
        euipf: EUIndustryProductFactor = EUIndustryProductFactorEurostat()
        df: DataFrame = euipf.generate("01-01-2018", "01-01-2020")
        self.assertAlmostEqual(1.021, df.head(1)[euipf.col_name].values[0])
