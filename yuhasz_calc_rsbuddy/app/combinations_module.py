import urllib
import re
import time
import json
from app.models import *
from datetime import datetime

'''
################################################################################################
#                                DATABASE QUERY                                                #
################################################################################################

################################################################################################
'''

def query_item_price(item_name):
    #query = Items.objects.raw("SELECT * FROM app_items WHERE item_name='" + str(item_name) + "'")
    query = Items.objects.filter(item_name=item_name).values('item_price')
    return query


'''
################################################################################################
#                       1 or multiple values for calculation?                                  #
################################################################################################
TERMS:

'base' = The "raw" material required. I.E... for herbs it would be the clean herb.
        for smithing it would be the Iron bar for example. For fletching it would be
        the longbow(u) or shortbow(u)

'secondary_A' = would be the first secondary ingredient. Such as spiders eggs. However,
                it is important to note that this should be the parameter to use for ingredients
                that require multiples. For example, it takes multiple swamptars to make tarrmonin
                tar.

################################################################################################
'''

def one_to_one_combo(finished_product, base, secondary_A):
    #Grab Query Sets
    finished_product_query = query_item_price(finished_product)
    base_query = query_item_price(base)
    secondary_A_query = query_item_price(secondary_A)
    #Call upon the queryset like a list and then grab the dictionary value from key 'item_price'
        # then assign it to a variable
    finished_product_price = finished_product_query[0]['item_price']
    base_price = base_query[0]['item_price']
    secondary_A_price = secondary_A_query[0]['item_price']
    #Check for multiplier item
    if secondary_A == 'Swamp tar':
        secondary_A_price = secondary_A_price * int(15)
    else:
        pass
    #Perform the calculations
    cost_to_produce = int(base_price) + int(secondary_A_price)
    net_profit = int(finished_product_price) - int(cost_to_produce)
    return [finished_product, base, base_price, secondary_A, secondary_A_price, cost_to_produce, finished_product_price, net_profit ]


################################################################################################
'''
################################################################################################
#                                EXECUTION
################################################################################################

################################################################################################
'''

def deploy_herbs():
    Attack_potion = herblore_combo('Attack potion')
    Antipoison = herblore_combo('Antipoison')
    str_potion = herblore_combo("Strength potion")
    return [Attack_potion, Antipoison, str_potion]

################################################################################################
'''
################################################################################################
#                                MAIN CODE                                                     #
################################################################################################

################################################################################################
'''


def herblore_combo(end_potion):
    clean_herbs = ['Guam leaf', 'Marrentill', 'Tarromin', 'Harralander', 'Ranarr weed', 
                   'Irit leaf', 'Avantoe', 'Kwuarm', 'Cadantine', 'Dwarf weed', 'Torstol', 
                   'Lantadyme', 'Toadflax', 'Snapdragon' ]
    end_potion_3 = end_potion + '(3)'
    if end_potion == 'Attack potion':
        return one_to_one_combo(end_potion_3, 'Guam leaf', 'Eye of newt')
    if end_potion == 'Antipoison':
        return one_to_one_combo(end_potion_3, 'Marrentill', 'Unicorn horn dust')
    if end_potion == "Strength potion":
        return one_to_one_combo(end_potion_3, "Tarromin", 'Limpwurt root')
    else:
        print('Invalid Request')
        return 'Invalid Request'

'''
################################################################################################
#                                SPECIAL UTILITIES
################################################################################################

################################################################################################
'''