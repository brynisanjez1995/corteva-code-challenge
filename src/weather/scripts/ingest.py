import csv
import psycopg2
import environ
import os
import logging
import datetime

env = environ.Env()
environ.Env.read_env()
SECRET_KEY = env("SECRET_KEY")

logging.basicConfig(filename="logs/ingestion.log", level=logging.INFO,
                    format='%(asctime)s.%(msecs)03d %(levelname)s {%(module)s} [%(funcName)s] %(message)s',
                    datefmt='%Y-%m-%d,%H:%M:%S')
logger = logging.getLogger("ingest")


def create_connection():
    return psycopg2.connect(database=env("DATABASE_NAME"),
                            user=env("DATABASE_USER"), password=env("DATABASE_PASSWORD"),
                            host=env("DATABASE_HOST"), port=env("DATABASE_PORT")
                            )


def load_files(input_dir, processed_dir):
    conn = create_connection()
    try:
        conn.autocommit = True
        cursor = conn.cursor()
        file_count = 0
        for file in os.listdir(input_dir):
            file_path = f"{input_dir}/{file}"
            station_id = file.split('.')[0]
            processed_path = f"{processed_dir}/{file}"
            load_file(cursor, file_path, station_id)
            os.rename(file_path, processed_path)
            file_count = file_count + 1
        return file_count
    finally:
        conn.close()


def build_insert_sql(values):
    sql_pre = "insert into weather.daily_weather " \
              "(station_id, date, min_temp, max_temp, precipitation) " \
              "values "

    on_conflict_clause = ' on conflict on constraint station_id_date_uk do update ' \
                         'set min_temp = EXCLUDED.min_temp, ' \
                         'max_temp = EXCLUDED.max_temp, ' \
                         'precipitation = EXCLUDED.precipitation'

    return sql_pre + ','.join(values) + on_conflict_clause


def load_file(cursor, file, station_id):
    values = []

    with open(file, mode='r') as f:
        rows = csv.reader(f, delimiter='\t')
        for row in rows:
            date = row[0][0:4] + '-' + row[0][4:6] + '-' + row[0][6:]
            min_temp = row[1] if row[1] != '-9999' else 'null'
            max_temp = row[2] if row[2] != '-9999' else 'null'
            precipitation = row[3] if row[3] != '-9999' else 'null'
            values.append(f"('{station_id}', '{date}', {min_temp}, {max_temp}, {precipitation})")

    sql = build_insert_sql(values)

    logger.info(f"Loading file {file}")
    logger.debug(f"Using sql {sql}")
    cursor.execute(sql)

def load_stats():
    sql = """
    insert
        into
        weather.yearly_weather_stats (station_id,
        year,
        avg_min_temp,
        avg_max_temp,
        total_precipitation)
    select
        station_id,
        extract(year from date),
        avg(min_temp),
        avg(max_temp),
        sum(precipitation) / 1000
    from
        weather.daily_weather
    group by
        station_id,
        extract(year from date)
    on conflict on constraint station_id_year_uk 
    do update set
        avg_min_temp = EXCLUDED.avg_min_temp, 
        avg_max_temp = EXCLUDED.avg_max_temp, 
        total_precipitation = EXCLUDED.total_precipitation
    """

    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
    finally:
        conn.close()



def main():
    input_path = env("INPUT_PATH")
    processed_path = env("PROCESSED_PATH")

    start_time = datetime.datetime.now()
    logger.info(f"Processing files from {input_path}")
    file_count = load_files(input_path, processed_path)

    completion_time = datetime.datetime.now()
    elapsed_time = (completion_time - start_time).total_seconds()
    logger.info(f"Processed {file_count} file(s) in {elapsed_time} second(s)")

    logger.info(f"Processing stats")
    start_time = datetime.datetime.now()
    load_stats()

    completion_time = datetime.datetime.now()
    elapsed_time = (completion_time - start_time).total_seconds()
    logger.info(f"Updated stats in {elapsed_time} second(s)")

if __name__ == "__main__":
    main()
