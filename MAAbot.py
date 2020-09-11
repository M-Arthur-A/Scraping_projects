#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# http://t.me/botMAAbot
'''
Топ ввп и отдельно
Валюты: евро, доллар, франк, йена, гонконгский доллар, юань, турецкая лира, индийский рупий
Товары: wti, brent, urals, золото, медь, серебро, платина, никель, алюминий
Индексы ДоуДжонс, Насдак, СНП500, ММВБ, РТС, шанхай композит, nifti, nikkei, DAX
Акции TOP5-доуджонс и моекс
Недвижка
Топ-новостей
Монетка
'''
import logging
from aiogram import Bot, Dispatcher, executor, types
from pymongo import MongoClient
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton, InputMediaPhoto, ParseMode
from aiogram.utils.markdown import text, bold, italic, code, pre
import random



# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

client = MongoClient('localhost', 27017)  # подключение к машине
mongo_base = client.db
collections = [mongo_base['macro'],
               mongo_base['cur'],
               mongo_base['indexes'],
               mongo_base['commodities'],
               mongo_base['gov_bonds'],
               mongo_base['irn'],
               mongo_base['news'],
               mongo_base['stocks'],
               mongo_base['cian']]

countries = ['/Russia', '/United_States', '/United_Kingdom', '/Ukraine', '/China', '/Japan', '/France',
             '/Germany', '/Spain', '/Turkey', '/India', '/Afghanistan', '/Albania', '/Algeria', '/Angola',
             '/Argentina', '/Armenia', '/Australia', '/Austria', '/Azerbaijan', '/Bahamas', '/Bahrain',
             '/Bangladesh', '/Belarus', '/Belgium', '/Benin', '/Bhutan', '/Bolivia', '/Bosnia_and_Herzegovina',
             '/Botswana', '/Brazil', '/Brunei', '/Bulgaria', '/Burkina_Faso', '/Burundi', '/Cambodia',
             '/Cameroon', '/Canada', '/Cape_Verde', '/Cayman_Islands', '/Central_African_Republic', '/Chad',
             '/Chile', '/Colombia', '/Comoros', '/Congo', '/Costa_Rica', '/Croatia', '/Cuba', '/Cyprus',
             '/Czech_Republic', '/Denmark', '/Djibouti', '/Dominican_Republic', '/East_Timor', '/Ecuador',
             '/Egypt', '/El_Salvador', '/Equatorial_Guinea', '/Eritrea', '/Estonia', '/Ethiopia', '/Euro_Area',
             '/Fiji', '/Finland', '/Gabon', '/Gambia', '/Georgia', '/Ghana', '/Greece', '/Guatemala', '/Guinea',
             '/Guinea_Bissau', '/Guyana', '/Haiti', '/Honduras', '/Hong_Kong', '/Hungary', '/Iceland',
             '/Indonesia', '/Iran', '/Iraq', '/Ireland', '/Israel', '/Italy', '/Ivory_Coast', '/Jamaica',
             '/Jordan', '/Kazakhstan', '/Kenya', '/Kosovo', '/Kuwait', '/Kyrgyzstan', '/Laos', '/Latvia',
             '/Lebanon', '/Lesotho', '/Liberia', '/Libya', '/Liechtenstein', '/Lithuania', '/Luxembourg',
             '/Macau', '/Macedonia', '/Madagascar', '/Malawi', '/Malaysia', '/Maldives', '/Mali', '/Malta',
             '/Mauritania', '/Mauritius', '/Mexico', '/Moldova', '/Monaco', '/Mongolia', '/Montenegro',
             '/Morocco', '/Mozambique', '/Myanmar', '/Namibia', '/Nepal', '/Netherlands', '/New_Caledonia',
             '/New_Zealand', '/Nicaragua', '/Niger', '/Nigeria', '/Norway', '/Oman', '/Pakistan', '/Palestine',
             '/Panama', '/Papua_New_Guinea', '/Paraguay', '/Peru', '/Philippines', '/Poland', '/Portugal',
             '/Puerto_Rico', '/Qatar', '/Republic_of_the_Congo', '/Romania', '/Rwanda', '/Sao_Tome_and_Princi',
             '/Saudi_Arabia', '/Senegal', '/Serbia', '/Seychelles', '/Sierra_Leone', '/Singapore', '/Slovakia',
             '/Slovenia', '/Somalia', '/South_Africa', '/South_Korea', '/South_Sudan', '/Sri_Lanka', '/Sudan',
             '/Suriname', '/Swaziland', '/Sweden', '/Switzerland', '/Syria', '/Taiwan', '/Tajikistan',
             '/Tanzania', '/Thailand', '/Togo', '/Trinidad_and_Tobago', '/Tunisia', '/Turkmenistan', '/Uganda',
             '/United_Arab_Emirates', '/Uruguay', '/Uzbekistan', '/Venezuela', '/Vietnam', '/Yemen', '/Zambia',
             '/Zimbabwe']
currencies = ['/USDRUB', '/AUDRUB', '/EURRUB', '/GBPRUB', '/RUBJPY', '/AUDBRL', '/AUDCAD', '/AUDCHF', '/AUDCNY',
              '/AUDHKD', '/AUDIDR', '/AUDINR', '/AUDJPY', '/AUDKRW', '/AUDMXN', '/AUDNZD', '/AUDSGD', '/AUDUSD',
              '/BRLJPY', '/BTCUSD', '/CADJPY', '/CHFJPY', '/CLPCLF', '/CNYJPY', '/DXY', '/ETHUSD', '/EURAUD', '/EURBRL',
              '/EURCAD', '/EURCHF', '/EURCNY', '/EURCZK', '/EURDKK', '/EURGBP', '/EURHKD', '/EURIDR', '/EURINR',
              '/EURISK', '/EURJPY', '/EURKRW', '/EURMXN', '/EURNOK', '/EURNZD', '/EURSEK', '/EURSGD', '/EURUSD',
              '/EURZAR', '/GBPAUD', '/GBPBRL', '/GBPCAD', '/GBPCHF', '/GBPCNY', '/GBPCZK', '/GBPDKK', '/GBPHKD',
              '/GBPIDR', '/GBPINR', '/GBPJPY', '/GBPKRW', '/GBPMXN', '/GBPNZD', '/GBPSGD', '/GBPUSD', '/HKDJPY',
              '/IDRJPY', '/INRJPY', '/KRWJPY', '/MXNJPY', '/NZDJPY', '/NZDUSD', '/RTGS', '/SGDJPY', '/USDAED',
              '/USDAFN', '/USDALL', '/USDAMD', '/USDAOA', '/USDARS', '/USDAZN', '/USDBDT', '/USDBGN', '/USDBHD',
              '/USDBIF', '/USDBIH', '/USDBND', '/USDBOB', '/USDBRL', '/USDBSD', '/USDBWP', '/USDBYR', '/USDCAD',
              '/USDCDF', '/USDCHF', '/USDCLP', '/USDCNY', '/USDCOP', '/USDCRC', '/USDCUC', '/USDCVE', '/USDCZK',
              '/USDDJF', '/USDDKK', '/USDDOP', '/USDDZD', '/USDEGP', '/USDERN', '/USDETB', '/USDFJD', '/USDGEL',
              '/USDGHS', '/USDGMD', '/USDGNF', '/USDGTQ', '/USDGYD', '/USDHKD', '/USDHNL', '/USDHRV', '/USDHTG',
              '/USDHUF', '/USDIDR', '/USDILS', '/USDINR', '/USDIQD', '/USDIRR', '/USDISK', '/USDJMD', '/USDJOD',
              '/USDJPY', '/USDKES', '/USDKGS', '/USDKHR', '/USDKMF', '/USDKPW', '/USDKRW', '/USDKWD', '/USDKYD',
              '/USDKZT', '/USDLAK', '/USDLBP', '/USDLKR', '/USDLRD', '/USDLSL', '/USDLYD', '/USDMAD', '/USDMDL',
              '/USDMGA', '/USDMKD', '/USDMMK', '/USDMNT', '/USDMOP', '/USDMRO', '/USDMUR', '/USDMVR', '/USDMWK',
              '/USDMXN', '/USDMYR', '/USDMZN', '/USDNAD', '/USDNGN', '/USDNIO', '/USDNOK', '/USDNPR', '/USDOMR',
              '/USDPAB', '/USDPEN', '/USDPGK', '/USDPHP', '/USDPKR', '/USDPLN', '/USDPYG', '/USDQAR', '/USDRON',
              '/USDRWF', '/USDSAR', '/USDSCR', '/USDSDG', '/USDSEK', '/USDSGD', '/USDSLL', '/USDSOS', '/USDSRB',
              '/USDSRD', '/USDSSP', '/USDSTD', '/USDSVC', '/USDSYP', '/USDSZL', '/USDTHB', '/USDTJS', '/USDTMT',
              '/USDTND', '/USDTRY', '/USDTTD', '/USDTWD', '/USDTZS', '/USDUAH', '/USDUGX', '/USDURY', '/USDUZS',
              '/USDVES', '/USDVND', '/USDXAF', '/USDXOF', '/USDXPF', '/USDYER', '/USDZAR', '/USDZMW', '/XRPUSD']
indexies = ['/Dow_Jones', '/S&P_500', '/NASDAQ_100', '/S&P_VIX', '/FTSE_100', '/DAX', '/CAC_40', '/FTSE_MIB',
            '/IBEX_35', '/MOEX', '/AEX', '/ADX_General', '/All-Share_Index', '/ASE', '/ASPI', '/ASX_200', '/ASX_50',
            '/Athens_General', '/ATX', '/Australian_All', '/BELEX_15', '/BET', '/BIST_100', '/Blom', '/BSX', '/BUX',
            '/BVPSI', '/Casablanca_CFG_25', '/COLCAP', '/CROBEX', '/CSE_General', '/CSI_300', '/DFM_general',
            '/Dow_Jones', '/DSE_Broad', '/DSEI', '/Ecuador_General_Index', '/Egypt_EGX_30', '/Estirad',
            '/Euro_Stoxx_50', '/Euronext_100', '/Euronext_BEL_20', '/FKLCI', '/FTSE/JSE_TOP_40', '/Gaborone', '/GGSECI',
            '/Hang_Seng', '/HNX', '/IBC', '/iBovespa', '/ICEX', '/IGPA', '/IPC_Mexico', '/ISEQ', '/JALSH-All_Share',
            '/JCI', '/JSE', '/KASE', '/KOSPI', '/KSE_100', '/LSX_Composite', '/LuxX', '/MBI_10', '/Merval',
            '/MONEX_INDEX', '/MSE_TOP_20', '/MSE', '/MSM_TOP_30', '/Nairobi_20', '/NASDAQ_100', '/NASDAQ', '/NIFTY_50',
            '/NIKKEI_225', '/Nikkei_Volatility_Index', '/NSE_All_Share', '/NSE-All_Share', '/NSX_Overall', '/NZX_50',
            '/OMX_Copenhagen', '/OMX_Helsinki_25', '/OMX_Helsinki', '/OMX_Riga', '/OMX_Tallinn', '/OMX_Vilnius',
            '/OMXS_30', '/Oslo_Bors_All-Share', '/PFTS', '/PSEi', '/PSI_20', '/PSI_Geral', '/PX', '/QE',
            '/Russell_2000', '/S&P_500', '/S&P_Europe_350', '/S&P_Global_1200', '/S&P_MidCap_400', '/S&P_VIX',
            '/S&P/BVL_Peru_General_Index_TR_(PEN)', '/SASX-10', '/SAX', '/SBITOP', '/SEMDEX', '/SENSEX', '/SET_50',
            '/SHANGHAI_50', '/SHANGHAI', '/SMI', '/SOFIX', '/STI', '/STOXX_Europe_600', '/TA-100', '/TAIEX', '/TASI',
            '/TEDPIX', '/TSX', '/TUN', '/USE_All_Share_Index', '/VN', '/WIG', '/Zimbabwe_Industrial_Index']
commodities = ['/Aluminum_(USD/T)', '/Baltic_Dry_(Index_Points)', '/Beef_(BRL/Kg)', '/Bitumen_(CNY/T)',
               '/Brent_(USD/Bbl)', '/Canola_(CAD/T)', '/Cheese_(USD/Lbs)', '/Coal_(USD/T)', '/Cobalt_(USD/T)',
               '/Cocoa_(USD/T)', '/Coffee_(USd/Lbs)', '/Copper_(USD/Lbs)', '/Corn_(USd/BU)', '/Cotton_(USd/Lbs)',
               '/CRB_Index_(Index_Points)', '/Crude_Oil_(USD/Bbl)', '/Ethanol_(USD/Gal)', '/Feeder_Cattle_(USd/Lbs)',
               '/Gasoline_(USD/Gal)', '/Gold_(USD/t.oz)', '/Heating_oil_(USD/Gal)', '/Iron_Ore_(62%_fe_USD/T)',
               '/Iron_Ore_(USD/T)', '/Lead_(USD/T)', '/Lean_Hogs_(USd/Lbs)', '/Lithium_(CNY/T)',
               '/Live_Cattle_(USd/Lbs)', '/LME_Index_(Index_Points)', '/Lumber_(USD/1000_board_feet)',
               '/Manganese_(CNY/T)', '/Milk_(USD/CWT)', '/Molybdenum_(USD/Kg)', '/Naphtha_(USD/T)',
               '/Natural_gas_(USD/MMBtu)', '/Neodymium_(CNY/T)', '/Nickel_(USD/T)', '/Oat_(USd/Bu)',
               '/Orange_Juice_(USd/Lbs)', '/Palladium_(USD/t.oz)', '/Palm_Oil_(MYR/T)', '/Platinum_(USD/t.oz)',
               '/Poultry_(BRL/Kgs)', '/Propane_(USD/Gal)', '/Rhodium_(USD/t_oz.)', '/Rice_(USD/cwt)',
               '/Rubber_(JPY/Kg)', '/S&P_GSCI_(Index_Points)', '/Silver_(USD/t.oz)', '/Soda_Ash_(CNY/T)',
               '/Soybeans_(USd/Bu)', '/Steel_(CNY/T)', '/Sugar_(USd/Lbs)', '/Tea_(USD/Kgs)', '/Tin_(USD/T)',
               '/Uranium_(USD/Lbs)', '/Wheat_(USd/Bu)', '/Wool_(AUD/100Kg)', '/Zinc_(USD/T)']
gov_bonds = ['/b_Australia_20Y', '/b_Australia_2Y', '/b_Australia_30Y', '/b_Australia_3Y', '/b_Australia_52W',
             '/b_Australia_5Y', '/b_Australia_7Y', '/b_Australia', '/b_Austria', '/b_Belgium_2Y_Bond_Yield',
             '/b_Belgium', '/b_Brazil_2Y', '/b_Brazil_3M', '/b_Brazil_3Y', '/b_Brazil_52W', '/b_Brazil_5Y',
             '/b_Brazil_6M', '/b_Brazil', '/b_Bulgaria', '/b_Canada_1M', '/b_Canada_20Y', '/b_Canada_2Y',
             '/b_Canada_30Y', '/b_Canada_3M', '/b_Canada_3Y', '/b_Canada_52W', '/b_Canada_5Y', '/b_Canada_6M',
             '/b_Canada_7Y', '/b_Canada', '/b_Chile', '/b_China_20Y', '/b_China_2Y', '/b_China_30Y', '/b_China_3Y',
             '/b_China_52W', '/b_China_5Y', '/b_China_7Y', '/b_China', '/b_Colombia', '/b_Croatia', '/b_Czech_Republic',
             '/b_Denmark_2Y_Bond_Yield', '/b_Denmark', '/b_Finland_2Y_Bond_Yield', '/b_Finland', '/b_France_1M',
             '/b_France_20Y', '/b_France_2Y', '/b_France_30Y', '/b_France_3M', '/b_France_3Y', '/b_France_52W',
             '/b_France_5Y', '/b_France_6M', '/b_France_7Y', '/b_France', '/b_Germany_2Y', '/b_Germany_30Y',
             '/b_Germany_3M', '/b_Germany_3Y', '/b_Germany_52W', '/b_Germany_5Y', '/b_Germany_6M', '/b_Germany_7Y',
             '/b_Germany', '/b_Greece_1M', '/b_Greece_20Y', '/b_Greece_3M', '/b_Greece_6M', '/b_Greece', '/b_Hong_Kong',
             '/b_Hungary', '/b_Iceland', '/b_India_2Y', '/b_India_30Y', '/b_India_3M', '/b_India_3Y', '/b_India_52W',
             '/b_India_5Y', '/b_India_6M', '/b_India_7Y', '/b_India', '/b_Indonesia_1M', '/b_Indonesia_20Y',
             '/b_Indonesia_30Y', '/b_Indonesia_3M', '/b_Indonesia_3Y', '/b_Indonesia_52W', '/b_Indonesia_5Y',
             '/b_Indonesia_6M', '/b_Indonesia', '/b_Ireland', '/b_Israel', '/b_Italy_1M', '/b_Italy_20Y', '/b_Italy_2Y',
             '/b_Italy_30Y', '/b_Italy_3M', '/b_Italy_3Y', '/b_Italy_52W', '/b_Italy_5Y', '/b_Italy_7Y', '/b_Italy',
             '/b_Japan_1M', '/b_Japan_20Y', '/b_Japan_2Y', '/b_Japan_30Y', '/b_Japan_3M', '/b_Japan_3Y', '/b_Japan_52W',
             '/b_Japan_5Y', '/b_Japan_6M', '/b_Japan_7Y', '/b_Japan', '/b_Kenya', '/b_Latvia', '/b_Lithuania',
             '/b_Malaysia', '/b_Mexico', '/b_Netherlands_2Y_Bond_Yield', '/b_Netherlands_3M', '/b_Netherlands_6M',
             '/b_Netherlands', '/b_New_Zealand', '/b_Nigeria', '/b_Norway', '/b_Pakistan', '/b_Peru_15Y',
             '/b_Philippine', '/b_Poland', '/b_Portugal_20Y', '/b_Portugal_2Y', '/b_Portugal_30Y', '/b_Portugal_3M',
             '/b_Portugal_3Y', '/b_Portugal_52W', '/b_Portugal_5Y', '/b_Portugal_6M', '/b_Portugal_7Y', '/b_Portugal',
             '/b_Qatar', '/b_Romania', '/b_Russia_1M', '/b_Russia_20Y', '/b_Russia_2Y', '/b_Russia_3M', '/b_Russia_3Y',
             '/b_Russia_52W', '/b_Russia_5Y', '/b_Russia_6M', '/b_Russia_7Y', '/b_Russia', '/b_Singapore',
             '/b_Slovakia', '/b_Slovenia', '/b_South_Africa_20Y', '/b_South_Africa_2Y', '/b_South_Africa_30Y',
             '/b_South_Africa_3M', '/b_South_Africa_5Y', '/b_South_Africa', '/b_South_Korea_20Y', '/b_South_Korea_2Y',
             '/b_South_Korea_30Y', '/b_South_Korea_3Y', '/b_South_Korea_52W', '/b_South_Korea_5Y', '/b_South_Korea',
             '/b_Spain_2Y_Bond_Yield', '/b_Spain_3M', '/b_Spain_3Y', '/b_Spain_52W', '/b_Spain_5Y', '/b_Spain_6M',
             '/b_Spain', '/b_Sweden_2Y_Bond_Yield', '/b_Sweden', '/b_Switzerland_2Y_Bond_Yield', '/b_Switzerland',
             '/b_Taiwan', '/b_Thailand', '/b_Turkey_2Y_Bond_Yield', '/b_Turkey', '/b_UK_1M', '/b_UK_20Y', '/b_UK_30Y',
             '/b_UK_3M', '/b_UK_3Y', '/b_UK_52W', '/b_UK_5Y', '/b_UK_6M', '/b_UK_7Y', '/b_UK',
             '/b_United_Kingdom_2Y_Bond_Yield', '/b_US_1M', '/b_US_20Y', '/b_US_2Y', '/b_US_30Y', '/b_US_3M',
             '/b_US_3Y', '/b_US_52W', '/b_US_5Y', '/b_US_6M', '/b_US_7Y', '/b_US', '/b_Venezuela', '/b_Vietnam',
             '/b_Zambia_Government_Bond_10y']
shares = []
news = ['/Экономика_вся', '/Финансы_все']  # '/Экономика_ТОП10', '/Финансы_ТОП10'
news_data = []


# @dp.message_handler(commands='start')
@dp.message_handler(commands='start')
async def start_cmd_handler(message: types.Message, btns=0):
    keyboard_markup = types.InlineKeyboardMarkup(row_width=30)
    # default row_width is 3, so here we can omit it actually
    # kept for clearness
    if btns == 0:
        text_and_data = (('Макростатистика', 'macro'),
                         ('Курсы валют', 'currency'),
                         ('Цены на товары', 'commodities'),
                         ('Индексы', 'index'),
                         ('Недвижимость', 'estate'),
                         ('Акции', 'shares'),
                         ('Гособлигации', 'bonds'),
                         ('Новости', 'news'),
                         ('Монетка', 'dice'))
    else:
        text_and_data = btns
    # in real life for the callback_data the callback data factory should be used
    # here the raw string is used for the simplicity
    row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
    for but in row_btns:
        keyboard_markup.row(but)
    await message.reply("Привет!\nЧто Вас интересует?", reply_markup=keyboard_markup)


@dp.callback_query_handler(text='macro')
@dp.callback_query_handler(text='currency')
@dp.callback_query_handler(text='commodities')
@dp.callback_query_handler(text='index')
@dp.callback_query_handler(text='estate')
@dp.callback_query_handler(text='shares')
@dp.callback_query_handler(text='bonds')
@dp.callback_query_handler(text='news')
@dp.callback_query_handler(text='dice')
async def inline_kb_answer_callback_handler(query: types.CallbackQuery):
    answer_data = query.data
    # always answer callback queries, even if you have nothing to say
    await query.answer(f'Ваш выбор - рублика {answer_data!r}')

    if answer_data == 'macro':
        # choice_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        # for country in countries:
        #     choice_kb.add(KeyboardButton(country))
        # text = 'По какой стране показать статистику?'
        # await bot.send_message(query.from_user.id, text, reply_markup=choice_kb)
        text = 'В разработке!'
        await bot.send_message(query.from_user.id, text)

    elif answer_data == 'currency':
        choice_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        for currency in currencies:
            choice_kb.add(KeyboardButton(currency))
        text = 'Какой курс валют интересует?'
        await bot.send_message(query.from_user.id, text, reply_markup=choice_kb)

    elif answer_data == 'commodities':
        choice_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        for commodity in commodities:
            choice_kb.add(KeyboardButton(commodity))
        text = 'Какой товар Вас интересует?'
        await bot.send_message(query.from_user.id, text, reply_markup=choice_kb)

    elif answer_data == 'index':
        choice_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        for index in indexies:
            choice_kb.add(KeyboardButton(index))
        text = 'Какой индекс Вас интересует?'
        await bot.send_message(query.from_user.id, text, reply_markup=choice_kb)

    elif answer_data == 'estate':
        choice_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        choice_kb.add(KeyboardButton('/IRN_Moscow_index'))
        text = 'Пока доступен только IRN'
        await bot.send_message(query.from_user.id, text, reply_markup=choice_kb)

    elif answer_data == 'shares':
        text = 'Введите интересующий тикер после "/t_". \nНапример, /t_AAPL'
        collection = collections[7]
        global shares
        shares = collection.distinct('stocks_ticker')
        shares = list(map(lambda x: '/t_'+str(x), shares))
        await bot.send_message(query.from_user.id, text)

    elif answer_data == 'bonds':
        choice_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        for bond in gov_bonds:
            choice_kb.add(KeyboardButton(bond))
        text = 'Выберите госбумагу'
        await bot.send_message(query.from_user.id, text, reply_markup=choice_kb)

    elif answer_data == 'news':
        choice_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        for new in news:
            choice_kb.add(KeyboardButton(new))
        text = 'Какие новости Вас интересуют?'
        await bot.send_message(query.from_user.id, text, reply_markup=choice_kb)

    elif answer_data == 'dice':
        text = 'Орёл! (Да)' if random.randint(0, 1) else 'Решка! (Нет)'
        await bot.send_message(query.from_user.id, text)


@dp.message_handler()
async def process_start_command(message: types.Message):
    def tabletext(body, header, mode='big'):
        if mode == 'big':
            maxlen = [0, '1']
            for i in body:
                if len(str(i)) > len(maxlen[1]):
                    maxlen[0] = len(i)
                    maxlen[1] = i
            maxlen = maxlen[0]
            top = u'\u250C' + ' ' * maxlen + (u'\u252C' + ' ' * maxlen) * (
                    len(body) - 1) + u'\u2510' + '\n'  # u'\u2500'
            mid = u'\u251C' + ' ' * maxlen + (u'\u253C' + ' ' * maxlen) * (len(body) - 1) + u'\u2524' + '\n'
            heads = map(lambda x: str(x) if len(str(x)) == maxlen else ' ' * (maxlen - len(str(x))) + str(x), header)
            head = u'\u2502' + u'\u2502'.join(heads) + u'\u2502' + '\n'
            items = map(lambda x: str(x) if len(str(x)) == maxlen else ' ' * (maxlen - len(str(x))) + str(x), body)
            vals = u'\u2502' + u'\u2502'.join(items) + u'\u2502' + '\n'
            bot = u'\u2514' + ' ' * maxlen + (u'\u2534' + ' ' * maxlen) * (len(body) - 1) + u'\u2518' + '\n'
            return top + head + mid + vals + bot
        if mode == 'small':
            prehead = ''
            if '(' in body[0]:
                prehead = '(' + body[0].split(' (')[1] + '\n'
                body[0] = body[0].split(' (')[0]
            vals = ''
            maxlen = [0, '1']
            for i in body + header:
                if len(str(i)) > len(maxlen[1]):
                    maxlen[0] = len(i)
                    maxlen[1] = i
            maxlen = maxlen[0]
            top = u'\u250C' + ' ' * maxlen + (u'\u252C' + ' ' * maxlen) + u'\u2510' + '\n'
            items = map(lambda x: str(x) if len(str(x)) == maxlen else ' ' * (maxlen - len(str(x))) + str(x), body)
            heads = map(lambda x: str(x) if len(str(x)) == maxlen else ' ' * (maxlen - len(str(x))) + str(x), header)
            for i, j in list(zip(heads, items)):
                vals += u'\u2502' + u'\u2502'.join([i, j]) + u'\u2502' + '\n'
            bot = u'\u2514' + ' ' * maxlen + (u'\u2534' + ' ' * maxlen) + u'\u2518' + '\n'
            return prehead + top + vals + bot

    await message.reply('Чтобы начать сначала, введите /start')
    choice = str(message.text).replace('_', ' ')[1:]
    print(choice)
    if message.text in countries:
        collection = collections[0]
        collection.find({})

    if message.text in currencies:
        collection = collections[1]
        query = collection.find_one({'cur_name': choice})
        header = ['Курс', 'Цена', 'День', 'Мес', 'Год', 'Акт.']
        body = [query['cur_name'], query['cur_price'], query['cur_delta_day'], query['cur_delta_month'],
                query['cur_delta_year'], query['cur_data_date']]
        text = ''
        text = tabletext(body, header, 'small')
        await message.reply('<code>' + text + '</code>', parse_mode='HTML')

    if message.text in commodities:
        collection = collections[3]
        header = ['Товар', 'Цена', 'День', 'Мес', 'Год', 'Акт.']
        body = [query['commodities_name'], query['commodities_price'], query['commodities_delta_day'],
                query['commodities_delta_month'],
                query['commodities_delta_year'], query['commodities_data_date']]
        text = ''
        text = tabletext(body, header, 'small')
        await message.reply('<code>' + text + '</code>', parse_mode='HTML')

    if message.text in indexies:
        collection = collections[2]
        query = collection.find_one({'index_name': choice})
        header = ['Индекс', 'Цена', 'День', 'Мес', 'Год', 'Акт.']
        body = [query['index_name'], query['index_price'], query['index_delta_day'],
                query['index_delta_month'],
                query['index_delta_year'], query['index_data_date']]
        text = ''
        text = tabletext(body, header, 'small')
        await message.reply('<code>' + text + '</code>', parse_mode='HTML')

    if message.text in ['/IRN_Moscow_index']:
        collection = collections[5]
        text = 'Индексы цен на недвижимость Москвы'
        query = r'/home/arthur/Project/mySoft/TelegramBot/images/irn'
        query = r'https://www.irn.ru/graph/services/classes2.php?class=all&type=1&period=1&grnum=1&currency=0'
        await bot.send_photo(message.from_user.id, photo=query)

    if message.text in ['/cian']:
        collection = collections[8]
        text = 'Индексы цен на недвижимость'
        path = '/home/arthur/Project/mySoft/TelegramBot/logo.gif'
        with open(path, 'rb') as photo:
            await message.reply_photo(photo)

    if message.text in gov_bonds:
        choice = str(choice)[2:]
        collection = collections[4]
        query = collection.find_one({'bonds_name': choice})
        header = ['ЦБ', 'Цена', 'День', 'Мес', 'Год', 'Акт.']
        body = [query['bonds_name'], query['bonds_price'], query['bonds_delta_day'], query['bonds_delta_month'],
                query['bonds_delta_year'], query['bonds_data_date']]
        text = ''
        text = tabletext(body, header, 'small')
        await message.reply('<code>' + text + '</code>', parse_mode='HTML')

    if message.text in news:  # второй вопрос
        collection = collections[6]
        if choice.split('_')[0] == 'Экономика':
            query = collection.find({'news_rubric': 'economics'})
        else:
            query = collection.find({'news_rubric': 'finance'})
        for i in query:
            text = '*' + i['news_topic'] + '*\n' + i['news_resume'] + '\n' + i['news_href']
            await message.reply(text, parse_mode=ParseMode.MARKDOWN)

    global shares
    if message.text in shares:
        collection = collections[7]
        choice = str(choice)[2:]
        query = collection.find_one({'stocks_ticker': choice})
        header = ['Тикер', 'Имя', 'Цена', 'День', 'Год', 'Акт.']
        body = [query['stocks_ticker'], query['stocks_name'], query['stocks_price'], query['stocks_delta_day'],
                query['stocks_delta_year'], query['stocks_data_date']]
        text = ''
        text = tabletext(body, header, 'small')
        await message.reply('<code>' + text + '</code>', parse_mode='HTML')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
