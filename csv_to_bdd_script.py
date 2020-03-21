#!/usr/bin/python3.7
import csv
import sqlite3


def import_csv_to_sqlite():
    """ Read CSV file and import lines to sqlite. """
    sqlite3.register_adapter(str, str)

    with sqlite3.connect('db.sqlite3') as connexion, open('correspondance-code-insee-code-postal.csv', 'rt',
                                                          encoding='utf-8', newline='') as src:

        cursor = connexion.cursor()

        # Clear tables and reset auto-increment of primary keys
        cursor.execute('DELETE FROM test_app_region')
        cursor.execute('DELETE FROM sqlite_sequence WHERE name="test_app_region"')
        cursor.execute('DELETE FROM test_app_county')
        cursor.execute('DELETE FROM sqlite_sequence WHERE name="test_app_county"')
        cursor.execute('DELETE FROM test_app_city')
        cursor.execute('DELETE FROM sqlite_sequence WHERE name="test_app_city"')

        states = dict()
        counties = dict()
        for row in csv.DictReader(src, delimiter=';'):
            code_region, region, code_departement, departement, code_insee, code_postal, commune, population, superficie = \
                row.get('Code Région'), row.get('Région'), row.get('Code Département'), row.get('Département'), row.get(
                    'Code INSEE'), row.get('Code Postal'), row.get('Commune'), row.get('Population'), row.get(
                    'Superficie')
            if code_region not in states:
                state_query = "INSERT INTO test_app_region (code, name) VALUES (?, ?)"
                state_data = (code_region, region)
                cursor.execute(state_query, state_data)
                # Add state to dictionary to avoid duplicates
                states[code_region] = cursor.lastrowid

            if departement not in counties:
                county_query = "INSERT INTO test_app_county (code, name, region_id) VALUES (?, ?, ?)"
                county_data = (code_departement, departement, states[code_region])
                cursor.execute(county_query, county_data)
                # Add county to dictionary to avoid duplicates
                counties[departement] = cursor.lastrowid

            city_query = "INSERT INTO test_app_city (code_insee, code_postal, name, population, area, county_id) " \
                         "VALUES (?, ?, ?, ?, ?, ?)"
            city_data = (code_insee, code_postal, commune, population, superficie, counties[departement])
            cursor.execute(city_query, city_data)


import_csv_to_sqlite()
