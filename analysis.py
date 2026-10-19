from pathlib import Path
import textwrap
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages

ROOT = Path(__file__).resolve().parent
DATA, IMAGES = ROOT / "Data", ROOT / "images"
REPORT = ROOT / "Docs" / "Indian_Railways_Analytics_Report.pdf"
AUTHOR = "Mansi Saxena"
AUTHOR_LINKEDIN = "https://www.linkedin.com/in/mansi-saxena-049102362"
AUTHOR_GITHUB = "https://github.com/050804mansi"
AUTHOR_EMAIL = "mansi53245@gmail.com"
SOURCE = "https://rdso.indianrailways.gov.in/railwayboard/uploads/directorate/stat_econ/2025/IR%20Year%20Book%202023-24-English.pdf"
NAVY, TEAL, GOLD, MUTED = "#14283f", "#1d8a8a", "#e6a23c", "#607487"
plt.rcParams.update({"figure.facecolor":"white","axes.facecolor":"white","axes.edgecolor":"#d7dee5",
 "axes.labelcolor":NAVY,"axes.titlecolor":NAVY,"xtick.color":MUTED,"ytick.color":MUTED,
 "font.family":"DejaVu Sans","axes.spines.top":False,"axes.spines.right":False})

def load_data():
    return (
        pd.read_csv(DATA / "railway_historical_indicators.csv"),
        pd.read_csv(DATA / "state_rail_infrastructure_2023_24.csv"),
        pd.read_csv(DATA / "zone_rail_infrastructure_2023_24.csv"),
        pd.read_csv(DATA / "consequential_train_accidents.csv"),
    )

def summary(h, s, z, a):
    first, last = h.iloc[0], h.iloc[-1]
    state = s.query("Region_Type == 'State'").nlargest(1, "Route_Km").iloc[0]
    zone = z.nlargest(1, "Route_Km").iloc[0]
    accident = a.iloc[-1]
    return {
        "journey_multiple": last.Passengers_Originating_Million / first.Passengers_Originating_Million,
        "passenger_km_multiple": last.Passenger_Kilometres_Million / first.Passenger_Kilometres_Million,
        "route_change_pct": (last.Route_Km / first.Route_Km - 1) * 100,
        "freight_multiple": last.Revenue_Freight_Tonnes_Million / first.Revenue_Freight_Tonnes_Million,
        "top_state": state.State_or_Union_Territory,
        "top_state_km": int(state.Route_Km),
        "top_zone": zone.Railway_Zone,
        "top_zone_km": int(zone.Route_Km),
        "accidents": int(accident.Total_Consequential_Accidents),
        "derailment_pct": accident.Derailments / accident.Total_Consequential_Accidents * 100,
    }

def _save(fig, name):
    fig.tight_layout()
    fig.savefig(IMAGES / name, dpi=180, bbox_inches="tight")
    plt.close(fig)

def generate_charts():
    IMAGES.mkdir(parents=True, exist_ok=True)
    h, states, zones, accidents = load_data()
    sns.set_palette([TEAL, GOLD, "#5e7790", "#bd6248"])
    p = h.Passengers_Originating_Million / h.Passengers_Originating_Million.iloc[0] * 100
    pk = h.Passenger_Kilometres_Million / h.Passenger_Kilometres_Million.iloc[0] * 100
    fig, ax = plt.subplots(figsize=(11,5.5))
    ax.plot(h.Financial_Year, p, marker="o", lw=2.5, label="Passenger journeys")
    ax.plot(h.Financial_Year, pk, marker="o", lw=2.5, label="Passenger-kilometres")
    ax.set(title="Passenger demand has grown over the long run", ylabel="Index (1950-51 = 100)", xlabel="")
    ax.tick_params(axis="x", rotation=35); ax.grid(axis="y", alpha=.22); ax.legend(frameon=False, ncol=2)
    fig.text(.01,.005,f"Source: Railway Board Year Book 2023-24 | Prepared by {AUTHOR}",color=MUTED,fontsize=8)
    _save(fig,"01_passenger_demand_index.png")

    fig, ax = plt.subplots(figsize=(11,5.5))
    for col,label,color in [("Route_Km","Route length",NAVY),("Running_Track_Km","Running track",TEAL),("Total_Track_Km","Total track",GOLD)]:
        ax.plot(h.Financial_Year,h[col]/1000,marker="o",lw=2.4,label=label,color=color)
    ax.set(title="Rail network length across selected years",ylabel="Kilometres (thousands)",xlabel="")
    ax.tick_params(axis="x",rotation=35); ax.grid(axis="y",alpha=.22); ax.legend(frameon=False,ncol=3)
    fig.text(.01,.005,f"Selected financial-year observations | {AUTHOR}",color=MUTED,fontsize=8)
    _save(fig,"02_network_length.png")

    ft = h.Revenue_Freight_Tonnes_Million / h.Revenue_Freight_Tonnes_Million.iloc[0] * 100
    nt = h.Revenue_Freight_NTKm_Million / h.Revenue_Freight_NTKm_Million.iloc[0] * 100
    fig, ax = plt.subplots(figsize=(11,5.5))
    ax.plot(h.Financial_Year,ft,marker="o",lw=2.5,label="Revenue-earning freight tonnes")
    ax.plot(h.Financial_Year,nt,marker="o",lw=2.5,label="Net tonne-kilometres")
    ax.set(title="Freight output increased substantially",ylabel="Index (1950-51 = 100)",xlabel="")
    ax.tick_params(axis="x",rotation=35); ax.grid(axis="y",alpha=.22); ax.legend(frameon=False,ncol=2)
    fig.text(.01,.005,f"Freight series excludes Konkan Railway per source note | {AUTHOR}",color=MUTED,fontsize=8)
    _save(fig,"03_freight_output_index.png")

    state = states.query("Region_Type == 'State'").nlargest(10,"Route_Km").sort_values("Route_Km")
    fig, ax = plt.subplots(figsize=(10,6.2))
    ax.barh(state.State_or_Union_Territory,state.Route_Km,color=sns.color_palette("crest",n_colors=len(state)))
    ax.set(title="States with the most route kilometres (2023-24)",xlabel="Route kilometres")
    ax.grid(axis="x",alpha=.2)
    for y,v in enumerate(state.Route_Km): ax.text(v+80,y,f"{v:,}",va="center",fontsize=9,color=NAVY)
    ax.set_xlim(0,state.Route_Km.max()*1.18)
    fig.text(.01,.005,f"States only; Union Territories are in data | Official Year Book | {AUTHOR}",color=MUTED,fontsize=8)
    _save(fig,"04_state_route_km_top10.png")

    zone = zones.nlargest(10,"Route_Km").sort_values("Route_Km")
    fig, ax = plt.subplots(figsize=(10,6.2))
    ax.barh(zone.Railway_Zone,zone.Route_Km,color=sns.color_palette("crest",n_colors=len(zone)))
    ax.set(title="Railway zones by route kilometres (2023-24)",xlabel="Route kilometres")
    ax.grid(axis="x",alpha=.2)
    for y,v in enumerate(zone.Route_Km): ax.text(v+70,y,f"{v:,}",va="center",fontsize=9,color=NAVY)
    ax.set_xlim(0,zone.Route_Km.max()*1.18)
    fig.text(.01,.005,f"Official Year Book 2023-24 | Prepared by {AUTHOR}",color=MUTED,fontsize=8)
    _save(fig,"05_zone_route_km.png")

    cols=["Collisions","Derailments","Level_Crossing_Accidents","Fire_in_Trains","Miscellaneous_Accidents"]
    labels=["Collisions","Derailments","Level crossings","Fire in trains","Miscellaneous"]
    colors=[NAVY,TEAL,GOLD,"#bd6248","#8297a7"]
    fig, ax=plt.subplots(figsize=(10,5.5)); bottom=np.zeros(len(accidents))
    for col,label,color in zip(cols,labels,colors):
        vals=accidents[col].to_numpy(); ax.bar(accidents.Financial_Year,vals,bottom=bottom,label=label,color=color,width=.65); bottom+=vals
    ax.set(title="Consequential accidents by category",ylabel="Accidents",xlabel="")
    ax.grid(axis="y",alpha=.2); ax.legend(frameon=False,ncol=3,loc="upper right")
    fig.text(.01,.005,f"Series ends in 2023-24 | Official Year Book | {AUTHOR}",color=MUTED,fontsize=8)
    _save(fig,"06_consequential_accidents.png")

def _img(ax,name,title):
    import matplotlib.image as mpimg
    ax.imshow(mpimg.imread(IMAGES/name)); ax.set_title(title,loc="left",fontsize=12,weight="bold"); ax.axis("off")

def _footer(fig,page):
    fig.text(.04,.018,f"Indian Railways Analytics | {AUTHOR} | Railway Board Year Book 2023-24",fontsize=8,color=MUTED)
    fig.text(.96,.018,str(page),fontsize=8,color=MUTED,ha="right")

def build_report():
    h,s,z,a=load_data(); m=summary(h,s,z,a); REPORT.parent.mkdir(parents=True,exist_ok=True)
    with PdfPages(REPORT,metadata={"Title":"Indian Railways Network and Traffic Analytics","Author":AUTHOR,"Subject":"Analysis of official railway statistics"}) as pdf:
        fig=plt.figure(figsize=(11.7,8.3)); fig.patch.set_facecolor("#f5f8fb")
        fig.text(.07,.91,"INDIAN RAILWAYS",fontsize=12,color=TEAL,weight="bold")
        fig.text(.07,.84,"Network & Traffic Analytics",fontsize=27,color=NAVY,weight="bold")
        fig.text(.07,.79,"Passenger demand, freight movement and infrastructure",fontsize=12,color=MUTED)
        fig.text(.07,.735,f"Prepared by {AUTHOR}",fontsize=12,color=NAVY,weight="bold")
        fig.text(.07,.695,"LinkedIn: Mansi Saxena",fontsize=8,color=TEAL,url=AUTHOR_LINKEDIN)
        fig.text(.39,.695,"GitHub: 050804mansi",fontsize=8,color=TEAL,url=AUTHOR_GITHUB)
        fig.text(.68,.695,f"Email: {AUTHOR_EMAIL}",fontsize=8,color=TEAL,url=f"mailto:{AUTHOR_EMAIL}")
        cards=[("6,905 million","passenger journeys\nin FY 2023-24"),("69,181 km","route length\nin FY 2023-24"),(f"{m['journey_multiple']:.1f}x","journey count\nvs 1950-51")]
        for i,(num,label) in enumerate(cards):
            x=.07+i*.30
            fig.patches.append(plt.Rectangle((x,.55),.26,.12,transform=fig.transFigure,facecolor="white",edgecolor="#d7e1e9"))
            fig.text(x+.02,.615,num,fontsize=17,color=TEAL,weight="bold"); fig.text(x+.02,.568,label,fontsize=9,color=MUTED)
        fig.text(.07,.48,"Executive summary",fontsize=15,color=NAVY,weight="bold")
        bullets=[
          f"Passenger journeys rose from 1,284 million in 1950-51 to 6,905 million in 2023-24; passenger-kilometres grew {m['passenger_km_multiple']:.1f}x.",
          f"Route length increased {m['route_change_pct']:.1f}% across selected observations; revenue-earning freight tonnes increased {m['freight_multiple']:.1f}x.",
          f"{m['top_state']} had the largest state route length ({m['top_state_km']:,} km); {m['top_zone']} had the largest zone route length ({m['top_zone_km']:,} km).",
          f"There were {m['accidents']} consequential accidents in 2023-24; derailments were {m['derailment_pct']:.1f}% of that total."
        ]
        y=.425
        for b in bullets:
            fig.text(.08,y,"•",fontsize=14,color=GOLD,weight="bold")
            fig.text(.105,y,textwrap.fill(b,112),fontsize=10,color=NAVY,va="top",linespacing=1.4); y-=.085
        fig.text(.07,.07,"Selected financial-year snapshots are not a complete annual panel. These descriptive statistics do not establish causes or predict future performance.",fontsize=9,color=MUTED,wrap=True)
        _footer(fig,1); pdf.savefig(fig,bbox_inches="tight"); plt.close(fig)

        for page,title,files in [
          (2,"Passenger use and network length",[("01_passenger_demand_index.png","Passenger demand index (1950-51 = 100)"),("02_network_length.png","Network length")]),
          (3,"Freight movement and state infrastructure",[("03_freight_output_index.png","Freight output index"),("04_state_route_km_top10.png","Top states by route kilometres")]),
          (4,"Railway zones and safety context",[("05_zone_route_km.png","Zone route kilometres"),("06_consequential_accidents.png","Accident categories, 2019-20 to 2023-24")])]:
            fig,axs=plt.subplots(2,1,figsize=(11.7,8.3))
            for ax,(name,sub) in zip(axs,files): _img(ax,name,sub)
            fig.suptitle(title,x=.04,y=.98,ha="left",fontsize=18,weight="bold",color=NAVY)
            fig.subplots_adjust(top=.91,bottom=.06,hspace=.08,left=.04,right=.96)
            _footer(fig,page); pdf.savefig(fig,bbox_inches="tight"); plt.close(fig)

        notes=[
          ("Primary source","Ministry of Railways (Railway Board), Indian Railways Year Book 2023-24, pp. 23-24, 40, 53, 61-63."),
          ("Measures","Passenger originating counts journeys in millions; passenger-kilometres are in millions; freight tonnes and net tonne-kilometres are millions. Route, running-track and total-track kilometres are distinct measures."),
          ("Coverage","Historical figures are only the observations printed in the Year Book. State and zone figures are a 2023-24 snapshot. The freight series excludes Konkan Railway as noted in the source."),
          ("Safety caveat","Consequential-accident counts use the report's category definition and are not a complete safety assessment."),
          ("Source data quality","Goa is listed with 122 running-track km and 113 total-track km. Both published figures are preserved; this apparent inconsistency is flagged, not silently corrected."),
          ("Interpretation","COVID-19 affected passenger services in 2020-21. Sparse observations and changing operating conditions limit comparisons; no causal claim or forecast is made."),
          ("Rights","Original notebook, code, report narrative and charts are © 2026 Mansi Saxena, All Rights Reserved. Source data remain subject to applicable publisher terms. See DATA_SOURCES.md and COPYRIGHT.txt.")
        ]
        fig=plt.figure(figsize=(11.7,8.3)); fig.text(.06,.93,"Method, definitions and limitations",fontsize=20,color=NAVY,weight="bold")
        y=.85
        for head,body in notes:
            fig.text(.07,y,head,fontsize=11,color=TEAL,weight="bold",va="top")
            fig.text(.25,y,textwrap.fill(body,105),fontsize=9.5,color=NAVY,va="top",linespacing=1.35); y-=.105
        fig.text(.07,.065,f"Official source PDF: {SOURCE}",fontsize=7.2,color=MUTED,wrap=True)
        _footer(fig,5); pdf.savefig(fig,bbox_inches="tight"); plt.close(fig)

def main():
    generate_charts(); build_report()
    h,s,z,a=load_data()
    print(f"Created {len(list(IMAGES.glob('*.png')))} charts and report: {REPORT}")
    print(summary(h,s,z,a))

if __name__=="__main__":
    main()
