"""
Reads data from a CCS811 eCO2 sensor and sends it to Google BigQuery.
"""

import os
import time
from datetime import datetime

import adafruit_ccs811
import board
import busio
from dotenv import load_dotenv
from google.cloud import bigquery


class CCS811(adafruit_ccs811.CCS811):
    """
    CCS881 class that can take measurements.
    """

    _READY_WAIT_TIME = 0.1

    def __init__(self, sensor_id):
        i2c = busio.I2C(board.SCL, board.SDA)
        super().__init(i2c)
        self._sensor_id = sensor_id

    @classmethod
    def from_env(cls):
        """
        Creates an instance of CCS881 from environment variables.
        """
        return cls(os.environ["CCS811_SENSOR_ID"])

    @property
    def _measurement(self):
        while not self.data_ready:
            time.sleep(self._READY_WAIT_TIME)
        return {"eco2": self.eco2, "tvoc": self.tvoc}

    @property
    def measurement(self):
        """
        Takes a measurement.
        """
        measurement_ = {}
        measurement_["sensor_id"] = self._sensor_id
        measurement_["requested_at"] = datetime.now()
        measurement_.update(self._measurement)
        return measurement_


def _gbq_setup():
    project_id = os.environ["GBQ_PROJECT_ID"]
    dataset_id = os.environ["GBQ_DATASET_ID"]
    table_id = os.environ["GBQ_TABLE_ID"]
    client = bigquery.Client()
    dataset = bigquery.dataset.DatasetReference.from_string(
        f"{project_id}.{dataset_id}"
    )
    table = client.get_table(dataset.table(table_id))
    return client, table


def _gbq_insert(measurement, client, table):
    errors = client.insert_rows(table, [measurement])
    if errors:
        raise RuntimeError(errors)


if __name__ == "__main__":
    load_dotenv()
    client, table = _gbq_setup()
    sensor = CCS811.from_env()
    measurement = sensor.measurement
    print(measurement)
    # _gbq_insert(measurement, client, table)
