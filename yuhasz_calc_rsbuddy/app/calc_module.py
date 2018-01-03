import urllib
import re
import time
import json
from app.models import *
from datetime import datetime 

'''
################################################################################################
#                               TIME HANDLERS                                                  #
################################################################################################
'''

def retrieve_db_update_time():
    filename = "app/db_last_update.txt"
    fr = open(filename, "r")
    DATA_FROM_FILE = fr.readline()
    fr.close()
    return DATA_FROM_FILE

def store_db_update_time():
    filename = "app/db_last_update.txt"
    fh = open(filename, "w")
    fh.write(str(datetime.now()))
    fh.close()

'''
################################################################################################
#                                DATABASE CREATION                                             #
################################################################################################
# 1.) def get_jsonparsed_data(url) ---- opens URL to any JSON page                             #
# 2.) def new_database() ---- will pull all the JSON data from RSBuddy and insert converted    #
#                             values into database                                             #
# 3.) def update_sepcific_prices() - NOT FINISHED!                                             #
# 4.) def display_entire_db() --- Will display the entire "Items" table from app_items.        #
################################################################################################
'''
################################################################## 1
def get_jsonparsed_data(url):
    '''
    Takes URL, Gives JSON
    '''
    response = urllib.request.urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)

################################################################## 2
def new_database():
    '''
    Refreshes: [id, item_name, item_price] of database
    '''
    url = ("https://rsbuddy.com/exchange/summary.json")
    x = get_jsonparsed_data(url)
    y = x.keys()
    for i in range(0,30000):
        d = str(i)
        try:
            ID = x[d]['id']
            NAME = x[d]['name']
            PRICE = x[d]['overall_average']
            print(ID, NAME, PRICE)
            T = Items(id=ID,item_name=NAME,item_price=PRICE)
            T.save()
        except:
            pass
    store_db_update_time()
    return url
################################################################## 3
def update_specific_prices():
    '''
    NOT FINISHED.
    Function will accept multiple IDs, with a maximum of 5 and update them individually.
    '''
    all_ids = [6, 2]
    object_save_counter = 0
    for i in range(len(all_ids)):
        A = all_ids[i]
        id_var = A
        try:
            object = Items.objects.get(pk=id_var)
            url = ("https://api.rsbuddy.com/grandExchange?a=guidePrice&i=" + str(id_var))
            ofj = get_jsonparsed_data(url)
            PRICE = ofj[id_var]['overall_average']
            object.item_price = int(PRICE)
            object.save()
            print("Updated Item: " + object.item_name)
            object_save_counter += 1
        except:
            null = "Item Does Not Exist"
            print("Item Does Not Exist")

    update = "Update Complete"
    print("Updated Price Objects Counter: ", object_save_counter)
    print(all_ids)
    return update, object_save_counter
################################################################## 4
def display_entire_db():
    '''
    Output: Items.id, Items.item_name, Items.item_price
    '''
    query_results = Items.objects.all()
    return query_results
################################################################## END DB CREATION FUNCTIONS
'''
################################################################################################
#                                DATABASE QUERY                                                #
################################################################################################
1.) fetch_price_from_db(item_name) -- will fetch only the price of the item by '%item_name%'
2.) fetch_from_db(item_name) -- will fetch all values in a list[dictionary{}] format
3.) fetch_exact_from_db(item_name) will fetch the EXACT item_name and return ONLY the item price
################################################################################################
'''
################################################################## 1
def fetch_price_from_db(item_name):
    query = Items.objects.filter(item_name__icontains=item_name).values('item_price')
    return query
################################################################## 2
def fetch_from_db(item_name):
    query = Items.objects.filter(item_name__icontains=item_name).values()
    return query
def fetch_exact_from_db(item_name):
    #query = Items.objects.raw("SELECT * FROM app_items WHERE item_name='" + str(item_name) + "'")
    query = Items.objects.filter(item_name=item_name).values('item_price')
    return query
################################################################## END DB QUERY FUNCTIONS
'''
################################################################################################
#                                VIEW DEPLOYMENT                                               #
################################################################################################
1.) deploy_all()

Store functions inside this function to automatically generate a table on the raw_materials page

variable = function('start_item', 'end_product', 'skill_selector', 'blast_furnace')

EXAMPLE:
raw_mats = one_to_one('logs', 'longbow (u), '1', '0')

2.) one_to_one(item_one, item_two, skill, blast_furnace) 
        - will return a list set for a 5 column table
        - will loop through all items alike and provide profit for the 5th column
        - ORE to BARs
        - LOGS to BOW(u)
        - blast_furnace must have a value, just put 0.
        - PUT A VALUE OF '0' FOR blast_furnace for it to NOT APPLY to BARS or ANYTHING!... A value must be present for it to work.
        - PUT A VALUE OF '1' FOR blast_furnace for it to APPLY to BARs.
################################################################################################
'''
################################################################################################# 1

def deploy_all():
    logs_to_longbow = one_to_one('logs', 'longbow (u)', '1', '0') #logs to longbow (u)
    logs_to_shortbow = one_to_one('logs', 'shortbow (u)', '1', '0') #logs to shortbow (u)
    ore_to_bar = one_to_one('ore', 'bar', '2', '0') #All ores to bars Iron and Up WITHOUT BLAST FURNACE
    ore_to_bar_bf = one_to_one('ore', 'bar', '2', '1') #All ores to bars Iron and Up WITH BLAST FURNACE
    logs_to_stock = one_to_one('logs', 'stock', '1', '0') #test for logs to crossbow stock
    grimy_to_clean_herbs = one_to_one('grimy', 'null', '3', '0') #All Grimy Herbs to Clean Herbs
    return [logs_to_longbow, logs_to_shortbow, ore_to_bar, ore_to_bar_bf, logs_to_stock, grimy_to_clean_herbs]

################################################################################################# 2
def one_to_one(item_one, item_two, skill, blast_furnace):
    '''
    Skill == 1 MEANS Cutting logs into bow Us
    Skill == 2 MEANS Ores TO Bars
    Skill == 3 MEANS Grimy Herbs to Clean Herbs
    '''
    raw_material = fetch_from_db(item_one)
    product = fetch_from_db(item_two)
    raw_list = [ ]
    product_list = [ ]
    #FOR FLETCHING LOGS TO U's
    if skill == '1':
        for i in range(len(raw_material)):
            r_name = raw_material[i]['item_name']
            raw_list.append(r_name)
        for i in range(len(product)):
            p_name = product[i]['item_name']
            product_list.append(p_name)
        both_lists = organize_skill_A(product_list, raw_list)
        calculations = calculate_skill_1(both_lists)
        packed = pack_A(both_lists, calculations[0], calculations[1], calculations[2])
        return packed
    #FOR SMITHING ORES TO BARS
    if skill == '2':
        for i in range(len(raw_material)):
            r_name = raw_material[i]['item_name']
            raw_list.append(r_name)
        for i in range(len(product)):
            p_name = product[i]['item_name']
            product_list.append(p_name)
        both_lists = organize_skill_A(product_list, raw_list)
        if blast_furnace == '0':
            calculations = calculate_skill_ORE_TO_BAR(both_lists, '0')
        elif blast_furnace == '1':
            calculations = calculate_skill_ORE_TO_BAR(both_lists, '1')
        else:
            print("INVALID CODE FOR BLAST FURNACE.")
        packed = pack_A(both_lists, calculations[0], calculations[1], calculations[2])
        return packed
    #FOR HERBLORE
    if skill == '3':
        for i in range(len(raw_material)):
            r_name = raw_material[i]['item_name']
            raw_list.append(r_name)
        clean_herbs = ['Guam leaf', 'Marrentill', 'Tarromin', 'Harralander', 'Ranarr weed', 'Irit leaf', 'Avantoe', 'Kwuarm', 'Cadantine', 'Dwarf weed', 'Torstol', 'Lantadyme', 'Toadflax', 'Snapdragon' ]
        both_lists = [raw_list, clean_herbs]
        calculations = calculate_skill_HERBLORE(both_lists)
        packed = pack_A(both_lists, calculations[0], calculations[1], calculations[2])
        return packed

################################################################################################# END VIEW DEPLOYMENT FUNCTIONS
'''
################################################################################################
#                   PULL AND ORGANIZE RAW MATERIALS AND FINAL PRODUCT LISTS                    #
################################################################################################
1.) organize_skill_A(product_list, raw_list)

            BECAUSE I WAS LAZY AND RELIED ON "icontains" QUERYSETS. Didn't know what an equals
            sign was until like yesterday.

            This can function can easily be fixed/deleted by applying a "item_name__exact" with 
            the ".filter()" to one of the query functions. Which I already did for herblore.
'''
################################################################################################# 1
def organize_skill_A(product_list, raw_list):
    '''
    FOR LOGS TO U's AND ores to bars
    '''
    new_raw_list = [ ]
    new_product_list = [ ]
    for i in range(len(product_list)):
        try:
            f = product_list[i]
            split_f = f.split()
            indicies = [p for p, o in enumerate(raw_list) if split_f[0] in o]
            #print("SPLITF: ", split_f)
            refined_item = raw_list[indicies[0]]
            #print("INDICIES: ", raw_list[indicies[0]])
            new_raw_list.append(refined_item)
        except:
            #print("Item Removed")
            pass
    for i in range(len(new_raw_list)):
        try:
            f = new_raw_list[i]
            split_f = f.split()
            indicies = [p for p, o in enumerate(product_list) if split_f[0] in o]
            #print("SPLITF: ", split_f)
            refined_item = product_list[indicies[0]]
            new_product_list.append(refined_item)
        except:
            #print("NONE")
            pass
    sorted(new_raw_list)
    sorted(new_product_list)
    return [new_raw_list, new_product_list]
################################################################################################ END OF PULL AND ORGANISE
'''
################################################################################################
#                                SKILL CALCULATIONS                                            #
################################################################################################
LOGS TO BOW U's - calculate_skill_1(both_lists)
ORE TO BARS - calculate_skill_ORE_TO_BAR(both_lists)
HERBLORE - calculate_skill_HERBLORE(both_lists)

Pretty sraightforward. All of the calculation functions are very similar, with a few minor
differences.
'''

####################################################################################### 1

def calculate_skill_1(both_lists):
    '''
    LOGS TO BOW U
    '''
    start_product = both_lists[0]
    end_product = both_lists[1]
    profit_list = [ ]
    start_prices_list = [ ]
    end_prices_list = [ ]
    for i in range(len(start_product)):
        end_product_price_query = fetch_price_from_db(end_product[i])
        start_product_price_query = fetch_price_from_db(start_product[i])
        end_product_price = end_product_price_query[0]['item_price']
        start_product_price = start_product_price_query[0]['item_price']
        profit = int(end_product_price) - int(start_product_price)
        profit_list.append(profit)
        start_prices_list.append(start_product_price)
        end_prices_list.append(end_product_price)
    return [profit_list, start_prices_list, end_prices_list]

####################################################################################### 2

def calculate_skill_ORE_TO_BAR(both_lists, blast_furnace):
    '''
    ORES TO BAR
    '''
    if blast_furnace == '0':
        A = 1
    elif blast_furnace == '1':
        A = 2
    start_product = both_lists[0]
    end_product = both_lists[1]
    profit_list = [ ]
    start_prices_list = [ ]
    end_prices_list = [ ]
    coal_query = fetch_price_from_db('Coal')
    coal_price = coal_query[0]['item_price']
    for i in range(len(start_product)):
        end_product_price_query = fetch_price_from_db(end_product[i])
        start_product_price_query = fetch_price_from_db(start_product[i])
        end_product_price = end_product_price_query[0]['item_price']
        start_product_price = start_product_price_query[0]['item_price']
        if end_product[i] == 'Iron bar':
            profit = int(end_product_price) - int(start_product_price)
            profit_list.append(profit)
        if end_product[i] == 'Gold bar':
            profit = int(end_product_price) - int(start_product_price)
            profit_list.append(profit)
        if end_product[i] == 'Silver bar':
            profit = int(end_product_price) - int(start_product_price)
            profit_list.append(profit)
        if end_product[i] == 'Steel bar':
            coal = int(coal_price) * (2/A)
            profit = int(end_product_price) - int(start_product_price) - coal
            profit_list.append(profit)
        if end_product[i] == 'Mithril bar':
            coal = int(coal_price) * (4/A)
            profit = int(end_product_price) - int(start_product_price) - coal
            profit_list.append(profit)
        if end_product[i] == 'Adamantite bar':
            coal = int(coal_price) * (6/A)
            profit = int(end_product_price) - int(start_product_price) - coal
            profit_list.append(profit)
        if end_product[i] == 'Runite bar':
            coal = int(coal_price) * (8/A)
            profit = int(end_product_price) - int(start_product_price) - coal
            profit_list.append(profit)
        start_prices_list.append(start_product_price)
        end_prices_list.append(end_product_price)
    return [profit_list, start_prices_list, end_prices_list]

####################################################################################### 3

def calculate_skill_HERBLORE(both_lists):
    '''
    HERBLORE
    '''
    start_product = both_lists[0]
    end_product = both_lists[1]
    profit_list = [ ]
    start_prices_list = [ ]
    end_prices_list = [ ]
    for i in range(len(start_product)):
        end_product_price_query = fetch_exact_from_db(end_product[i])
        start_product_price_query = fetch_exact_from_db(start_product[i])
        end_product_price = end_product_price_query[0]['item_price']
        start_product_price = start_product_price_query[0]['item_price']
        profit = int(end_product_price) - int(start_product_price)
        profit_list.append(profit)
        start_prices_list.append(start_product_price)
        end_prices_list.append(end_product_price)
    return [profit_list, start_prices_list, end_prices_list]

###################################################################################### END OF CALCULATION FUNCTIONS

'''
#######################################################################################
#                            PACK FOR HTML VIEWING                                    #
#######################################################################################
1.) pack_A(both_lists, profits, start_prices_list, end_prices_list)

This function is by far the most important. This will take all of the data and aggregate
it into a single list. This is what essentially forms the row in the table on the HTML 
page when the 'for loop' is called.

This packs a SINGLE ROW, so the foreign function that is calling this function needs
to loop. We are packing a bunch of lists into another list (2D list). A list of lists.

'''

def pack_A(both_lists, profits, start_prices_list, end_prices_list):
    set_range = both_lists[0]
    start_product_list = both_lists[0]
    end_product_list = both_lists[1]
    packed_list = [ ]
    for i in range(len(set_range)):
        new_list = [start_product_list[i], start_prices_list[i], end_product_list[i], end_prices_list[i], profits[i]]
        packed_list.append(new_list)
    return packed_list

####################################################################################### END OF PACK
#######################################################################################
#######################################################################################
####################################################################################### END OF ALL PROGRAM CODE
'''
#######################################################################################
#                                END OF CODE                                          #
#######################################################################################
#######################################################################################
################################ OLD CODE BELOW #######################################

'''
'''
def grab_attrib(variable, attrib):
    variable_set = [ ]
    if attrib == 'item_name':
        for each in range(len(variable)):
            i = variable[each].item_name
            variable_set.append(i)
        return variable_set
    if attrib == 'id':
        for each in range(len(variable)):
            i = variable[each].id
            variable_set.append(i)
        return variable_set
    if attrib == 'item_price':
        for each in range(len(variable)):
            i = variable[each].item_price
            variable_set.append(i)
        return variable_set
    else:
        variable_set.append('Invalid Attribute')
        return variable_set

def run_query(contain, attrib):
    query = Items.objects.filter(item_name__icontains=contain)
    set_1 = grab_attrib(query, attrib)
    return set_1
'''
'''
'''
'''
    def string_bows():
        #bow minus string
        #bow minus log and string
    def projectiles_arrows():
        #arrows minus arrow tips
        #10 arrows minus (1 bar)
    def progectiles_bolts():
        #bolts minus bolt tips
        #10 bolttips minus uncet gem
        #10 bolts minus uncut gem
    def darts():
        #darts minus dart-tips
        #10 dart-tips minus bar
        #10 darts minus bar
        return 0
    def javelins():
        #5 javelin heads minus one bar
        #5 javelins per bar
        return 0
    return 1

def cooking():

    return 1

'''
'''

This one below is just absolutely horrendous. Never, ever, ever, ever use this shit.

def fetch_items(item_1, item_2, prohibited_list):

#    Runs Queries and relates one item to another.
#    The loop will loop for each item in the length of the querylist
#    j is assigned to each object of the querylist
#    j is then split to get the first element. I.E. so if it's Willow longbow (u), it will split it to make a list with the three elements "Willow, longbow, (u)"
#    Then it will call upon split_j[0], because we want the first element which is "Willow"
#    THEN, it moves onto indicies. The indicies variable executes an expression that will look for "Willow" aka split_j[0] in query_3 which is a querylist of logs.
#    indicies will then return the index of the item 'Willow logs' using only the string 'Willow'. Note the indicies command will return ALL elements that match split_j[0]... so if there is Willow Logs and Willow Fire Logs, it will return both!
#    Then the variable f is used to grab 'Willow Logs' from query3 with the indicies as the variable for the index number.
#    In the loop a new list is created to store both j AKA 'Willow longbow (u)' and f AKA 'Willow Logs'


    query = run_query(item_1, 'item_name')
    query_2 = run_query(item_2, 'item_name')
    query_set_list = [ ]
    for i in range(len(query)):
        if query[i] not in prohibited_list:
            j = query[i]
            split_j = j.split()
            print("SPLIT_J: " + str(split_j))
            print("SPLTI_J[0]: " + str(split_j[0]))
            indicies = [p for p, o in enumerate(query_2) if split_j[0] in o]
            print("INDICIES: ", indicies)
            try:
                f = query_2[indicies[0]]
                print(f)
                price_j = run_query(j, 'item_price')
                price_f = run_query(f, 'item_price')
                profit = price_j[0] - price_f[0]
                new_list = [str(f), str(price_f[0]), str(j), str(price_j[0]), str(profit)]
                query_set_list.append(new_list)
            except:
                print("Nothing")
        
    return query_set_list

def fletching_fetch(item_1, item_2):
    prohibited_list = ['Longbow (u)', 'Shortbow (u)']
    return fetch_items(item_1, item_2, prohibited_list)
'''
##########################
##########################
########OLD CODE##########
##########################

#This function will update the db
#def new_database():
#    #ITEM_ID, ITEM_NAME
#    me_list = [ ]
#    f = urllib.request.urlopen('https://rsbuddy.com/exchange/summary.json')
#    html = f.read().decode('utf-8')
#    words = re.split('}', html)
#    c = len(words)
#    second_counter = 0
#    for i in range(c):
#        A = words[i]
#        B = re.split('{|"|,|:|}', A)
#        C = [x for x in B if x !='']
#        D = [x for x in C if x !=' ']
#        print(D)
#        #time.sleep(10)
#        me_list.append(D)
#       count = len(D)
#        if count == 15:
#            print('Item_ID: ',D[0])
#            print('Item_Name: ', D[2])
#            print('Item_price: ', D[10])
#            T = Items(id=D[0],item_name=D[2],item_price=D[10])
#            T.save()
#            second_counter += 1
#            print("Saved " + str(second_counter) + " objects to database.")
#        else:
#            print("SKIPPED")
#    return me_list


################################

#def update_specific_prices():
#    all_ids = [6, 2]
#    object_save_counter = 0
#    for i in range(len(all_ids)):
#        A = all_ids[i]
#        id_var = A
#        try:
#            object = Items.objects.get(pk=id_var)
#            f = urllib.request.urlopen('https://api.rsbuddy.com/grandExchange?a=guidePrice&i='+ str(id_var))
#            html = f.read().decode('utf-8')
#            words = re.split('{|"|,|:|\s|}', html)
#            words = [x for x in words if x !='']
#            list_names = [ ]
#            list_names.append(words[1])
#            list_names.append(object.item_name)
#            object.item_price = int(words[1])
#            object.save()
#            print("Updated Item: " + object.item_name)
#            object_save_counter += 1
#        except:
#            null = "null"
#            print(id_var)
#            print(type(id_var))
#    update = "Update Complete"
#    print(object_save_counter)
#    print(all_ids)
#    return update, object_save_counter
#####################################################################
#def fletching():
#    retrieval_error = "Error recieving from db. Invalid key."
#    def cut_bows():
#        #bow(u) minus log
#        logs = Items.objects.get(pk=1511)
#        oak_logs = Items.objects.get(pk=1521)
#        willow_logs = Items.objects.get(pk=1519)
#        maple_logs = Items.objects.get(pk=1517)
#        yew_logs = Items.objects.get(pk=1515)
#        magic_logs = Items.objects.get(pk=1513)
#        log_list = [ logs, oak_logs, willow_logs, maple_logs, yew_logs, magic_logs ]
#        #####
#        shortbow_u = Items.objects.get(pk=50)
#        oak_shortbow_u = Items.objects.get(pk=54)
#        willow_shortbow_u = Items.objects.get(pk=60)
#        maple_shortbow_u = Items.objects.get(pk=64)
#        yew_shortbow_u = Items.objects.get(pk=68)
#        magic_shortbow_u = Items.objects.get(pk=72)
#        shortbow_u_list = [shortbow_u, oak_shortbow_u, willow_shortbow_u, maple_shortbow_u, yew_shortbow_u, magic_shortbow_u]
#        profit_log_shortbow_list = [ ]
#        for i in range(len(log_list)):
#            le_name = log_list[i].item_name
#            le_price = log_list[i].item_price
#            le_shortbow_name = shortbow_u_list[i].item_name
#            le_shortbow_price = shortbow_u_list[i].item_price
#            le_profit = le_shortbow_price - le_price
#            data_set_list = [ le_name, le_price, le_shortbow_name, le_shortbow_price, le_profit ]
#            profit_log_shortbow_list.append(data_set_list)
#        return profit_log_shortbow_list
#    return cut_bows()