import logging
from telegram.ext import Application, MessageHandler, filters
import sqlalchemy as db
import random
from threading import Timer
from datetime import datetime, timedelta

START = datetime.today()
END = datetime.strptime("1.01.2027", "%d.%m.%Y")
AIRPORTS = ["AAH", "AAB", "AAI", "AAZ", "ABP", "AGW", "AKB", "AMS", "AWP", "AXC", "AXD", "AVX", "AZR", "AZD", "AYD",
            "AZZ", "ARH", "AQI", "APW", "AOM", "ANS", "ANO", "ANJ", "ALL", "ALT", "AIZ", "AGK"]


engine = db.create_engine('sqlite:///tickets.db')
conn = engine.connect()
metadata = db.MetaData()
tickets = db.Table("tickets", metadata,
  db.Column("ticket_id", db.Integer, primary_key=True),
    db.Column("date", db.Date),
    db.Column("from", db.Text),
    db.Column('to', db.Text),
    db.Column("price", db.Integer))
metadata.create_all(engine)


def random_date(st, e):
    dlt = e - st
    return st + timedelta(random.randint(0, dlt.days))


def Table_update():
    inf = []
    z_pr = random.randint(10000, 15000)
    for i in range(50):
        sql = tickets.delete()
        conn.execute(sql)
        fr = random.choice(AIRPORTS)
        inf.append({"date": random_date(START, END), "from": fr, "to": random.choice([i for i in AIRPORTS if i  != fr]),  "price": z_pr * (i + 1)})
    insertion_query = tickets.insert().values(inf)
    conn.execute(insertion_query)
    conn.commit()
    t = Timer(600, Table_update)
    t.start()
Table_update()
select_all_query = db.select(tickets)
select_all_results = conn.execute(select_all_query)
k = [", ".join([str(j) for j in i]) for i in select_all_results.fetchall()[:10]]
k = ";".join(k)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


async def tickets(update, context):
    await update.message.reply_text(k)


def main():
    application = Application.builder().token("8126296240:AAEZhuvduMd7LOtfpwhOOPfiqfYqlVCrbyY").build()
    text_handler = MessageHandler(filters.TEXT, tickets)
    application.add_handler(text_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
