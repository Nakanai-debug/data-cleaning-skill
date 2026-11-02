from pathlib import Path
import csv,sqlite3
BASE=Path(__file__).parent;OUT=BASE/'output';OUT.mkdir(exist_ok=True)
con=sqlite3.connect(':memory:')
con.execute('CREATE TABLE orders (order_id TEXT PRIMARY KEY,customer_id TEXT,order_date TEXT,status TEXT,category TEXT,amount_vnd INTEGER)')
with (BASE/'data'/'orders.csv').open(newline='',encoding='utf-8') as f: rows=list(csv.DictReader(f))
for r in rows:
    if int(r['amount_vnd'])<0 or r['status'] not in ('completed','cancelled'): raise ValueError('Invalid order')
con.executemany('INSERT INTO orders VALUES (?,?,?,?,?,?)',[(r['order_id'],r['customer_id'],r['order_date'],r['status'],r['category'],int(r['amount_vnd'])) for r in rows])
sql='\n'.join(line for line in (BASE/'metrics.sql').read_text().splitlines() if not line.lstrip().startswith('--'))
for name,stmt in zip(['monthly_kpis','category_performance','repeat_purchase'],[s.strip() for s in sql.split(';') if s.strip()]):
    cur=con.execute(stmt)
    with (OUT/(name+'.csv')).open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow([x[0] for x in cur.description]);w.writerows(cur.fetchall())
    print('Wrote',name)
