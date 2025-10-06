import os
import csv
import json
import argparse

def scrape_repo(root_dir):
    output = {}

    for company in os.listdir(root_dir):
        company_path = os.path.join(root_dir, company)
        if not os.path.isdir(company_path):
            continue

        company_data = {}
        for file in sorted(os.listdir(company_path)):
            if not file.endswith(".csv"):
                continue

            plan_name = os.path.splitext(file)[0]  # e.g., "Thirty Days"
            problems = []

            file_path = os.path.join(company_path, file)
            with open(file_path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    title = row.get("Title") or row.get("title") or ""
                    url = row.get("Link") or row.get("URL") or row.get("Leetcode Link") or ""
                    difficulty = row.get("Difficulty") or row.get("difficulty") or ""

                    problems.append({
                        "id": title.strip().replace(" ", "-").lower(),
                        "title": title.strip(),
                        "url": url.strip(),
                        "difficulty": difficulty.strip()
                    })

            company_data[plan_name] = problems

        output[company] = company_data

    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape leetcode-company-wise-problems CSVs into problems.js")
    parser.add_argument("--path", required=True, help="Root directory containing company folders")
    args = parser.parse_args()

    root_dir = os.path.abspath(args.path)
    if not os.path.isdir(root_dir):
        raise ValueError(f"Provided path is not a valid directory: {root_dir}")

    data = scrape_repo(root_dir)

    output_file = os.path.join("problems.js")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("window.PROBLEMS = ")
        json.dump(data, f, indent=2)
        f.write(";")

    print(f"✅ problems.js generated at {output_file}")
