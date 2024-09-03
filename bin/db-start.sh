#!/bin/bash

echo "REMOVE DB"
rm database/db.db

echo "CREATE DB"
sqlite3 database/db.db < sql/raw_db.sql