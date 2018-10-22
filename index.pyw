# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QInputDialog
from PyQt5 import uic
import mysql.connector
from mysql.connector import errorcode
import time
from datetime import datetime
from sys import exit
from time import sleep
import os
from PIL import Image
import shutil
import sys


#load  ui files
first_window = 'Ui/first_window'
form_1, base_1 = uic.loadUiType(first_window)

input_window = 'Ui/input_case.ui'
form_2, base_2 = uic.loadUiType(input_window)

show_all_cases_window = 'Ui/show_all_cases.ui'
form_3, base_3 = uic.loadUiType(show_all_cases_window)

search_by_name = 'Ui/search_by_name.ui'
form_4, base_4 = uic.loadUiType(search_by_name)

show_case_in_form = 'Ui/show_case_in_form.ui'
form_5, base_5 = uic.loadUiType(show_case_in_form)

update_people_in_form = 'Ui/update_people_in_form.ui'
form_6, base_6 = uic.loadUiType(update_people_in_form)

cases_counter = 'Ui/cases_counter.ui'
form_7, base_7 = uic.loadUiType(cases_counter)

explain_app = 'Ui/explain_app.ui'
form_8, base_8 = uic.loadUiType(explain_app)

class msj_rhm(object):

	def __init__(self):

    	self.username = 'root'  # input("username: ")
        self.password = '123456'  # input("password: ")
        self.database = 'msj_rhm'  # input("DataBase: ")

        # DataBase data

        self.config = {
            'user': self.username,  # from mysqlserver or workbench
            'password': self.password,
            'host': '127.0.0.1',
            'database': self.database

        }

        self.DBconnection()

    def DBconnection(self):

        # Check error Access
        try:
            self.cnx = mysql.connector.connect(**self.config)


            self.cursor = self.cnx.cursor()
            #print("ok")
            return ('نجاح الاتصال','تم الاتصال بقاعدة البيانات بنجاح')

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                #print("Something is wrong with your uesrname or password")
                return ('فشل الاتصال','خطأ في الاتصال بقاعدة البيانات | إسم المستخدم أو كلمة المرور')
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                #print("database dosen't exist")
                return ('فشل الاتصال','خطأ في الاتصال بقاعدة البيانات | قاعدة البيانات غير موجودة')
            else:
                #print(err)
                return ('فشل الاتصال','خطأ في الاتصال بقاعدة البيانات')

    #Extract Data from data base
    # 1 # By Combo Boxes
    def show_all_data(self,b,c,p,s,h,i,k,m,u):

        self.query = ("""SELECT lower(`case_main`.`CaseID`),
                            `case_main`.`Class`,
                            `case_main`.`TypeOfCase`,
                            LOWER(`case_main`.`FamilyCount`),


                            `case_needs`.`CaseNeeds`,
                            `case_needs`.`CaseOtherNeeds`,

                            `home_info`.`HomeType`,
                            `home_info`.`Address`,

                            `case_people`.`Name`,
                            `case_people`.`NationalID`,
                            `case_people`.`ParentOrSon`,
                            lower(`case_people`.`DoB`),
                            `case_people`.`PhoneNo`,
                            `case_people`.`jop`,
                            `case_people`.`LearningStatus`,

                            `income`.`IncomeStatement`,
                            LOWER(`income`.`IncomeSalary`),
                            `income`.`OtherIncome`,
                            LOWER(`income`.`SalaryOfOtherIncome`),
                            `income`.`NameOfOtherIncome`,

                            `health_status`.`HealthStatus`,
                            `health_status`.`TypeOfDisease`,

                            `case_main`.`CaseDescription`,
                            `case_people`.`folder`

                            FROM
                            case_main

                            RIGHT JOIN `case_needs`
                            ON
                            `case_main`.`CaseID` = `case_needs`.`CaseID`

                            RIGHT JOIN `home_info`
                            ON
                            `case_main`.`CaseID` = `home_info`.`CaseID`

                            RIGHT JOIN `case_people`
                            ON
                            `case_main`.`CaseID` = `case_people`.`CaseID`

                            RIGHT JOIN `income`
                            ON
                            `case_people`.`NationalID` = `income`.`NationalID`

                            RIGHT JOIN `health_status`
                            ON
                            `case_people`.`NationalID` = `health_status`.`NationalID`

                            WHERE `case_main`.`TypeOfCase` LIKE %r
                             AND `case_main`.`Class` LIKE %r
                             AND `case_needs`.`CaseNeeds` LIKE %r
                             AND `home_info`.`HomeType` LIKE %r
                             AND `case_people`.`ParentOrSon` LIKE %r
                             AND `case_people`.`LearningStatus` LIKE %r
                             AND `income`.`IncomeStatement` LIKE %r
                             AND `income`.`OtherIncome` LIKE %r
                             AND `health_status`.`HealthStatus` LIKE %r

                              ;""")


        self.cursor.execute(self.query % (b,c,p,s,h,i,k,m,u)  )


        result = self.cursor.fetchall()
        return result
    # 2 # By adv. search
    def show_all_data_by_adv_search(self,column_name,value,op,x,y):

        self.query = ("""SELECT lower(`case_main`.`CaseID`),
                            `case_main`.`Class`,
                            `case_main`.`TypeOfCase`,
                            lower(`case_main`.`FamilyCount`),


                            `case_needs`.`CaseNeeds`,
                            `case_needs`.`CaseOtherNeeds`,

                            `home_info`.`HomeType`,
                            `home_info`.`Address`,

                            `case_people`.`Name`,
                            `case_people`.`NationalID`,
                            `case_people`.`ParentOrSon`,
                            lower(`case_people`.`DoB`),
                            `case_people`.`PhoneNo`,
                            `case_people`.`jop`,
                            `case_people`.`LearningStatus`,

                            `income`.`IncomeStatement`,
                            LOWER(`income`.`IncomeSalary`),
                            `income`.`OtherIncome`,
                            LOWER(`income`.`SalaryOfOtherIncome`),
                            `income`.`NameOfOtherIncome`,

                            `health_status`.`HealthStatus`,
                            `health_status`.`TypeOfDisease`,

                            `case_main`.`CaseDescription`,
                            `case_people`.`folder`

                            FROM
                            case_main

                            RIGHT JOIN `case_needs`
                            ON
                            `case_main`.`CaseID` = `case_needs`.`CaseID`

                            RIGHT JOIN `home_info`
                            ON
                            `case_main`.`CaseID` = `home_info`.`CaseID`

                            RIGHT JOIN `case_people`
                            ON
                            `case_main`.`CaseID` = `case_people`.`CaseID`

                            RIGHT JOIN `income`
                            ON
                            `case_people`.`NationalID` = `income`.`NationalID`

                            RIGHT JOIN `health_status`
                            ON
                            `case_people`.`NationalID` = `health_status`.`NationalID`

                            WHERE %s %s %r %s %r


                              ;""")

        self.cursor.execute(self.query % (column_name,op,value,x,y))

        result = self.cursor.fetchall()
        return result

####################################
    #Extract data to case form
    def show_case_main(self, c_id):

        self.query = ("""SELECT
                                lower(`case_main`.`CaseID`),
                                `case_main`.`Class`,
                                `case_main`.`TypeOfCase`,
                                `case_main`.`FamilyCount`,


                                `case_needs`.`CaseNeeds`,
                                `case_needs`.`CaseOtherNeeds`,

                                `home_info`.`HomeType`,
                                `home_info`.`Address`,


                                `case_main`.`CaseDescription`


                                FROM
                                case_main

                                RIGHT JOIN `case_needs`
                                ON
                                `case_main`.`CaseID` = `case_needs`.`CaseID`

                                RIGHT JOIN `home_info`
                                ON
                                `case_main`.`CaseID` = `home_info`.`CaseID`


                                WHERE `case_main`.`CaseID` = %r


                                  ;""")

        self.cursor.execute(self.query % c_id)

        result = self.cursor.fetchall()
        return result

    def show_people_in_table(self, c_id):
        self.query = ("""SELECT

                            `case_people`.`Name`,
                            `case_people`.`NationalID`,
                            lower(`case_people`.`DoB`),
                            LOWER(YEAR(CURRENT_TIMESTAMP()) - YEAR(DoB)) as age,
                            `case_people`.`ParentOrSon`,

                            `case_people`.`jop`,
                            `case_people`.`LearningStatus`,
                            `health_status`.`HealthStatus`,
                            `health_status`.`TypeOfDisease`,
                            `case_people`.`PhoneNo`,



                            `income`.`IncomeStatement`,
                            LOWER(`income`.`IncomeSalary`),
                            `income`.`OtherIncome`,
                            `income`.`NameOfOtherIncome`,
                            LOWER(`income`.`SalaryOfOtherIncome`),





                            `case_people`.`folder`

                            FROM
                            `case_people`

                            RIGHT JOIN `income`
                            ON
                            `case_people`.`NationalID` = `income`.`NationalID`

                            RIGHT JOIN `health_status`
                            ON
                            `case_people`.`NationalID` = `health_status`.`NationalID`

                            WHERE `case_people`.`CaseID` = %r


                              ;""")

        self.cursor.execute(self.query % c_id)

        result = self.cursor.fetchall()
        return result

    def show_people_in_form(self, c_id, nat_id):
        self.query = ("""SELECT
                            `case_people`.`CaseID`,
                            `case_people`.`Name`,
                            `case_people`.`NationalID`,
                            `case_people`.`DoB`,

                            `case_people`.`ParentOrSon`,

                            `case_people`.`jop`,
                            `case_people`.`LearningStatus`,
                            `health_status`.`HealthStatus`,
                            `health_status`.`TypeOfDisease`,
                            `case_people`.`PhoneNo`,



                            `income`.`IncomeStatement`,
                            LOWER(`income`.`IncomeSalary`),
                            `income`.`OtherIncome`,
                            `income`.`NameOfOtherIncome`,
                            LOWER(`income`.`SalaryOfOtherIncome`),

                            `case_people`.`folder`

                            FROM
                            `case_people`

                            RIGHT JOIN `income`
                            ON
                            `case_people`.`NationalID` = `income`.`NationalID`

                            RIGHT JOIN `health_status`
                            ON
                            `case_people`.`NationalID` = `health_status`.`NationalID`

                            WHERE `case_people`.`CaseID` = %r
                            AND
                            `case_people`.`NationalID` = %r


                              ;""")

        self.cursor.execute(self.query % (c_id, nat_id))

        result = self.cursor.fetchall()
        return result
########################
    # insert DAta
    def data_insertion_case(self,c,b,d,r,p,q,s,t):
###############################
####### Case_Main Table #######
###############################
        self.query_case_main = ("INSERT INTO Case_Main"
                      "(Class,TypeOfCase,FamilyCount,CaseDescription)"
                      " VALUES (%r,%r,%r,%r)")

        self.cursor.execute(self.query_case_main % (c, b, d, r))

###############################
####### Home_info Table #######
###############################
        self.query_Home = ("""
        INSERT INTO Home_info (CaseID,HomeType,Address)
        VALUES(LAST_INSERT_ID(),%r,%r)""")

        self.cursor.execute(self.query_Home%(p,q))

###############################
####### Case_Needs Table ######
###############################
        self.query_case_needs=("""
        INSERT INTO Case_Needs(CaseID,CaseNeeds,CaseOtherNeeds)
        VALUES(LAST_INSERT_ID(),%r,%r)""")

        self.cursor.execute(self.query_case_needs %(s,t))


# Commit Data
        self.cnx.commit()

    def data_insertion_people(self,f,e,g,h,x,i,j, k, l, m, n, o,u,v,folderpath):# To insert People

###############################
####### Case_People Table #####
###############################
        self.query_case_people = ("""
                INSERT INTO Case_People(CaseID,NationalID,Name,DoB,ParentOrSon,jop,LearningStatus,PhoneNo,folder)
                VALUES(LAST_INSERT_ID(),%r,%r,%r,%r,%r,%r,%r,%r)""")

        self.cursor.execute(self.query_case_people % (f, e, g, h,x, i, j,folderpath))

###############################
####### Income Table ##########
###############################
        self.query_income = ("""
            INSERT INTO Income(NationalID,IncomeStatement,IncomeSalary,OtherIncome,NameOfOtherIncome,SalaryOfOtherIncome)
            VALUES(%r,%r,%r,%r,%r,%r)""")

        self.cursor.execute(self.query_income % (f, k, l, m, n, o))

###############################
####### Health_Status Table ###
###############################

        self.query_health_status = ("""
                 INSERT INTO Health_Status(NationalID, HealthStatus, TypeOfDisease )
                 VALUES(%r, %r, %r)""")

        self.cursor.execute(self.query_health_status % (f, u, v))

# Commit Data
        self.cnx.commit()

# Add new people to an exist case: here not using last insert Id func.
    def data_insertion_new_people(self,a, f, e, g, h, x, i, j, k, l, m, n, o, u, v, folderpath):  # To insert People

        ###############################
        ####### Case_People Table #####
        ###############################
        self.query_case_people = ("""
                        INSERT INTO Case_People(CaseID,NationalID,Name,DoB,ParentOrSon,jop,LearningStatus,PhoneNo,folder)
                        VALUES(%r,%r,%r,%r,%r,%r,%r,%r,%r)""")

        self.cursor.execute(self.query_case_people % (a,f, e, g, h, x, i, j, folderpath))

        ###############################
        ####### Income Table ##########
        ###############################
        self.query_income = ("""
                    INSERT INTO Income(NationalID,IncomeStatement,IncomeSalary,OtherIncome,NameOfOtherIncome,SalaryOfOtherIncome)
                    VALUES(%r,%r,%r,%r,%r,%r)""")

        self.cursor.execute(self.query_income % (f, k, l, m, n, o))

        ###############################
        ####### Health_Status Table ###
        ###############################

        self.query_health_status = ("""
                         INSERT INTO Health_Status(NationalID, HealthStatus, TypeOfDisease )
                         VALUES(%r, %r, %r)""")

        self.cursor.execute(self.query_health_status % (f, u, v))

        # Commit Data
        self.cnx.commit()

        #################

    def id_find(self): # To return ID to any  GUI object

        self.cursor.execute("SELECT LAST_INSERT_ID();")

        for i in self.cursor:
            return i[0]
#################

    def data_update_people(self, f, e, g, h,x, i, j, k, l, m, n, o, u, v, folderpath,  nat_id_sent):  # To insert People

        ###############################
        ####### Case_People Table #####
        ###############################
        self.query_case_people = ("""
                        UPDATE Case_People SET
                        NationalID = %r,
                        Name = %r,
                        DoB = %r,
                        ParentOrSon = %r,
                        jop = %r,
                        LearningStatus = %r,
                        PhoneNo = %r,
                        folder = %r

                        WHERE Case_People.NationalID = %r;
                        """)

        self.cursor.execute(self.query_case_people % (f, e, g, h, x, i, j, folderpath,nat_id_sent))

        ###############################
        ####### Income Table ##########
        ###############################
        self.query_income = ("""
                    UPDATE Income SET
                    NationalID = %r,
                    IncomeStatement = %r,
                    IncomeSalary = %r,
                    OtherIncome = %r,
                    NameOfOtherIncome = %r ,
                    SalaryOfOtherIncome = %r

                    WHERE Income.NationalID = %r;
                    """)

        self.cursor.execute(self.query_income % (f,k, l, m, n, o,nat_id_sent))

        ###############################
        ####### Health_Status Table ###
        ###############################

        self.query_health_status = ("""
                         UPDATE Health_Status SET
                         NationalID = %r,
                         HealthStatus = %r,
                         TypeOfDisease = %r

                        WHERE Health_Status.NationalID = %r;

                         """)

        self.cursor.execute(self.query_health_status % (f,u, v,nat_id_sent))

        # Commit Data
        self.cnx.commit()

    def data_update_case(self,case_id_sent,c,b,d,r,p,q,s,t):
        ###############################
        ####### Case_Main Table #######
        ###############################
        self.query_case_main = ("""
                                UPDATE Case_Main SET
                                Class = %r,
                                TypeOfCase = %r,
                                FamilyCount = %r,
                                CaseDescription = %r

                                Where Case_Main.CaseID = %r
                                """)

        self.cursor.execute(self.query_case_main % (c, b, d, r,case_id_sent))

        ###############################
        ####### Home_info Table #######
        ###############################
        self.query_Home = ("""
                                UPDATE Home_info SET
                                HomeType = %r,
                                Address = %r
                                Where Home_info.CaseID = %r
                                """)

        self.cursor.execute(self.query_Home % (p, q, case_id_sent))

        ###############################
        ####### Case_Needs Table ######
        ###############################
        self.query_case_needs = ("""
                                UPDATE Case_Needs SET
                                CaseNeeds = %r,
                                CaseOtherNeeds = %r
                                Where Case_Needs.CaseID = %r
                                """)

        self.cursor.execute(self.query_case_needs % (s, t,case_id_sent))

        # Commit Data
        self.cnx.commit()
#################
    def delete_case(self,case_id):
        ###############################
        ####### Case_Main Table #######
        ###############################
        self.query_case_main = ("""
                                    DELETE FROM Case_Main

                                    Where Case_Main.CaseID = %r
                                    """)

        self.cursor.execute(self.query_case_main % (case_id))

        ###############################
        ####### Home_info Table #######
        ###############################
        self.query_Home = ("""
                                    DELETE FROM Home_info
                                    Where Home_info.CaseID = %r
                                    """)

        self.cursor.execute(self.query_Home % (case_id))

        ###############################
        ####### Case_Needs Table ######
        ###############################
        self.query_case_needs = ("""
                                    DELETE FROM Case_Needs
                                    Where Case_Needs.CaseID = %r
                                    """)

        self.cursor.execute(self.query_case_needs % (case_id))

        # Commit Data
        self.cnx.commit()

    def delete_case_people(self,nat_id):
        ###############################
        ####### Case_People Table #####
        ###############################
        self.query_case_people = ("""
                            DELETE FROM Case_People
                            WHERE Case_People.NationalID = %r;
                            """)

        self.cursor.execute(self.query_case_people % (nat_id))

        ###############################
        ####### Income Table ##########
        ###############################
        self.query_income = ("""
                        DELETE FROM Income

                        WHERE Income.NationalID = %r;
                        """)

        self.cursor.execute(self.query_income % (nat_id))

        ###############################
        ####### Health_Status Table ###
        ###############################

        self.query_health_status = ("""
                             DELETE FROM Health_Status

                            WHERE Health_Status.NationalID = %r;

                             """)

        self.cursor.execute(self.query_health_status % (nat_id))

        # Commit Data
        self.cnx.commit()



###############################################################
################### ***( Engine of Application )***############
###############################################################
class Engine(object):

    connection = msj_rhm()

    app_folder = ('برنامج إدارة الحالات')
    app_folder_path = r'C:\Program Files\%s' % app_folder

    if not os.path.exists(app_folder_path):
        os.makedirs(app_folder_path)

    #############################
    ###### **( Windows Opening )** ######
    #############################
    # 1

    def open_input_w(self):  # open input new case window
        self.input = InputWindow()
        self.input.showMaximized()
        self.close()

    # 2
    def open_all_cases_w(self):  # open the show all cases window
        self.all_cases = ShowAllCases()
        self.all_cases.showMaximized()
        self.close()


    # 3
    def open_adv_search_w(self, search):  # open the show all cases window with advanced search
        self.search_name = AdvSearch(search)
        self.search_name.showMaximized()
        self.close()

    # 4
    def open_case_in_form_w(self):
        try:

            self.open_form = ShowCaseInForm(self.current_cell_of_case_id().text())
            self.open_form.showMaximized()
            self.close()
        except:
            self.show_message('خطأ' , 'يرجي تحديد الحالة أولا ! ')

    # 5
    def open_update_people_form_w(self):
        try:
            self.people_form = UpdatePeopleInForm(self.current_case_id_from_case_form(), self.current_nat_id_from_table())
            self.people_form.showMaximized()
            self.close()
        except:
            self.show_message("خطأ" , "يرجي تحديد الفرد المراد تحديثه أولا !")

    def open_add_new_people_form_w(self):
        try:
            self.addpeople_form = AddNewPeopleInForm(str(self.current_case_id_from_case_form()))
            self.addpeople_form.showMaximized()
            self.close()
        except:
            self.show_message("خطأ", "خطأ | يرجي المحاولة مرة آخرى !")

    # 6
    def open_statistics_w(self):
        self.statistics = Statistics()
        self.statistics.show()
        self.close()
    # 7
    def open_explain_w(self):
        self.explain = Explain()
        self.explain.showMaximized()
        self.close()

    # 8
    def contact_dev(self):
        self.show_message("الاتصال بمطور البرنامج ",
                          """
                                  في حالة مواجهة أي صعوبات أو أخطاء تشغيل لا تتردد في الاتصال علي
            01119329320  | 011255555371
            admainstrator@gmail.com
                          """)
    #######################################################################

# Check Boxes list
    def chk_bxes(self):
        self.check_boxes = {
            self.chb_id: 0,
            self.chb_class: 1,
            self.chb_type: 2,
            self.chb_count_family: 3,
            self.chb_case_needs: 4,
            self.chb_other_needs: 5,
            self.chb_home_type: 6,
            self.chb_address: 7,
            self.chb_people_name: 8,
            self.chb_nat_id: 9,
            self.chb_parent_or_son: 10,
            self.chb_dob: 11,
            self.chb_phone_no: 12,
            self.chb_jop: 13,
            self.chb_learn_status: 14,
            self.chb_income_statement: 15,
            self.chb_income_salary: 16,
            self.chb_income_st_other: 17,
            self.chb_salary_from_other: 18,
            self.chb_name_of_other: 19,
            self.chb_health_status: 20,
            self.chb_type_ofdisease: 21,
            self.chb_description: 22,
            self.chb_folder: 23

        }

        return self.check_boxes

######################
##**(Menu Triggers)**#
######################

    def menu_triggers(self):
        self.mn_input_cases.triggered.connect(self.open_input_w)
        self.mn_view_cases.triggered.connect(self.open_all_cases_w)
        self.mn_search_name.triggered.connect(lambda :self.open_adv_search_w('name'))
        self.mn_search_natid.triggered.connect(lambda: self.open_adv_search_w('nat_id'))
        self.mn_search_code.triggered.connect(lambda: self.open_adv_search_w('c_id'))
        self.mn_search_age.triggered.connect(lambda: self.open_adv_search_w('age'))
        self.mn_search_salary.triggered.connect(lambda: self.open_adv_search_w('salary'))
        self.mn_search_jop.triggered.connect(lambda: self.open_adv_search_w('jop'))
        self.mn_search_count_f.triggered.connect(lambda: self.open_adv_search_w('family_count'))
        self.mn_search_phone.triggered.connect(lambda: self.open_adv_search_w('phone_no'))
        self.mn_search_cmb.triggered.connect(self.open_all_cases_w)
        self.mn_cases_counter.triggered.connect(self.open_statistics_w)
        self.mn_update_case.triggered.connect(self.menu_action_update_case)
        self.mn_explain.triggered.connect(self.open_explain_w)
        self.mn_contact.triggered.connect(self.contact_dev)
# some trigger functions
    def menu_action_update_case(self):
        self.show_message("بحث الحالات" , "قم باختيار الحالة المراد تحديثها !")
        self.open_all_cases_w()

######################
  ##**( Buttons )**#
######################

## 1 ## Buttons in new input case Window ####

    def buttons_new_input_case(self):
        self.btn_add_case.clicked.connect(self.add_case)
        self.btn_add_to_case.clicked.connect(self.add_people)
        self.btn_add_documents.clicked.connect(self.copy_files)
        self.btn_activate_new_case.clicked.connect(self.activate_new_case)


        self.btn_view_cases.clicked.connect(self.open_all_cases_w)
        self.btn_search.clicked.connect(self.open_all_cases_w)

    # Functions of buttons
    def finderid(self):
        a = self.connection.id_find()
        self.c_id.setText(str(a))

    def add_case(self):
        self.b = (self.type_of_case.itemText(self.type_of_case.currentIndex()))
        self.c = (self.case_class.itemText(self.case_class.currentIndex()))
        self.d = int(self.family_count.text())
        self.r = (str(self.case_describtion.toPlainText()))
        self.p = (self.home_type.itemText(self.home_type.currentIndex()))
        self.q = (str(self.address.text()))
        self.s = (self.case_needs.itemText(self.case_needs.currentIndex()))
        self.t = (str(self.other_needs.toPlainText()))

        self.connection.data_insertion_case(self.c, self.b, self.d, self.r, self.p, self.q, self.s, self.t)
        self.finderid()
        self.family_count.setValue(0)
        self.case_describtion.clear()
        self.address.clear()
        self.other_needs.clear()

        self.groupBox.setEnabled(True)
        self.btn_add_case.setEnabled(False)
        self.btn_activate_new_case.setEnabled(True)
        self.btn_add_documents.setEnabled(False)

        self.show_message(" تمت إضافة حالة بنجاح " , "  والآن , قم بإضافة الأفراد للحالة \n يرجي العلم بأنه في حالة عدم إضافة أفراد سيتم تجاهل الحالة في البحث  ")
    def add_people(self):
        try:
            self.a = (self.c_id.text())
            self.e = (self.name.text())
            self.f = int(self.nat_id.text())
            self.g = (self.dob.text())
            self.h = (self.parent_or_son.itemText(self.parent_or_son.currentIndex()))
            self.i = (self.learn_status.itemText(self.learn_status.currentIndex()))
            self.j = (self.phone_no.text())
            self.k = (self.income_statement.itemText(self.income_statement.currentIndex()))
            self.l = int(self.income_salary.text())
            self.m = (self.other_income.itemText(self.other_income.currentIndex()))
            self.n = (self.name_of_other_income.text())
            self.o = int(self.salary_of_other_income.text())
            self.u = (self.health_status.itemText(self.health_status.currentIndex()))
            self.v = (self.Type_of_desease.text())
            self.x = (self.jop.text())

            folder_name = ('%r + %s' % (self.a, self.e))
            self.newpath = r'C:\Program Files\%s\ %s' % (self.app_folder,folder_name)

            if not os.path.exists(self.newpath):
                os.makedirs(self.newpath)

            self.connection.data_insertion_people(self.f, self.e, self.g,
                                                  self.h, self.x, self.i,
                                                  self.j, self.k, self.l, self.m,
                                                  self.n, self.o, self.u, self.v, self.newpath)

            self.name.clear()
            self.nat_id.clear()
            self.dob.setDate(QtCore.QDate(1900, 1, 1))
            self.phone_no.clear()
            self.income_salary.setText('0')
            self.name_of_other_income.clear()
            self.salary_of_other_income.setText('0')
            self.Type_of_desease.clear()
            self.btn_add_documents.setEnabled(True)

            file = open(r'%s\%s.txt' % (self.newpath, self.e), 'w+')
            file.writelines("  كود الحالة  " + self.a + '\n' +
                            "  الاسم  " + self.e + '\n' +
                            "   الرقم القومي   " + str(self.f) + '\n' +
                            "   تاريخ الميلاد   " + self.g + '\n' +
                            "   الصفة   " + self.h + '\n' +
                            "   الحالة التعليمية   " + self.i + '\n' +
                            "   التليفون   " + self.j + '\n' +
                            "   بيان الدخل   " + self.k + '\n' +
                            "   مبلغ الدخل   " + str(self.l) + '\n' +
                            "  مصادر الدخل الاخرى   " + self.m + '\n' +
                            "    اسم مصادر الدخل الاخرى   " + self.n + '\n' +
                            "    مبلغ من مصادر الدخل الاخرى   " + str(self.o) + '\n' +
                            "    الحالة الصحية   " + self.u + '\n' +
                            "    بيان الحالة الصحية   " + self.v)
            self.show_message(" تم بنجاح" , "تمت اضافة الفرد بنجاح، الآن تستطيع إضافة مستندات للفرد - أو - إضافة فرد آخر")
        except:
            self.show_message('خطأ !','خطأ في إضافة البيانات ، يرجي التأكد من صحة البيانات !! ')

    def copy_files(self):
        try:
            openfile = QtWidgets.QFileDialog.getOpenFileName(self, 'نسخ الصور والمستندات', 'c:/')
            shutil.copy(openfile[0], self.newpath)  # Which newpath is defined in add people
            os.startfile(openfile[0])
            self.show_message(' تم بنجاح' , ' تمت عملية إضافة المستندات بنجاح ...')
        except:
            self.show_message('خطأ', 'خطأ في نسخ المستندات يرجي المحاولة مرة آخرى')
    def activate_new_case(self):
        button_reply = QtWidgets.QMessageBox.question(self, 'تأكيد',
                                                      'سوف يتم الانتقال إلي إضافة حالة جديدةهل انت متأكد من انتهائك من إضافة الأفراد ؟ ',
                                                      QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                      QtWidgets.QMessageBox.No)
        if button_reply == QtWidgets.QMessageBox.Yes:
            try:
                self.show_message('تم بنجاح','تمت عملية إضافة الحالة  ، الآن تستطيع إضافة حالة جديدة !! ')
                self.btn_add_case.setEnabled(True)
                self.c_id.setText('0')
                self.groupBox.setEnabled(False)
            except:
                self.show_message('خطأ', 'خطأ | يرجي المحاولة مرة آخرى')
        else:pass


###########################################################

## 2 ## Buttons in Show All Cases Window #### search by combo boxes

    def buttons_all_cases(self):
        self.btn_open_case_form.clicked.connect(self.open_case_in_form_w)
        self.btn_open_folder.clicked.connect(self.open_folder)
        self.btn_show_columns.clicked.connect(self.show_columns)
        self.btn_hide_columns.clicked.connect(self.hide_columns)

    def search_button_cmb(self):
        self.btn_search_now.clicked.connect(self.filter_data)
## 3 ## Buttons in Show All Cases Window #### ADV. search

    def search_button_adv(self):
        self.btn_search_now.clicked.connect(self.filter_data_adv)


## 4 ## Buttons in Case Form Window ####

    def buttons_update_case(self):
        self.btn_update_main_case.clicked.connect(self.update_case)
        self.btn_update_people.clicked.connect(self.open_update_people_form_w)
        self.btn_delete_case.clicked.connect(self.delete_all_case)
        self.btn_view_cases.clicked.connect(self.open_all_cases_w)
        self.btn_open_folder.clicked.connect(self.open_people_folder_from_case_form)
        self.btn_add_people.clicked.connect(self.open_add_new_people_form_w)

    #Functions of buttons
    def update_case(self):
        try:
            self.a = int(self.c_id.text())
            self.b = (self.type_of_case.itemText(self.type_of_case.currentIndex()))
            self.c = (self.case_class.itemText(self.case_class.currentIndex()))
            self.d = int(self.family_count.text())
            self.r = (str(self.case_describtion.toPlainText()))
            self.p = (self.home_type.itemText(self.home_type.currentIndex()))
            self.q = (str(self.address.text()))
            self.s = (self.case_needs.itemText(self.case_needs.currentIndex()))
            self.t = (str(self.other_needs.toPlainText()))

            self.connection.data_update_case(self.a, self.c, self.b, self.d, self.r, self.p, self.q, self.s, self.t)
            self.show_message('نجاح العملية',"تم تحديث الحالة بنجاح")

        except:
            self.show_message('خطأ','يوجد خطأ في تحديث البيانات ، يرجي المحاولة مرة آخري')
    def delete_all_case(self):
        button_reply = QtWidgets.QMessageBox.question(self,'تأكيد الحذف','سوف يتم حذف الحالة نهائيا، هل بالتأكيد تريد حذف الحالة ؟ ',QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,QtWidgets.QMessageBox.No)
        if button_reply == QtWidgets.QMessageBox.Yes:
            try:
                self.a = int(self.c_id.text())
                self.connection.delete_case(self.a)
                self.show_message("تم الحذف","تمت عملية حذف الحالة بنجاح")
            except:
                self.show_message("خطأ", "خطأ في حذف البيانات ، يرجي المحاولة مرة آخري !")
        else:pass

    def open_people_folder_from_case_form(self):
        try:
            row = self.tableWidget.currentRow()
            self.a = self.tableWidget.item(row, 15)
            os.startfile(self.a.text())
        except:
            self.show_message('خطأ','محاولة خاطئة ، يرجي إعادة المحاولة !')

## 5 ## Buttons in Update people Window ####

    def buttons_update_people(self):
        self.btn_update_people_now.clicked.connect(self.update_people)
        self.btn_delete_people_now.clicked.connect(self.delete_from_people)
        a = int(self.c_id.text())
        self.btn_back_to_case.clicked.connect(lambda: self.back_to_case(a))
        self.btn_add_documents.clicked.connect(self.update_copy_files)
        self.btn_open_folder.clicked.connect(self.open_folder_people_form)
        self.btn_add_new_people.clicked.connect(self.add_new_people)
    # Functions of buttons
    def update_people(self):
        try:
            self.a = (self.c_id.text())
            self.e = (self.name.text())
            self.f = int(self.nat_id.text())
            self.g = (self.dob.text())
            self.h = (self.parent_or_son.itemText(self.parent_or_son.currentIndex()))
            self.i = (self.learn_status.itemText(self.learn_status.currentIndex()))
            self.j = (self.phone_no.text())
            self.k = (self.income_statement.itemText(self.income_statement.currentIndex()))
            self.l = int(self.income_salary.text())
            self.m = (self.other_income.itemText(self.other_income.currentIndex()))
            self.n = (self.name_of_other_income.text())
            self.o = int(self.salary_of_other_income.text())
            self.u = (self.health_status.itemText(self.health_status.currentIndex()))
            self.v = (self.Type_of_desease.text())
            self.x = (self.jop.text())

            folder_name = ('%r + %s' % (self.a, self.e))
            self.newpath = r'C:\Program Files\%s\ %s' % (self.app_folder,folder_name)

            if not os.path.exists(self.newpath):
                os.makedirs(self.newpath)
                ###########################
            self.connection.data_update_people(self.f, self.e, self.g,
                                               self.h, self.x, self.i,
                                               self.j, self.k, self.l, self.m,
                                               self.n, self.o, self.u, self.v, self.newpath, self.pre_nat)
            ###################################


            file = open(r'%s\%s.txt' % (self.newpath, self.e), 'w+')
            file.writelines("  كود الحالة  " + self.a + '\n' +
                            "  الاسم  " + self.e + '\n' +
                            "   الرقم القومي   " + str(self.f) + '\n' +
                            "   تاريخ الميلاد   " + self.g + '\n' +
                            "   الصفة   " + self.h + '\n' +
                            "   الحالة التعليمية   " + self.i + '\n' +
                            "   التليفون   " + self.j + '\n' +
                            "   بيان الدخل   " + self.k + '\n' +
                            "   مبلغ الدخل   " + str(self.l) + '\n' +
                            "  مصادر الدخل الاخرى   " + self.m + '\n' +
                            "    اسم مصادر الدخل الاخرى   " + self.n + '\n' +
                            "    مبلغ من مصادر الدخل الاخرى   " + str(self.o) + '\n' +
                            "    الحالة الصحية   " + self.u + '\n' +
                            "    بيان الحالة الصحية   " + self.v)


            self.show_message('تم بنجاح','تمت عملية تحديث البيانات بنجاح !')

        except:
            self.show_message('خطأ','يوجد خطأ في تحديث البيانات ، يرجي المحاولة مرة آخرى')

    def delete_from_people(self):
        button_reply = QtWidgets.QMessageBox.question(self, 'تأكيد الحذف',
                                                      'سوف يتم حذف الفرد نهائيا، هل بالتأكيد تريد الحذف ؟ ',
                                                      QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                      QtWidgets.QMessageBox.No)
        if button_reply == QtWidgets.QMessageBox.Yes:
            try:
                self.f = int(self.nat_id.text())
                self.connection.delete_case_people(self.f)
                self.show_message('تم الحذف','تمت عملية حذف الفرد بنجاح')
            except:
                self.show_message('خطأ', 'خطأ في عملية الحذف، يرجي المحاولة مرة آخرى')
    def back_to_case(self,a):
        self.back_form = ShowCaseInForm(a)
        self.back_form.showMaximized()
        self.close()

    def open_folder_people_form(self):
        try:
            os.startfile(self.folder_path.text())
        except:
            self.show_message('خطأ', 'محاولة خاطئة ، يرجي إعادة المحاولة !')

    def update_copy_files(self):
        try:
            openfile = QtWidgets.QFileDialog.getOpenFileName(self, 'نسخ الصور والمستندات', 'c:/')
            shutil.copy(openfile[0], self.folder_path.text())  # Which newpath is defined in add people
            os.startfile(openfile[0])
            self.show_message(' تم بنجاح', ' تمت عملية إضافة المستندات بنجاح ...')
        except:
            self.show_message('خطأ', 'خطأ في نسخ المستندات يرجي المحاولة مرة آخرى')

    def add_new_people(self):
        try:
            self.a = (self.c_id.text())
            self.e = (self.name.text())
            self.f = int(self.nat_id.text())
            self.g = (self.dob.text())
            self.h = (self.parent_or_son.itemText(self.parent_or_son.currentIndex()))
            self.i = (self.learn_status.itemText(self.learn_status.currentIndex()))
            self.j = (self.phone_no.text())
            self.k = (self.income_statement.itemText(self.income_statement.currentIndex()))
            self.l = int(self.income_salary.text())
            self.m = (self.other_income.itemText(self.other_income.currentIndex()))
            self.n = (self.name_of_other_income.text())
            self.o = int(self.salary_of_other_income.text())
            self.u = (self.health_status.itemText(self.health_status.currentIndex()))
            self.v = (self.Type_of_desease.text())
            self.x = (self.jop.text())

            folder_name = ('%r + %s' % (self.a, self.e))
            self.newpath = r'C:\Program Files\%s\ %s' % (self.app_folder,folder_name)

            if not os.path.exists(self.newpath):
                os.makedirs(self.newpath)

            self.connection.data_insertion_new_people(self.a,self.f, self.e, self.g,
                                                  self.h, self.x, self.i,
                                                  self.j, self.k, self.l, self.m,
                                                  self.n, self.o, self.u, self.v, self.newpath)



            self.folder_path.setText(self.newpath)
            file = open(r'%s\%s.txt' % (self.newpath, self.e), 'w+')
            file.writelines("  كود الحالة  " + self.a + '\n' +
                            "  الاسم  " + self.e + '\n' +
                            "   الرقم القومي   " + str(self.f) + '\n' +
                            "   تاريخ الميلاد   " + self.g + '\n' +
                            "   الصفة   " + self.h + '\n' +
                            "   الحالة التعليمية   " + self.i + '\n' +
                            "   التليفون   " + self.j + '\n' +
                            "   بيان الدخل   " + self.k + '\n' +
                            "   مبلغ الدخل   " + str(self.l) + '\n' +
                            "  مصادر الدخل الاخرى   " + self.m + '\n' +
                            "    اسم مصادر الدخل الاخرى   " + self.n + '\n' +
                            "    مبلغ من مصادر الدخل الاخرى   " + str(self.o) + '\n' +
                            "    الحالة الصحية   " + self.u + '\n' +
                            "    بيان الحالة الصحية   " + self.v)
            self.show_message(" تم بنجاح",
                              "تمت اضافة الفرد بنجاح، الآن تستطيع إضافة مستندات للفرد - أو - إضافة فرد آخر")
        except:
            self.show_message('خطأ !', 'خطأ في إضافة البيانات ، يرجي التأكد من صحة البيانات !! ')

    ## 6 ## Button in Statistics Window ####

    def count_from_combo_boxes(self):
        self.b = (self.type_of_case.itemText(self.type_of_case.currentIndex()))
        self.c = (self.case_class.itemText(self.case_class.currentIndex()))
        self.p = (self.home_type.itemText(self.home_type.currentIndex()))
        self.s = (self.case_needs.itemText(self.case_needs.currentIndex()))
        self.h = (self.parent_or_son.itemText(self.parent_or_son.currentIndex()))
        self.i = (self.learn_status.itemText(self.learn_status.currentIndex()))
        self.k = (self.income_statement.itemText(self.income_statement.currentIndex()))
        self.m = (self.other_income.itemText(self.other_income.currentIndex()))
        self.u = (self.health_status.itemText(self.health_status.currentIndex()))

        if "الكل" in self.b: self.b = "%"
        if "الكل" in self.c: self.c = "%"
        if "الكل" in self.p: self.p = "%"
        if "الكل" in self.s: self.s = "%"
        if "الكل" in self.h: self.h = "%"
        if "الكل" in self.i: self.i = "%"
        if "الكل" in self.k: self.k = "%"
        if "الكل" in self.m: self.m = "%"
        if "الكل" in self.u: self.u = "%"

        self.count_now(self.b,self.c, self.s ,self.p , self.h, self.i, self.k,self.m ,self.u  )
    def count_now(self,b,c,p,s,h,i,k,m,u):
        self.query = ("""SELECT
                            COUNT(*)

                            FROM
                            case_main

                            RIGHT JOIN `case_needs`
                            ON
                            `case_main`.`CaseID` = `case_needs`.`CaseID`

                            RIGHT JOIN `home_info`
                            ON
                            `case_main`.`CaseID` = `home_info`.`CaseID`

                            RIGHT JOIN `case_people`
                            ON
                            `case_main`.`CaseID` = `case_people`.`CaseID`

                            RIGHT JOIN `income`
                            ON
                            `case_people`.`NationalID` = `income`.`NationalID`

                            RIGHT JOIN `health_status`
                            ON
                            `case_people`.`NationalID` = `health_status`.`NationalID`

                            WHERE `case_main`.`TypeOfCase` LIKE %r
                             AND `case_main`.`Class` LIKE %r
                             AND `case_needs`.`CaseNeeds` LIKE %r
                             AND `home_info`.`HomeType` LIKE %r
                             AND `case_people`.`ParentOrSon` LIKE %r
                             AND `case_people`.`LearningStatus` LIKE %r
                             AND `income`.`IncomeStatement` LIKE %r
                             AND `income`.`OtherIncome` LIKE %r
                             AND `health_status`.`HealthStatus` LIKE %r

                              ;""")

        self.connection.cursor.execute(self.query % (b, c,p, s, h, i, k, m, u))
        result = self.connection.cursor.fetchall()
        #return result
        self.lbl_show_result.setText(str(result[0][0]))


###########################################################

    def show_message(self, title, message):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec_()


    def extract_data(self, b, c, p, s, h, i, k, m, u):

        ####################################################
        ####### extract data when loading
        ##############################################################
        self.t_view_data.setRowCount(0)
        result = self.connection.show_all_data(b, c, p, s, h, i, k, m, u)
        # self.t_view_data.setRowCount(0)
        # self.t_view_data.setLayoutDirection(QtCore.Qt.RightToLeft)

        for row_number, row_data in enumerate(result):
            self.t_view_data.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.t_view_data.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(data))
        self.t_view_data.resizeColumnsToContents()

    def filter_data(self):

        self.b = (self.type_of_case.itemText(self.type_of_case.currentIndex()))
        self.c = (self.case_class.itemText(self.case_class.currentIndex()))
        self.p = (self.home_type.itemText(self.home_type.currentIndex()))
        self.s = (self.case_needs.itemText(self.case_needs.currentIndex()))
        self.h = (self.parent_or_son.itemText(self.parent_or_son.currentIndex()))
        self.i = (self.learn_status.itemText(self.learn_status.currentIndex()))
        self.k = (self.income_statement.itemText(self.income_statement.currentIndex()))
        self.m = (self.other_income.itemText(self.other_income.currentIndex()))
        self.u = (self.health_status.itemText(self.health_status.currentIndex()))

        if "الكل" in self.b: self.b = "%"
        if "الكل" in self.c: self.c = "%"
        if "الكل" in self.p: self.p = "%"
        if "الكل" in self.s: self.s = "%"
        if "الكل" in self.h: self.h = "%"
        if "الكل" in self.i: self.i = "%"
        if "الكل" in self.k: self.k = "%"
        if "الكل" in self.m: self.m = "%"
        if "الكل" in self.u: self.u = "%"

        self.extract_data(self.b,self.c,self.s,self.p,self.h,self.i,self.k,self.m,self.u)

    def filter_data_adv(self):
        try:
            self.e = (self.name.text())
            self.f = (self.nat_id.text())
            self.g = (self.dob.text())
            self.d = (self.family_count.text())
            self.x = (self.jop.text())
            self.j = (self.phone_no.text())
            self.l = int(self.income_salary_from.text())
            self.z = int(self.income_salary_to.text())
            self.a = (self.c_id.text())

            lista = {
                self.name : [self.e,"`Case_People`.`Name`",'=','',''],
                self.nat_id : [self.f,"`Case_People`.`NationalID`",'=','',''],
                self.dob : [self.g ,"`Case_People`.`DoB`",'=','',''],
                self.family_count : [self.d,"`Case_Main`.`FamilyCount`",'=','',''],
                self.jop : [self.x,"`Case_People`.`jop`",'=','',''],
                self.phone_no : [self.j,"`Case_People`.`PhoneNo`",'=','',''],
                self.income_salary_from : [self.l,"`Income`.`IncomeSalary`",'BETWEEN','AND',self.z],

                self.c_id : [self.a,"`Case_Main`.`CaseID`",'=','','']
            }
            for item , value in lista.items():
                if item.isEnabled():

                    self.t_view_data.setRowCount(0)
                    result = self.connection.show_all_data_by_adv_search(value[1],value[0],value[2],value[3],value[4])

                    for row_number, row_data in enumerate(result):
                        self.t_view_data.insertRow(row_number)
                        for column_number, data in enumerate(row_data):
                            self.t_view_data.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(data))
                            #self.t_view_data.resizeColumnsToContents()
        except:
            self.show_message("خطأ","خطأ | يرجي المحاولة مرة آخري !")

    def hide_columns(self):

        columns_list = []



        for chb,column_no in self.chk_bxes().items():
            if chb.isChecked() == False:
                columns_list.append(column_no)
                #chb.setCheckState(QtCore.Qt.PartiallyChecked)



        for column in columns_list:

            if self.t_view_data.isColumnHidden(column) == False:
                self.t_view_data.setColumnHidden(column,True)

    def show_columns(self):

            columns_list = []

            for chb, column_no in self.chk_bxes().items():
                if chb.isChecked() == True:
                    columns_list.append(column_no)
                    # chb.setCheckState(QtCore.Qt.PartiallyChecked)

            for column in columns_list:

                if self.t_view_data.isColumnHidden(column) == True:
                    self.t_view_data.setColumnHidden(column, False)

    def open_folder(self):
        try:
            self.t_view_data.setLayoutDirection(QtCore.Qt.RightToLeft)
            row = self.t_view_data.currentRow()

            column = self.t_view_data.currentColumn()

            self.a = self.t_view_data.item(row, 23)

            os.startfile(self.a.text())
        except AttributeError:
            self.show_message("خطأ !!","يرجي تحديد خانة مجلد مستندات الحالة")
        except FileNotFoundError:
            self.show_message("خطأ !!", "هذا المجلد غير موجود !")

    def extract_into_form(self,case_id):


        main_case = self.connection.show_case_main(case_id)

        for data in main_case:
            self.c_id.setText(data[0])
            self.case_class.setCurrentText(data[1])
            self.type_of_case.setCurrentText(data[2])
            self.family_count.setValue(data[3])
            self.case_needs.setCurrentText(data[4])
            self.other_needs.setText(data[5])
            self.home_type.setCurrentText(data[6])
            self.address.setText(data[7])
            self.case_describtion.setText(data[8])

        people = self.connection.show_people_in_table(case_id)

        self.tableWidget.setRowCount(0)
        result = people
        # self.t_view_data.setRowCount(0)
        # self.t_view_data.setLayoutDirection(QtCore.Qt.RightToLeft)

        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(data))




    def current_cell_of_case_id(self):

        row = self.t_view_data.currentRow()

        cell = self.t_view_data.item(row, 0)

        return cell

    def current_case_id_from_case_form(self):
        code = int(self.c_id.text())

        return code

    def current_nat_id_from_table(self):
        row = self.tableWidget.currentRow()

        cell = self.tableWidget.item(row, 1)
        return  int(cell.text())

    def extract_people_in_form(self,case_id,nat_id):
        people = self.connection.show_people_in_form(case_id, nat_id)

        for data in people:
            self.c_id.setText(str(data[0]))
            self.name.setText(data[1])
            self.nat_id.setText(data[2])
            self.dob.setDate(QtCore.QDate((data[3])))
            self.parent_or_son.setCurrentText(data[4])
            self.jop.setText(data[5])
            self.learn_status.setCurrentText(data[6])
            self.health_status.setCurrentText(data[7])
            self.Type_of_desease.setText(data[8])
            self.phone_no.setText(data[9])
            self.income_statement.setCurrentText(data[10])
            self.income_salary.setText(data[11])
            self.other_income.setCurrentText(data[12])
            self.name_of_other_income.setText(data[13])
            self.salary_of_other_income.setText(data[14])
            self.folder_path.setText(data[15])

###############################################################
################# Windows Classes ############
###############################################################

class FirstWindow(base_1, form_1,Engine):
    def __init__(self):
        super(base_1,self).__init__()
        self.setupUi(self)
        self.btn_open_input.clicked.connect(self.open_input_w)
        self.btn_open_output.clicked.connect(self.open_all_cases_w)

        self.show_message("التحقق من الاتصال",self.connection.DBconnection()[1])


class InputWindow(base_2, form_2,Engine):
    def __init__(self):

        super(base_2, self).__init__()
        self.setupUi(self)
        self.menu_triggers()
        self.buttons_new_input_case()

class ShowAllCases(base_3, form_3,Engine):

    def __init__(self):

        super(base_3, self).__init__()

        self.setupUi(self)

        self.extract_data("%", "%", "%", "%", "%", "%", "%", "%", "%")

        self.menu_triggers()

        self.buttons_all_cases()
        self.search_button_cmb()

class AdvSearch(base_4, form_4,Engine):
    def __init__(self,search):
        super(base_4, self).__init__()

        self.setupUi(self)

        self.extract_data("%", "%", "%", "%", "%", "%", "%", "%", "%")

        self.menu_triggers()

        self.buttons_all_cases()
        self.search_button_adv()

        #self.Nat_Id_completer()

        adv_search = {
            'c_id' : [self.Name_completer,
                        self.name.setFocus,
                        self.nat_id.setEnabled,
                        self.name.setEnabled,
                        self.dob.setEnabled,
                        self.family_count.setEnabled,
                        self.jop.setEnabled,
                        self.phone_no.setEnabled,
                        self.income_salary_from.setEnabled,
                        self.income_salary_to.setEnabled,
                        self.c_id.setDisabled],
            'name' : [self.Name_completer,
                        self.name.setFocus,
                        self.nat_id.setEnabled,
                        self.name.setDisabled,
                        self.dob.setEnabled,
                        self.family_count.setEnabled,
                        self.jop.setEnabled,
                        self.phone_no.setEnabled,
                        self.income_salary_from.setEnabled,
                        self.income_salary_to.setEnabled,
                        self.c_id.setEnabled],
            'age' : [self.Name_completer,
                        self.name.setFocus,
                        self.nat_id.setEnabled,
                        self.name.setEnabled,
                        self.dob.setDisabled,
                        self.family_count.setEnabled,
                        self.jop.setEnabled,
                        self.phone_no.setEnabled,
                        self.income_salary_from.setEnabled,
                        self.income_salary_to.setEnabled,
                        self.c_id.setEnabled],
            'nat_id' : [self.Nat_Id_completer,
                        self.nat_id.setFocus,
                        self.nat_id.setDisabled,
                        self.name.setEnabled,
                        self.dob.setEnabled,
                        self.family_count.setEnabled,
                        self.jop.setEnabled,
                        self.phone_no.setEnabled,
                        self.income_salary_from.setEnabled,
                        self.income_salary_to.setEnabled,
                        self.c_id.setEnabled
                        ],
            'salary' : [self.Name_completer,
                        self.name.setFocus,
                        self.nat_id.setEnabled,
                        self.name.setEnabled,
                        self.dob.setEnabled,
                        self.family_count.setEnabled,
                        self.jop.setEnabled,
                        self.phone_no.setEnabled,
                        self.income_salary_from.setDisabled,
                        self.income_salary_to.setDisabled,
                        self.c_id.setEnabled],
            'jop' : [self.Name_completer,
                        self.name.setFocus,
                        self.nat_id.setEnabled,
                        self.name.setEnabled,
                        self.dob.setEnabled,
                        self.family_count.setEnabled,
                        self.jop.setDisabled,
                        self.phone_no.setEnabled,
                        self.income_salary_from.setEnabled,
                        self.income_salary_to.setEnabled,
                        self.c_id.setEnabled],
            'family_count':[self.Name_completer,
                        self.name.setFocus,
                        self.nat_id.setEnabled,
                        self.name.setEnabled,
                        self.dob.setEnabled,
                        self.family_count.setDisabled,
                        self.jop.setEnabled,
                        self.phone_no.setEnabled,
                        self.income_salary_from.setEnabled,
                        self.income_salary_to.setEnabled,
                        self.c_id.setEnabled],
            'phone_no' :[self.Name_completer,
                        self.name.setFocus,
                        self.nat_id.setEnabled,
                        self.name.setEnabled,
                        self.dob.setEnabled,
                        self.family_count.setEnabled,
                        self.jop.setEnabled,
                        self.phone_no.setDisabled,
                        self.income_salary_from.setEnabled,
                        self.income_salary_to.setEnabled,
                        self.c_id.setEnabled]

        }
        for key,value in adv_search.items():
            if search in key:
                (value[0](),value[1](),value[2](False),value[3](False),value[4](False),
                 value[5](False),value[6](False),
                value[7](False),value[7](False),value[8](False),value[9](False),value[10](False))


            else:pass

###########################
##### Auto Complete Names##

    def Auto_Complete_Name(self,model):
        self.connection.cursor.execute("SELECT Name FROM Case_People;")

        names_list = []

        for name in self.connection.cursor:
            names_list.append(name[0])
        model.setStringList(names_list)

    def Name_completer(self):
        names_line_edit = self.name
        completer = QtWidgets.QCompleter()
        names_line_edit.setCompleter(completer)
        model = QtCore.QStringListModel()
        completer.setModel(model)
        self.Auto_Complete_Name(model)

############################
##### Auto Complete Nat Id##

    def Auto_Complete_nat_id(self,model):
        self.connection.cursor.execute("SELECT `NationalID` FROM Case_People;")
        nat_id_list = []

        for name in self.connection.cursor:
            nat_id_list.append(name[0])
        model.setStringList(nat_id_list)

    def Nat_Id_completer(self):
        nat_id_line = self.nat_id
        completer = QtWidgets.QCompleter()
        nat_id_line.setCompleter(completer)
        model = QtCore.QStringListModel()
        completer.setModel(model)
        self.Auto_Complete_nat_id(model)

class ShowCaseInForm(base_5,form_5,Engine):

    def __init__(self,code):
        super(base_5, self).__init__()

        self.setupUi(self)



        self.menu_triggers()
        self.extract_into_form(code)
        self.buttons_update_case()

class UpdatePeopleInForm(base_6,form_6,Engine):
    def __init__(self,x,y):
        super(base_6, self).__init__()

        self.setupUi(self)

        self.menu_triggers()
        self.extract_people_in_form(x,y)
        self.buttons_update_people()
        self.pre_nat = int(self.nat_id.text())

class AddNewPeopleInForm(base_6,form_6,Engine):
    def __init__(self,case_id):
        super(base_6, self).__init__()

        self.setupUi(self)

        self.menu_triggers()
        self.c_id.setText(case_id)
        self.buttons_update_people()
        self.btn_update_people_now.setEnabled(False)
        self.groupBox.setTitle("إضافة فرد جديد للحالة")


class Statistics(base_7,form_7,Engine):
    def __init__(self):
        super(base_7, self).__init__()

        self.setupUi(self)

        self.menu_triggers()

        self.btn_search_now.clicked.connect(self.count_from_combo_boxes)

class Explain(base_8,form_8,Engine):
    def __init__(self):
        super(base_8, self).__init__()

        self.setupUi(self)

        self.menu_triggers()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    root = FirstWindow()
    root.show()
    sys.exit(app.exec_())



