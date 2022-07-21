NAME_DB = "fast_test"
NAME_TABEL = "test_tabel"
HOST = "51.250.27.5"
Refresh_TABLE = f"""
DROP TABLE IF EXISTS {NAME_TABEL};
CREATE TABLE {NAME_TABEL}
(
    id    serial PRIMARY KEY,
    email varchar(255),
    buy   money
);
"""
