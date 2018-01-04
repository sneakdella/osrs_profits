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
        finished_product_price = finished_product_price * int(15)
    if base == 'Extended antifire':
        secondary_A_price = secondary_A_price * int(4)
        secondary_A = 'Lava scales shard (x4)'
        base = 'Extended antifire(4)'
    if base == 'Anti-venom':
        secondary_A_price = secondary_A_price * int(15)
        secondary_A = "Zulrah's scales (x20)"
        finished_product = 'Anti-venom(4)'
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
    serum_207 = herblore_combo('Serum 207')
    guam_tar = herblore_combo('Guam tar')
    restore_pot = herblore_combo('Restore potion')
    energy_pot = herblore_combo('Energy potion')
    #noblamishoil
    defence_pot = herblore_combo('Defence potion')
    marrentill_tar = herblore_combo('Marrentill tar')
    agility_pot = herblore_combo('Agility potion')
    combat_pot = herblore_combo('Combat potion')
    prayer_pot = herblore_combo('Prayer potion')
    tarromin_tar = herblore_combo('Tarromin tar')
    harralander_tar = herblore_combo('Harralander tar')
    super_atk_pot = herblore_combo('Super attack')
    super_antipoison_pot = herblore_combo('Superantipoison')
    fishing_pot = herblore_combo('Fishing potion')
    super_energy_pot = herblore_combo('Super energy')
    hunter_pot = herblore_combo('Hunter potion')
    super_str = herblore_combo('Super strength')
    weap_pois = herblore_combo('Weapon poison')
    sup_restore = herblore_combo('Super restore')
    sup_defence = herblore_combo('Super defence')
    anti_fire_pot = herblore_combo('Antifire potion')
    ##
    range_pot = herblore_combo('Ranging potion')
    magic_pot = herblore_combo('Magic potion')
    stam_pot = herblore_combo('Stamina potion')
    sara_brew = herblore_combo('Saradomin brew')
    extended_antifire = herblore_combo('Extended antifire')
    anti_venom = herblore_combo('Anti-venom')
    anti_venom_plus = herblore_combo('Anti-venom(+)')

    return [Attack_potion, Antipoison, str_potion, serum_207, guam_tar, restore_pot, energy_pot, defence_pot, 
            marrentill_tar, agility_pot, combat_pot, prayer_pot, tarromin_tar, harralander_tar, super_atk_pot,
            super_antipoison_pot, fishing_pot, super_energy_pot, hunter_pot, super_str, weap_pois, sup_restore,
            sup_defence, anti_fire_pot, range_pot, magic_pot, stam_pot, sara_brew, extended_antifire, anti_venom,
            anti_venom_plus]

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
        return one_to_one_combo(end_potion_3, 'Grimy guam leaf', 'Eye of newt')
    if end_potion == 'Antipoison':
        return one_to_one_combo(end_potion_3, 'Grimy marrentill', 'Unicorn horn dust')
    if end_potion == "Strength potion":
        return one_to_one_combo(end_potion_3, "Grimy tarromin", 'Limpwurt root')
    if end_potion == 'Serum 207':
        #requires a space
        end_potion_3 = end_potion + ' (3)'
        return one_to_one_combo(end_potion_3, 'Grimy tarromin', 'Ashes')
    if end_potion == 'Guam tar':
        #no need for (3) because its not a potion
        end_potion_3 = end_potion
        new_list = one_to_one_combo(end_potion_3, 'Grimy guam leaf', 'Swamp tar')
        #tars are made by the 15s
        new_list[0] = 'Guam Tar (x15)'
        return new_list
    if end_potion == 'Restore potion':
        return one_to_one_combo(end_potion_3, 'Grimy harralander', "Red spiders' eggs")
    if end_potion == 'Energy potion':
        return one_to_one_combo(end_potion_3, 'Grimy harralander', 'Chocolate dust')
    if end_potion == 'Defence potion':
        return one_to_one_combo(end_potion_3, 'Grimy ranarr weed', 'White berries')
    if end_potion == 'Marrentill tar':
        #no need for (3) because its not a potion
        end_potion_3 = end_potion
        new_list = one_to_one_combo(end_potion_3, 'Grimy marrentill', 'Swamp tar')
        #tars are made by the 15s
        new_list[0] = 'Marrentill Tar (x15)'
        return new_list
    if end_potion == 'Agility potion':
        return one_to_one_combo(end_potion_3, 'Toadflax', "Toad's legs")
    if end_potion == 'Combat potion':
        return one_to_one_combo(end_potion_3, 'Grimy harralander', 'Goat horn dust')
    if end_potion == 'Prayer potion':
        return one_to_one_combo(end_potion_3, 'Grimy ranarr weed', 'Snape grass')
    if end_potion == 'Tarromin tar':
        #no need for (3) because its not a potion
        end_potion_3 = end_potion
        new_list = one_to_one_combo(end_potion_3, 'Grimy tarromin', 'Swamp tar')
        #tars are made by the 15s
        new_list[0] = 'Tarromin Tar (x15)'
        return new_list
    if end_potion == 'Harralander tar':
        #no need for (3) because its not a potion
        end_potion_3 = end_potion
        new_list = one_to_one_combo(end_potion_3, 'Grimy harralander', 'Swamp tar')
        #tars are made by the 15s
        new_list[0] = 'Harralander Tar (x15)'
        return new_list
    if end_potion == 'Super attack':
        return one_to_one_combo(end_potion_3, 'Grimy irit leaf', 'Eye of newt')
    if end_potion == 'Superantipoison':
        return one_to_one_combo(end_potion_3, 'Grimy irit leaf', 'Unicorn horn dust')
    if end_potion == 'Fishing potion':
        return one_to_one_combo(end_potion_3, 'Grimy avantoe', 'Snape grass')
    if end_potion == 'Super energy':
        return one_to_one_combo(end_potion_3, 'Grimy avantoe', 'Mort myre fungus')
    if end_potion == 'Hunter potion':
        return one_to_one_combo(end_potion_3, 'Grimy avantoe', 'Kebbit teeth dust')
    if end_potion == 'Super strength':
        return one_to_one_combo(end_potion_3, 'Grimy kwuarm', 'Limpwurt root')
    if end_potion == 'Weapon poison':
        end_potion_3 = 'Weapon poison'
        return one_to_one_combo(end_potion_3, 'Grimy kwuarm', 'Dragon scale dust')
    if end_potion == 'Super restore':
        return one_to_one_combo(end_potion_3, 'Grimy snapdragon', "Red spiders' eggs")
    if end_potion == 'Super defence':
        return one_to_one_combo(end_potion_3, 'Grimy cadantine', 'White berries')
    if end_potion == 'Antifire potion':
        return one_to_one_combo(end_potion_3, 'Grimy lantadyme', 'Dragon scale dust')
    if end_potion == 'Ranging potion':
        return one_to_one_combo(end_potion_3, 'Grimy dwarf weed', 'Wine of zamorak')
    if end_potion == 'Magic potion':
        return one_to_one_combo(end_potion_3, 'Grimy lantadyme', 'Potato cactus')
    if end_potion == 'Stamina potion':
        return one_to_one_combo(end_potion_3, 'Super energy(4)', 'Amylase crystal')
    if end_potion == 'Zamorak brew':
        return one_to_one_combo(end_potion_3, 'Grimy torstol', 'Jangerberries')
    if end_potion == 'Saradomin brew':
        return one_to_one_combo(end_potion_3, 'Grimy toadflax', "Crushed nest")
    if end_potion == 'Extended antifire':
        # needs a space
        end_potion_3 = 'Extended antifire (4)'
        return one_to_one_combo(end_potion_3, 'Antifire potion(4)', 'Lava scale shard')
    if end_potion == 'Anti-venom':
        return one_to_one_combo('Anti-venom(3)', 'Antidote++(3)', "Zulrah's scales")
    if end_potion == 'Anti-venom(+)':
        end_potion_3 = 'Anti-venom+(4)'
        return one_to_one_combo(end_potion_3, 'Anti-venom(4)', 'Grimy torstol')

    else:
        print('Invalid Request')
        return 'Invalid Request'

'''
################################################################################################
#                                SPECIAL UTILITIES
################################################################################################

################################################################################################
'''