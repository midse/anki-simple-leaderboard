ADDON="simple-leaderboard"
FILES="__init__.py utils.py stats.py config.json config.md LICENSE"

mkdir -p /mnt/c/Users/irtim/AppData/Roaming/Anki2/addons21/$ADDON
cp -v $FILES /mnt/c/Users/irtim/AppData/Roaming/Anki2/addons21/$ADDON/

rm $ADDON.zip
zip $ADDON.zip $FILES