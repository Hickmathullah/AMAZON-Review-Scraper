from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

#url = "https://www.amazon.co.uk/All-New-Fire-Tablet-Alexa-Display/product-reviews/B07952CV7L/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
#url = "https://www.amazon.co.uk/All-New-Fire-Tablet-Alexa-Display/product-reviews/B07952CV7L/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber=1"

review_list = []        # Reviews will be stored here


def get_soup(url):      # to get the response content from the url
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      'Chrome/90.0.4430.212 Safari/537.36'}     # header for the request paramater
    response = requests.get(url, headers=header)
    soup = bs(response.content, 'html.parser')
    return soup         # returns the HTML content


def get_reviews(soup):      # to get the data from the elements in teh website
    reviews = soup.find_all('div', {'data-hook': 'review'})     # gets the review block from the website

    try:
        for items in reviews:       # for loop to get all the data requested and saves it in the review json
            review = {
                'review_title': items.find('a', {'data-hook': 'review-title'}).text.strip(),
                'review_description': items.find('span', {'data-hook': 'review-body'}).text.strip(),
                'rating': items.find('i', {'data-hook': 'review-star-rating'}).text.replace('out of 5 stars',
                                                                                            '').strip(),
                'username': items.find('span', {'class': 'a-profile-name'}).text.capitalize().strip(),
                'review_date': items.find('span', {'data-hook': 'review-date'}).text.replace('Reviewed in the United Kingdom on', '').strip()
            }
            review_list.append(review)      # appends the json data to the review_list declared above
    except Exception as e:
        print(f'An error occurred --> {e}') 


for x in range(1, 501):         # to loop through the pages to get all the review in that particular page
    soup = get_soup(f'https://www.amazon.co.uk/All-New-Fire-Tablet-Alexa-Display/product-reviews/B07952CV7L/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber={x}')
    print(f'Getting review from page: {x}')         # current page we are getting reviews from
    get_reviews(soup)
    print(len(review_list))                         # to display the length of the reviews fetched from a page
    if not soup.find('li', {'class': 'a-disabled a-last'}):     # checks for last page of the review
        pass
    else:
        break

df = pd.DataFrame(review_list)          # pandas as pd --> used DataFrame to store the data in a variable 'df'
df.to_excel('amazon_reviews.xlsx', index=False)         # inserting the data into excel with to_excel with default excel index format
print('Finished !')             # to indicate if the program has completed or else . . .

