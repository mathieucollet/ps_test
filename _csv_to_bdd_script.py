#!/usr/bin/python3.7
import csv
import sqlite3


def test_read_sqlite_literals():
    """ Read SQLite literals from a CSV file. """
    sqlite3.register_adapter(str, str)

    with sqlite3.connect('db.sqlite3') as conn, open('correspondance-code-insee-code-postal.csv', 'rt',
                                                     encoding='utf-8', newline='') as src:
        conn.execute('DELETE FROM test_app_region')
        conn.execute('DELETE FROM sqlite_sequence WHERE name="test_app_region"')
        conn.execute('DELETE FROM test_app_county')
        conn.execute('DELETE FROM sqlite_sequence WHERE name="test_app_county"')
        conn.execute('DELETE FROM test_app_city')
        conn.execute('DELETE FROM sqlite_sequence WHERE name="test_app_city"')

        regions_data = []
        counties_data = []
        cities_data = []
        for row in csv.DictReader(src, delimiter=';'):
            regions_data.append((row.get('Code Région'), row.get('Région')))
            counties_data.append((row.get('Code Département'), row.get('Département')))
            cities_data.append((
                row.get('Code INSEE'), row.get('Code Postal'), row.get('Commune'), row.get('Population'),
                row.get('Superficie')))

        counties_data = list(set(counties_data))
        counties_data.sort()
        regions_data = list(set(regions_data))
        regions_data.sort()
        cities_data = list(set(cities_data))
        cities_data.sort()

        regions_query = "INSERT INTO test_app_region (code, name) VALUES (?, ?)"
        counties_query = "INSERT INTO test_app_county (code, name, region_id) VALUES (?, ?, ?)"
        cities_query = "INSERT INTO test_app_city (code_insee, code_postal, name, population, area) " \
                       "VALUES (?, ?, ?, ?, ?)"
        conn.executemany(regions_query, regions_data)
        conn.executemany(counties_query, counties_data)
        conn.executemany(cities_query, cities_data)


test_read_sqlite_literals()
