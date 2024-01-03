# iMessage Top Words!  
a multi-threaded fuzzy search script that finds the top words used in your iMessage conversations!

1. Download your iMessage chat history from your Mac. Use `sqlite3 ~/Library/Messages/chat.db` to open the database. Then, run the following commands:
2. `.output 2023.txt`
3. `SELECT text FROM message WHERE datetime((date / 1000000000) + 978307200, 'unixepoch', 'localtime') > datetime(1672560000, 'unixepoch', 'localtime') and is_from_me == 1;`
4. Move to this folder and just type `python3 main.py` and you're good to go!

change up --threshold for the fuzzy search and --n_words for the number of words you want to see! To generate a wordcloud add --wordcloud to the end of the command

