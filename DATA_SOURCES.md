# Data sources and definitions

## Primary source

Ministry of Railways (Railway Board), Indian Railways Year Book 2023-24, Government of India:

https://rdso.indianrailways.gov.in/railwayboard/uploads/directorate/stat_econ/2025/IR%20Year%20Book%202023-24-English.pdf

The CSV tables are manually transcribed and normalized from:

- Data/railway_historical_indicators.csv: passenger originating, passenger-kilometres and average lead (pp. 23-24); revenue-earning freight tonnes, net tonne-kilometres and average lead (p. 40); route, running-track and total-track kilometres (p. 61).
- Data/state_rail_infrastructure_2023_24.csv: state and Union Territory network length (pp. 62-63).
- Data/zone_rail_infrastructure_2023_24.csv: zonal network length (pp. 61-62).
- Data/consequential_train_accidents.csv: accident counts by category and accident rate (p. 53).

## Definitions

- Passenger originating counts journeys, in millions; it is not a count of unique people.
- Passenger-kilometres are journeys multiplied by distance, in millions.
- Average passenger lead is the average distance per journey, in kilometres.
- Freight tonnes and net tonne-kilometres are millions. The historical revenue-earning freight series excludes Konkan Railway per the source note.
- Route, running-track and total-track kilometres are different infrastructure measures.
- Accident categories follow the Railway Board table's consequential accident classification.
- Year labels refer to Indian financial years.

## Treatment and caveats

Thousands separators were removed and values converted to numeric columns. State names are kept as printed where practical. The source says remaining States/Union Territories have no railway line. State route-kilometre values sum to the published all-India total. The source lists Goa with 122 running-track km and 113 total-track km; both are retained and flagged as an apparent source inconsistency.

Historical observations are selected years, not annual records. COVID-19 affected passenger traffic in 2020-21. Definitions and operating conditions may also vary over the long series. Interpret calculated ratios as descriptive summaries of published values.

## Attribution and rights

Attribution: Ministry of Railways (Railway Board), Indian Railways Year Book 2023-24, Government of India, pp. 23-24, 40, 53, 61-63, official PDF linked above.

This project separates the source statistics from Mansi Saxena's original notebook, code, narrative and charts. The official PDF is not represented as released under a particular open-data license. Check the publisher's applicable terms before reusing source material. For datasets expressly published on India's OGD Platform, consult their license record and the Government Open Data License - India at https://data.gov.in/Godl.
