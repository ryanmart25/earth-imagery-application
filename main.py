import PySimpleGUI as sg
from owslib.wms import WebMapService

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


MAXREQUESTS = 3


def makeRequest(n, image_number, date):
    wms = WebMapService('https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?', version='1.1.1')

    # Configure request for MODIS_Terra_CorrectedReflectance_TrueColor
    img = wms.getmap(layers=['MODIS_Terra_CorrectedReflectance_TrueColor'],  # Layers
                     srs='epsg:4326',  # Map projection
                     bbox=(-180, -90, 180, 90),  # Bounds
                     size=(1200, 600),  # Image size
                     time=date,  # Time of data

                     format='image/png',  # Image format
                     transparent=True)  # Nodata transparency
    if img is None:
        return 'FAILED'
    else:
        # make unique path
        image_path = f"Images/MODIS_Terra_CorrectedReflectance_TrueColor.png"
        # Save output PNG to a file
        out = open(image_path, 'wb')
        out.write(img.read())
        out.close()
        return image_path


def main(image_number: int, date: str) -> str:
    path = makeRequest(MAXREQUESTS, image_number, date)
    return path


if __name__ == '__main__':
    main(0, "2022-08-01")
# Build GUI


# Connect to GIBS WMS Service


# View image
# Image('python-examples/MODIS_Terra_CorrectedReflectance_TrueColor.png')


# Construct capability URL.
# wmsUrl = 'https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?\
# SERVICE=WMS&REQUEST=GetCapabilities'

# Request WMS capabilities.
# response = requests.get(wmsUrl)

# Display capabilities XML in original format. Tag and content in one line.
# WmsXml = xmltree.fromstring(response.content)
# print(xmltree.tostring(WmsXml, pretty_print = True, encoding = str))


# productType = "wmts/epsg4326/"
# visualizationTime = "best/"
# baseUrl = "https://gibs.earthdata.nasa.gov/"
# LayerIdentifier = "MODIS_Terra_CorrectedReflectance_TrueColor/"
#
# tilematrixset = "250m/"
# tilematrix = "6/"
# searchurl = ""
#
# def buildURL():
#
#    time: str = input("Format: [YYYY-MM-DD]\nEnter time: ")
#    row = input("Input Row: ")
#    column = input("Input column: ")
#    searchURL = f'{baseUrl}{productType}{visualizationTime}{LayerIdentifier}default/{time}/{tilematrixset}{tilematrix}{row}/{column}/.jpg'
#    print(searchURL)
# def requestImage(url):
#    try:
#        response = requests.get(url)
#    except requests.HTTPError:
#        print(response.status_code)
# def getCountryCodes(country) -> str:
#    country_codes = {
#        "AF": "Afghanistan",
#        "AX": "Åland Islands",
#        "AL": "Albania",
#        "DZ": "Algeria          ",
#        "AS": "American Samoa     ",
#        "AD": "Andorra          ",
#        "AO": "Angola             ",
#        "AI": "Anguilla         ",
#        "AQ": "Antarctica         ",
#        "AG": "Antigua and Barbuda",
#        "AR": "Argentina          ",
#        "AM": "Armenia          ",
#        "AW": "Aruba              ",
#        "AU": "Australia        ",
#        "AT": "Austria            ",
#        "AZ": "Azerbaijan       ",
#        "BS": "Bahamas            ",
#        "BH": "Bahrain          ",
#        "BD": "Bangladesh         ",
#        "BB": "Barbados         ",
#        "BY": "Belarus            ",
#        "BE": "Belgium          ",
#        "BZ": "Belize             ",
#        "BJ": "Benin            ",
#        "BM": "Bermuda            ",
#        "BT": "Bhutan           ",
#        "BO": "Bolivia, Plurinational State of",
#        "BQ": "Bonaire, Sint Eustatius and Saba",
#        "BR": "Brazil             ",
#        "BS": "Bulgaria         ",
#        "BW": "Botswana           ",
#        "BV": "Bouvet Island      ",
#        "BR": "Brazil             ",
#        "IO": "British Indian Ocean Territory",
#        "BN": "Brunei Darussalam  ",
#        "BG": "Bulgaria         ",
#        "BF": "Burkina Faso       ",
#        "BI": "Burundi          ",
#        "KH": "Cambodia           ",
#        "CM": "Cameroon         ",
#        "CA": "Canada             ",
#        "CV": "Cape Verde         ",
#        "KY": "Cayman Islands     ",
#        "CF": "Central African Republic",
#        "TD": "Chad               ",
#        "CL": "Chile            ",
#        "CN": "China              ",
#        "CX": "Christmas Island   ",
#        "CC": "Cocos(Keeling) Islands",
#        "CO": "Colombia         ",
#        "KM": "Comoros            ",
#        "CG": "Congo            ",
#        "CD": "Congo, Democratic Republic of the",
#        "CK": "Cook Islands       ",
#        "CR": "Costa Rica         ",
#        "CI": "Côted Ivoire       ",
#        "HR": "Croatia            ",
#        "CU": "Cuba             ",
#        "CW": "Curaçao            ",
#        "CY": "Cyprus           ",
#        "CZ": "Czech Republic     ",
#        "DK": "Denmark          ",
#        "DJ": "Djibouti           ",
#        "DM": "Dominica         ",
#        "DO": "Dominican Republic ",
#        "EC": "Ecuador          ",
#        "EG": "Egypt              ",
#        "SV": "El Salvador        ",
#        "GQ": "Equatorial Guinea  ",
#        "ER": "Eritrea          ",
#        "EE": "Estonia            ",
#        "ET": "Ethiopia         ",
#        "FK": "Falkland Islands(Malvinas)",
#        "FO": "Faroe Islands      ",
#        "FJ": "Fiji               ",
#        "FI": "Finland          ",
#        "FR": "France             ",
#        "GF": "French Guiana      ",
#        "PF": "French Polynesia   ",
#        "TF": "French Southern Territories",
#        "GA": "Gabon              ",
#        "GM": "Gambia           ",
#        "GE": "Georgia            ",
#        "GH": "Ghana            ",
#        "GI": "Gibraltar          ",
#        "GR": "Greece           ",
#        "GL": "Greenland          ",
#        "GD": "Grenada          ",
#        "GP": "Guadeloupe         ",
#        "GU": "Guam             ",
#        "GT": "Guatemala          ",
#        "GG": "Guernsey         ",
#        "GN": "Guinea             ",
#        "GW": "Guinea - Bissau    ",
#        "GY": "Guyana             ",
#        "HT": "Haiti            ",
#        "HM": "Heard Island and McDonald Islands",
#        "HN": "Honduras         ",
#        "HK": "Hong Kong          ",
#        "HU": "Hungary          ",
#        "IS": "Iceland            ",
#        "IN": "India            ",
#        "ID": "Indonesia          ",
#        "IR": "Iran, Islamic Republic of",
#        "IQ": "Iraq               ",
#        "IE": "Ireland          ",
#        "IM": "Isle of Man        ",
#        "IL": "Israel           ",
#        "IT": "Italy              ",
#        "JM": "Jamaica          ",
#        "JP": "Japan              ",
#        "JE": "Jersey           ",
#        "JO": "Jordan             ",
#        "KZ": "Kazakhstan       ",
#        "KE": "Kenya              ",
#        "KI": "Kiribati         ",
#        "KP": "Korea, Democratic People's Republic of",
#        "KR": "Korea, Republic of ",
#        "KW": "Kuwait             ",
#        "KG": "Kyrgyzstan       ",
#        "LA": "Lao People's Democratic Republic",
#        "LV": "Latvia           ",
#        "LB": "Lebanon            ",
#        "LS": "Lesotho          ",
#        "LR": "Liberia            ",
#        "LY": "Libya            ",
#        "LI": "Liechtenstein      ",
#        "LT": "Lithuania        ",
#        "LU": "Luxembourg         ",
#        "MO": "Macao            ",
#        "MK": "Macedonia,the former Yugoslav Republic of",
#        "MG": "Madagascar       ",
#        "MW": "Malawi             ",
#        "MY": "Malaysia         ",
#        "MV": "Maldives           ",
#        "ML": "Mali             ",
#        "MT": "Malta              ",
#        "MH": "Marshall Islands   ",
#        "MQ": "Martinique         ",
#        "MR": "Mauritania       ",
#        "MU": "Mauritius          ",
#        "YT": "Mayotte          ",
#        "MX": "Mexico             ",
#        "FM": "Micronesia, Federated States of",
#        "MD": "Moldova, Republic of",
#        "MC": "Monaco           ",
#        "MN": "Mongolia           ",
#        "ME": "Montenegro       ",
#        "MS": "Montserrat         ",
#        "MA": "Morocco          ",
#        "MZ": "Mozambique         ",
#        "MM": "Myanmar          ",
#        "NA": "Namibia            ",
#        "NR": "",
#        "US": "United States of America"
#    }
#    country_codes = {value: key for key, value in country_codes.items()}
#    return country_codes[country]
#
#
# def getstatecode(state) -> str:
#    state_codes = {
#        "AL": "Alabama",
#        "AK": "Alaska",
#        "AZ": "Arizona",
#        "AR": "Arkansas",
#        "CA": "California",
#        "CO": "Colorado",
#        "CT": "Connecticut",
#        "DE": "Delaware",
#        "FL": "Florida",
#        "GA": "Georgia",
#        "HI": "Hawaii",
#        "ID": "Idaho",
#        "IL": "Illinois",
#        "IN": "Indiana",
#        "IA": "Iowa",
#        "KS": "Kansas",
#        "KY": "Kentucky",
#        "LA": "Louisiana",
#        "ME": "Maine",
#        "MD": "Maryland",
#        "MA": "Massachusetts",
#        "MI": "Michigan",
#        "MN": "Minnesota",
#        "MS": "Mississippi",
#        "MO": "Missouri",
#        "MT": "Montana",
#        "NE": "Nebraska",
#        "NV": "Nevada",
#        "NH": "New Hampshire",
#        "NJ": "New Jersey",
#        "NM": "New Mexico",
#        "NY": "New York",
#        "NC": "North Carolina",
#        "ND": "North Dakota",
#        "OH": "Ohio",
#        "OK": "Oklahoma",
#        "OR": "Oregon",
#        "PA": "Pennsylvania",
#        "RI": "Rhode Island",
#        "SC": "South Carolina",
#        "SD": "South Dakota",
#        "TN": "Tennessee",
#        "TX": "Texas",
#        "UT": "Utah",
#        "VT": "Vermont",
#        "VA": "Virginia",
#        "WA": "Washington",
#        "WV": "West Virginia",
#        "WI": "Wisconsin",
#        "WY": "Wyoming",
#    }
#    state_codes = {value: key for key, value in state_codes.items()}
#    return state_codes[state]
#
#
# if __name__ == '__main__':
#    buildURL()
#    requestImage(searchurl)
#
