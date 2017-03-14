# Download raw data from Verizon's site first
import csv
import shutil
import os
import datetime
from collections import Counter
#from Tkinter import Tk
#from tkFileDialog import askopenfilename
from operator import itemgetter
import sys
import zipfile

# we don't need a full GUI, so keep the root window from appearing
#Tk().withdraw()

# show an "Open" dialog box and return the path to the selected file
#vz_file = askopenfilename(
#    title='Choose the "Acct & Wireless Charges Detail Summary Usage" File')

vzwzip=zipfile.ZipFile(sys.argv[1])
listofnames=vzwzip.namelist()

vz_file=''

for i in listofnames:
    basename='Acct & Wireless Charges Detail Summary Usage_'
    if basename in i:
        vz_file=i
# print vz_file

vzwzip.extract(vz_file, './uploads/')

# Pass upload file to backend program to process
# vz_file = sys.argv[1]
vz_file='./uploads/' + vz_file
# print vz_file


file_read = csv.reader(open(vz_file, 'rb'), delimiter='\t')
with open(vz_file, 'rb') as csv_file:
    lol = list(csv.reader(csv_file, delimiter='\t'))
    row_count = len(lol)
# row_count = sum(1 for row in file_read)
# lol = list(csv.reader(open(vz_file, 'rb'), delimiter='\t'))

write_report = 'current_report.rtf'
csv_charge_file = 'charge_list.csv'  # write_csv_file
csv_equip_file = 'equip_charge_list.csv'
csv_data_file = 'data_list.csv'

# This creates a charges list to be saved to a CSV.
charges_list = []
charges_list_titles = []

for i in lol:
    if 'Cost' in i[21]:
        temp_list = [i[5], i[6], i[11], i[21]]
        charges_list_titles.append(temp_list)
    else:
        #[8] is Item Category not Description
        if float(i[21]) > 0 and (('Voice' in i[8]) or ('Messaging' in i[8])
                                 or ('Roaming' in i[8]) or ('Data' in i[8])
                                 or ('Additional Services' in i[8]) 
                                 or ('International' in i[8])
                                 or ('Outside the US' in i[8])
                                 or ('In the US' in i[8])):
            temp_list = [i[5], i[6], i[11],
                         ("$ {0:.2f}".format(float(i[21])))]
            charges_list.append(temp_list)

# Sort charges_list by name and then cost center.
charges_list = sorted(charges_list, key=itemgetter(0))
charges_list = sorted(charges_list, key=itemgetter(1))

# This adds titles to the table.
charges_list.insert(0, charges_list_titles[0])

with open(csv_charge_file, 'wb') as new_csv_charge_file:
    wr = csv.writer(new_csv_charge_file, quoting=csv.QUOTE_ALL)
    wr.writerows(charges_list)

# This creates a charges list to be saved to a CSV.
equip_charge_list = []
equip_charge_list_titles = []

for i in lol:
    if 'Cost' in i[21]:
        temp_list = [i[5], i[6], i[11], i[21]]
        equip_charge_list_titles.append(temp_list)
    else:
        if float(i[21]) > 0 and ('Equipment' in i[8]):
            temp_list = [i[5], i[6], i[11],
                         ("$ {0:.2f}".format(float(i[21])))]
            equip_charge_list.append(temp_list)

# Sort equip_charge_list by name and then cost center.
equip_charge_list = sorted(equip_charge_list, key=itemgetter(0))

# This adds titles to the table.
equip_charge_list.insert(0, equip_charge_list_titles[0])

with open(csv_equip_file, 'wb') as new_equip_csv_file:
    wr = csv.writer(new_equip_csv_file, quoting=csv.QUOTE_ALL)
    wr.writerows(equip_charge_list)

######################################################################
# This creates a data list to be saved to a CSV.
used_data_list = []
used_data_list_titles = []

for i in lol:
    if 'Used' in i[19]:
        temp_list = [i[5], i[6], i[19]]
        used_data_list_titles.append(temp_list)
    else:
        if (('KILOBYTE' in i[11]) and ((float(i[19])) > 2621440)):
            temp_list = [i[5], i[6], ((float(i[19])) / 1048576)]
            used_data_list.append(temp_list)
        elif ('GIGABYTE' in i[11] and ((float(i[19])) > 2.5)):
            temp_list = [i[5], i[6], ((float(i[19])))]
            used_data_list.append(temp_list)
        else:
            None

        # Sort used_data_list by name and then cost center.
used_data_list = sorted(used_data_list, key=itemgetter(2), reverse=True)

# This adds titles to the table.
used_data_list.insert(0, used_data_list_titles[0])

with open(csv_data_file, 'wb') as new_csv_charge_file:
    wr = csv.writer(new_csv_charge_file, quoting=csv.QUOTE_ALL)
    wr.writerows(used_data_list)

######################################################################

# This copies the template file into the reports dir with a new name.
shutil.copy('Template.rtf', write_report)

# Verizon variables to be used in the program.
msg_total = 0  # All messaging costs.
four_one_one = 0
long_distance = 0

msg_overages = 0
total_discount = 0
equipment = 0
smartphone_hotspot = 0
additional_services = 0
data_cost = 0
monthly_charges = 0
taxes = 0
vzw_surcharges = 0
voice_overages = 0

data_kilobytes = 0
data_gigabytes = 0
four_one_one_total = 0

travelpass =0
roaming = 0
international = 0
total_current_charges = 0


# http://stackoverflow.com/questions/4128144/replace-string-within-file-contents
def inplace_change(filename, old_string, new_string):
    s = open(filename).read()
    if old_string in s:
        s = s.replace(old_string, new_string)
        f = open(filename, 'w')
        f.write(s)
        f.flush()
        f.close()
    else:
        print 'No occurances of "{old_string}" found.'.format(
            **locals())


# Iterates over Column 'L' and Column 'V'
# for i in range(1, (row_count - 1)):
# Make sure you skip the first row that has the title with 'lol[1:]'.
for i in lol[1:]:
    description = i[11]
    cost = float(i[21])
    category = i[8]


    if 'Payment Received' in description:
        pass
    else:
        total_current_charges += cost

    if cost <= 0:
        continue

    # columns_LV_d[description] = cost
    if 'Nationwide Bus Talk & Text' in description:
        msg_total += 20  # Difference in plan costs 44.99 and 64.99
    elif 'Message' in description:
        msg_total += cost
    elif 'Txt' in description:
        msg_total += cost
    elif 'PICTURE & VIDEO' in description:
        msg_total += cost
    elif 'TEXT' in description:
        msg_total += cost
    elif '500 Msg Allowance + Unl In Msg ' in description:
        msg_total += cost
    elif '411 Search' in description:
        four_one_one += cost
    elif 'Long Distance' in description:
        long_distance += cost
    elif 'International minutes' in description:
        international += cost 
    elif "International messages" in description:
        international += cost
    elif "International Data" in description:
        international += cost
    elif '22%' in description:
        total_discount += cost
    elif 'Roaming' in description:
        roaming += cost
    elif 'TRAVELPASS' in description:
        international += cost
    elif 'INT TRVL' in description:
        international += cost
    else:
        pass

    if (('International' in category) and (cost > 0)):
        international += cost


# Iterates over Column 'I' and Column 'V'
for i in lol[1:]:
    description = i[8]
    cost = float(i[21])
    # columns_IV_d[description] = cost
    if 'Additional Services' in description:
        additional_services += cost
    elif 'Data' in description:
        data_cost += cost
    elif 'Equipment Charges' in description:
        equipment += cost
    elif 'Messaging' in description:
        msg_overages += cost
    elif 'Monthly Charges' in description:
        monthly_charges += cost
    elif 'Taxes, Governmental Surcharges and Fees' in description:
        taxes += cost
    elif 'Voice' in description:
        voice_overages += cost
    elif 'VZW Surcharges' in description:
        vzw_surcharges += cost
    else:
        pass

# Iterates over Column 'L' and Column 'T'
for i in lol[1:]:
    if i[19] == 'NA':
        continue
    description = i[11]
    cost = float(i[19])
    # columns_LT_d[description] = cost
    if 'GIGABYTE USAGE' in description:
        data_gigabytes += cost
    elif 'KILOBYTE USAGE' in description:
        data_kilobytes += cost
    elif '411 Search' in description:
        four_one_one_total += cost
    else:
        pass


def total_data():
    sum = data_gigabytes + ((data_kilobytes / 1024) / 1024)
    return sum


d = datetime.date.today()
today_date = d.strftime("%B %d, %Y")
d_this_month = d.strftime("%b")
# get current and prior month
# http://stackoverflow.com/questions/9724906/python-date-of-the-previous-month 
d_beg = d.replace(day=1)
d_lastmonth = d_beg - datetime.timedelta(days=1)
d_lastmonth_format = d_lastmonth.strftime("%b")
d_period = d_lastmonth_format + " 04 - " + d_this_month + " 03"
numbers_in_lines = []
for i in lol[1:]:
    numbers_in_lines.append(i[4])
number_of_lines = len(Counter(numbers_in_lines))

# print total_current_charges
# print equipment
# print number_of_lines

average_line_cost_wo_equipment = ("{0:.2f}".format(((
                                total_current_charges - equipment) / number_of_lines)))
variable_charges = (four_one_one + msg_overages + long_distance +
                    roaming + data_cost + equipment + additional_services +
                    international + travelpass)

# Number format changes to $
roaming = ("{0:.2f}".format(roaming))
data_cost = ("{0:.2f}".format(data_cost))
msg_overages = ("{0:.2f}".format(msg_overages))
equipment = ("{0:.2f}".format(equipment))
variable_charges = ("{0:.2f}".format(variable_charges))
additional_services = ("{0:.2f}".format(additional_services))
international = ("{0:.2f}".format(international))
travelpass = ("{0:.2f}".format(travelpass))
four_one_one = ("{0:.2f}".format(four_one_one))
long_distance = ("{0:.2f}".format(long_distance))

# print "international " + international
# print msg_overages
# print four_one_one
# print total_discount
# print equipment
# print smart phone_hot spot
# print additional_services
# print data_cost
# print monthly_charges
# print taxes
# print vzw_surcharges
# print voice_overages
# print long_distance

# print data_kilobytes
# print data_gigabytes
# print four_one_one_total
# print "The total amount of data used was {0:.0f}GB.".format(total_data())
# print variable_charges
# print today_date
# print number_of_lines
# print total_current_charges
# print average_line_cost_wo_equipment
# print d_period


# Replace form place holders with live data.
inplace_change(write_report, '<four_one_one_total>',
               str(int(four_one_one_total)))
inplace_change(write_report, '<four_one_one>', str(four_one_one))
inplace_change(write_report, '<msg_overages>', str(msg_overages))
inplace_change(write_report, '<long_distance>', str(long_distance))
inplace_change(write_report, '<roaming>', str(roaming))
inplace_change(write_report, '<data_cost>', str(data_cost))
inplace_change(write_report, '<equipment>', str(equipment))
inplace_change(write_report, '<today_date>', str(today_date))
inplace_change(write_report, '<number_of_lines>', str(number_of_lines))
inplace_change(write_report, '<average_line_cost_wo_equipment>',
               str(average_line_cost_wo_equipment))
inplace_change(write_report, '<additional_serv>',str(additional_services))
inplace_change(write_report, '<variable_charges>', str(variable_charges))
inplace_change(write_report, '<international>', str(international))
inplace_change(write_report, '<travelpass>', str(travelpass))
inplace_change(write_report, '<d_period>', str(d_period))

# alt + /  will turn on and off block comment in Sublime Text 

shutil.copyfile('current_report.rtf', 'uploads/current_report.rtf')




#os.startfile(write_report)
#os.startfile(csv_charge_file)
#os.startfile(csv_equip_file)
#os.startfile(csv_data_file)
