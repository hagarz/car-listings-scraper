import pandas as pd
from openpyxl.workbook import Workbook
import json
import csv


# cars parameters
ENGINE_SIZE = ['0L', '1.25L']
for i in range(5, 200):
    ENGINE_SIZE.append(f'{i/10}L')
GEARBOX = ['Automatic', 'Manual']
BODY_TYPE = ['Convertible', 'Coupe', 'Estate', 'Hatchback', 'MPV', 'Pickup', 'SUV', 'Saloon']
FUEL_TYPE = ['Bi Fuel', 'Diesel', 'Electric', 'Hybrid – Diesel/Electric', 'Hybrid – Diesel/Electric Plug-in',
             'Hybrid – Petrol/Electric', 'Hybrid – Petrol/Electric Plug-in', 'Petrol']



def load_json(json_filepath):
    with open(json_filepath) as json_file:
        json_data = json.load(json_file)
    return json_data


def transform(json_data):
    """correct missing data and transform JSON data to fit Pandas DataFrame"""
    n = 12
    title, price, fuel, engine_size, gearbox, mileage, body_type, reg_year, brake_horse_power, num_owners, emission, else_\
        = ([] for a in range(n))

    print("Total number of cars scraped:", len(json_data))

    for car in json_data:
        if not car["attributes"]:
            continue

        title.append(car['type'][0])
        price.append(car['price'][0])
        for item in car["attributes"]:
            if item in ENGINE_SIZE:
                engine_size.append(item)
            elif item in GEARBOX:
                gearbox.append(item)
            elif item in BODY_TYPE:
                body_type.append(item)
            elif item in FUEL_TYPE:
                fuel.append(item)
            elif 'miles' in item:
                mileage.append(item)
            elif 'reg' in item:
                reg_year.append(item)
            elif 'BHP' in item or 'PS' in item:
                brake_horse_power.append(item)
            elif 'owner' in item:
                num_owners.append(item)
            elif 'ULEZ' in item:
                emission.append(item)
            else:
                else_.append(item)

        # data correction
        if all("owner" not in i for i in car["attributes"]):
            num_owners.append("")
        if all(s not in j for s in ENGINE_SIZE for j in car["attributes"]):
            engine_size.append("")
        if all("reg" not in i for i in car["attributes"]):
            reg_year.append("N/A")
        if all(s not in j for s in BODY_TYPE for j in car["attributes"]):
            body_type.append("")
        if all(s not in j for s in ('BHP', 'PS') for j in car["attributes"]):
            brake_horse_power.append("")
        if all("ULEZ" not in i for i in car["attributes"]):
            emission.append("")

    cars_dict = {
        'title': title, 'Price': price,
        'Reg Year': reg_year, 'Body Type': body_type, 'Mileage': mileage, 'Engine Size': engine_size,'Gearbox': gearbox,
        'Fuel Type': fuel, 'BHP': brake_horse_power, "Number of owners": num_owners, "Emission": emission
    }

    print(f"Will convert to Excel {len(title)} cars listings\n")
    for i in cars_dict:
        print(i, len(cars_dict[i]))

    return cars_dict



def json_to_csv():
    """Convert JSON to CSV"""

    # Opening JSON file and loading the data into the variable data
    with open(json_filepath) as json_file:
        data = json.load(json_file)
    cars_data = data

    # open a file for writing
    data_file = open('cars_data.csv', 'w')

    # create the csv writer object
    csv_writer = csv.writer(data_file)

    # Counter variable used for writing
    # headers to the CSV file
    count = 0

    for car in cars_data:
        if count == 0:
            # Writing headers of CSV file
            header = car.keys()
            csv_writer.writerow(header)
            count += 1

        # Writing data of CSV file
        csv_writer.writerow(car.values())

    data_file.close()




def data_to_excel(cars_dict):
    df = pd.DataFrame(cars_dict)
    df.to_excel('cars_listings.xlsx')



if __name__ == '__main__':
    # dirname = os.path.dirname(__file__)
    # json_filepath = os.path.join(dirname,'/cars_s.json')
    json_filepath = 'cars_s.json'

    json_data = load_json(json_filepath)
    data_to_excel(transform(json_data))
