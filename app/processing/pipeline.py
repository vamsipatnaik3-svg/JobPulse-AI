
from app.gmail.email_fetcher import fetch_emails

from app.processing.email_cleaner import clean_email
from app.processing.job_filter import filter_job_related_emails
from app.processing.deduplication import deduplicate_emails

from app.intelligence.intelligence_pipeline import analyze_email

from app.database.repository import (
    save_email_analysis,
    get_successfully_processed_message_ids
)


def process_emails():

    print("\n========== JOBPULSE AI ==========")

    # Step 1: Fetch Gmail emails
    print("\nStep 1: Fetching Gmail emails...")

    emails = fetch_emails(max_results=50)

    print(f"Total fetched: {len(emails)}")

    # Step 2: Skip successfully processed emails
    print("\nStep 2: Checking previously processed emails...")

    processed_ids = get_successfully_processed_message_ids()

    new_emails = [
        email for email in emails
        if email.get("id") not in processed_ids
    ]

    print(f"New emails to process: {len(new_emails)}")
    print(
        f"Previously processed emails skipped: "
        f"{len(emails) - len(new_emails)}"
    )

    if not new_emails:
        print("\nNo new emails to process.")
        print("\n========== PROCESSING COMPLETED ==========")
        return []

    # Step 3: Clean emails
    print("\nStep 3: Cleaning email content...")

    cleaned_emails = [
        clean_email(email) for email in new_emails
    ]

    print(f"Cleaned emails: {len(cleaned_emails)}")

    # Step 4: Filter job-related emails
    print("\nStep 4: Filtering job-related emails...")

    job_emails = filter_job_related_emails(cleaned_emails)

    print(f"Potential job emails: {len(job_emails)}")

    # Step 5: Remove duplicates
    print("\nStep 5: Removing duplicates...")

    unique_emails = deduplicate_emails(job_emails)

    print(f"Unique job emails: {len(unique_emails)}")

    if not unique_emails:
        print("\nNo new job-related emails found.")
        print("\n========== PROCESSING COMPLETED ==========")
        return []

    # Step 6: GenAI analysis and database storage
    print("\nStep 6: Starting GenAI analysis...")

    analyzed_emails = []

    for index, email in enumerate(unique_emails, start=1):

        print(f"\nAnalyzing email {index}/{len(unique_emails)}")

        try:
            analysis = analyze_email(email)

            email_result = {
                "email": email,
                "analysis": analysis,
                "processing_status": "SUCCESS"
            }

            print("\nClassification:")
            print(analysis.get("classification"))

            print("\nExtracted Details:")
            print(analysis.get("extracted_details"))

            print("\nSummary:")
            print(analysis.get("summary"))

        except Exception as error:

            print(f"AI analysis failed: {error}")

            email_result = {
                "email": email,
                "analysis": None,
                "processing_status": "FAILED",
                "error": str(error)
            }

        analyzed_emails.append(email_result)

        # Save each email immediately
        try:
            record_id = save_email_analysis(email_result)

            print(f"Database record saved: {record_id}")

        except Exception as db_error:

            print(f"Database saving failed: {db_error}")

    # Step 7: Final results
    print("\n========== FINAL JOBPULSE AI RESULTS ==========")

    successful = sum(
        1 for item in analyzed_emails
        if item["processing_status"] == "SUCCESS"
    )

    failed = sum(
        1 for item in analyzed_emails
        if item["processing_status"] == "FAILED"
    )

    print(f"Total emails processed: {len(analyzed_emails)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")

    print("\n========== PROCESSING COMPLETED ==========")

    return analyzed_emails


if __name__ == "__main__":
    process_emails()
