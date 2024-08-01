import eurostat

from timeseries_generator.external_factors.external_factor import ExternalFactor
from pandas import DataFrame
from pandas._libs.tslibs.timestamps import Timestamp
import pandas as pd
from timeseries_generator.external_factors.external_factor import ExternalFactor


MIN_DATE = Timestamp("01-01-2021")
MAX_DATE = Timestamp("10-31-2024")


class EUIndustryProductFactorEurostat(ExternalFactor):
    def __init__(self, col_name="eu_industry_product_factor", intensive_scale=1):
        """
        p

         Args:
             col_name: column name of the factor

        """
        super().__init__(col_name=col_name, min_date=MIN_DATE, max_date=MAX_DATE)
        self._intensive_sale = intensive_scale

    def load_data(self) -> DataFrame:
        dataset_id = "sts_inpr_m"
        df = eurostat.get_data_df(
            dataset_id,
            filter_pars={
                "geo": "EU27_2020",
                "nace_r2": "MIG_NRG_X_E",
                "unit": "I21",
                "s_adj": "SCA",
            },
        )
        df = df.iloc[:, 6:].transpose()
        df.index = pd.to_datetime(df.index)

        # get daily sample and forward fill
        df = df.resample("D").ffill()

        # reset index and rename
        df = df.reset_index()
        df.columns = [self._date_col_name, self._col_name]

        # normalize the industry product index
        df[self._col_name] = df[self._col_name] / 100 * self._intensive_sale

        return df
