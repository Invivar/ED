sites = {'Inara': {'link': 'https://inara.cz/elite/news/',
                   'desc': 'THIS WEBSITE IS NOT AN OFFICIAL TOOL FOR THE GAME ELITE: DANGEROUS AND IS NOT '
                           'AFFILIATED WITH FRONTIER DEVELOPMENTS. ALL INFORMATION PROVIDED IS BASED ON '
                           'PUBLICLY AVAILABLE INFORMATION AND MAY NOT BE ENTIRELY ACCURATE.',
                   'image': r'logo\inaralogo.png'},
         'Roguey': {'link': 'https://roguey.co.uk/',
                    'desc': 'Welcome to help section, in here you will find information, guides and more on '
                            'Elite & Dangerous.',
                    'image': r'logo\rogueylogo.png'},
         'CMDR Tollbox': {'link': 'https://cmdrs-toolbox.com/',
                          'desc': 'This site was created to help both new and old players in Elite Dangerous. '
                                  'The site was created by Down To Earth Astronomy.',
                          'image': r'logo\cmdrtoolbox.png'},
         'Spansh - Plotter': {'link': 'https://www.spansh.co.uk/plotter/',
                              'desc': 'This page will allow you to plot between two different star systems. '
                                      'The result will show you every time you need to go to the galaxy map '
                                      'in order to plot a new route '
                                      '(for instance when you are at a neutron star)',
                              'image': r'logo\spanch.png'},
         'ED Legacy (I love it more)': {'link': 'http://edlegacy.iloveitmore.com.au/',
                                        'desc': ' If you are selling, you want a high Sell Price '
                                                'with a high Demand, if you are buying, you want a low Buy '
                                                'Price and a high Supply.',
                                        'image': r'logo\edlegacy.png'},
         'Elite Dangerous Star Map': {'link': 'https://www.edsm.net',
                                      'desc': 'EDSM (Elite Dangerous Star Map) was at first a community effort '
                                              'to store and calculate systems coordinates around the Elite: '
                                              'Dangerous galaxy.It is now the main API used by dozens of '
                                              'software and websites to find systems, coordinates, information '
                                              '(governement, allegiance, faction...) and celestial bodies '
                                              '(types, materials...).',
                                      'image': 'logo\edsmlogo.png'},
         'Coriolis': {'link': 'https://coriolis.io/',
                      'desc': 'Coriolis is a ship bulider for Elite: Dangrous.',
                      'image': 'logo\coriolislogo.png'}
         }
info = '''F2 - SETTINGS
F3 - INFO AT THE TOP + COPY DESTINATION
F4 - ROUTE PROGRESS + COPY SELECTED DESTINATION
F5 - COMMODITY + COPY DESTINATION
F6 - SET COMMODITY
F10 - CLOSE APP


LOGS:
ALL LOGS MOSTLY ARE STORED IN: D:\SteamLibrary\steamapps\common\Elite Dangerous\Products\elite-dangerous-64\Logs
IF NOT PLEASE SELECT YOUR DESTINATION PATH   !!!

CSV:
PLEASE VISIT: https://www.spansh.co.uk/plotter/, FILL REQUIRED FIELDS AND DOWNLOAD CSV FILE

JSON:
AUTOMATICALLY CREATES A PATH, IF YOU WANT TO SAVE MULTIPLE PROGRESS, CREATE UNIQUE NAMES'''
products_list = ["advancedcatalysers",
                 "advancedmedicines",
                 "agriculturalmedicines",
                 "agronomictreatment",
                 "alexandrite",
                 "algae",
                 "aluminium",
                 "animalmeat",
                 "animalmonitors",
                 "aquaponicsystems",
                 "articulationmotors",
                 "atmosphericextractors",
                 "autofabricators",
                 "basicmedicines",
                 "basicnarcotics",
                 "battleweapons",
                 "bauxite",
                 "beer",
                 "benitoite",
                 "bertrandite",
                 "beryllium",
                 "bioreducinglichen",
                 "biowaste",
                 "bismuth",
                 "bootlegliquor",
                 "bromellite",
                 "buildingfabricators",
                 "ceramiccomposites",
                 "chemicalwaste",
                 "clothing",
                 "cmmcomposite",
                 "cobalt",
                 "coffee",
                 "coltan",
                 "combatstabilisers",
                 "computercomponents",
                 "conductivefabrics",
                 "consumertechnology",
                 "coolinghoses",
                 "copper",
                 "cropharvesters",
                 "cryolite",
                 "damagedescapepod",
                 "diagnosticsensor",
                 "domesticappliances",
                 "emergencypowercells",
                 "evacuationshelter",
                 "exhaustmanifold",
                 "explosives",
                 "fish",
                 "foodcartridges",
                 "fruitandvegetables",
                 "gallite",
                 "gallium",
                 "geologicalequipment",
                 "gold",
                 "goslarite",
                 "grain",
                 "grandidierite",
                 "hazardousenvironmentsuits",
                 "heatsinkinterlink",
                 "heliostaticfurnaces",
                 "hnshockmount",
                 "hostage",
                 "hydrogenfuel",
                 "hydrogenperoxide",
                 "imperialslaves",
                 "indite",
                 "indium",
                 "insulatingmembrane",
                 "iondistributor",
                 "jadeite",
                 "landmines",
                 "lanthanum",
                 "leather",
                 "lepidolite",
                 "liquidoxygen",
                 "liquor",
                 "lithium",
                 "lithiumhydroxide",
                 "lowtemperaturediamond",
                 "magneticemittercoil",
                 "marinesupplies",
                 "medicaldiagnosticequipment",
                 "metaalloys",
                 "methaneclathrate",
                 "methanolmonohydratecrystals",
                 "microcontrollers",
                 "militarygradefabrics",
                 "mineralextractors",
                 "mineraloil",
                 "modularterminals",
                 "moissanite",
                 "monazite",
                 "musgravite",
                 "mutomimager",
                 "nanobreakers",
                 "naturalfabrics",
                 "neofabricinsulation",
                 "nerveagents",
                 "nonlethalweapons",
                 "occupiedcryopod",
                 "onionheadc",
                 "opal",
                 "osmium",
                 "painite",
                 "palladium",
                 "performanceenhancers",
                 "personaleffects",
                 "personalweapons",
                 "pesticides",
                 "platinum",
                 "polymers",
                 "powerconverter",
                 "powergenerators",
                 "powergridassembly",
                 "powertransferconduits",
                 "praseodymium",
                 "progenitorcells",
                 "pyrophyllite",
                 "radiationbaffle",
                 "reactivearmour",
                 "reinforcedmountingplate",
                 "resonatingseparators",
                 "rhodplumsite",
                 "robotics",
                 "rutile",
                 "samarium",
                 "scrap",
                 "semiconductors",
                 "serendibite",
                 "silver",
                 "skimercomponents",
                 "slaves",
                 "structuralregulators",
                 "superconductors",
                 "surfacestabilisers",
                 "survivalequipment",
                 "syntheticfabrics",
                 "syntheticmeat",
                 "syntheticreagents",
                 "taaffeite",
                 "tantalum",
                 "tea",
                 "telemetrysuite",
                 "terrainenrichmentsystems",
                 "thallium",
                 "thermalcoolingunits",
                 "thorium",
                 "titanium",
                 "tobacco",
                 "tritium",
                 "uraninite",
                 "uranium",
                 "usscargoblackbox",
                 "usscargorareartwork",
                 "water",
                 "waterpurifiers",
                 "wine",
                 "wreckagecomponents",
                 ]
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
what = ['selling', 'buying']

CONFIG_JSON_FILE = 'data/internal/config.json'
LAST_COMMODITY_FILE = 'data/internal/commodity.json'
CSV_DIRECTORY = 'data/csv_plots'
JSON_DIRECTORY = 'data/json_plots'
JSON_CCH = 'data/json_plots/Colonia Connection Highway.json'
BOOKMARKS_JSON_FILE = 'data/internal/bookmark.json'
INARA = 'data/internal/inara_result.json'
SAFE_LOG_PATH_REQ = r'Elite Dangerous.Products.elite-dangerous-64.Logs'
UID_SYNTAX = r'^.*UID=\d+\s*name=(?P<name>.*)'
SHIP_SYNTAX = r'^\{.*}\s*System:"(?P<current_pos>.*)"\s*StarPos:.*'
INARA_SYNTAX = r'(second)|(minute)|(hour)|(day)'

LOC_DATA = {'path': '',
            'in_use': '',
            'size': ''}
standard_highway = {
    "Col 359 Sector UM-T c4-6": {
        "data": [
            "CB-1 Argon's Reach",
            "Megaship",
            "Colonia Bridge 1",
            "335",
            "21,705\n"
        ],
        "done": 0
    },
    "Snake Sector OD-S b4-2": {
        "data": [
            "CB-2 Memories of Oresrati",
            "Megaship",
            "Colonia Bridge 1",
            "610",
            "21,441\n"
        ],
        "done": 0
    },
    "Mammon": {
        "data": [
            "Mammon Monitoring Facility",
            "Asteroid Base",
            "Other",
            "999",
            "21,004\n"
        ],
        "done": 0
    },
    "IC 1287 Sector RO-Q b5-1": {
        "data": [
            "CB-3 Geo Chandler Memorial",
            "Megaship",
            "Colonia Bridge 1",
            "1,007",
            "20,997\n"
        ],
        "done": 0
    },
    "Pru Euq WO-D b53-8": {
        "data": [
            "CB-4 Danieros Serenity",
            "Megaship",
            "Colonia Bridge 1",
            "1,387",
            "20,665\n"
        ],
        "done": 0
    },
    "Bleae Thua KY-L c7-12": {
        "data": [
            "CB-5 Ultzer-Noromia",
            "Megaship",
            "Colonia Bridge 1",
            "1,849",
            "20,294\n"
        ],
        "done": 0
    },
    "Blu Thua AI-A c14-10": {
        "data": [
            "CB-6 Carbis Bay",
            "Megaship",
            "Colonia Bridge 1",
            "2,105",
            "20,112\n"
        ],
        "done": 0
    },
    "Bleae Thua WD-M b49-1": {
        "data": [
            "CB-7 Endless Flight",
            "Megaship",
            "Colonia Bridge 1",
            "2,563",
            "19,676\n"
        ],
        "done": 0
    },
    "Smojue PZ-R c4-5": {
        "data": [
            "CB-8 Tamandua",
            "Megaship",
            "Colonia Bridge 1",
            "3,003",
            "19,282\n"
        ],
        "done": 0
    },
    "Smojue IY-Q b32-1": {
        "data": [
            "CB-9 Monolith",
            "Megaship",
            "Colonia Bridge 1",
            "3,488",
            "18,825\n"
        ],
        "done": 0
    },
    "Droju OH-T a99-0": {
        "data": [
            "CB-10 EVERGREEN",
            "Megaship",
            "Colonia Bridge 1",
            "3,851",
            "18,467\n"
        ],
        "done": 0
    },
    "NGC 6530 Sector ZE-X b2-0": {
        "data": [
            "CB-11 Junoo's Leap",
            "Megaship",
            "Colonia Bridge 1",
            "4,215",
            "18,115\n"
        ],
        "done": 0
    },
    "Lagoon Sector NI-S b4-10": {
        "data": [
            "Amundsen Terminal",
            "Planetary Outpost",
            "Colonia Connection",
            "4,481",
            "17,845\n"
        ],
        "done": 0
    },
    "Lagoon Sector FW-W d1-122": {
        "data": [
            "Attenborough's Watch",
            "Asteroid Base",
            "Other",
            "4,510",
            "17,820\n"
        ],
        "done": 0
    },
    "Bleia Dryiae HK-Y c17-9": {
        "data": [
            "CB-13 The Pit Stop",
            "Megaship",
            "Colonia Bridge 1",
            "4,875",
            "17,472\n"
        ],
        "done": 0
    },
    "Trifid Sector IR-W d1-52": {
        "data": [
            "Observation Post Epsilon",
            "Asteroid Base",
            "Other",
            "5,219",
            "17,152\n"
        ],
        "done": 0
    },
    "Trifid Sector GW-W d1-220": {
        "data": [
            "CB-14 Ashwin's Delight",
            "Megaship",
            "Colonia Bridge 1",
            "5,221",
            "17,148\n"
        ],
        "done": 0
    },
    "Bleia Dryiae EE-E d13-178": {
        "data": [
            "CB-15 Sevastopol",
            "Megaship",
            "Colonia Bridge 1",
            "5,336",
            "16,905\n"
        ],
        "done": 0
    },
    "Omega Sector OD-S b4-0": {
        "data": [
            "Rock of Isolation",
            "Detention Centre",
            "Other",
            "5,503",
            "16,617\n"
        ],
        "done": 0
    },
    "Omega Sector VE-Q b5-15": {
        "data": [
            "CB-16 Colonia Bridge",
            "Megaship",
            "Colonia Bridge 1",
            "5,513",
            "16,612\n"
        ],
        "done": 0
    },
    "Gria Drye IR-F a38-10": {
        "data": [
            "CB-17 Tsumago",
            "Megaship",
            "Colonia Bridge 1",
            "5,960",
            "16,171\n"
        ],
        "done": 0
    },
    "Byeia Eurk OC-I b37-13": {
        "data": [
            "CB-18 RBNF Orbital",
            "Megaship",
            "Colonia Bridge 1",
            "6,389",
            "15,744\n"
        ],
        "done": 0
    },
    "Byeia Eurk IE-L b49-4": {
        "data": [
            "CB-19 Kastilione's Vault",
            "Megaship",
            "Colonia Bridge 1",
            "6,686",
            "15,447\n"
        ],
        "done": 0
    },
    "Eagle Sector IR-W d1-105": {
        "data": [
            "Eagle Sector Secure Facility",
            "Asteroid Base",
            "Other",
            "7,006",
            "15,128\n"
        ],
        "done": 0
    },
    "Eagle Sector IR-W d1-117": {
        "data": [
            "CB-20 Colonia Bridge",
            "Megaship",
            "Colonia Bridge 1",
            "7,018",
            "15,113\n"
        ],
        "done": 0
    },
    "Plaa Aescs QD-T c3-28": {
        "data": [
            "CB-21 Ragnar's Rest",
            "Megaship",
            "Colonia Bridge 1",
            "7,249",
            "14,808\n"
        ],
        "done": 0
    },
    "Lysoosms YS-U d2-61": {
        "data": [
            "CB-22 Colonia Bridge",
            "Megaship",
            "Colonia Bridge 1",
            "7,467",
            "14,555\n"
        ],
        "done": 0
    },
    "Nyeajaae VU-Y a27-9": {
        "data": [
            "Mjolnir's Wrath",
            "Detention Centre",
            "Other",
            "7,688",
            "14,320\n"
        ],
        "done": 0
    },
    "Rohini": {
        "data": [
            "CB-23 Colonia Bridge",
            "Megaship",
            "Colonia Bridge 1",
            "7,692",
            "14,315\n"
        ],
        "done": 0
    },
    "Nyeajaae SC-B b33-7": {
        "data": [
            "CB-24 Colonia Bridge",
            "Megaship",
            "Colonia Bridge 1",
            "8,139",
            "13,864\n"
        ],
        "done": 0
    },
    "Nyeajaae NB-Q b52-14": {
        "data": [
            "CB-25 Colonia Bridge",
            "Megaship",
            "Colonia Bridge 1",
            "8,607",
            "13,397\n"
        ],
        "done": 0
    },
    "Flyiedge VN-W c4-51": {
        "data": [
            "CB-26 Passarola",
            "Megaship",
            "Colonia Bridge 2",
            "9,028",
            "12,976\n"
        ],
        "done": 0
    },
    "Flyiedge KP-K b27-6": {
        "data": [
            "CB-27 Stargazer's Legacy",
            "Megaship",
            "Colonia Bridge 2",
            "9,475",
            "12,528\n"
        ],
        "done": 0
    },
    "Flyiedge JE-Z b46-9": {
        "data": [
            "CB-28 Red Panda Rest Stop",
            "Megaship",
            "Colonia Bridge 2",
            "9,954",
            "12,049\n"
        ],
        "done": 0
    },
    "Skaude DR-A c2-1": {
        "data": [
            "CB-29 P.T.N. Profit's Prophet",
            "Megaship",
            "Colonia Bridge 2",
            "10,377",
            "11,627\n"
        ],
        "done": 0
    },
    "Skaude ZK-X e1-203": {
        "data": [
            "CB-30 Ironstar Varangia",
            "Megaship",
            "Colonia Bridge 2",
            "10,825",
            "11,185\n"
        ],
        "done": 0
    },
    "Skaudai GM-S b35-5": {
        "data": [
            "CB-31 Leaping Frog",
            "Megaship",
            "Colonia Bridge 2",
            "11,245",
            "10,770\n"
        ],
        "done": 0
    },
    "Skaudai AO-V b47-0": {
        "data": [
            "CB-32 Song of Deimos",
            "Megaship",
            "Colonia Bridge 2",
            "11,522",
            "10,493\n"
        ],
        "done": 0
    },
    "Skaudai CH-B d14-34": {
        "data": [
            "CB-33 Jewel of Pirigen",
            "Megaship",
            "Colonia Bridge 2",
            "11,797",
            "10,220\n"
        ],
        "done": 0
    },
    "Prua Phoe MI-B b17-5": {
        "data": [
            "CB-34 Hotel Canonnia",
            "Megaship",
            "Colonia Bridge 2",
            "12,216",
            "9,799\n"
        ],
        "done": 0
    },
    "Prua Phoe VF-M d8-1046": {
        "data": [
            "CB-35 Amanogawa Tenjin",
            "Megaship",
            "Colonia Bridge 2",
            "12,633",
            "9,386\n"
        ],
        "done": 0
    },
    "Prua Phoe PI-I b55-3": {
        "data": [
            "CB-36 Reaper's Respite",
            "Megaship",
            "Colonia Bridge 2",
            "13,098",
            "8,916\n"
        ],
        "done": 0
    },
    "Clooku VJ-E b16-27": {
        "data": [
            "CB-37 Mami Wata",
            "Megaship",
            "Colonia Bridge 2",
            "13,568",
            "8,443\n"
        ],
        "done": 0
    },
    "Clooku AA-Q b37-41": {
        "data": [
            "CB-38 Senner's Triumphal Rush",
            "Megaship",
            "Colonia Bridge 2",
            "14,035",
            "7,973\n"
        ],
        "done": 0
    },
    "Gru Hypue KS-T d3-31": {
        "data": [
            "Gagarin Gate",
            "Planetary Outpost",
            "Colonia Connection",
            "14,317",
            "7,863\n"
        ],
        "done": 0
    },
    "Clooku QA-E c28-713": {
        "data": [
            "CB-39 Dumont's Demoiselle",
            "Megaship",
            "Colonia Bridge 2",
            "14,454",
            "7,561\n"
        ],
        "done": 0
    },
    "Stuelou UT-E b17-51": {
        "data": [
            "CB-40 MANLALAKBAY",
            "Megaship",
            "Colonia Bridge 2",
            "14,920",
            "7,100\n"
        ],
        "done": 0
    },
    "Stuelou VV-X c17-395": {
        "data": [
            "CB-41 S. Daskalova",
            "Megaship",
            "Colonia Bridge 2",
            "15,306",
            "6,718\n"
        ],
        "done": 0
    },
    "Stuelou AT-J c25-24": {
        "data": [
            "Penal Ship Omicron",
            "Detention Centre",
            "Other",
            "15,615",
            "6,412\n"
        ],
        "done": 0
    },
    "Gandharvi": {
        "data": [
            "Caravanserai",
            "Ocellus Starport",
            "Blue Star Line",
            "15,620",
            "6,406\n"
        ],
        "done": 0
    },
    "Blua Eaec RD-Z d1-1228": {
        "data": [
            "CB-43 PBO Headquarters",
            "Megaship",
            "Colonia Bridge 2",
            "16,070",
            "5,962\n"
        ],
        "done": 0
    },
    "Blua Eaec WW-E c14-1293": {
        "data": [
            "CB-44 Entire Prize",
            "Megaship",
            "Colonia Bridge 2",
            "16,455",
            "5,579\n"
        ],
        "done": 0
    },
    "Blua Eaec US-Z b46-4": {
        "data": [
            "CB-45 Inter Mundos",
            "Megaship",
            "Colonia Bridge 2",
            "16,896",
            "5,132\n"
        ],
        "done": 0
    },
    "Boewnst KS-S c20-959": {
        "data": [
            "Polo Harbour",
            "Planetary Outpost",
            "Colonia Connection",
            "17,589",
            "4,786\n"
        ],
        "done": 0
    },
    "Boelts ZN-Y b5-69": {
        "data": [
            "CB-46 Viride Umbrella",
            "Megaship",
            "Colonia Bridge 2",
            "17,348",
            "4,677\n"
        ],
        "done": 0
    },
    "Boelts UB-P b24-98": {
        "data": [
            "CB-47 Manatee Lounge",
            "Megaship",
            "Colonia Bridge 2",
            "17,788",
            "4,238\n"
        ],
        "done": 0
    },
    "Boelts YK-P c21-5": {
        "data": [
            "CB-48 The Butini\u0102\u00a8re",
            "Megaship",
            "Colonia Bridge 2",
            "18,224",
            "3,798\n"
        ],
        "done": 0
    },
    "Eoch Flyuae PL-D c138": {
        "data": [
            "CB-49 Lajeado",
            "Megaship",
            "Colonia Bridge 2",
            "18,687",
            "3,324\n"
        ],
        "done": 0
    },
    "Eoch Flyuae ZU-Y b17-16": {
        "data": [
            "CB-50 The Green Star",
            "Megaship",
            "Colonia Bridge 2",
            "19,100",
            "2,907\n"
        ],
        "done": 0
    },
    "Kashyapa": {
        "data": [
            "CB-51 Constellation",
            "Megaship",
            "Colonia Bridge 2",
            "19,470",
            "2,532\n"
        ],
        "done": 0
    },
    "Eoch Flyuae QK-E d12-2118": {
        "data": [
            "CB-52 Nikita Orbital",
            "Megaship",
            "Colonia Bridge 1",
            "19,923",
            "2,081\n"
        ],
        "done": 0
    },
    "Dryio Flyuae KV-P b8-112": {
        "data": [
            "CB-53 Aburaya",
            "Megaship",
            "Colonia Bridge 1",
            "20,370",
            "1,637\n"
        ],
        "done": 0
    },
    "Dryooe Flyou NQ-G b27-103": {
        "data": [
            "CB-54 Hussars Inn",
            "Megaship",
            "Colonia Bridge 1",
            "20,821",
            "1,193\n"
        ],
        "done": 0
    },
    "Dryooe Flyou WB-T b47-10": {
        "data": [
            "CB-55 V.I.T.R.I.O.L",
            "Megaship",
            "Colonia Bridge 1",
            "21,306",
            "704\n"
        ],
        "done": 0
    },
    "Eol Prou GE-A c1-291": {
        "data": [
            "CB-56 Colonia Bridge",
            "Megaship",
            "Colonia Bridge 1",
            "21,659",
            "343\n"
        ],
        "done": 0
    }
}