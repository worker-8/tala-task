echo "REMOVE DB"
rm db.db
# DB COMMAND CREATION

echo "CREATE DB"
sqlite3 db.db < ./sql/raw_db.sql