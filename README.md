# Parser DATACVR

## Requirements
- python3.8
- mongodb

## Run
Необходимо получить доступ к базе данных в формате URI и прописать его в файле datacvr/mongo/conn
Запустить программу с помощью команды из корневой папки 
```bash
python3.8 -m scrapy runspider datacvr/spiders/datacrv_spider.py
```

## Description
Разработан парсер информации о компаниях с сайта https://data.virk.dk/
Парсер собирает информацию и размещает ее в mongodb

## How does it work

1) Формируем процесс отправки запросов. Выполняем редирект, пока не появятся куки, 
после которых получится ответ со статусом 200

2) Логика разбора html-страниц. В парсере есть два типа страниц: список компаний и
страница конкретной компании. Из страницы со списком компаний вытаскиваем cvr
компании, который в дальнейшем будет использоваться для формирования запроса к странице конкретной компании

## Example
Информация взята со страницы компании MGHM Limited, дочерней компании MGHM Limited, Англия:
```
{
  "company_name": "MGHM Limited filial af MGHM Limited, England",
  "cvr_number": "41542446",
  "address": "MÃ¸llebakkevej 3A SÃ¸nder HÃ¸jrup",
  "postal_code": "5750",
  "city": "Ringe",
  "business_type": ["Filial af udenlandsk aktieselskab", "Kommanditakties"],
  "advertising_protection": "No",
  "status": "Normal",
  "expanded_business_information": {
    "municipality": "Faaborg-Midtfyn",
    "activity_code": "773200",
    "activity_code_description": "Udlejning og leasing af entreprenÃ¸rmateriel",
    "objects": "Udleje og leasing af byggeri og anlÃ¦gsmaskiner og udstyr"
  },
  "power_to_bind_and_key_individuals_and_auditor": {
    "power_to_bind": "Filialen tegnes af en filialbestyrer",
    "branch_manager": {
      "name": "Johnny Oluf Kjellerup",
      "address": "MÃ¸llebakkevej 3A",
      "postal_code": "5750",
      "city": "Ringe",
      "country": "Danmark"
    }
  },
  "information_on_main_company": {
    "name_of_main_company": "MGHM Limited, England",
    "registered office": "Storbritannien",
    "address": "112C High Street Hadleigh Suffolk IP7 5EL UK",
    "registration_authority": "Companies House",
    "objects": "Hovedselskabets formÃ¥l er at udleje og lease byggeri og anlÃ¦gsmaskiner og udstyr",
    "subscribed_capital": "1,00 GBP",
    "name_of_person_empowered_to_sign": "Jens Gadegaard",
    "address_of_peron_empowered_to_sign": "White Court, Kings Ride 9, Alfriston, BN26 5XP Polegate, UK",
    "power_to_bind": "Hovedselskabet tegnes af en direktÃ¸r",
    "fiscal_year_eng": "From 01.02 to 31.01"
  },
  "production_units": {
    "name": "MGHM Limited filial af MGHM Limited, England",
    "p_number": "1026065778",
    "address": "MÃ¸llebakkevej 3A SÃ¸nder HÃ¸jrup",
    "postal_code": "5750",
    "city": "Ringe",
    "start_date": "14.07.2020",
    "sector_code": "773200",
    "sector_code_description": "Udlejning og leasing af entreprenÃ¸rmateriel",
    "advertising protection": "No"
  },
  "registration_history_in_danish": [{
    "record_date": "27.07.2020",
    "record_type": "Nye selskaber",
    "record": {
      "cvr_number": "41542446",
      "name_and_address": [
        "MGHM Limited filial af MGHM Limited, England",
        "MÃ¸llebakkevej 3A, SÃ¸nder HÃ¸jrup, 5750 Ringe"
      ],
      "branch_manager": "Johnny Oluf Kjellerup",
      "branch_manager_appointed_on": "14.07.2020",
      "branch_manager_powers_to_bind": "Filialen tegnes af en filialbestyrer",
      "purpose": "Udleje og leasing af byggeri og anlÃ¦gsmaskiner og udstyr Hovedselskabets registreringsnummer 11749266",
      "registering_authority": ["Companies House", "Storbritannien"],
      "name": "MGHM Limited, England",
      "address": "112C High Street, Hadleigh, Suffolk , IP7 5EL, UK, Storbritannien",
      "subscribed_capital": "GBP 1,00",
      "authorized_to_subscribe": "Jens Gadegaard, White Court, Kings Ride 9AlfristonBN26 5XP PolegateUK",
      "authorized_to_subscribe_powers_to_bind": "Hovedselskabet tegnes af en direktÃ¸r",
      "fiscal_year": "01.02 - 31.01",
      "purpose_of_parent_company": "Hovedselskabets formÃ¥l er at udleje og lease byggeri og anlÃ¦gsmaskiner og udstyr"
    }
  }]
}
```
