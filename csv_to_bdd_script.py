#!/usr/bin/python3.7
import csv
import sqlite3


def test_read_sqlite_literals():
    """ Read SQLite literals from a CSV file. """
    sqlite3.register_adapter(str, str)

    with sqlite3.connect('db.sqlite3') as conn, open('correspondance-code-insee-code-postal.csv', 'rt',
                                                     encoding='utf-8', newline='') as src:

        cursor = conn.cursor()
        cursor.execute('DELETE FROM test_app_region')
        cursor.execute('DELETE FROM sqlite_sequence WHERE name="test_app_region"')
        cursor.execute('DELETE FROM test_app_county')
        cursor.execute('DELETE FROM sqlite_sequence WHERE name="test_app_county"')
        cursor.execute('DELETE FROM test_app_city')
        cursor.execute('DELETE FROM sqlite_sequence WHERE name="test_app_city"')

        regions_data = dict()
        counties_data = dict()
        cities_data = dict()
        for row in csv.DictReader(src, delimiter=';'):
            code_region, region, code_departement, departement, code_insee, code_postal, commune, population, superficie = \
                row.get('Code Région'), row.get('Région'), row.get('Code Département'), row.get('Département'), row.get(
                    'Code INSEE'), row.get('Code Postal'), row.get('Commune'), row.get('Population'), row.get(
                    'Superficie')
            if code_region not in regions_data:
                region_query = "INSERT INTO test_app_region (code, name) VALUES (?, ?)"
                region_data = (code_region, region)
                cursor.execute(region_query, region_data)
                regions_data[code_region] = cursor.lastrowid

            if departement not in counties_data:
                county_query = "INSERT INTO test_app_county (code, name, region_id) VALUES (?, ?, ?)"
                county_data = (code_departement, departement, regions_data[code_region])
                cursor.execute(county_query, county_data)
                counties_data[departement] = cursor.lastrowid

            if code_insee not in cities_data:
                city_query = "INSERT INTO test_app_city (code_insee, code_postal, name, population, area, county_id) " \
                             "VALUES (?, ?, ?, ?, ?, ?)"
                city_data = (code_insee, code_postal, commune, population, superficie, counties_data[departement])
                cursor.execute(city_query, city_data)

        # counties_data.append((row.get('Code Département'), row.get('Département')))
        # counties_query = "INSERT INTO test_app_county (code, name, region_id) VALUES (?, ?, ?)"
        # cursor.executemany(counties_query, counties_data)


test_read_sqlite_literals()
