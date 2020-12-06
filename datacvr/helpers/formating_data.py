from typing import List, Dict
from datacvr.items import CompanyItem, ProductionUnitsItem, ExpandedBusinessInformationItem, InformationOnMainCompany, \
    RegistrationHistoryInDanish
from scrapy.selector import Selector
from scrapy import Item


def formatting_string(lines: List[str]):
    """Очистка от переносов строк и пробелов по бокам"""
    return ' '.join(lines).replace('\n', '').strip()


def formatting_number(lines: List[str]):
    """Очистка от переносов строк и пробелов"""
    try:
        return int(formatting_string(lines))
    except:
        return None


def parse_tables(response):
    company_props = {
        'CVR nummer': 'cvr_number',
        'Address': 'address',
        'Postal code and city': 'postal_code_and_city',
        'Business type': 'business_type',
        'Advertising protection': 'advertising_protection',
        'Status': 'status'
    }

    expanded_business_information_props = {
        'Municipality': 'municipality',
        'Activity code': 'activity_code_and_description',
        'Objects': 'objects',
    }
    information_on_main_company_props = {
        'Name of main company': 'name_of_main_company',
        'Registered office': 'registered',
        'Address': 'address',
        'Registration authority': 'registration_authority',
        'Objects': 'objects',
        'Subscribed capital': 'subscribed_capital',
        'Empowered to sign': 'name_of_person_empowered_to_sign',
        'Power to bind': 'power_to_bind',
        'Regnskabsår eng': 'fiscal_year_eng'
    }

    production_units_props = {
        'Name': 'name',
        'P-number': 'p_number',
        'Address': 'address',
        'Postal code and city': 'postal_code_and_city',
        'start_date': 'Start date',
        'sector_code_and_description': 'Sector code',
        'advertising': 'Advertising protection',
    }

    company_item = CompanyItem()
    expanded_business_information_item = ExpandedBusinessInformationItem()
    information_on_main_company_item = InformationOnMainCompany()
    production_units_item = ProductionUnitsItem()

    company_info_table = response.xpath('//*[@class="table stamdata"]/div').getall()

    company_item['company_name'] = formatting_string(response.xpath('.//*[@class="enhedsnavn"]/text()').getall())
    company_item['crv_number'] = formatting_number(response.css('.col-sm-6.cvrreg::text').getall())
    company_item = parse_table(company_item, company_info_table, company_props)

    expanded_business_block = response.xpath('//*[@id="accordion-Flere-Stamdata"]/div').get()
    expanded_business_information_table = Selector(text=expanded_business_block). \
        xpath('//*[@data-pdf-class="sektion"]/div').getall()
    expanded_business_information_item = \
        parse_table(expanded_business_information_item,
                    expanded_business_information_table,
                    expanded_business_information_props)

    information_on_main_company_block = response.xpath('//*[@id="accordion-Oplysninger-om-hovedselskab"]/div').get()
    if information_on_main_company_block:
        information_on_main_company_table = Selector(text=information_on_main_company_block). \
            xpath('//*[@data-pdf-class="sektion"]/div').getall()
        information_on_main_company_item = parse_table(information_on_main_company_item,
                                                       information_on_main_company_table,
                                                       information_on_main_company_props)

    production_units_block = response.xpath('//*[@id="accordion-P-enheder"]/div').get()
    production_units_table = Selector(text=production_units_block).xpath(
        '//*[@class="row dataraekker"]/div').getall()
    production_units_item = parse_table(production_units_item,
                                        production_units_table,
                                        production_units_props)

    registration_history_item = RegistrationHistoryInDanish()
    registration_history_block = response.xpath('//*[@id="accordion-Historisk"]/div').get()
    registration_history_item = parse_registration_history(registration_history_item, registration_history_block)

    company_item['expanded_business_information'] = expanded_business_information_item
    company_item['information_on_main_company'] = information_on_main_company_item
    company_item['production_units'] = production_units_item
    company_item['registration_history'] = registration_history_item
    return company_item


def parse_table(item: Item, rows: List[str], prop_dict: Dict):
    for row in rows:
        header = Selector(text=row).xpath('//strong/text()').get()
        if header is not None:
            header = header.replace('\n', '').strip()
            value = formatting_string(Selector(text=row).xpath('//div/div/text()').getall())
            if not value:
                value = formatting_string(Selector(text=row).xpath('//div/div/a/text()').getall())

            if header in list(prop_dict.keys()):
                prop = prop_dict[header]
                if prop == 'postal_code_and_city':
                    item['postal_code'] = formatting_number([value.split(' ')[0]])
                    item['city'] = value.split(' ')[1]
                    continue
                if prop == 'branch_manager':
                    # TODO: распарсить таблицу по ссылке
                    pass
                if prop == 'activity_code_and_description':
                    item['activity_code'] = formatting_number([value.split(' ')[0]])
                    item['activity_code_description'] = formatting_string(value.split(' ')[1:])
                    continue
                if prop == 'sector_code_and_description':
                    item['sector_code'] = formatting_number([value.split(' ')[0]])
                    item['sector_code_description'] = formatting_string(value.split(' ')[1:])
                    continue
                item[prop] = value
    return item


def parse_registration_history(item: Item, row):
    record_date_and_type = Selector(text=row).xpath('.//*[@class="col-sm-12"]/b/text()').get()
    item['record_date'] = record_date_and_type.split(' ')[0]
    item['record_type'] = formatting_string(record_date_and_type.split(' ')[1:])
    result = {}
    record_item_props = {
        'CVR number:': 'crv_number',
        'Filialbestyrer:': 'branch_manager',
        'Formål:': 'purpose',
        'Registrerende myndighed:': 'registering_authority',
        'Navn:': 'name',
        'Adresse:': 'address',
        'Tegnet kapital:': 'subscribed_capital',
        'Tegningsberettiget': 'authorized_to_subscribe_powers_to_bind_and_powers_to_bind',
        'Regnskabsår:': 'fiscal_year',
        'Formål for hovedselskab:': 'purpose_of_parent_company'
    }
    headers = Selector(text=row).xpath(
        '//*[@class="col-sm-12"]/h1/text()').getall()

    for header in headers:
        info_row = Selector(text=row).xpath(f'//h1[text()="{header}"]/following::p[1]/text()').get()
        key = header.replace('\n', '').strip()
        if key in list(record_item_props.keys()):
            prop = record_item_props[key]
            if prop == 'authorized_to_subscribe_powers_to_bind_and_powers_to_bind':
                result['authorized_to_subscribe_powers_to_bind'] = \
                    Selector(text=row).xpath(f'//h1[text()="{header}"]/following::p[1]/text()').get()
                result['authorized_to_powers_to_bind'] = \
                    Selector(text=row).xpath(f'//h1[text()="{header}"]/following::p[2]/text()').get()
            else:
                result[prop] = info_row
    item['record'] = result
    return item
