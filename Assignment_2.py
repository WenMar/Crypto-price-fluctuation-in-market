"""
Scenario

This program aims to tell the user(investor) which crypto in their portfolio are making you money in the last 24 hours.
The user needs to type a crypto available in their portfolio, and the program will retrieve crypto name, symbols, price (usd), market cap, crypto change in 24h. 
The program is using a free API of CoinCap (https://api.coincap.io/v2/assets/). The API do not requires auth.  


"""


import requests # the module that allows to send HTTP requests using Python
import os # the module that allows to clean text file
def get_crypto_data (crypto): # Function to get data from the API CoinCap 
    crypto_url = f'https://api.coincap.io/v2/assets/{crypto}' #variable contain as value the URL of the API
    response = requests.get(crypto_url) #variable contain the request to get data inside the API
    if response.status_code == 200: #this line means if the response is successfull
        return response.json() ['data'] # return response in json 
    else:
        print(f'Data for {crypto}  are not available at the moment. Please try later on') #this notification will show up to the user if data could not be fetch 
        return None
    
def display_crypto_data(crypto_data): #created this function to display a table that shows in a user-friendly manner the cryptos asked by the user
    Table_header = (f"{'Name':<20} {'Symbol':<20} {'Price (USD)':<20} {'Market Cap':<20} {'Change (24h)':<20}") #to create row table for titles and padding 
    name = crypto_data['name'] #extract crypto name, symbol, price, market cap and 24h change
    name = name[:10] + '...' if len(name) > 10 else name #Use string slicing to limit the length of the name for display
    symbol = crypto_data['symbol']
    price = float(crypto_data['priceUsd'])
    market_cap = float(crypto_data['marketCapUsd'])
    change_24h = float(crypto_data['changePercent24Hr'])

    row = f"{name:<20} {symbol:<20} ${price:<20} ${market_cap:<20} {change_24h:<20}%\n"  # Data row 
    return Table_header + '\n' + '\n'+ row

def save_results_textfile(results): #this function allows to save results in a text file
    with open('Assignment_2.txt','a') as text_file:
        text_file.write(results)

def main(): # this is the starting point for program execution  
     Portfolio_crypto = ['bitcoin', 'ethereum', 'ripple', 'litecoin', 'cardano', 'shiba-inu'] #list of cryptos in investor portofolio
     investor_input = input(f'This feature tells you which crypto in your portfolio are making you money in the last 24 hours.\nType in the names of your crypto and see who is making it rain with cash and who is just making it drizzle! \nThese are the cryptos currently available in your portfolio {Portfolio_crypto}, \nPlease type crypto name: ' ).lower() #investor input 
     
     if os.path.exists('Assignment_2.txt'): # clean text file
        os.remove('Assignment_2.txt')
     for crypto in investor_input.split(): # loop to process crypto entered by the investor so the program can retrieved data 
         if crypto in Portfolio_crypto: # if entered crypto is in portfolio, the data will be shown to the investor 
            crypto_data = get_crypto_data(crypto)
            if crypto_data:
                results = display_crypto_data(crypto_data)
                change_24h = float(crypto_data['changePercent24Hr'])  # check if the crypto is going up or down
                if change_24h > 0:  # for positive crypto trend                     
                    output = 'Your crypto is going up! You are making the $ bag! Please contact your financial advisor if you have any queries.' # this variable will give the string in the text file  

                elif change_24h < 0: #for negative crypto trend
                    
                    output = 'Your crypto is going down! You are losing money, but best time to invest, please contact your financial advisor for further details.' # this variable will give the string in the text file
                    
                else: 
                    output =f'{crypto} is not in the portfolio. Please contact your financial advisor if you would like to invest in {crypto}.' #if investor type a crypto not in their portfolio, and the variable will give the string in the text fil
                
                print(results) #print the results
                print(output) #print the output of the if else in the terminal 
                save_results_textfile(results) #save in text file 
                save_results_textfile(output)

main()