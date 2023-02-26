from tabulate import tabulate

PURPLE = '\033[95m'
CYAN = '\033[96m'
DARKCYAN = '\033[36m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
END = '\033[0m'
CBEIGE2  = '\33[96m'

# Creating a class for shoe and defining the attributes
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity
        
    def get_cost(self):
        print(self.cost)


    def get_quantity(self):
        print(self.quantity)
    

    def __str__(self):
        return f'{self.country},{self.code},{self.product},{self.cost},{self.quantity}'

shoe_list = []

def read_shoes_data():
    # clearing the shoe list data to ensure we are continuously refreshing our read of the txt file
    shoe_list.clear()
    # exception handling to ensure the data in txt file is valid in terms of file path, number of indexes, correct data types
    try:
        open_inventory = open('T32 Capstone 4 Project/inventory.txt', 'r')
        read_inventory = open_inventory.readlines()[1:]
        # loop through the lines in the txt file and split
        for line,shoe_obj in enumerate(read_inventory):
            temp = shoe_obj.strip('\n')
            temp = temp.split(',')
            # append each index per line into a shoe object 
            shoe_list.append(Shoe(temp[0], temp[1], temp[2], float(temp[3]), int(temp[4])))
    except FileNotFoundError as error:
        print('Please ensure the file path for the inventory file is correct')
        print()
        print(error)
    except IndexError:
            print(f'Error on line {line+2}:'
            '\nmissing data on this line')
            exit()
    except ValueError:
            print(f'Error on line {line+2}'
            '\nThe cost entered must be of float type and the quantity must be an integer.')
            exit()
        
    open_inventory.close()


def capture_shoes():
    read_shoes_data()
    open_inventory = open('T32 Capstone 4 Project/inventory.txt', 'a+')
    # creating a new shoe object based on user input, then write the new object to the file using the append mode
    while True:
        try:
            new_shoe_object = Shoe(input('Please enter country: '), input('Please enter code: '), input('Please enter product name: '), float(input('Please enter shoe cost: ')), int(input('Please enter shoe quantity: ')))
            break
        except ValueError:
            print('One of your inputs does not have the correct data type, please try again')
            continue
    # also append to the shoe list
    open_inventory.write(f'\n{str(new_shoe_object)}')
    shoe_list.append(new_shoe_object)
    open_inventory.close()
    

def view_all():
    read_shoes_data()
    # made a 2D list out of the objects in the shoe object list, then was able to use tabulate to display data in a nice table
    object_list = []
    for shoe_obj in shoe_list:
        object_list.append([shoe_obj.country, shoe_obj.code, shoe_obj.product, shoe_obj.cost, shoe_obj.quantity])
    print(tabulate(object_list,headers=['Country', 'Code', 'Product', 'Cost', 'Quantity'],tablefmt='fancy_grid'))
    

def re_stock():
    read_shoes_data()
    # finding the first quantity in the file and then comparing it to subsequent quantities to get the smallest
    lowest_quantity = shoe_list[0].quantity
    for shoe in shoe_list:
        if shoe.quantity < lowest_quantity:
            lowest_quantity = shoe.quantity
            lowest_shoe = shoe
    # loop through the shoe list and add additional stock amount to the lowest shoe 
    addition = int(input(f'The product with the least stock is the [{lowest_shoe.product} | Code: {lowest_shoe.code}]\n\nHow much stock would you like to add?\n'))
    for shoe_obj in shoe_list:
        if shoe_obj.product == lowest_shoe.product:
            shoe_obj.quantity += addition
    with open('T32 Capstone 4 Project/inventory.txt','w') as file: 
        file.write('Country,Code,Product,Cost,Quantity')     
    # overwriting the headers and then appending the new data with the updated quanity for lowest shoe
    with open('T32 Capstone 4 Project/inventory.txt','a') as file:
        for shoe in shoe_list:
            shoe_string = f'\n{shoe.country},{shoe.code},{shoe.product},{shoe.cost},{shoe.quantity}'
            file.write(shoe_string)
    

def search_shoe():
    read_shoes_data()
    shoe_code = input('Please enter the code of the shoe you want to search for: ')
    # if the shoe object code entered matches the code in our shoe object, return the attributes for this particular shoe
    for shoe_obj in shoe_list:
        if shoe_obj.code == shoe_code:
            output = '\n=========== Search Result ==============\n'
            output += f'Country: \t{shoe_obj.country}\n'
            output += f'Code: \t\t{shoe_obj.code}\n'
            output += f'Product: \t{shoe_obj.product}\n'
            output += f'Cost: \t\t{shoe_obj.cost}\n'
            output += f'Quantity: \t{shoe_obj.quantity}\n'
            print(output)                
                

def value_per_item():
    value_list = []
    read_shoes_data()
    for shoe_obj in shoe_list:
        # appended to a new 2D list containing the product name and the total value of the shoe
        value_line = [shoe_obj.product, (float(shoe_obj.cost) * int(shoe_obj.quantity))]        
        value_list.append(value_line)
    print()
    # then able to use this 2D list for the tabulate function
    print(tabulate(value_list,headers=['Product', 'Total Value'],tablefmt='fancy_grid'))
    print()
    

def highest_qty():
    read_shoes_data()
    # same method as lowest quantity just needed to switch the operator to greater than to find highest quantity stock
    lowest_quantity = shoe_list[0].quantity
    for shoe in shoe_list:
        if shoe.quantity > lowest_quantity:
            lowest_quantity = shoe.quantity
            highest_shoe = shoe
    # print(f'\n{highest_shoe.product} is for SALE!')
    print(f'\n════════════ 🔴 {RED}{highest_shoe.product} IS ON SALE! OFFER ENDS SOON!{END} 🔴 ══════════════\n')


while True:
    print(f"""           
        {RED}╔══════════════════════╗{END}
        {BOLD}  INVENTORY MAIN MENU 
        {RED}╚══════════════════════╝{END}
    """)
    print('')
    option = int(input("""please select an option from the below:\n
🔸 1 - add new shoe
🔸 2 - view all shoes
🔸 3 - restock lowest quantity item
🔸 4 - search shoe
🔸 5 - view value of all shoes
🔸 6 - view highest quantity stock
🔸 7 - exit program\n"""))
    if option == 1:
        capture_shoes()

    elif option == 2:
        view_all()

    elif option == 3:
        re_stock()

    elif option == 4:
        search_shoe()

    elif option == 5:
        value_per_item()

    elif option == 6:
        highest_qty()

    elif option == 7:
        print(f'\n═════════════════ 👋 {YELLOW}{BOLD}Goodbye!!!{END} 👋 ══════════════════\n')
        exit()

    else:
        print('Oops, you have not selected a valid option, please try again')
