# fbcrawl
so this project is a personal project for educational purposes on scraping and mining data from a website, the reason I chose facebook is because I use facebook on daily basis and I thought I could use whatever I know on facebook due to me using it all the time and implemant it in my work
I had no idea how python/scrapy work before i started this, The very first project that i saw that was related to my project was another github project called fbcrawl(https://github.com/rugantio/fbcrawl/), almost everything i learned came from there, i try and work on my project the same way the author of fbcrawl does,
my spiders (https://docs.scrapy.org/en/latest/topics/spiders.html for further understanding) deal with crawling and scraping data from : 
-PAGES : with a provided page link, credentials and an interface language (currently only french and english, i think the fbcrawl author is working on other languages, i might add more languages later on) and a year and you can have a list of the name of the page, date of post creation, number of reacts, number of comments and  the URL leading to the story
-COMMENTS : with a provided post link, credentials and an interface language you can have a list of the comments made on that post, the list has the profile of the commentator, the post or comment he's replying to, number of reacts on that comment, date of the comment, and the url leading to that comment
-GROUPS : does the exact same thing of the spider of PAGES but with GROUPS instead of pages
-REACTIONS : with a provided post link, credentials and an interface language you can have a list of the reactions made on that post, the list contains the url of the user that reacted and the reaction type
-PROFILE : with a provided profile link, credentials and an interface language you can have information on that profile, including the name of the user, the url of his profile the place and date of birth, and any friends the user allows you to see

my spiders behave the same way a user might behave, first of all they log into facebook, then they ignore the save device step, then they naviguate to the provided URL, and start crawling by selecting information that each spider is designed to collect and then clicks on the next page if needed(see more posts in a group/page, see more friends in a friends list, see more comments in a post)
my spiders dont crawl facebook as fast as possible and overload the server with requests, they have timers I added in order to make my crawling as "responsible" as possible

the spiders are not fully done yet, here's my to do list, i will include detailed tasks that i want to do, the problems that i might/will encounter in order to do these tasks and eventually a solution to these tasks (this is an educational project afterall) :
THIS LIST WILL GROW AS I ENCOUNTER PROBLEMS OR NEED TO ADD FEATURES IN MY CRAWLER

## TO DO LIST :

1)to do :collect all the spiders in one giant spider instead of diving it to smaller spiders(starting from a page url, the spider will collect all posts made on that page, collect all the reactions and comments made on that post, naviguate and collect information provided by the users that made these comments and reactions on the said post, do the same thing for groups)

1)potential problems of the above : the spider needs to naviguate to the needed link, might encounter some problems with the scrapy.request urls, needs further testing

1)solutions/tips : none yet


2)to do: fix the way the profile urls are collected, currently profile urls are in a rather messy format, i need to add a condition to my selectors to only collect the url until they reach a certain character IF the profile isnt a profile.php kind of profile, otherwise it needs to stop at another set character

2)potential problems of the above : the selector is xpath, however i do not know how to add conditions in xpath, so if they encouter a certain string they do X otherwise they do Y, also i dont know how to stop my selector at a a chain of numbers end and a chain of chars start for the profile.php, will need to look into that

2)solutions/tips : look into "xpath substring-before"


3)to do: export all my items to a database instead of a CSV file

3)potential problems of the above : the crawling might lead to hundred of thousands maybe even millions of input in my database, thus the database needs to be very well orgonised in order to function properly and efficiently, also the crawler might be faster be collecting data faster than the data is inserted in my database very further on in my project

3)solutions/tips : looking into database index fragmentation for now, further on looking into graph databases (the same type of database facebook uses)


4) to do : link a facebook user to a post/page/group via a comment or a reaction

4)potential problems of the above : the data might not transfer correctly

4)solutions/tips : look into "meta" in the scrapy.request(https://docs.scrapy.org/en/latest/topics/request-response.html?highlight=request%20meta)
