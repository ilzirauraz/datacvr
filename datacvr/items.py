# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DatacrvItem(scrapy.Item):
    crv = scrapy.Field()

class ProductionUnitsItem(scrapy.Item):
    name = scrapy.Field()
    p_number = scrapy.Field()
    address = scrapy.Field()
    postal_code = scrapy.Field()
    city = scrapy.Field()
    start_date = scrapy.Field()
    sector_code = scrapy.Field()
    sector_code_description = scrapy.Field()
    advertising_protection = scrapy.Field()

class ExpandedBusinessInformationItem(scrapy.Item):
    municipality = scrapy.Field()
    activity_code = scrapy.Field()
    activity_code_description = scrapy.Field()
    objects = scrapy.Field()

class PowerToBindAndKeyIndividualsAndAuditorItem(scrapy.Item):
    power_to_bind = scrapy.Field()
    branch_manager = scrapy.Field() #BranchManagerItem

class BranchManagerItem(scrapy.Item):
    name = scrapy.Field()
    address = scrapy.Field()
    postal_code = scrapy.Field()
    city = scrapy.Field()
    country = scrapy.Field()

class InformationOnMainCompany(scrapy.Item):
    name_of_main_company = scrapy.Field()
    registered = scrapy.Field()
    address = scrapy.Field()
    registration_authority = scrapy.Field()
    objects = scrapy.Field()
    subscribed_capital = scrapy.Field()
    name_of_person_empowered_to_sign = scrapy.Field()
    address_of_peron_empowered_to_sign = scrapy.Field()
    power_to_bind = scrapy.Field()
    fiscal_year_eng = scrapy.Field()

class RegistrationHistoryInDanish(scrapy.Item):
    record_date = scrapy.Field()
    record_type = scrapy.Field()
    record = scrapy.Field()

class CompanyItem(scrapy.Item):
    _id = scrapy.Field()
    company_name = scrapy.Field()
    crv_number = scrapy.Field()
    address = scrapy.Field()
    postal_code = scrapy.Field()
    city = scrapy.Field()
    business_type = scrapy.Field()
    advertising_protection = scrapy.Field()
    status = scrapy.Field()
    production_units = scrapy.Field()
    expanded_business_information = scrapy.Field()
    information_on_main_company = scrapy.Field()
    registration_history = scrapy.Field()

