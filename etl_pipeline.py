import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from extract import extract_data
from transform import transform_data
from load import load_data

logging.basicConfig(
    filename="logs/etl.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def run_etl():
    try:
        logging.info("ETL Started")
        
        raw = extract_data()
        clean = transform_data(raw)
        load_data(clean)
        
        logging.info("ETL Completed Successfully")
        
    except Exception as e:
        logging.error(f"ETL Failed: {e}")

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(run_etl, "interval", minutes=5)
    
    print("ETL running every 5 minutes...")
    scheduler.start()