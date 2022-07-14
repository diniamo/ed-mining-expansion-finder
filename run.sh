source ./update_db.sh

pypy3 EDStationFinder.py $@ || python EDStationFinder.py $@
