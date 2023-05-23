import pandas as pd
import json

input_path = "../../../data/ethnologue/ethnologue20.tab"
location_path = "../../../data/ethnologue/locations.tsv"
isocodes_path = "../../../data/parallel/isocodes.json"
continent_path = "../../../data/ethnologue/cont-country-map.csv"
x = pd.read_csv(input_path, sep="\t")
y = pd.read_csv(location_path, sep='\t')
isocodes = set(json.load(open(isocodes_path)).values())
continents = pd.read_csv(continent_path)


y.columns = ['country_code', 'lat', 'long', 'country_name']
y['n']  = 0
y['homecontinent'] = 'Asia'
print(y.head())
print(continents.head())
table = []
for i in range(x.shape[0]):
    lang = x.loc[i,  :]['name']
    code = x.loc[i,  :]['ISO 639-3']
    bool_iso = code in isocodes

    if bool_iso:
        country = x.loc[i,  :]['Country']

        if country == "Myanmar":
            country = "Myanmar [Burma]"
        elif country == "Viet Nam":
            country = "Vietnam"
        elif country == "Democratic Republic of the Congo":
            country = "Congo [DRC]"
        elif country == "Vatican State":
            country = "Vatican City"
        elif country == "Russian Federation":
            country = "Russia"
        elif country == "South Sudan":
            country = "Sudan"
        elif country == "Korea, South":
            country = "South Korea"
        elif country == "Macedonia":
            country = "Macedonia [FYROM]"
        elif country == "Cape Verde Islands":
            country = "Cape Verde"

        bool_country = country in y['country_name'].values
        if bool_country:
            y.loc[y['country_name'] == country, 'n'] += 1
            c_code = y.loc[y['country_name'] == country, 'country_code'].values[0]
            try:
                cont_name = continents.loc[continents['Two_Letter_Country_Code'] == c_code, 'Continent_Name'].values[0]
            except:
                cont_name = "NA"
            y.loc[y['country_name'] == country, 'homecontinent'] = cont_name


y = y.drop(['country_name', 'country_code'], axis=1)
y = y.sort_values(by='n', ascending=False)
y.columns = ['homelat', 'homelon', 'n', 'homecontinent']
y = y[['homelat', 'homelon', 'homecontinent', 'n']]
y.to_csv("../../../data/ethnologue/visual.csv", index=False)

for i in range(y.shape[0]):
    string = "{"
    string += f"homelat: \"{y['homelat'][i]}\", homelon: \"{y['homelon'][i]}\", homecontinent: \"{y['homecontinent'][i]}\", n: \"{y['n'][i]}\""
    string += "},"
    print(string)



#
