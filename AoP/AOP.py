from tkinter import *
from time import sleep
from enum import Enum, auto
from PIL import Image, ImageTk
import os
import math

# --- TO-DO ---
#
# 
#
# People:
#
#  Happiness increased by one if there are no homeless people -done
#  Park price exponentially increases per bought park - done
#  Add menu where you can hire more than one philosopher at a time
#
# Economy:
#
#  Prefix system for above 999 of any resource - done
#  Happiness affects output of production - done
#
# Philosophy tree:
#
#  Adding/removing philosiphers - done
#  Unlockable buildings - done
#  Building at least one 'Festival tent' unlocks 'events' on the main menu - an event can be activated at a cost then last for a certain number of ticks, can be extended
#
# Important
#
#  Civilisation development level - designed ( Ages )
#  Saving/Loading - done
#  Learn how to create a py to an excecutable
#  Completely build the festival menu and systems
#
# Continuous:  # Have to be done somewhat regularly
# 
#  Update save/load functions
#  Increase available prefixes - Up to DuoDe
#  Add new buildings
#
# Bugs:
#
#  Large numbers mess up the building GUIs - fixed
#  Building a wood camp does not affect the wood gain rate - fixed
#  Tavern philosophy menu back goes to building not building branch - fixed
#  Loading before save crashes game - fixed
#  Going to next menu before unlocked crashes the game - fixed
#  Loading system keeps extra happiness even if there are homeless people - fixed
#  Pop still increases too fast in latergame  - fixed
#  Missed a load item - fixed
#  After loading a save, all philosophies are unlocked - fixed
#  Festival tent menu not showing 'Festival tent philosophised' when done - fixed
#  Unemployed potentiallly calculated incorrectly at higher numbers - unknown
#  Philosophy does not increase when not in philosophy menu - feature

root = Tk()
root.title("The Ages Of Production")
root.geometry("500x450")
root.configure(bg="#121212")
p1 = PhotoImage(file='AoPImg.png')
root.iconphoto(False, p1)
file = open("AoPsavedata.txt", "a")
file.close()
screen = Text(root, width=60, height=20, bg="#212121", bd="0", fg="white", insertbackground="white", font="Georgia")
screen.configure(state="disabled")
screen.pack(pady=20, padx=20, expand=True)


class Menu(Enum):
    MAIN = auto()
    SAVEMENU = auto()
    LOADMENU = auto()

    BUILD = auto()
    HOUSE = auto()
    FARM = auto()
    LUMBER_CAMP = auto()
    PARK = auto()
    CARPENTRY = auto()
    MILL = auto()
    TAX_OFFICE = auto()
    OBSERVATORY = auto()
    TAVERN = auto()
    BUILD2 = auto()
    PHARMACY = auto()
    FESTIVALTENT = auto()

    BREAKDOWN = auto()
    PEOPLE_BREAKDOWN = auto()
    BUILDING_BREAKDOWN = auto()
    BUILDING_BREAKDOWN2 = auto()

    ECONOMY = auto()
    TAX = auto()

    PHILOSOPHY = auto()
    PHILOSOPHY_TREE = auto()
    BUILDING_BRANCH = auto()
    BUILDING_BRANCH2 = auto()
    CARPENTRY_PHILOSOPHY = auto()
    TAX_OFFICE_PHILOSOPHY = auto()
    MILL_PHILOSOPHY = auto()
    OBSERVATORY_PHILOSOPHY = auto()
    TAVERN_PHILOSOPHY = auto()
    PHARMACY_PHILOSOPHY = auto()
    FESTIVALTENT_PHILOSOPHY = auto()
    GOLDENSTATUE_PHILOSOPHY = auto()
    GOLDENSTATUE_MENU = auto()
    CONFIRM_RENNISSANCE = auto()
    RENNISSANCE_CHANGELOG = auto()

    FESTIVALMENU = auto()
    FESTIVALCHOICESMENU = auto()
    FESTIVALSMENU = auto()



class Role(Enum):
    MILLER = auto()
    CARPENTER = auto()
    PHILOSIPHIST = auto()
    TAX_COLECTER = auto()
    FARMER = auto()
    UNEMPLOYED = auto()
    LUMBERJACK = auto()


class Game:
    def __init__(self):
        self.age = 1
        self.menu = Menu.MAIN
        self.house = 20
        self.farm = 1
        self.park = 1
        self.lumber_camp = 1
        self.carpentry = 0
        self.tax_office = 0
        self.mill = 0
        self.tavern = 0.5
        self.pharmacy = 1
        self.festival_tent = 0
        self.lumberjack = 0
        self.philosopher = 0
        self.carpenter = 0
        self.miller = 0
        self.tax_collector = 0
        self.pharmacist = 0
        self.observatory = 0
        self.farmer = 0
        self.homeless = 0
        self.criminals = 0
        self.pop = 0
        self.true_pop = 0
        self.pop_growth = (((2 ** (math.sqrt(self.pharmacy+1))))/200 + (self.pop / 20000))
        self.tax = 0.1
        self.true_gold = 0
        self.food = 0
        self.true_food = 10
        self.wood = 0
        self.true_wood = 0
        self.time = 1
        self.philosophies = 0
        self.carpentry_multiplier = 2 * self.carpentry
        self.mill_multiplier = 2 * self.mill
        self.tax_office_multiplier = 2 * self.tax_office
        self.final_multiplier = (1 * (2 * (self.tavern + 0.5))) ** (self.festival_tent + 1)+self.age/10
        self.play_music = True
        self.carpentry_Unlocked = False
        self.mill_Unlocked = False
        self.tax_office_Unlocked = False
        self.observatory_Unlocked = False
        self.tavern_Unlocked = False
        self.pharmacy_Unlocked = False
        self.festival_tent_Unlocked = False
        self.golden_statue_Unlocked = False
        self.time_since_last_play = 100
        self.men_main = True
        self.men_build = False
        self.men_law = False
        self.men_research = False
        self.men_economy = False
        self.Researching_carpentry = False
        self.Researching_mill = False
        self.Researching_tax_office = False
        self.Researching_observatory = False
        self.Researching_pharmacy = False
        self.Researching_festival_tent = False
        self.Researching_golden_statue = False
        self.Researching_tavern = 0
        self.carpentry_progress = 0
        self.mill_progress = 0
        self.tax_office_progress = 0
        self.observatory_progress = 0
        self.tavern_progress = 0
        self.pharmacy_progress = 0
        self.festival_tent_progress = 0
        self.goldenstatue_progress = 0
        self.settler_list = []
        self.building_list = [{'house': 2}, {'farm': 1}, {'lumber_camp': 1}, {'park': 1}, {'carpentry': 0}, {'mill': 0},
                              {'tax office': 0}, {'observatory': 0}, {'tavern': 0}, {'pharmacy': 0}, {'festival_tent': 0} ]
        self.key_input = ''
        self.gold_gain = (2 + (2 + (2 * (self.house * self.tax))) * (
                    self.tax_office_multiplier * 2)) * self.final_multiplier
        self.food_gain = (0.1 + (0.1 + (0.1 * self.farm)) * (self.mill_multiplier * 2) + 0.1) * self.final_multiplier
        self.wood_gain = (0.1 + (0.1 * self.lumber_camp) * (
                    (self.carpentry_multiplier + 0.1) * 2)) * self.final_multiplier
        self.happiness = ((1 * self.park) - (self.tax * 10))
        self.unemployed = self.true_pop - (
                    self.farmer + self.philosopher + self.lumberjack + self.carpenter + self.miller)
        self.park_gold_price = 1000 ** self.park
        self.park_wood_price = 100 ** self.park

    def prefix(self, num):
        num = int(num)
        if len(str(num)) < 4:
            return str(num)
        elif len(str(num)) == 4:
            return str(str(num)[0] + '.' + str(num)[1] + str(num)[2] + " k")
        elif len(str(num)) == 5:
            return str(str(num)[0] + str(num)[1] + '.' + str(num)[2] + ' k')
        elif len(str(num)) == 6:
            return str(str(num)[0] + str(num)[1] + str(num)[2] + ' k')
        elif len(str(num)) == 7:
            return str(str(num)[0] + '.' + str(num)[1] + str(num)[2] + " M")
        elif len(str(num)) == 8:
            return str(str(num)[0] + str(num)[1] + '.' + str(num)[2] + ' M')
        elif len(str(num)) == 9:
            return str(str(num)[0] + str(num)[1] + str(num)[2] + ' M')
        elif len(str(num)) == 10:
            return str(str(num)[0] + '.' + str(num)[1] + str(num)[2] + " B")
        elif len(str(num)) == 11:
            return str(str(num)[0] + str(num)[1] + '.' + str(num)[2] + ' B')
        elif len(str(num)) == 12:
            return str(str(num)[0] + str(num)[1] + str(num)[2] + ' B')
        elif len(str(num)) == 13:
            return str(str(num)[0] + '.' + str(num)[1] + str(num)[2] + " T")
        elif len(str(num)) == 14:
            return str(str(num)[0] + str(num)[1] + '.' + str(num)[2] + ' T')
        elif len(str(num)) == 15:
            return str(str(num)[0] + str(num)[1] + str(num)[2] + ' T')
        elif len(str(num)) == 16:
            return str(str(num)[0] + '.' + str(num)[1] + str(num)[2] + " Quad")
        elif len(str(num)) == 17:
            return str(str(num)[0] + str(num)[1] + '.' + str(num)[2] + ' Quad')
        elif len(str(num)) == 18:
            return str(str(num)[0] + str(num)[1] + str(num)[2] + ' Quad')
        elif len(str(num)) == 19:
            return str(str(num)[0] + '.' + str(num)[1] + str(num)[2] + " Quin")
        elif len(str(num)) == 20:
            return str(str(num)[0] + str(num)[1] + '.' + str(num)[2] + ' Quin')
        elif len(str(num)) == 21:
            return str(str(num)[0] + str(num)[1] + str(num)[2] + ' Quin')
        elif len(str(num)) == 22:
            return str(str(num)[0] + '.' + str(num)[1] + str(num)[2] + " Sx")
        elif len(str(num)) == 23:
            return str(str(num)[0] + str(num)[1] + '.' + str(num)[2] + ' Sx')
        elif len(str(num)) == 24:
            return str(str(num)[0] + str(num)[1] + str(num)[2] + ' Sx')
        elif len(str(num)) == 25:
            return str(str(num)[0] + '.' + str(num)[1] + str(num)[2] + " Sp")
        elif len(str(num)) == 26:
            return str(str(num)[0] + str(num)[1] + '.' + str(num)[2] + ' Sp')
        elif len(str(num)) == 27:
            return str(str(num)[0] + str(num)[1] + str(num)[2] + ' Oc')
        elif len(str(num)) == 28:
            return str(str(num)[0] + '.' + str(num)[1] + str(num)[2] + " Oc")
        elif len(str(num)) == 29:
            return str(str(num)[0] + str(num)[1] + '.' + str(num)[2] + ' Oc')
        elif len(str(num)) == 30:
            return str(str(num)[0] + str(num)[1] + str(num)[2] + ' Oc')
        elif len(str(num)) == 31:
            return str(str(num)[0] + '.' + str(num)[1] + str(num)[2] + " No")
        elif len(str(num)) == 32:
            return str(str(num)[0] + str(num)[1] + '.' + str(num)[2] + ' No')
        elif len(str(num)) == 33:
            return str(str(num)[0] + str(num)[1] + str(num)[2] + ' No')
        elif len(str(num)) == 34:
            return str(str(num)[0] + '.' + str(num)[1] + str(num)[2] + " De")
        elif len(str(num)) == 35:
            return str(str(num)[0] + str(num)[1] + '.' + str(num)[2] + ' De')
        elif len(str(num)) == 36:
            return str(str(num)[0] + str(num)[1] + str(num)[2] + ' De')
        elif len(str(num)) == 37:
            return str(str(num)[0] + '.' + str(num)[1] + str(num)[2] + "UnDe")
        elif len(str(num)) == 38:
            return str(str(num)[0] + str(num)[1] + '.' + str(num)[2] + ' UnDe')
        elif len(str(num)) == 39:
            return str(str(num)[0] + str(num)[1] + str(num)[2] + ' UnDe')
        elif len(str(num)) == 40:
            return str(str(num)[0] + '.' + str(num)[1] + str(num)[2] + " DuoDe")
        elif len(str(num)) == 41:
            return str(str(num)[0] + str(num)[1] + '.' + str(num)[2] + ' DuoDe')
        elif len(str(num)) == 42:
            return str(str(num)[0] + str(num)[1] + str(num)[2] + ' DuoDe')
        else:
            return str(str(num)[0] + str(num)[1] + str(num)[2] + ' !?!')

    def get_settler_list(self):
        return self.settler_list

    def snip(self, num):
        num = num * 100
        num = int(num)
        num /= 100
        return num

    def main(self):
        clear()
        root.bind('<KeyPress>', self.key_press)
        self.mat_change()
        self.menu_manager()
        self.game_clock()

    def Add_settler(self, role, happines, hunger, health):
        self.true_pop += 1
        settler = Settler(role, happines, hunger, health)
        self.settler_list.append(settler)

    def key_press(self, e):
        self.key_input = e.char

    def menu_manager(self):
        if self.menu == Menu.MAIN:
            if self.key_input == '1':
                self.key_input = ''
                self.menu = Menu.BUILD
                self.build_menu()
            elif self.key_input == "2":
                self.key_input = ''
                self.menu = Menu.PHILOSOPHY
                self.philosophy_menu()
            elif self.key_input == "0":
                self.key_input = ''
                self.main_menu()
            elif self.key_input == "3":
                self.menu = Menu.ECONOMY
                self.economy_menu()
            elif self.key_input == "4":
                self.key_input = ''
                self.menu = Menu.BREAKDOWN
                self.breakdown_menu()
            elif self.key_input == "5" and self.festival_tent_Unlocked == True:
                self.key_input = ''
                self.menu = Menu.FESTIVALMENU
                self.festival_menu()
            ##            elif self.key_input == 'g':
            ##                self.key_input =''
            ##                self.menu = Menu.MAIN
            ##                self.park += 30000000
            ##                self.observatory_Unlocked = True
            ##                self.observatory += 300
            elif self.key_input == 'e':
                            self.key_input =''
                            self.menu = Menu.MAIN
                            self.true_gold += 100000000000000000000000000000000000000000000000000000000
                            self.true_wood += 100000000000000000000000000000000000000000000000000000000
                            self.true_food += 100000000000000000000000000000000000000000000000000000000
                            print('Observatory dev tool: active')
                            self.pharmacy_Unlocked = True
                            self.observatory_Unlocked = True
                            self.festival_tent_Unlocked = True
                            self.festival_tent_progress = 49999
                            self.observatory += 30
            elif self.key_input == "l":
                self.key_input == ''
                self.menu = Menu.LOADMENU
                self.load_menu()
            elif self.key_input == 's':
                self.key_input = ''
                self.menu = Menu.SAVEMENU
                self.save_menu()
            else:
                self.main_menu()


        elif self.menu == Menu.BUILD:
            if self.key_input == '1':
                self.key_input = ''
                self.menu = Menu.MAIN
                self.main_menu()
            elif self.key_input == '2':
                self.key_input = ''
                self.menu = Menu.HOUSE
                self.house_menu()
            elif self.key_input == '3':
                self.key_input = ''
                self.menu = Menu.FARM
                self.farm_menu()
            elif self.key_input == '4':
                self.key_input = ''
                self.menu = Menu.LUMBER_CAMP
                self.lumber_camp_menu()
            elif self.key_input == '5':
                self.key_input = ''
                self.menu = Menu.PARK
                self.park_menu()
            elif self.key_input == '6' and self.carpentry_Unlocked == True:
                self.key_input = ''
                self.menu = Menu.CARPENTRY
                self.carpentry_menu()
            elif self.key_input == '7' and self.mill_Unlocked == True:
                self.key_input = ''
                self.menu = Menu.MILL
                self.mill_menu()
            elif self.key_input == '8' and self.tax_office_Unlocked == True:
                self.key_input = ''
                self.menu = Menu.TAX_OFFICE
                self.tax_office_menu()
            elif self.key_input == '9' and self.observatory_Unlocked == True:
                self.key_input = ''
                self.menu = Menu.OBSERVATORY
                self.observatory_menu()
            elif self.key_input == '0':
                self.key_input = ''
                self.menu = Menu.BUILD2
                self.build_menu2()
            else:
                self.build_menu()


        elif self.menu == Menu.ECONOMY:
            if self.key_input == "1":
                self.key_input = ''
                self.menu = Menu.MAIN
                self.main_menu()
            elif self.key_input == "0":
                self.key_input = ''
                self.menu = Menu.ECONOMY
                self.economy_menu()
            elif self.key_input == "2":
                self.key_input = ''
                self.menu = Menu.TAX
                self.tax_menu()

            else:
                self.economy_menu()


        elif self.menu == Menu.BREAKDOWN:
            if self.key_input == "1":
                self.key_input = ''
                self.menu = Menu.MAIN
                self.main_menu()
            elif self.key_input == "0":
                self.key_input = ''
                self.menu = Menu.BREAKDOWN

                self.breakdown_menu()
            elif self.key_input == "2":
                self.key_input = ''
                self.menu = Menu.PEOPLE_BREAKDOWN
                self.people_breakdown_menu()
            elif self.key_input == "3":
                self.key_input = ''
                self.menu = Menu.BUILDING_BREAKDOWN
                self.building_breakdown_menu()

            else:
                self.breakdown_menu()


        elif self.menu == Menu.PEOPLE_BREAKDOWN:
            if self.key_input == "1":
                self.key_input = ''
                self.menu = Menu.BREAKDOWN
                self.breakdown_menu()
            else:
                self.people_breakdown_menu()

        elif self.menu == Menu.BUILDING_BREAKDOWN:
            if self.key_input == "1":
                self.key_input = ''
                self.menu = Menu.BREAKDOWN
                self.breakdown_menu()
            elif self.key_input == "2":
                self.key_input == ''
                self.menu = Menu.BUILDING_BREAKDOWN2
                self.building_breakdown2_menu()
            else:
                self.building_breakdown_menu()
        elif self.menu == Menu.BUILDING_BREAKDOWN2:
            if self.key_input == "1":
                self.key_input = ''
                self.menu = Menu.BUILDING_BREAKDOWN
                self.building_breakdown_menu()
            else:
                self.building_breakdown2_menu()
        elif self.menu == Menu.PHILOSOPHY:
            if self.key_input == "1":
                self.key_input = ''
                self.menu = Menu.MAIN
                self.main_menu()
            elif self.key_input == "0":
                self.key_input = ''
                self.menu = Menu.PHILOSOPHY
                self.philosophy_menu()
            elif self.key_input == "2":
                self.key_input = ''
                self.menu = Menu.PHILOSOPHY_TREE
                self.philosophy_tree_menu()
            elif self.key_input == "3":
                self.key_input = ''
                if self.unemployed >= 1:
                    self.philosophy_menu()
                    self.philosopher += 1
                    self.unemployed -= 1
                    self.unemployed = self.true_pop - (
                                self.farmer + self.philosopher + self.lumberjack + self.carpenter + self.miller)
                else:
                    self.philosophy_menu()
                    write("\n\n Not enough unemployed people")
            elif self.key_input == "4":
                self.key_input = ''
                self.philosophy_menu()
                if self.philosopher >= 1:
                    self.philosopher -= 1
                    self.unemployed += 1
                    self.unemployed = self.true_pop - (
                                self.farmer + self.philosopher + self.lumberjack + self.carpenter + self.miller)
                else:
                    self.philosophy_menu()
                    write("\n\nNot enough Philosophers")
            else:
                self.philosophy_menu()

        elif self.menu == Menu.BUILD2:
            if self.key_input == "1":
                self.key_input = ''
                self.menu = Menu.BUILD
                self.build_menu()
            elif self.key_input == "2" and self.tavern_Unlocked == True:
                self.key_input = ''
                self.menu = Menu.TAVERN
                self.tavern_menu()
            elif self.key_input == "3" and self.pharmacy_Unlocked == True:
                self.key_input = ''
                self.menu = Menu.PHARMACY
                self.pharmacy_menu()
            elif self.key_input == "4" and self.festival_tent_Unlocked == True:
                self.key_input = ''
                self.menu = Menu.FESTIVALTENT
                self.festival_tent_menu()
            else:
                self.build_menu2()

        elif self.menu == Menu.FARM:
            if self.key_input == '1':

                self.key_input = ''
                self.menu = Menu.BUILD
                self.build_menu()
            elif self.key_input == "0":
                self.key_input = ''
                self.farm_menu()
            else:
                self.farm_menu()

        elif self.menu == Menu.HOUSE:
            if self.key_input == '1':
                self.key_input = ''
                self.menu = Menu.BUILD
                self.build_menu()
            elif self.key_input == "0":
                self.key_input = ''
                self.house_menu()
            else:
                self.house_menu()


        elif self.menu == Menu.LUMBER_CAMP:
            if self.key_input == '1':
                self.key_input = ''
                self.menu = Menu.BUILD
                self.build_menu()
            elif self.key_input == "0":
                self.key_input = ''
                self.lumber_camp_menu()
            else:
                self.lumber_camp_menu()
        elif self.menu == Menu.PARK:
            if self.key_input == '1':
                self.key_input = ''
                self.menu = Menu.BUILD
                self.build_menu()
            elif self.key_input == "0":
                self.key_input = ''
                self.park_menu()
            else:
                self.park_menu()

        elif self.menu == Menu.TAX:
            if self.key_input == '1':
                self.key_input = ''
                self.menu = Menu.ECONOMY
                self.build_menu()
            elif self.key_input == "0":
                self.key_input = ''
                self.tax_menu()
            elif self.key_input == "2":
                if self.tax < 0.99:
                    self.key_input = ''
                    self.tax += 0.1
                    self.happiness = ((1 * self.park) - (self.tax * 10))
                    self.gold_gain = (2 + (2 + (2 * (self.house * self.tax))) * (
                                self.tax_office_multiplier * 2)) * self.final_multiplier
                    self.tax_menu()
                else:
                    self.tax_menu()
                    write("\nMaximum tax  rate reached!")
            elif self.key_input == "3":
                if self.tax > 0.1:
                    self.key_input = ''
                    self.tax -= 0.1
                    self.happiness = ((1 * self.park) - (self.tax * 10))
                    self.gold_gain = (2 + (2 + (2 * (self.house * self.tax))) * (
                                self.tax_office_multiplier * 2)) * self.final_multiplier
                    self.tax_menu()
                else:
                    self.tax_menu()
                    write("\nMinimum tax  rate reached!")
            else:
                self.tax_menu()


        elif self.menu == Menu.PHILOSOPHY_TREE:
            if self.key_input == '1':
                self.key_input = ''
                self.menu = Menu.PHILOSOPHY
                self.philosophy_menu()
            elif self.key_input == "0":

                self.key_input = ''
                self.philosophy_tree_menu()
            elif self.key_input == "2":
                self.key_input = ''
                self.menu = Menu.BUILDING_BRANCH
                self.building_branch_menu()
            else:
                self.philosophy_tree_menu()

        elif self.menu == Menu.BUILDING_BRANCH:
            if self.key_input == '1':
                self.key_input = ''
                self.menu = Menu.PHILOSOPHY_TREE
                self.philosophy_tree_menu()
            elif self.key_input == "0":
                self.key_input = ''
                self.building_branch_menu()
            elif self.key_input == "2":
                self.key_input = ''
                self.menu = Menu.CARPENTRY_PHILOSOPHY
                self.carpentry_philosophy_menu()
            elif self.key_input == "3":
                self.key_input = ''
                self.menu = Menu.MILL_PHILOSOPHY
                self.mill_philosophy_menu()
            elif self.key_input == "4":
                self.key_input = ''
                self.menu = Menu.TAX_OFFICE_PHILOSOPHY
                self.tax_office_philosophy_menu()
            elif self.key_input == "5":
                self.key_input = ''
                self.menu = Menu.OBSERVATORY_PHILOSOPHY
            elif self.key_input == "6":
                self.key_input = ''
                self.menu = Menu.TAVERN_PHILOSOPHY
                self.tavern_philosophy_menu()
            elif self.key_input == "7":
                self.key_input = ''
                self.menu = Menu.PHARMACY_PHILOSOPHY
                self.pharmacy_philosophy_menu()
            elif self.key_input == "8":
                self.key_input = ''
                self.menu = Menu.OBSERVATORY_PHILOSOPHY
                self.observatory_philosophy_menu()
            elif self.key_input == "9":
                self.key_input = ''
                self.menu = Menu.FESTIVALTENT_PHILOSOPHY
                self.festival_tent_philosophy_menu()
            elif self.key_input == "0":
                self.key_input = ''
                self.menu = Menu.BUILDING_BRANCH2
                self.building_branch2_menu()
            else:
                self.building_branch_menu()
        elif self.menu == Menu.BUILDING_BRANCH2:
            if self.key_input == "1":
                self.key_input = ''
                self.menu = Menu.BUILDING_BRANCH
                self.building_branch_menu()
            elif self.key_input == "2":
                self.key_input = ''
                self.menu = Menu.GOLDENSTATUE_PHILOSOPHY
                self.goldstatue_menu()



        elif self.menu == Menu.CARPENTRY_PHILOSOPHY:
            if self.key_input == '1':
                self.key_input = ''
                self.menu = Menu.BUILDING_BRANCH
                self.building_branch_menu()
            elif self.key_input == "0":

                self.key_input = ''
                self.carpentry_philosophy_menu()
            elif self.key_input == "2":
                self.key_input = ''
                self.Researching_carpentry = True
                self.carpentry_philosophy_menu()
            else:
                self.carpentry_philosophy_menu()

        elif self.menu == Menu.MILL_PHILOSOPHY:
            if self.key_input == '1':
                self.key_input = ''
                self.menu = Menu.BUILDING_BRANCH
                self.building_branch_menu()
            elif self.key_input == "0":
                self.key_input = ''
                self.mill_philosophy_menu()
            elif self.key_input == "2":
                self.key_input = ''
                self.Researching_mill = True
                self.mill_philosophy_menu()
            else:
                self.mill_philosophy_menu()

        elif self.menu == Menu.TAX_OFFICE_PHILOSOPHY:
            if self.key_input == '1':
                self.key_input = ''
                self.menu = Menu.BUILDING_BRANCH
                self.building_branch_menu()
            elif self.key_input == "0":

                self.key_input = ''
                self.tax_office_philosophy_menu()
            elif self.key_input == "2":
                self.key_input = ''
                self.Researching_tax_office = True
                self.tax_office_philosophy_menu()
            else:
                self.tax_office_philosophy_menu()

        elif self.menu == Menu.OBSERVATORY_PHILOSOPHY:
            if self.key_input == '1':
                self.key_input = ''
                self.menu = Menu.BUILDING_BRANCH
                self.building_branch_menu()
            elif self.key_input == "0":

                self.key_input = ''
                self.tax_office_philosophy_menu()
            elif self.key_input == "2":
                self.key_input = ''
                self.Researching_observatory = True
                self.observatory_philosophy_menu()
            else:
                self.observatory_philosophy_menu()


        elif self.menu == Menu.CARPENTRY:
            if self.key_input == '1':
                self.key_input = ''
                self.menu = Menu.BUILD
                self.build_menu()
            elif self.key_input == "0":

                self.key_input = ''
                self.carpentry_menu()
            else:
                self.carpentry_menu()

        elif self.menu == Menu.MILL:
            if self.key_input == '1':
                self.key_input = ''
                self.menu = Menu.BUILD
                self.build_menu()
            elif self.key_input == "0":

                self.key_input = ''
                self.mill_menu()
            else:
                self.mill_menu()

        elif self.menu == Menu.TAX_OFFICE:
            if self.key_input == '1':
                self.key_input = ''
                self.menu = Menu.BUILD
                self.build_menu()
            elif self.key_input == "0":

                self.key_input = ''
                self.tax_office_menu()
            else:
                self.tax_office_menu()

        elif self.menu == Menu.OBSERVATORY:
            if self.key_input == '1':
                self.key_input = ''
                self.menu = Menu.BUILD
                self.build_menu()
            elif self.key_input == "0":

                self.key_input = ''
                self.observatory_menu()
            else:
                self.observatory_menu()

        elif self.menu == Menu.TAVERN_PHILOSOPHY:
            if self.key_input == '1':
                self.key_input = ''
                self.menu = Menu.BUILDING_BRANCH
                self.building_branch_menu()
            elif self.key_input == "2":
                self.key_input = ""
                self.Researching_tavern = True

            else:
                self.tavern_philosophy_menu()

        elif self.menu == Menu.TAVERN:
            if self.key_input == '1':
                self.key_input = ''
                self.menu = Menu.BUILD2
                self.build_menu2()
            elif self.key_input == "0":
                self.key_input = ''
                self.tavern_menu()
            else:
                self.tavern_menu()

        elif self.menu == Menu.PHARMACY_PHILOSOPHY:
            if self.key_input == '1':
                self.key_input = ''
                self.menu = Menu.BUILDING_BRANCH
                self.building_branch_menu()
            elif self.key_input == "0":
                self.key_input = ''
                self.pharmacy_philosophy_menu()
            elif self.key_input == "2":
                self.key_input = ""
                self.Researching_pharmacy = True
            else:
                self.pharmacy_philosophy_menu()

        elif self.menu == Menu.FESTIVALTENT:
            if self.key_input == '1':
                self.key_input = ''
                self.menu = Menu.BUILD2
                self.build_menu2()
            elif self.key_input == "0":
                self.key_input = ''
                self.festival_tent_menu()
            else:
                self.festival_tent_menu()



        elif self.menu == Menu.LOADMENU:
            if self.key_input == '1':
                self.key_input = ''
                self.menu = Menu.MAIN
                self.main_menu()
            elif self.key_input == '2':
                self.key_input = ''
                self.load_menu()
                self.load()
            else:
                self.load_menu()

        elif self.menu == Menu.SAVEMENU:
            if self.key_input == '1':
                self.menu = Menu.MAIN
                self.main_menu()
            elif self.key_input == '2':
                self.key_input = ''
                self.save_menu()
                self.save()
            else:
                self.save_menu()

        elif self.menu == Menu.FESTIVALTENT_PHILOSOPHY:
            if self.key_input == '1':
                self.key_input = ''
                self.menu = Menu.BUILDING_BRANCH
                self.building_branch_menu()
            elif self.key_input == "0":
                self.key_input = ''
                self.festival_tent_philosophy_menu()
            elif self.key_input == "2":
                self.key_input = ""
                self.Researching_festival_tent = True
            else:
                self.festival_tent_philosophy_menu()
        elif self.menu == Menu.PHARMACY:
            if self.key_input == "1":
                self.key_input = ''
                self.menu = Menu.BUILD2
            else:
                self.pharmacy_menu()
        elif self.menu == Menu.GOLDENSTATUE_PHILOSOPHY:
            if self.key_input == '1':
                self.key_input = ''
                self.menu = Menu.BUILDING_BRANCH
                self.building_branch_menu()
            elif self.key_input == "0":
                self.key_input = ''
                self.festival_tent_philosophy_menu()
            elif self.key_input == "2":
                self.key_input = ""
                self.Researching_golden_statue = True
        elif self.menu == Menu.FESTIVALMENU:
            if self.key_input == "1":
                self.key_input = ''
                self.menu = Menu.MAIN
            elif self.key_input == "2":
                self.key_input = ''
                self.menu = Menu.FESTIVALSMENU
                self.festivals_menu()
            else:
                self.festival_menu()




    def main_menu(self):
        write("\n\nPress one to see the buildings menu\n")
        write("Press two to see philosophy\n")
        write("Press three to see economy\n")
        write("Press four to see the breakdowns\n")
        if self.festival_tent_Unlocked == True:
            write("Press five to enter festival menu")
        if self.happiness >= 100000:
            write("\n\n\n\n--------------------------Hacker!-----------------------")
            write("                                           Nothing works")
        elif self.happiness >= 200:
            write("\n\n\n\n--------Your people regard you to be a deity!-----------")
            write("\n                         3000% increase in all production")
        elif self.happiness >= 100:
            write("\n\n\n\n------Cheer in your kingdom banishes disease!-----------")
            write("\n                 300% increase in all production")
        elif self.happiness >= 50:
            write("\n\n\n\n-------------The merry parade the streets!--------------")
            write("\n                  200% increase in all production")
        elif self.happiness >= 25:
            write("\n\n\n\n---------Your kingdom is a constant festival!-----------")
            write("\n                 175% increase in all production")
        elif self.happiness >= 10:
            write("\n\n\n\n-------------Your people are overjoyed!-----------------")
            write("\n                 150% increase in all production")
        elif self.happiness >= 7:
            write("\n\n\n\n-------------Your people are very happy!----------------")
            write("\n                  120% increase in all production")
        elif self.happiness >= 3:
            write("\n\n\n\n------------Your people are quite happy!----------------")
            write("\n                 110% increase in all production")
        elif self.happiness >= 1:
            write("\n\n\n\n------------------Your people are happy-------------------")
            write("\n                  105% increase in all production")
        elif self.happiness == 0:
            write("\n\n\n\n------------------Your people are satisfied!------------")
            write("\n                                    Production unaffected")
        elif self.happiness >= -2:
            write("\n\n\n\n--------------Your people are disgruntled!--------------")
            write("\n                             5% decrease in all production")
        elif self.happiness >= -4:
            write("\n\n\n\n-----------------Your people are sad!-------------------")
            write("\n                           10% decrease in all production")
        elif self.happiness >= -6:
            write("\n\n\n\n----------------Your people are angry!------------------")
            write("\n                           20% decrease in all production")
        else:
            write("\n\n\n\n----------------Your people are rioting!----------------")
            write("\n                           50% decrease in all production")

    def save_menu(self):
        write("\n\nYou are in the save menu")
        write("\nPress one to go back")
        write("\nPress 2 to save")

    def load_menu(self):
        write("\n\nYou are in the load menu")
        write("\nPress one to go back")
        write("\nPress 2 to Load")

    def philosophy_menu(self):
        write("\n\nYou are in the philosophy menu\n")
        write("Press one to return to the Main Menu\n")
        write("Press two to open the philosophy tree\n")
        write("Press three to add another philosopher\n")
        write("Press four to fire a philosopher\n")
        write("\n Current philosophers = " + str(self.philosopher))

    def philosophy_tree_menu(self):
        write("\n\nYou are in the philosophy tree\n")
        write("Press one to return to the Philosophy Menu\n")
        write("Press two to enter the building branch\n")
        if self.festival_tent_Unlocked == True:
            write("Press three to enter the festivals branch\n")
        if self.carpentry_Unlocked == True and self.mill_Unlocked == True and self.tax_office_Unlocked == True and self.observatory_Unlocked == True and self.tavern_Unlocked == True and self.pharmacy_Unlocked == True and self.observatory_Unlocked == True and self.festival_tent_Unlocked == True:
            write("Press four to enter the golden statue philosophy menu\n")

    def building_branch_menu(self):
        write("\n\nYou are in the building branch of the philosophy tree")
        write("\nPress one to return to the philosophy tree")
        write("\nPress two to enter the carpentry philosophy menu")
        write("\nPress three to enter the mill philosophy menu")
        write("\nPress four to enter the tax office philosophy menu")
        write("\nPress five to enter the observatory philosophy menu")
        write("\nPress six to enter the tavern philosophy menu")
        write("\nPress seven to enter the pharmacy philosophy menu")
        write("\nPress eight to enter the observatory philosophy menu")
        write("\nPress nine to enter the festival tent philosophy menu")
        write("\nPress zero to go to the next section of the building branch")

    def building_branch2_menu(self):
        write("\n\nYou are in the second building branch of the philosophy tree")
        write("\nPress one to return to the first building branch")
        write("\nPress two to philosophise the golden statue")

    def economy_menu(self):
        write("\n\nYou are in the economy menu\n")
        write("Press one to return to Main Menu\n")
        write("Press two to adjust tax\n")

    def build_menu(self):
        write("\n\nYou are in the building menu\n")
        write("Press one to go back\n")
        write("Press two to build a house\n")
        write("Press three to build a farm\n")
        write("Press four to build a lumber camp\n")
        write("Press five to build a park\n")
        if self.carpentry_Unlocked == True:
            write("press six to build a carpentry\n")
        if self.mill_Unlocked == True:
            write("press seven to build a mill\n")
        if self.tax_office_Unlocked == True:
            write("press eight to build a tax office\n")
        if self.observatory_Unlocked == True:
            write("Press nine to build an observatory\n")
        write("Press zero to advance to the next menu\n")

    def build_menu2(self):
        write("\n\nYou are in building menu 2\n")
        write("Press one to go back\n")
        if self.tavern_Unlocked == True:
            write("Press two to build a tavern\n")
        if self.pharmacy_Unlocked == True:
            write("Press three to build a pharmacy\n")
        if self.festival_tent_Unlocked == True:
            write("Press four to build a festival tent\n")

    def breakdown_menu(self):
        write("\n\nYou are in the breakdown menu\n")
        write("Press one to return to the main menu\n")
        write("Press two to view your people\'s employment\n")
        write("Press three to see the buildings in your kingdom\n")

    def house_menu(self):
        write("\n\nA house costs 10 wood, you have " + str(self.prefix(self.wood)) + ' wood\n')
        write("Press one to go back\n")
        write("Press two to build a house\n")
        if self.true_wood >= 10:
            if self.key_input == '2':
                self.key_input = ''
                self.building_list[0]['house'] += 1
                self.true_wood -= 10
                self.house += 10
        else:
            write("You do not have enough wood")

    def farm_menu(self):  # Farm menu GUI

        write("\nA farm costs 5 wood, you have " + str(self.prefix(self.wood)) + ' wood\n')
        write("Press one to go back\n")
        write("Press two to build a farm\n")
        if self.true_wood >= 5:
            if self.key_input == '2':
                if self.unemployed >= 5:
                    self.key_input = ''
                    self.building_list[1]['farm'] += 1
                    self.true_wood -= 5
                    self.farmer += 5
                    self.unemployed = self.true_pop - (
                                self.farmer + self.philosopher + self.lumberjack + self.carpenter + self.miller + self.tax_collector)
                    self.farm += 1
                    self.food_gain = (0.1 + (0.1 + (0.1 * self.farm)) * (
                                self.mill_multiplier * 2)) * self.final_multiplier
                else:
                    write("Not enough unemployed people to run the farm")

        else:
            write("You do not have enough wood")

    def lumber_camp_menu(self):  # Lumber Camp GUI

        write(
            "\nA lumber camp costs 10 wood and 10 food, you have " + str(self.prefix(self.wood)) + ' wood\n and ' + str(
                self.prefix(int(self.true_food))) + ' food\n')
        write("Press one to go back\n")
        write("Press two to build a lumber camp\n")
        if self.true_wood >= 10 and self.true_food >= 10:
            if self.key_input == '2':
                if self.unemployed >= 3:
                    self.key_input = ''
                    self.building_list[2]['lumber_camp'] += 1
                    self.true_wood -= 10
                    self.true_food -= 10
                    self.lumber_camp += 1
                    self.wood_gain = (0.1 + (0.1 * self.lumber_camp) * (
                                (self.carpentry_multiplier + 0.1) * 2)) * self.final_multiplier
                    self.lumberjack += 3
                    self.unemployed = self.true_pop - (
                                self.farmer + self.philosopher + self.lumberjack + self.carpenter + self.miller + self.tax_collector)
                else:
                    write("Not enough unemployed people to run the lumber camp")

    def carpentry_menu(self):

        write("\nA carpentry costs 1 k food and 10 k gold, you have " + str(
            self.prefix(self.food)) + ' food\n and ' + str(self.prefix(int(self.true_gold))) + ' gold\n')
        write("Press one to go back\n")
        write("Press two to build a carpentry\n")
        if self.true_food >= 1000 and self.true_gold >= 10000:
            if self.key_input == '2':
                if self.unemployed >= 3:
                    self.key_input = ''
                    self.building_list[4]['carpentry'] += 1
                    self.true_food -= 1000
                    self.true_gold -= 10000
                    self.carpentry += 1
                    self.carpentry_multiplier = 2 * self.carpentry
                    self.wood_gain = (0.1 + (0.1 * self.lumber_camp) * (
                                (self.carpentry_multiplier + 0.1) * 2)) * self.final_multiplier
                    self.carpenter += 2
                    self.unemployed = self.true_pop - (
                                self.farmer + self.philosopher + self.lumberjack + self.carpenter + self.miller + self.tax_collector) + 10
                else:
                    write("Not enough unemployed people to run the carpentry")

    def mill_menu(self):

        write("\nA mill costs 1 k wood and 10 k gold, you have " + str(self.prefix(self.wood)) + ' wood\n and ' + str(
            self.prefix(int(self.true_gold))) + ' gold\n')
        write("Press one to go back\n")
        write("Press two to build a mill\n")
        if self.true_wood >= 1000 and self.true_gold >= 10000:
            if self.key_input == '2':
                if self.unemployed >= 3:
                    self.key_input = ''
                    self.building_list[5]['mill'] += 1
                    self.true_wood -= 1000
                    self.true_gold -= 10000
                    self.mill += 1
                    self.mill_multiplier = 2 * self.mill
                    self.food_gain = (0.1 + (0.1 + (0.1 * self.farm)) * (
                                self.mill_multiplier * 2)) * self.final_multiplier
                    self.miller += 3
                    self.unemployed = self.true_pop - (
                                self.farmer + self.philosopher + self.lumberjack + self.carpenter + self.miller + self.tax_collector) + 10
                else:
                    write("Not enough unemployed people to run the mill")

    def tax_office_menu(self):

        write("\nA tax  office costs 1 k food, 1 k wood and 10 k gold, you have\n " + str(
            self.prefix(self.wood)) + ' wood, ' + str(self.prefix(int(self.true_gold))) + ' gold and ' + str(
            self.prefix(int(self.true_food))) + ' food\n')
        write("Press one to go back\n")
        write("Press two to build a tax office\n")
        if self.true_wood >= 1000 and self.true_food >= 1000 and self.true_gold >= 10000:
            if self.key_input == '2':
                if self.unemployed >= 3:
                    self.key_input = ''
                    self.building_list[6]['tax office'] += 1
                    self.true_wood -= 1000
                    self.true_gold -= 10000
                    self.tax_collector += 1
                    self.tax_office_multiplier = 2 * self.mill
                    self.gold_gain = (2 + (2 + (2 * (self.house * self.tax))) * (
                                self.tax_office_multiplier * 2)) * self.final_multiplier
                    self.miller += 2
                    self.unemployed = self.true_pop - (
                                self.farmer + self.philosopher + self.lumberjack + self.carpenter + self.miller + self.tax_collector) + 10
                else:
                    write("Not enough unemployed people to run the tax office")

    def park_menu(self):
        self.park_gold_price = 1000 ** self.park
        self.park_wood_price = 100 ** self.park
        write("\nA park costs " + str(self.prefix(self.park_wood_price)) + " wood and " + str(
            self.prefix(self.park_gold_price)) + " gold you have " + str(self.prefix(self.wood)) + ' wood \nand ' + str(
            self.prefix(int(self.true_gold))) + ' gold\n')
        write("Press one to go back\n")
        write("Press two to build a park\n")
        if self.true_wood >= self.park_wood_price and self.true_gold >= self.park_gold_price:
            if self.key_input == '2':
                self.key_input = ''
                self.building_list[3]['park'] += 1
                self.true_wood -= 100
                self.true_gold -= 1000
                self.park += 1
                self.happiness = ((1 * self.park) - (self.tax * 10))
                self.gold_gain = (2 + (2 + (2 * (self.house * self.tax))) * (
                            self.tax_office_multiplier * 2)) * self.final_multiplier
        else:
            write("you do not have enough wood and/or gold")

    def carpentry_philosophy_menu(self):
        write("\n\nYou are in the carpentry philosophy menu")
        write("\nPress one to return to the building branch")
        if self.Researching_carpentry == True:
            if self.carpentry_progress <= 9999:
                self.researching_observatory = False
                self.Researching_mill = False
                self.Researching_tax_office = False
                write("\n\nPhilosophising carpentry")
                self.carpentry_progress += (0.1 * self.philosopher)
                self.true_gold -= (0.1 * self.philosopher)
                write("\n\n\n Current Progress = " + str(self.prefix(self.carpentry_progress)) + "/10 k")
            else:
                self.Researching_carpentry = False
                self.carpentry_Unlocked = True
        else:
            if self.carpentry_Unlocked == True:
                write("\nCarpentry philosophised")
            else:
                write("\n Press two to begin philosophising carpentry")
                write("\n\nNot currently philosophising carpentry")

    def mill_philosophy_menu(self):
        write("\n\nYou are in the mill philosophy menu")
        write("\nPress one to return to the building branch")
        if self.Researching_mill == True:
            if self.mill_progress <= 9999:
                self.researching_observatory = False
                self.Researching_carpentry = False
                self.Researching_tax_office = False
                write("\n\nPhilosophising mills")
                self.mill_progress += (0.1 * self.philosopher)
                self.true_gold -= (0.1 * self.philosopher)
                write("\n\n\n Current Progress = " + str(self.prefix(self.mill_progress)) + "/10 k")
            else:
                self.Researching_mill = False
                self.mill_Unlocked = True
        else:
            if self.mill_Unlocked == True:
                write("\nMills philosophised")
            else:
                write("\n Press two to begin philosophising mills")
                write("\n\nNot currently philosophising mills")

    def tax_office_philosophy_menu(self):
        write("\n\nYou are in the tax office philosophy menu")
        write("\nPress one to return to the building branch")
        if self.Researching_tax_office == True:
            if self.tax_office_progress <= 9999:
                self.researching_observatory = False
                self.Researching_carpentry = False
                self.Researching_mill = False
                write("\n\nPhilosophising tax office")
                self.tax_office_progress += (0.1 * self.philosopher)
                self.true_gold -= (0.1 * self.philosopher)
                write("\n\n\n Current Progress = " + str(self.prefix(self.tax_office_progress)) + "/10 k")
            else:
                self.Researching_tax_office = False
                self.tax_office_Unlocked = True
        else:
            if self.tax_office_Unlocked == True:
                write("\nTax office philosophised")
            else:
                write("\n Press two to begin philosophising the tax office")
                write("\n\nNot currently philosophising the tax office")

    def golden_statue_philosophy_menu(self):
        write("You are in the golden statue philosophy menu")
        write("Press one to return to the building branch")
        if self.Researching_golden_statue == True:
            if self.golden_statue_progress < 1000000:
                self.researching_observatory = False
                self.Researching_carpentry = False
                self.Researching_mill = False
                self.researching_pharmacy = False
                self.Researching_tax_office = False
            else:
                self.Researching_golden_statue = False
                self.golden_statue_Unlocked = True
        if self.golden_statue_Unlocked == True:
            write("Golden statue has been philosophised")
        else:
            write("\n Press two to begin philosophising the golden statue")
            write("\n\nNot currently philosophising the golden statue")

    def observatory_menu(self):
        write("\n\nAn observatory costs 10 k gold, you have " + str(self.prefix(int(self.true_gold))) + ' gold\n')
        write("Press one to go back\n")
        write("Press two to build an observatory\n")
        if self.true_gold >= 10000:
            if self.key_input == '2':
                self.key_input = ''
                self.building_list[7]['observatory'] += 1
                self.true_gold -= 10000
                self.observatory += 1

    def festival_tent_menu(self):
        write("\n\nA festival tent costs 50 k gold and 15k wood, you have " + str(self.prefix(int(self.true_gold))) + ' gold and '+str(self.prefix(int(self.true_wood)))+' wood\n')
        write("Press one to go back\n")
        write("Press two to build a festival tent\n")
        if self.true_gold >= 50000 and self.true_wood >=15000:
            if self.key_input == '2':
                self.key_input = ''
                self.building_list[10]['festival_tent'] += 1
                self.true_gold -= 50000
                self.true_wood -= 15000
                self.festival_tent += 1
        else:
            write('Not enough wood/gold')

    def tavern_menu(self):
        write("\n\nA tavern costs 10 k gold and 10k wood, you have " + str(
            self.prefix(int(self.true_gold))) + " gold \nand " + str(self.prefix(int(self.true_wood))) + " wood\n")
        write("Press one to go back\n")
        write("Press two to build a tavern\n")
        if self.true_gold >= 10000:
            if self.key_input == '2':
                self.key_input = ''
                self.building_list[8]['tavern'] += 1
                self.true_gold -= 10000
                self.true_wood -= 10000
                self.tavern += 1

    def pharmacy_menu(self):
        write("\n\nA pharmacy costs 10 k gold and 10k wood, you have " + str(
            self.prefix(int(self.true_gold))) + " gold \nand " + str(self.prefix(int(self.true_wood))) + " wood\n")
        write("Press one to go back\n")
        write("Press two to build a pharmacy\n")
        if self.true_gold >= 10000:
            if self.key_input == '2':
                self.key_input = ''
                self.building_list[9]['pharmacy'] += 1
                self.true_gold -= 10000
                self.true_wood -= 10000
                self.pharmacy += 1
                print(self.pop_growth)
        else:
            write("You do not have enough gold")

    def confirm_rennissance_menu(self):
        write("Building this statue will advance your civiliation to the next age, are you sure you want to do this?")
        write("Press one to cancel")
        write("Press two to go ahead")
        if self.key_input == "1":
            self.key_input = ''
            self.menu = Menu.BUILD2
            self.build_menu2()
        if self.key_input == "2":
            self.key_input = ''
            self.menu = Menu.RENNISSANCE_CHANGELOG
            self.rennissance_changelog_menu()

    def goldstatue_menu(self):
        write("The gold statue costs 1m gold, 500k wood and requires you to have at least 1k people in your kingdom\n You have ", +str(self.prefix(self.true_gold))+ " gold, "+ str(self.prefix(self.true_wood)), " wood and" + str(self.prefix(self.true_pop)), " people")
        if self.true_gold >= 1000000:
            if self.true_wood >= 500000:
                if self.true_pop >=1000:
                    if self.key_input  == 2:
                        self.key_input = ''
                        self.menu = Menu.CONFIRM_RENNISSANCE
                        self.confirm_renissance_menu()
                else:
                    write('You need a larger population!')
            else:
                write('Not enough wood!')
        else:
            write('Not enough gold!')

    def observatory_philosophy_menu(self):
        write("\n\nYou are in the observatory philosophy menu")
        write("\nPress one to return to the building branch")
        if self.Researching_observatory == True:
            if self.observatory_progress <= 19999:
                self.researching_tax_office = False
                self.Researching_carpentry = False
                self.Researching_mill = False
                write("\n\nPhilosophising observatory")
                self.observatory_progress += (0.1 * self.philosopher)
                self.true_gold -= (0.1 * self.philosopher)
                write("\n\n\n Current Progress = " + str(self.prefix(self.observatory_progress)) + "/20 k")
            else:
                self.Researching_observatory = False
                self.observatory_Unlocked = True
        else:
            if self.observatory_Unlocked == True:
                write("\nObservatory philosophised")
            else:
                write("\n Press two to begin philosophising the observatory")
                write("\n\nNot currently philosophising the observatory")

    def tavern_philosophy_menu(self):
        write("\n\nYou are in the tavern philosophy menu")
        write("\nPress one to return to the building branch")
        if self.Researching_tavern == True:
            if self.tavern_progress <= 29999:
                self.researching_tax_office = False
                self.Researching_carpentry = False
                self.Researching_mill = False
                self.Researching_observatory = False
                write("\n\nPhilosophising tavern")
                self.tavern_progress += (0.1 * self.philosopher)
                self.true_gold -= (0.1 * self.philosopher)
                write("\n\n\n Current Progress = " + str(self.prefix(self.tavern_progress)) + "/30 k")
            else:
                self.Researching_tavern = False
                self.tavern_Unlocked = True
        else:
            if self.tavern_Unlocked == True:
                write("\nTavern philosophised")
            else:
                write("\n Press two to begin philosophising the tavern")
                write("\n\nNot currently philosophising the tavern")

    def pharmacy_philosophy_menu(self):
        write("\n\nYou are in the pharmacy philosophy menu")
        write("\nPress one to return to the building branch")
        if self.Researching_pharmacy == True:
            if self.pharmacy_progress <= 29999:
                self.researching_tax_office = False
                self.Researching_carpentry = False
                self.Researching_mill = False
                self.Researching_observatory = False
                self.Researching_festival_tent = False
                write("\n\nPhilosophising pharmacy")
                self.pharmacy_progress += (0.1 * self.philosopher)
                self.true_gold -= (0.1 * self.philosopher)
                write("\n\n\n Current Progress = " + str(self.prefix(self.tavern_progress)) + "/30 k")
            else:
                self.Researching_pharmacy = False
                self.pharmacy_Unlocked = True
        else:
            if self.pharmacy_Unlocked == True:
                write("\nPharmacy philosophised")
            else:
                write("\n Press two to begin philosophising the pharnacy")
                write("\n\nNot currently philosophising the pharmacy")

    def festival_tent_philosophy_menu(self):
        write("\n\nYou are in the festival tent philosophy menu")
        write("\nPress one to return to the building branch")
        if self.Researching_festival_tent == True:
            if self.festival_tent_progress <= 49999:
                self.Researching_carpentry = False
                self.Researching_mill = False
                self.Researching_tax_office = False
                self.Researching_observatory = False
                self.Researching_pharmacy = False
                write("\n\nPhilosophising festival tent")
                self.festival_tent_progress += (0.1 * self.philosopher)
                self.true_gold -= (0.1 * self.philosopher)
                write("\n\n\n Current Progress = " + str(self.prefix(self.festival_tent_progress)) + "/50 k")
            else:
                self.Researching_festival_tent = False
                self.festival_tent_Unlocked = True
        else:
            if self.festival_tent_Unlocked == True:
                write("\nFestival tent philosophised")
            else:
                write("\n Press two to begin philosophising the festival tents")
                write("\n\nNot currently philosophising the festival tent")

    def people_breakdown_menu(self):
        write("\n\n----People breakdown Menu----")
        write("\nPress one to exit")
        write("\n\nUnemployed = " + str(self.prefix((self.unemployed) + 10)))
        write("\nPhilosophers = " + str(self.prefix(self.philosopher)))
        write("\nFarmers = " + str(self.prefix(self.farmer)))
        write("\nLumberjacks = " + str(self.prefix(self.lumberjack)))
        if self.carpentry_Unlocked == True:
            write("\nCarpenters = " + str(self.prefix(self.carpentry)))
        if self.mill_Unlocked == True:
            write("\nMillers = " + str(self.prefix(self.miller)))
        if self.tax_office_Unlocked == True:
            write("\nTax collectors =" + str(self.prefix(self.tax_collector)))

    def building_breakdown_menu(self):
        write("\n\n----Buildings breakdown Menu----")
        write("\nPress one to exit")
        write("\n\nHouses = " + str(int(self.house)))
        write("\nFarms = " + str(int(self.farm)))
        write("\nLumber camps = " + str(int(self.lumber_camp)))
        write("\nParks = " + str(int(self.park)))
        if self.carpentry_Unlocked == True:
            write("\n Carpentries = " + str(int(self.carpentry)))
        if self.mill_Unlocked == True:
            write("\nMills = " + str(int(self.mill)))
        if self.tax_office_Unlocked == True:
            write("\nTax offices = " + str(int(self.tax_office)))
        if self.observatory_Unlocked == True:
            write("\nObservatory = " + str(int(self.observatory)))
            write("\n\nPress two to go on to second breakdown page")

    def building_breakdown2_menu(self):
        write("\n\n----Buildings breakdown Menu----")
        write("\nPress one to go back")
        if self.tavern_Unlocked == True:
            write("\nTaverns =" + str(int(self.tavern)))
        if self.pharmacy_Unlocked == True:
            write("\nPharmacies ="+str(int(self.pharmacy)))

    def tax_menu(self):
        write("\n\n----Tax Menu----")
        write("\nPress one to exit")
        write("\nPress two to increase tax")
        write("\nPress three to decrease tax")
        write("\nCurrent tax rate " + str(int(self.tax * 100)) + "%")

    def festival_menu(self):
        write("\n\nYou are in the festival menu")
        write("\nPress one to begin a festival")
        write("\nPress two to see active festivals")
        write("\nPress three to cancel all festivals")

    def festivals_menu(self):
        write("\n\n-Menu of festivals-")
        write("\n  Basic festival")
        write("\n    20 food and 100 gold")
        write("\n     1% increase in prooduction")
        


    def dynamicrescheck(self):
        self.menu = Menu.MAIN
        self.pop_growth = (((2 ** (math.sqrt(self.pharmacy+1))))/200 + (self.pop / 20000))
        self.carpentry_multiplier = 2 * self.carpentry
        self.mill_multiplier = 2 * self.mill
        self.tax_office_multiplier = 2 * self.tax_office
        self.final_multiplier = (1 * (2 * (self.tavern + 0.5))) ** (self.festival_tent + 1)+self.age/10
        self.gold_gain = (2 + (2 + (2 * (self.house * self.tax))) * (
                    self.tax_office_multiplier * 2)) * self.final_multiplier
        self.food_gain = (0.1 + (0.1 + (0.1 * self.farm)) * (self.mill_multiplier * 2) + 0.1) * self.final_multiplier
        self.wood_gain = (0.1 + (0.1 * self.lumber_camp) * (
                    (self.carpentry_multiplier + 0.1) * 2)) * self.final_multiplier
        self.happiness = ((1 * self.park) - (self.tax * 10))
        self.unemployed = self.true_pop - (self.farmer + self.philosopher + self.lumberjack + self.carpenter + self.miller)
        self.park_gold_price = 1000 ** self.park
        self.park_wood_price = 100 ** self.park

    def mat_output(self):
        write("Food = " + str(self.prefix(self.food)) + "\n")
        write("Gold = " + str(self.prefix(int(self.true_gold))) + "\n")
        write("Wood = " + str(self.prefix(self.wood)) + "\n")
        write("Population = " + str(self.prefix(self.pop)) + "/" + str(self.prefix(self.house)) + "\n")
        write("Homeless = " + str(self.prefix(self.homeless)) + "\n")
        write("Happiness = " + str(int(self.happiness)))

    def save(self):
        if os.path.exists("AoPSaves/"):
            pass
        else:
            os.mkdir('AoPSaves/')
        file = open("AoPSaves/AoPsavedata.txt", "a")
        file.close()
        self.happiness = ((1 * self.park) - (self.tax * 10))
        file = open("AoPSaves/AoPsavedata.txt", "w")
        file.write('[')
        file.write(str(self.true_food))
        file.write(', ')
        file.write(str(self.true_gold))
        file.write(', ')
        file.write(str(self.true_wood))
        file.write(', ')
        file.write(str(self.true_pop))
        file.write(', ')
        file.write(str(self.happiness))
        file.write(',')
        file.write(str(self.house))
        file.write(',')
        file.write(str(self.farm))
        file.write(', ')
        file.write(str(self.lumber_camp))
        file.write(', ')
        file.write(str(self.carpentry))
        file.write(', ')
        file.write(str(self.mill))
        file.write(', ')
        file.write(str(self.tax_office))
        file.write(', ')
        file.write(str(self.tavern))
        file.write(', ')
        file.write(str(self.pharmacy))
        file.write(', ')
        file.write(str(self.observatory))
        file.write(', ')
        file.write(str(self.lumberjack))
        file.write(', ')
        file.write(str(self.farmer))
        file.write(', ')
        file.write(str(self.carpenter))
        file.write(', ')
        file.write(str(self.miller))
        file.write(', ')
        file.write(str(self.tax_collector))
        file.write(', ')
        file.write(str(self.pharmacist))
        file.write(', ')
        file.write(str(self.carpentry_Unlocked))
        file.write(', ')
        file.write(str(self.mill_Unlocked))
        file.write(', ')
        file.write(str(self.tax_office_Unlocked))
        file.write(', ')
        file.write(str(self.observatory_Unlocked))
        file.write(', ')
        file.write(str(self.tavern_Unlocked))
        file.write(', ')
        file.write(str(self.pharmacy_Unlocked))
        file.write(', ')
        file.write(str(self.carpentry_progress))
        file.write(', ')
        file.write(str(self.mill_progress))
        file.write(', ')
        file.write(str(self.tax_office_progress))
        file.write(', ')
        file.write(str(self.observatory_progress))
        file.write(', ')
        file.write(str(self.tavern_progress))
        file.write(', ')
        file.write(str(self.pharmacy_progress))
        file.write(', ')
        file.write(str(self.festival_tent))
        file.write(', ')
        file.write(str(self.festival_tent_Unlocked))
        file.write(', ')
        file.write(str(self.festival_tent_progress))

        file.write(']')

    ##        self.carpentry_progress = 0
    ##        self.mill_progress = 0
    ##        self.tax_office_progress = 0
    ##        self.observatory_progress = 0
    ##        self.tavern_progress = 0
    ##        self.pharmasist_progress = 0
    def load(self):
        try:
            file = open("AoPSaves/AoPsavedata.txt", "r")
            line = file.read()
            line = line.replace('[', '')
            line = line.replace(']', '')
            line = line.split(',')
            self.true_food = float(line[0])
            self.true_gold = float(line[1])
            self.true_wood = float(line[2])
            self.true_pop = float(line[3])
            self.happiness = float(line[4])
            self.house = int(line[5])
            self.farm = float(line[6])
            self.lumber_camp = float(line[7])
            self.carpentry = float(line[8])
            self.mill = float(line[9])
            self.tax_office = float(line[10])
            self.tavern = float(line[11])
            self.pharmacy = float(line[12])
            self.observatory = float(line[13])
            self.lumberjack = float(line[14])
            self.farmer = float(line[15])
            self.carpenter = float(line[16])
            self.miller = float(line[17])
            self.tax_collector = float(line[18])
            self.pharmacist = float(line[19])
            self.carpentry_Unlocked = eval(line[20])
            self.mill_Unlocked = eval(line[21])
            self.tax_office_Unlocked = eval(line[22])
            self.tavern_Unlocked = eval(line[23])
            self.observatory_Unlocked = eval(line[24])
            self.pharmacy_Unlocked = eval(line[25])
            self.carpentry_progress = float(line[26])
            self.mill_progress = float(line[27])
            self.tax_office_progress = float(line[28])
            self.observatory_progress = float(line[29])
            self.tavern_progress = float(line[30])
            self.pharmacy_progress = float(line[31])
            self.festival_tent = float(line[32])
            self.festival_tent_Unlocked = eval(line[33])
            self.festival_tent_progress = float(line[34])
        except:
            write("\nNo save data found")

    def mat_change(self):
        if self.happiness >= 100000:
            pass
        elif self.happiness >= 200:
            self.final_multiplier += 30

            self.true_food += self.food_gain
            self.food = int(self.true_food * 1.5)
            self.true_wood += self.wood_gain
            self.wood = int(self.true_wood * 1.5)
            self.mat_output()
            self.pop_growth = (((2 ** (math.sqrt(self.pharmacy+1))))/200 + (self.pop / 20000))
            self.true_pop += self.pop_growth
            self.unemployed += self.pop_growth
            self.pop = int(self.true_pop)
            self.true_gold += self.gold_gain * 1.5
            self.final_multiplier = (1 * (2 * (self.tavern + 0.5))) ** (self.festival_tent + 1)+self.age/10
            if self.Researching_carpentry == True:
                if self.carpentry_progress <= 9999 and self.true_gold >= 0:
                    self.carpentry_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_carpentry = False

            if self.Researching_mill == True:
                if self.mill_progress <= 9999 and self.true_gold >= 0:
                    self.mill_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_mill = False

            if self.Researching_tax_office == True:
                if self.tax_office_progress <= 9999 and self.true_gold >= 0:
                    self.tax_office_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_tax_office = False
            if self.Researching_tavern == True:
                if self.tavern_progress <= 29999 and self.true_gold >= 0:
                    self.tavern_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_tavern = False

            if (self.pop - self.house) > 0:
                self.homeless = self.pop - self.house
            else:
                self.homeless = 0
                self.happiness = ((1 * self.park) - (self.tax * 10)) + 1
        elif self.happiness >= 150:
            self.final_multiplier += 5

            self.true_food += self.food_gain
            self.food = int(self.true_food * 1.5)
            self.true_wood += self.wood_gain
            self.wood = int(self.true_wood * 1.5)
            self.mat_output()
            self.pop_growth = (((2 ** (math.sqrt(self.pharmacy+1))))/200 + (self.pop / 20000))
            self.true_pop += self.pop_growth
            self.unemployed += self.pop_growth
            self.pop = int(self.true_pop)
            self.true_gold += self.gold_gain * 1.5
            self.final_multiplier = (1 * (2 * (self.tavern + 0.5))) ** (self.festival_tent + 1)+self.age/10
            if self.Researching_carpentry == True:
                if self.carpentry_progress <= 9999 and self.true_gold >= 0:
                    self.carpentry_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_carpentry = False

            if self.Researching_mill == True:
                if self.mill_progress <= 9999 and self.true_gold >= 0:
                    self.mill_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_mill = False

            if self.Researching_tax_office == True:
                if self.tax_office_progress <= 9999 and self.true_gold >= 0:
                    self.tax_office_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_tax_office = False
            if self.Researching_tavern == True:
                if self.tavern_progress <= 29999 and self.true_gold >= 0:
                    self.tavern_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_tavern = False

            if (self.pop - self.house) > 0:
                self.homeless = self.pop - self.house
            else:
                self.homeless = 0
                self.happiness = ((1 * self.park) - (self.tax * 10)) + 1
        elif self.happiness >= 100:
            self.final_multiplier += 2.00
            self.gold_gain = (2 + (2 + (2 * (self.house * self.tax))) * (
                        self.tax_office_multiplier * 2)) * self.final_multiplier
            self.food_gain = (0.1 + (0.1 + (0.1 * self.farm)) * (self.mill_multiplier * 2)) * self.final_multiplier
            self.wood_gain = (0.1 + (0.1 * self.lumber_camp) * (
                        (self.carpentry_multiplier + 0.1) * 2)) * self.final_multiplier
            self.true_food += self.food_gain
            self.food = int(self.true_food * 1.5)
            self.true_wood += self.wood_gain
            self.wood = int(self.true_wood * 1.5)
            self.mat_output()
            self.pop_growth = (((2 ** (math.sqrt(self.pharmacy + 1)))) / 200 + (self.pop / 20000))
            self.true_pop += self.pop_growth
            self.unemployed += self.pop_growth
            self.pop = int(self.true_pop)
            self.true_gold += self.gold_gain * 1.5
            self.final_multiplier = (1 * (2 * (self.tavern + 0.5))) ** (self.festival_tent + 1)+self.age/10
            if self.Researching_carpentry == True:
                if self.carpentry_progress <= 9999 and self.true_gold >= 0:
                    self.carpentry_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_carpentry = False

            if self.Researching_mill == True:
                if self.mill_progress <= 9999 and self.true_gold >= 0:
                    self.mill_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_mill = False

            if self.Researching_tax_office == True:
                if self.tax_office_progress <= 9999 and self.true_gold >= 0:
                    self.tax_office_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_tax_office = False
            if self.Researching_tavern == True:
                if self.tavern_progress <= 29999 and self.true_gold >= 0:
                    self.tavern_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_tavern = False

            if (self.pop - self.house) > 0:
                self.homeless = self.pop - self.house
            else:
                self.homeless = 0
                self.happiness = ((1 * self.park) - (self.tax * 10)) + 1
        elif self.happiness >= 25:
            self.final_multiplier += 1.75
            self.gold_gain = (2 + (2 + (2 * (self.house * self.tax))) * (
                        self.tax_office_multiplier * 2)) * self.final_multiplier
            self.food_gain = (0.1 + (0.1 + (0.1 * self.farm)) * (self.mill_multiplier * 2)) * self.final_multiplier
            self.wood_gain = (0.1 + (0.1 * self.lumber_camp) * (
                        (self.carpentry_multiplier + 0.1) * 2)) * self.final_multiplier
            self.true_food += self.food_gain
            self.food = int(self.true_food * 1.5)
            self.true_wood += self.wood_gain
            self.wood = int(self.true_wood * 1.5)
            self.mat_output()
            self.pop_growth = (((2 ** (self.pharmacy+1)))/200 + (self.pop / 20000))
            self.true_pop += self.pop_growth
            self.unemployed += self.pop_growth
            self.pop = int(self.true_pop)
            self.true_gold += self.gold_gain * 1.5
            self.final_multiplier = (1 * (2 * (self.tavern + 0.5))) ** (self.festival_tent + 1)+self.age/104
            if self.Researching_carpentry == True:
                if self.carpentry_progress <= 9999 and self.true_gold >= 0:
                    self.carpentry_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_carpentry = False

            if self.Researching_mill == True:
                if self.mill_progress <= 9999 and self.true_gold >= 0:
                    self.mill_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_mill = False

            if self.Researching_tax_office == True:
                if self.tax_office_progress <= 9999 and self.true_gold >= 0:
                    self.tax_office_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_tax_office = False
            if self.Researching_tavern == True:
                if self.tavern_progress <= 29999 and self.true_gold >= 0:
                    self.tavern_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_tavern = False

            if (self.pop - self.house) > 0:
                self.homeless = self.pop - self.house
            else:
                self.homeless = 0
                self.happiness = ((1 * self.park) - (self.tax * 10)) + 1

        elif self.happiness >= 10:
            self.gold_gain = (2 + (2 + (2 * (self.house * self.tax))) * (
                        self.tax_office_multiplier * 2)) * self.final_multiplier
            self.food_gain = (0.1 + (0.1 + (0.1 * self.farm)) * (self.mill_multiplier * 2)) * self.final_multiplier
            self.wood_gain = (0.1 + (0.1 * self.lumber_camp) * (
                        (self.carpentry_multiplier + 0.1) * 2)) * self.final_multiplier
            self.true_food += self.food_gain
            self.food = int(self.true_food * 1.5)
            self.true_wood += self.wood_gain
            self.wood = int(self.true_wood * 1.5)
            self.mat_output()
            self.pop_growth = (((2 ** (math.sqrt(self.pharmacy+1))))/200 + (self.pop / 20000))
            self.true_pop += self.pop_growth
            self.unemployed += self.pop_growth
            self.pop = int(self.true_pop)
            self.true_gold += self.gold_gain * 1.5
            self.final_multiplier = (1 * (2 * (self.tavern + 0.5))) ** (self.festival_tent + 1) + self.age / 10
            if self.Researching_carpentry == True:
                if self.carpentry_progress <= 9999 and self.true_gold >= 0:
                    self.carpentry_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_carpentry = False

            if self.Researching_mill == True:
                if self.mill_progress <= 9999 and self.true_gold >= 0:
                    self.mill_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_mill = False

            if self.Researching_tax_office == True:
                if self.tax_office_progress <= 9999 and self.true_gold >= 0:
                    self.tax_office_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_tax_office = False
            if self.Researching_tavern == True:
                if self.tavern_progress <= 29999 and self.true_gold >= 0:
                    self.tavern_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_tavern = False

            if (self.pop - self.house) > 0:
                self.homeless = self.pop - self.house
            else:
                self.homeless = 0
                self.happiness = ((1 * self.park) - (self.tax * 10)) + 1
        elif self.happiness >= 7:
            self.gold_gain = (2 + (2 + (2 * (self.house * self.tax))) * (
                        self.tax_office_multiplier * 2)) * self.final_multiplier
            self.food_gain = (0.1 + (0.1 + (0.1 * self.farm)) * (self.mill_multiplier * 2)) * self.final_multiplier
            self.wood_gain = (0.1 + (0.1 * self.lumber_camp) * (
                        (self.carpentry_multiplier + 0.1) * 2)) * self.final_multiplier
            self.true_food += self.food_gain * 1.2
            self.food = int(self.true_food)
            self.true_wood += self.wood_gain * 1.2
            self.wood = int(self.true_wood)
            self.mat_output()
            self.pop_growth = (((2 ** (math.sqrt(self.pharmacy+1))))/200 + (self.pop / 20000))
            self.true_pop += self.pop_growth
            self.unemployed += self.pop_growth
            self.pop = int(self.true_pop)
            self.true_gold += self.gold_gain * 1.2
            self.final_multiplier = (1 * (2 * (self.tavern + 0.5))) ** (self.festival_tent + 1)+self.age/10
            if self.Researching_carpentry == True:
                if self.carpentry_progress <= 9999 and self.true_gold >= 0:
                    self.carpentry_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_carpentry = False

            if self.Researching_mill == True:
                if self.mill_progress <= 9999 and self.true_gold >= 0:
                    self.mill_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_mill = False

            if self.Researching_tax_office == True:
                if self.tax_office_progress <= 19999 and self.true_gold >= 0:
                    self.tax_office_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_tax_office = False

            if self.Researching_tavern == True:
                if self.tavern_progress <= 29999 and self.true_gold >= 0:
                    self.tavern_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_tavern = False
            if (self.pop - self.house) > 0:
                self.homeless = self.pop - self.house
            else:
                self.homeless = 0
                self.happiness = ((1 * self.park) - (self.tax * 10)) + 1
        elif self.happiness >= 3:
            self.gold_gain = (2 + (2 + (2 * (self.house * self.tax))) * (
                        self.tax_office_multiplier * 2)) * self.final_multiplier
            self.food_gain = (0.1 + (0.1 + (0.1 * self.farm)) * (self.mill_multiplier * 2)) * self.final_multiplier
            self.wood_gain = (0.1 + (0.1 * self.lumber_camp) * (
                        (self.carpentry_multiplier + 0.1) * 2)) * self.final_multiplier
            self.true_food += self.food_gain * 1.1
            self.food = int(self.true_food)
            self.true_wood += self.wood_gain * 1.1
            self.wood = int(self.true_wood)
            self.mat_output()
            self.pop_growth = (((2 ** (math.sqrt(self.pharmacy+1))))/200 + (self.pop / 20000))
            self.true_pop += self.pop_growth
            self.unemployed += self.pop_growth
            self.pop = int(self.true_pop)
            self.true_gold += self.gold_gain * 1.1
            self.final_multiplier = (1 * (2 * (self.tavern + 0.5))) ** (self.festival_tent + 1)+self.age/10
            if self.Researching_carpentry == True:
                if self.carpentry_progress <= 9999 and self.true_gold >= 0:
                    self.carpentry_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_carpentry = False

            if self.Researching_mill == True:
                if self.mill_progress <= 9999 and self.true_gold >= 0:
                    self.mill_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_mill = False

            if self.Researching_tax_office == True:
                if self.tax_office_progress <= 9999 and self.true_gold >= 0:
                    self.tax_office_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_tax_office = False

            if self.Researching_tavern == True:
                if self.tavern_progress <= 29999 and self.true_gold >= 0:
                    self.tavern_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_tavern = False

            if (self.pop - self.house) > 0:
                self.homeless = self.pop - self.house
            else:
                self.homeless = 0
                self.happiness = ((1 * self.park) - (self.tax * 10)) + 1
        elif self.happiness >= 1:

            self.true_food += self.food_gain * 1.05
            self.food = int(self.true_food)
            self.true_wood += self.wood_gain * 1.05
            self.wood = int(self.true_wood)
            self.mat_output()
            self.pop_growth = (((2 ** (math.sqrt(self.pharmacy+1))))/200 + (self.pop / 20000))
            self.true_pop += self.pop_growth
            self.unemployed += self.pop_growth
            self.pop = int(self.true_pop)
            self.true_gold += self.gold_gain * 1.05
            self.final_multiplier = (1 * (2 * (self.tavern + 0.5))) ** (self.festival_tent + 1)+self.age/10
            if self.Researching_carpentry == True:
                if self.carpentry_progress <= 9999 and self.true_gold >= 0:
                    self.carpentry_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_carpentry = False

            if self.Researching_mill == True:
                if self.mill_progress <= 9999 and self.true_gold >= 0:
                    self.mill_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_mill = False

            if self.Researching_tax_office == True:
                if self.tax_office_progress <= 9999 and self.true_gold >= 0:
                    self.tax_office_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_tax_office = False

            if self.Researching_tavern == True:
                if self.tavern_progress <= 29999 and self.true_gold >= 0:
                    self.tavern_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_tavern = False

            if (self.pop - self.house) > 0:
                self.homeless = self.pop - self.house
            else:
                self.homeless = 0
                self.happiness = ((1 * self.park) - (self.tax * 10)) + 1
        elif self.happiness == 0:
            self.gold_gain = (2 + (2 + (2 * (self.house * self.tax))) * (
                        self.tax_office_multiplier * 2)) * self.final_multiplier
            self.food_gain = (0.1 + (0.1 + (0.1 * self.farm)) * (self.mill_multiplier * 2)) * self.final_multiplier
            self.wood_gain = (0.1 + (0.1 * self.lumber_camp) * (
                        (self.carpentry_multiplier + 0.1) * 2)) * self.final_multiplier
            self.true_food += self.food_gain
            self.food = int(self.true_food)
            self.true_wood += self.wood_gain
            self.wood = int(self.true_wood)
            self.mat_output()
            self.pop_growth = (((2 ** (math.sqrt(self.pharmacy+1))))/200 + (self.pop / 20000))
            self.true_pop += self.pop_growth
            self.unemployed += self.pop_growth
            self.pop = int(self.true_pop)
            self.true_gold += self.gold_gain
            self.final_multiplier = (1 * (2 * (self.tavern + 0.5))) ** (self.festival_tent + 1)+self.age/10
            if self.Researching_carpentry == True:
                if self.carpentry_progress <= 9999 and self.true_gold >= 0:
                    self.carpentry_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_carpentry = False

            if self.Researching_mill == True:
                if self.mill_progress <= 9999 and self.true_gold >= 0:
                    self.mill_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_mill = False

            if self.Researching_tax_office == True:
                if self.tax_office_progress <= 9999 and self.true_gold >= 0:
                    self.tax_office_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_tax_office = False

            if self.Researching_tavern == True:
                if self.tavern_progress <= 29999 and self.true_gold >= 0:
                    self.tavern_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_tavern = False

            if (self.pop - self.house) > 0:
                self.homeless = self.pop - self.house
            else:
                self.homeless = 0
                self.happiness = ((1 * self.park) - (self.tax * 10)) + 1
        elif self.happiness >= -2:
            self.gold_gain = (2 + (2 + (2 * (self.house * self.tax))) * (
                        self.tax_office_multiplier * 2)) * self.final_multiplier
            self.food_gain = (0.1 + (0.1 + (0.1 * self.farm)) * (self.mill_multiplier * 2)) * self.final_multiplier
            self.wood_gain = (0.1 + (0.1 * self.lumber_camp) * (
                        (self.carpentry_multiplier + 0.1) * 2)) * self.final_multiplier
            self.true_food += self.food_gain * 0.95
            self.food = int(self.true_food)
            self.true_wood += self.wood_gain * 0.95
            self.wood = int(self.true_wood)
            self.mat_output()
            self.pop_growth = (((2 ** (math.sqrt(self.pharmacy+1))))/200 + (self.pop / 20000))
            self.true_pop += self.pop_growth
            self.unemployed += self.pop_growth
            self.pop = int(self.true_pop)
            self.true_gold += self.gold_gain * 0.95
            self.final_multiplier = (1 * (2 * (self.tavern + 0.5))) ** (self.festival_tent + 1)+self.age/10
            if self.Researching_carpentry == True:
                if self.carpentry_progress <= 9999 and self.true_gold >= 0:
                    self.carpentry_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_carpentry = False

            if self.Researching_mill == True:
                if self.mill_progress <= 9999 and self.true_gold >= 0:
                    self.mill_progress += (((0.1 * self.philosopher) * (1 + (self.observatory * 2))))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_mill = False

            if self.Researching_tax_office == True:
                if self.tax_office_progress <= 9999 and self.true_gold >= 0:
                    self.tax_office_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_tax_office = False

            if self.Researching_tavern == True:
                if self.tavern_progress <= 29999 and self.true_gold >= 0:
                    self.tavern_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_tavern = False

            if (self.pop - self.house) > 0:
                self.homeless = self.pop - self.house
                self.happiness -= 0.01
            else:
                self.homeless = 0
                self.happiness = ((1 * self.park) - (self.tax * 10)) + 1
        elif self.happiness >= -4:
            self.gold_gain = (2 + (2 + (2 * (self.house * self.tax))) * (
                        self.tax_office_multiplier * 2)) * self.final_multiplier
            self.food_gain = (0.1 + (0.1 + (0.1 * self.farm)) * (self.mill_multiplier * 2)) * self.final_multiplier
            self.wood_gain = (0.1 + (0.1 * self.lumber_camp) * (
                        (self.carpentry_multiplier + 0.1) * 2)) * self.final_multiplier
            self.true_food += self.food_gain * 0.9
            self.food = int(self.true_food)
            self.true_wood += self.wood_gain * 0.9
            self.wood = int(self.true_wood)
            self.mat_output()
            self.pop_growth = (((2 ** (self.pharmacy + 1))) / 200 + (self.pop / 20000))
            self.true_pop += self.pop_growth
            self.unemployed += self.pop_growth
            self.pop = int(self.true_pop)
            self.true_gold += self.gold_gain * 0.9
            self.final_multiplier = (1 * (2 * (self.tavern + 0.5))) ** (self.festival_tent + 1)+self.age/10
            if self.Researching_carpentry == True:
                if self.carpentry_progress <= 9999 and self.true_gold >= 0:
                    self.carpentry_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_carpentry = False

            if self.Researching_mill == True:
                if self.mill_progress <= 9999 and self.true_gold >= 0:
                    self.mill_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_mill = False

            if self.Researching_tax_office == True:
                if self.tax_office_progress <= 9999 and self.true_gold >= 0:
                    self.tax_office_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_tax_office = False

            if self.Researching_tavern == True:
                if self.tavern_progress <= 29999 and self.true_gold >= 0:
                    self.tavern_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_tavern = False
            if (self.pop - self.house) > 0:
                self.homeless = self.pop - self.house
            else:
                self.homeless = 0
                self.happiness = ((1 * self.park) - (self.tax * 10)) + 1
        elif self.happiness >= -6:
            self.gold_gain = (2 + (2 + (2 * (self.house * self.tax))) * (
                        self.tax_office_multiplier * 2)) * self.final_multiplier
            self.food_gain = (0.1 + (0.1 + (0.1 * self.farm)) * (self.mill_multiplier * 2)) * self.final_multiplier
            self.wood_gain = (0.1 + (0.1 * self.lumber_camp) * (
                        (self.carpentry_multiplier + 0.1) * 2)) * self.final_multiplier
            self.true_food += self.food_gain * 0.8
            self.food = int(self.true_food)
            self.true_wood += self.wood_gain * 0.8
            self.wood = int(self.true_wood)
            self.mat_output()
            self.pop_growth = (((2 ** (math.sqrt(self.pharmacy+1))))/200 + (self.pop / 20000))
            self.true_pop += self.pop_growth
            self.unemployed += self.pop_growth
            self.pop = int(self.true_pop)
            self.true_gold += self.gold_gain * 0.8
            self.final_multiplier = (1 * (2 * (self.tavern + 0.5))) ** (self.festival_tent + 1)+self.age/10
            if self.Researching_carpentry == True:
                if self.carpentry_progress <= 9999 and self.true_gold >= 0:
                    self.carpentry_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_carpentry = False

            if self.Researching_mill == True:
                if self.mill_progress <= 9999 and self.true_gold >= 0:
                    self.mill_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_mill = False

            if self.Researching_tax_office == True:
                if self.tax_office_progress <= 9999 and self.true_gold >= 0:
                    self.tax_office_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_tax_office = False

            if self.Researching_tavern == True:
                if self.tavern_progress <= 29999 and self.true_gold >= 0:
                    self.tavern_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_tavern = False

            if (self.pop - self.house) > 0:
                self.homeless = self.pop - self.house
            else:
                self.homeless = 0
                self.happiness = ((1 * self.park) - (self.tax * 10)) + 1
        else:
            self.gold_gain = (2 + (2 + (2 * (self.house * self.tax))) * (
                        self.tax_office_multiplier * 2)) * self.final_multiplier
            self.food_gain = (0.1 + (0.1 + (0.1 * self.farm)) * (self.mill_multiplier * 2)) * self.final_multiplier
            self.wood_gain = (0.1 + (0.1 * self.lumber_camp) * (
                        (self.carpentry_multiplier + 0.1) * 2)) * self.final_multiplier
            self.true_food += self.food_gain * 0.5
            self.food = int(self.true_food)
            self.true_wood += self.wood_gain * 0.5
            self.wood = int(self.true_wood)
            self.mat_output()
            self.pop_growth = (((2 ** (math.sqrt(self.pharmacy+1)))/200 + (self.pop / 20000)))
            self.true_pop += self.pop_growth
            self.unemployed += self.pop_growth
            self.pop = int(self.true_pop)
            self.true_gold += self.gold_gain * 0.5
            self.final_multiplier = (1 * (2 * (self.tavern + 0.5))) ** (self.festival_tent + 1) + self.age / 10
            if self.Researching_carpentry == True:
                if self.carpentry_progress <= 9999 and self.true_gold >= 0:
                    self.carpentry_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_carpentry = False

            if self.Researching_mill == True:
                if self.mill_progress <= 9999 and self.true_gold >= 0:
                    self.mill_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_mill = False

            if self.Researching_tax_office == True:
                if self.tax_office_progress <= 9999 and self.true_gold >= 0:
                    self.tax_office_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_tax_office = False

            if self.Researching_tavern == True:
                if self.tavern_progress <= 29999 and self.true_gold >= 0:
                    self.tavern_progress += ((0.1 * self.philosopher) * (1 + (self.observatory * 2)))
                    self.true_gold -= (0.01 * self.philosopher)
                else:
                    self.Researching_tavern = False

            if (self.pop - self.house) > 0:
                self.homeless = self.pop - self.house
            else:
                self.homeless = 0
                self.happiness = ((1 * self.park) - (self.tax * 10)) + 1

    def game_clock(self):
        root.after(100, self.main)


class Settler:
    def __init__(self, role, happines, hunger, health):
        class_role = role
        player.pop += 1
        job = 'undefined'


def write(text):
    screen.configure(state="normal")
    screen.insert("end", text)
    screen.configure(state="disabled")


def clear():
    screen.configure(state="normal")
    screen.delete('1.0', END)
    screen.configure(state="disabled")


##root.bind('<KeyPress>', key_press)
player = Game()
for i in range(10):
    player.Add_settler(Role.UNEMPLOYED, 10, 10, 10)
##print(player.building_list[1]['house'])
player.main()
root.mainloop()
