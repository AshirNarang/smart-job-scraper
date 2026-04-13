"""
Smart Job Scraper - Internshala

Author: Ashir Narang

Automates job search and extracts listings from Internshala.
Applies keyword-based filtering and saves results to a CSV file.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import datetime


# ------------------ DRIVER SETUP ------------------
def setup_driver():
    driver = webdriver.Chrome()
    driver.get("https://internshala.com/jobs/")
    return driver


# ------------------ SCROLL PAGE ------------------
def load_jobs(driver):
    wait = WebDriverWait(driver, 10)

    for _ in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    job_cards = wait.until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "individual_internship"))
    )

    print(f"Total jobs detected: {len(job_cards)}")
    return job_cards


# ------------------ GET FILTER KEYWORDS ------------------
def get_keywords():
    job_filter = input("Enter Filters: ")
    keywords = [k.lower().strip() for k in job_filter.split() if k.strip()]
    return keywords


# ------------------ EXTRACT + FILTER JOBS ------------------
def extract_filtered_jobs(driver, job_cards, keywords):
    filtered_jobs = []

    for card in job_cards:
        try:
            driver.execute_script("arguments[0].scrollIntoView();", card)
            time.sleep(0.1)

            title = card.find_element(By.CSS_SELECTOR, ".job-internship-name, .heading_4_5").text.strip()
            company = card.find_element(By.CSS_SELECTOR, ".company-name").text.strip()
            location = card.find_element(By.CSS_SELECTOR, ".location_link, .locations").text.strip()

            full_text = (title + company + location).lower()

            if any(k in full_text for k in keywords):
                job_data = [title, company, location]

                if job_data not in filtered_jobs:
                    print(f"MATCH FOUND: {title} at {company}")
                    filtered_jobs.append(job_data)

        except:
            continue

    return filtered_jobs


# ------------------ SAVE TO CSV ------------------
def save_to_csv(filtered_jobs):
    filename = f"jobs_{datetime.date.today()}.csv"

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Job Title", "Company", "Location"])
        writer.writerows(filtered_jobs)

    print(f"\nSaved {len(filtered_jobs)} jobs to {filename}")


# ------------------ MAIN ------------------
def main():
    driver = setup_driver()

    try:
        job_cards = load_jobs(driver)
        keywords = get_keywords()
        filtered_jobs = extract_filtered_jobs(driver, job_cards, keywords)
        save_to_csv(filtered_jobs)

    finally:
        time.sleep(10)
        driver.quit()


# ------------------ RUN ------------------
if __name__ == "__main__":
    main()