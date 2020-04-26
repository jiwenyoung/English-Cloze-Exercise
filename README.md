# English Gap Filling

This is a software which offer you great amount of gap-filling for English Learning. It collect English text from both RSS source as well as Local File. Splitting the text into sentences, it will find the "keyword" in the sentence and replace the word in the sentence with a gap, and such form a gap-filling sentence. It will offer you four possible options and you have to pick one to fill in. If you fill right, the question will be removed from database, and if you pick the wrong one, it will record it into a log file, that is, "wrong.log".

To run the program, you have to first of all run "setup" command which create database structure, and "fresh" command which fetches text and generate questions. It will get questions from text files in "article" directory and RSS source in the file named "rssfeeds.urls". In rssfeeds.urls file, rss source url is written line by line, and you can add it arbitrarily. 

"Keywords" is set of the words you want to practice, and it comes from two sources, one is the default 100 propositions which is pulled from the the url in "keywords.urls" file, and you can add your source into the file if you like (Source url must be return JSON Array File). The other one is the "keywords.user" file which you can add your own keyword line by line.

"config.ini" is the configuration file which could be used to setup most of features.

After the input prompt, you can remove a question by entering "r" or quit the program by entering "q", as well as input A,B,C,D for pick.

Until now, this software only offer cli interface.