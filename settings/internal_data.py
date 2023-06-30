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
SAFE_LOG_PATH_REQ = r'Elite Dangerous.Products.elite-dangerous-64.Logs'
UID_SYNTAX = r'^.*UID=\d+\s*name=(?P<name>.*)'
SHIP_SYNTAX = r'^\{.*}\s*System:"(?P<current_pos>.*)"\s*StarPos:.*'

LOC_DATA = {'path': '',
            'in_use': '',
            'size': ''}