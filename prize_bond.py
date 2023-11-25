import requests, csv, sys, os
from bs4 import BeautifulSoup
from tabulate import tabulate

def tableize(table):
    records=[]
    tempRow=[]
    for row in table:
        entities = row.find_all("div", attrs={"class": "divTableCell"})
        for entity in entities:
            tempRow.append(entity.text)
        records.append(tempRow)
        tempRow=[]
    return tabulate(records, headers="firstrow", tablefmt="rounded_grid", showindex=True)

def main():
    file_name='bonds.csv'
    searchURL = ("https://savings.gov.pk/latest/results.php")
    country_table={
        '1':'100',
        '2':'200',
        '3':'750',
        '4':'1500',
        '5':'7500',
        '6':'15000',
        '7':'25000',
        '8':'40000',
        '9':'40000 Premium Bond',
        '10':'25000 Premium Bond'
    }

    pb_number_list=''
    try:
        with open(file_name, 'r') as file:
            reader = csv.DictReader(file)
            while True:
                os.system("cls")
                country=input('''Select denomination you want to check:
    [1] 100
    [2] 200
    [3] 750
    [4] 1500
    [5] 7500
    [6] 15000
    [7] 25000
    [8] 40000
    [9] 40000 Premium Bond
    [10] 25000 Premium Bond
                              
Your input here: ''')
                try:
                    if 0<int(country)<=len(country_table): break
                except: continue
                else: continue
            for row in reader:
                try:
                    value = str(row[country_table[country]]).strip().replace(',','')
                    if 0 < len(value):
                        if len(value) < 6:
                            value=('0' * (6 - len(value))) + value
                        pb_number_list+=value+","
                except KeyError:
                    os.system("cls")
                    input(f"Denomination '{country_table[country]}' does not have any entries or the entries are invalid. Press [Enter] to exit.\n")
                    sys.exit()
    except FileNotFoundError:
        fieldnames=[]
        for i in country_table:
            fieldnames+=[country_table[i]]
        with open(file_name, 'w') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            os.system("cls")
            input(f'{file_name} has been created. Open the file, enter the entries and then save it. After that, run this program again.\nPress [Enter] to exit.\n')
            sys.exit()
        
    pb_number_list=pb_number_list[:-1]
    payload = {
        'country': country,
        'state': 'all',
        'range_from': "",
        'range_to': "",
        'pb_number_list': pb_number_list,
        'btnsearch': 'Search'
    }

    with requests.session() as s:
        try:
            r = s.post(searchURL, data=payload)
        except:
            os.system("cls")
            input("Please make sure that you are connected to the internet.\nPress [Enter] to exit.\n")
            sys.exit()
        soup = BeautifulSoup(r.text,'html.parser')
        try:
            table=soup.find_all("div", attrs={"class": "divTableRow"})
            
            os.system("cls")
            print("Congrats! you won the following bonds:\n")
            print(tableize(table))
        except:
            os.system("cls")
            print(f'None of {country_table[country]}s matched to the server.')
    input("\nPress [Enter] to exit.\n")

if __name__ == "__main__":
    main()

# pyinstaller -F -icon C:\Users\ar69k\OneDrive\Documents\Icons\prize_bond.ico prize_bond.py