from twilio.rest import TwilioRestClient 
 
# put your own credentials here 
ACCOUNT_SID = "ACd5d1f7c8bb9abc59170ecac5cfb3f9d7" 
AUTH_TOKEN = "4286e55f20da4ce0c34a033fc2dceaed" 
 
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 

client.messages.create(
    to="+919873522005", 
    from_="+12517322200", 
    body="My Name is Sukhmeet Singh.Yo", 
    media_url="https://c1.staticflickr.com/3/2899/14341091933_1e92e62d12_b.jpg", 
)