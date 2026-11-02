from pathlib import Path
import csv
BASE=Path(__file__).parent
OUT=BASE/'output'
OUT.mkdir(exist_ok=True)
rows=[]
with (BASE/'data'/'hotel_monthly.csv').open(newline='',encoding='utf-8') as f:
    for r in csv.DictReader(f):
        available=int(r['available_room_nights']);sold=int(r['sold_room_nights']);revenue=int(r['room_revenue_vnd'])
        if available<=0 or sold<0 or sold>available or revenue<0: raise ValueError('Invalid hotel data')
        rows.append({'month':r['month'],'occupancy_pct':round(100*sold/available,2),'adr_vnd':round(revenue/sold,2) if sold else 0,'revpar_vnd':round(revenue/available,2)})
with (OUT/'monthly_kpis.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=['month','occupancy_pct','adr_vnd','revpar_vnd']);w.writeheader();w.writerows(rows)
print('Wrote',len(rows),'rows')
