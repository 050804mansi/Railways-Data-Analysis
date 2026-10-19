# Indian Railways Network & Traffic Analytics

**Author: Mansi Saxena**

## Contact

- LinkedIn: [Mansi Saxena](https://www.linkedin.com/in/mansi-saxena-049102362)
- GitHub: [050804mansi](https://github.com/050804mansi)
- Email: [mansi53245@gmail.com](mailto:mansi53245@gmail.com)

An original railway analytics project using official Indian Railways statistics. It studies long-run passenger and freight trends, state and zone infrastructure, and recent consequential accident counts. It follows the reference project's deliverable pattern—data, Jupyter notebook, charts, report and README—while using different datasets and analysis.

## Project contents

- Data: four attributed CSV tables.
- Notebook/Indian_Railways_Analytics_Mansi_Saxena.ipynb: exploratory workflow.
- analysis.py: regenerates charts and the PDF report.
- images: generated figures.
- Docs/Indian_Railways_Analytics_Report.pdf: written report.
- DATA_SOURCES.md: dataset citations and definitions.
- COPYRIGHT.txt: project reuse notice and data-rights boundary.

## Questions explored

1. How have passenger journeys and passenger-kilometres changed across selected financial years?
2. How did route length, running track and total track change?
3. How has revenue-earning freight output changed?
4. Which states and railway zones had the most route kilometres in 2023-24?
5. How were consequential train accidents distributed from 2019-20 to 2023-24?

## Run

From this folder, install dependencies with pip install -r requirements.txt. Run python analysis.py to recreate six figures and the PDF report. Open the notebook in Jupyter at Notebook/Indian_Railways_Analytics_Mansi_Saxena.ipynb.

## Selected findings

- Passenger journeys rose from 1,284 million in 1950-51 to 6,905 million in 2023-24.
- Route length grew from 53,596 km to 69,181 km across the selected observations.
- Uttar Pradesh had the largest state route length in the 2023-24 table: 8,823 km.
- The source reports 40 consequential train accidents in 2023-24; 25 were derailments.

The historical table contains selected years, not a complete annual series. COVID-19 affected passenger operations in 2020-21. This is descriptive analysis and does not establish causes or make forecasts.

## Original work and reuse

The notebook, analysis code, report narrative and original charts are © 2026 Mansi Saxena, All Rights Reserved. No reuse license is granted for those original materials. Government statistics are separately attributed; the author does not claim exclusive ownership of source data. See COPYRIGHT.txt and DATA_SOURCES.md.

A copyright notice and attribution make authorship clear, but cannot technically prevent copying from a public repository. Keep the repository private if the files must not be publicly accessible. If published, retain the notice and source attribution.

This project is independent and is not endorsed by the Ministry of Railways or Government of India.
