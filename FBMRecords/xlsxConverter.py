import xlrd
import tweepy

#api keys to access twitter endpoints
CONSUMER_KEY        = ""
CONSUMER_SECRET     = ""
ACCESS_TOKEN        = ""
ACCESS_TOKEN_SECRET = ""

#initializes tweepy
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def convert():

    #empty list to store all of the @handles
    handles = []

    workbook = xlrd.open_workbook(r'twitterbot.xlsx', on_demand = True)
    worksheet = workbook.sheet_by_index(0)
    first_row = [] # The row where we stock the name of the column
    for col in range(worksheet.ncols):
        first_row.append( worksheet.cell_value(0,col) )
    # transform the workbook to a list of dictionaries
    data =[]
    for row in range(1, worksheet.nrows):
        elm = {}
        for col in range(worksheet.ncols):
            elm[first_row[col]]=worksheet.cell_value(row,col)
        data.append(elm)

    #only appends all of the @handles to the list
    for playersAndHandles in data:
        for key, value in playersAndHandles.items():
            if (key == "Handle"):
                handles.append(value)

    #empty list to store all of the UIDs that we are able to get by using the @handle
    UIDS = []

    for handle in handles:
        try:
            print(f"Converting: {handle}")
            user = api.get_user(handle)
            handle = user.id_str
            print(f"Converted: {handle}")
            UIDS.append(handle)
        except:
            print(f"User {handle} not found. Contining")

    #writes to a text file so that twitterbot.py can access it
    with open (r"UIDS.txt", 'w') as f:
        for UID in UIDS:
            f.write(UID)
            f.write("\n")

convert()