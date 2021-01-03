# ccs811-to-gbq

Retrieving data from a CCS811 eCO2 sensor and sending it to Google BigQuery.

## Getting Started

### Adjust I2C Bus Speed

This sensor is not supported well for the Raspberry Pi since it uses I2C clock stretching which the Pi cannot do without drastically slowing down the I2C speed (to 10 Kbit/s).

In `/boot/config.txt`, find the line containing "dtparam=i2c_arm=on" and add ",i2c_arm_baudrate=10000" where `10000` is the new speed (10 Kbit/s). **Note the comma.**

### Requirements

Install the dependencies in `requirements.txt` and activate the virtual environment.

### Google Cloud Authentication

Your application needs to be authenticated against Google Cloud. We recommend [passing credentials via environment variable](https://cloud.google.com/docs/authentication/production#passing_variable).

### BigQuery Table

You will need a BigQuery table with the following schema

```yaml
- name: sensor_id
  type: STRING
  mode: REQUIRED
- name: requested_at
  type: TIMESTAMP
  mode: REQUIRED
- name: eco2
  type: INTEGER
  mode: NULLABLE
- name: tvoc
  type: INTEGER
  mode: NULLABLE
```

### Environment Variables

Create a `.env` file (`cp .env.example .env`) and fill in the following information:

* `CCS811_SENSOR_ID`: The ID of the sensor (appears in BigQuery).
* `GBQ_PROJECT_ID`: The ID of your Google Cloud project, where your BigQuery dataset resides.
* `GBQ_DATASET_ID`: The ID of your BigQuery dataset, where your table resides.
* `GBQ_TABLE_ID`: The ID of the table, where your measurements should be stored.

## Running the Application

From your virtual environment, execute:

```sh
python3 main.py
```

### Running as Crontab

A simple crontab that runs every 5 minutes could look somewhat like this:

```sh
*/5 * * * * /usr/bin/env bash -c 'cd $HOME/path-to-your-application && source .venv/bin/activate && python3 main.py > .log 2>&1' > /dev/null 2>&1
```
