# Dataset Description

I collected a bunch of book data from Books to Scrape. It is a website that is designed for practicing web scraping. I scraped the first three pages of the site and then collected 60 total book records. I then stored them in a SQlite database using Peewee. Each book was stored with the title, price, and star rating. 

# Pipeline Description

The pipeline is broken into a few different functions that each have one purpose. It starts by pulling the web pages with the requests library, then BeautifulSoup digs through the HTML to get each book's title, price, and rating. After that the data gets saved into a SQLite database using a Peewee model. Before it adds anything the program checks and makes sure that the book isn't in there yet so it doesn't have any duplicates. Once everything's stored it pulls the data back out and loads it into a Pandas DataFrame. Then I use it to get summary stats and the average price for each rating. Finally matplotlib takes that and makes a bar chart showing the average price by rating.

# Findings

The dataset contained 60 books with an average price of about $35.00. The most expensive book cost $57.31 while the least expensive cost $12.84. Books with a rating of 3 had the highest average price at $38.81. To my surprise books with a rating of 5 did not have the highest average price. This showed that price and rating are not strongly related in this sample.

# Ethical Considerations

I used Books to Scrape which is a website specifically designed for educational web scraping practice. The scraper included a one-second delay between page requests to avoid sending requests too quickly. There wasn't any personal or sensitive information was collected.

# Limitations

There were only 3 pages analyzed so the results probably don't represent the entire catalog. Also, the ratings are done by the webside so they might not reflect the real customenrs opinions. With more time I would analyze more pages and see the relationships of price and ratings. 