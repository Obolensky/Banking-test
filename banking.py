import random
import sqlite3


class Accounts:
    def __init__(self):
        self.balance = 0
        self.cardNum = 0000000000000000
        self.pin = 0000

    def createaccount(self):
        account_id = str(random.randrange(111111111, 999999999))
        bank_id = "400000"
        calc = bank_id + account_id
        checksum = create_checksum(calc)
        self.cardNum = int(bank_id + account_id + checksum)
        pin = random.randrange(1111, 9999)
        self.pin = pin
        conn.commit()
        print("Your card has been created")
        print("Your card number:")
        print(self.cardNum)
        print("Your card PIN:")
        print(self.pin)
        c.execute("INSERT INTO card (number, pin) VALUES (?,?)", (self.cardNum, self.pin))
        conn.commit()


def create_checksum(number_str):
    number_sum = 0
    for i in range(len(number_str)):
        digit = number_str[i]
        if i % 2 != 1:
            x = int(digit) * 2
            if x > 9:
                digit = str(x // 10 + x % 10)
            else:
                digit = str(x)
        number_sum += int(digit)
    if number_sum % 10 == 0:
        return '0'
    else:
        return str(10 - number_sum % 10)


def login():
    testcard = (input("Enter your card number:\n"))
    testpin = int((input("Enter your PIN:\n")))
    c.execute("SELECT number FROM card")
    nums = [num[0] for num in c.fetchall()]
    if testcard in nums:
        c.execute('SELECT pin FROM card WHERE number = ?', (testcard,))
        goodpin = int(c.fetchone()[0])
        if testpin == goodpin:
            print("You have successfully logged in!")
            current_account = Accounts()
            current_account.cardNum = testcard
            c.execute('SELECT balance FROM card where number = ?', (testcard,))
            current_account.balance = int(c.fetchone()[0])
            logged(testcard)
        else:
            print("Wrong card number or PIN!")
    else:
        print("Wrong card number or PIN!")


def logged(card):
    connected = True
    while connected:
        print("1. Balance")
        print('2. Add income')
        print('3. Do transfer')
        print('4. Close account')
        print("5. Log out")
        print("0. Exit")
        select = int(input())
        if select == 1:
            balance(card)
        elif select == 2:
            add_income(card)
        elif select == 3:
            transfer(card)
        elif select == 4:
            close(card)
            connected = False
        elif select == 5:
            print("You have successfully logged out!")
            connected = False
        else:
            conn.close()
            exit()


def balance(card):
    c.execute('SELECT balance FROM card WHERE number = ?', (card,))
    print(c.fetchone()[0])


def add_income(card):
    income = int(input('Enter income:'))
    c.execute('SELECT balance FROM card WHERE number = ?', (card,))
    old_value = c.fetchone()[0]
    new_value = old_value + income
    c.execute('UPDATE card SET balance = ? WHERE number = ?', (new_value, card))
    conn.commit()
    print('Income was added!')


def transfer(card):
    dest = (input('Enter card number\n'))
    if dest != card:
        c.execute("SELECT number FROM card")
        nums = [num[0] for num in c.fetchall()]
        if dest not in nums:

            if erreurchecksum(int(dest)):
                print('Probably you made mistake in card number. Please try again!')
            else:
                print("Such a card does not exist.")

        else:
            current_account = Accounts()
            current_account.cardNum = card
            c.execute('SELECT balance FROM card where number = ?', (card,))
            current_account.balance = int(c.fetchone()[0])
            money_transfer = int(input('Enter how much money you want to transfer:'))
            if money_transfer > current_account.balance:
                print('Not enough money!')
            else:
                c.execute('SELECT balance FROM card WHERE number = ?', (current_account.cardNum,))
                old_value = c.fetchone()[0]
                new_value = old_value - money_transfer
                c.execute('UPDATE card SET balance = ? WHERE number = ?', (new_value, current_account.cardNum))
                conn.commit()
                c.execute('SELECT balance FROM card WHERE number = ?', (dest,))
                old_value = c.fetchone()[0]
                new_value = old_value + money_transfer
                c.execute('UPDATE card SET balance = ? WHERE number = ?', (new_value, dest))
                conn.commit()
                print('Success')
    else:
        print("You can't transfer money to the same account!")


def erreurchecksum(card):
    check = str(card % 10)   #store checksum of given card
    cardnum = str(card // 10)    #remove last digit from given card
    calccheck = create_checksum(cardnum)    #calculate checksum of given card number
    if calccheck != check:
        return True
    else:
        return False


def close(card):
    c.execute("DELETE from card WHERE number = ?", (card,))
    conn.commit()
    print('The account has been closed!')


def db_connection(db_file):
    return sqlite3.connect(db_file)


def create_table(cursor):
    cursor.execute('CREATE TABLE IF NOT EXISTS card ('
                   'id INTEGER PRIMARY KEY, '
                   'number TEXT NOT NULL UNIQUE, '
                   'pin TEXT NOT NULL, '
                   'balance INTEGER DEFAULT 0);')
    conn.commit()


def menu():
    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")
    choice = int(input())
    if choice == 1:
        new = Accounts()
        new.createaccount()
    elif choice == 2:
        login()
    else:
        conn.close()
        exit()


conn = db_connection('card.s3db')
c = conn.cursor()
create_table(c)

while True:
    menu()
