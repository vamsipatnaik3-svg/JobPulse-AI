
from app.database.db import SessionLocal
from app.database.models import EmailAnalysis


def save_email_analysis(email_result):
    """
    Save or update an email analysis record in the database.
    """

    session = SessionLocal()

    try:
        email = email_result.get("email", {})
        analysis = email_result.get("analysis") or {}

        # Get Gmail message ID
        message_id = (
            email.get("id")
            or email.get("gmail_message_id")
            or email.get("message_id")
        )

        if not message_id:
            raise ValueError("Gmail message ID is missing.")

        # Find existing record
        existing_record = (
            session.query(EmailAnalysis)
            .filter(
                EmailAnalysis.gmail_message_id == message_id
            )
            .first()
        )

        # Extract analysis information
        classification = analysis.get("classification", {})
        extracted_details = analysis.get("extracted_details", {})
        summary = analysis.get("summary")

        processing_status = email_result.get(
            "processing_status", "FAILED"
        )

        error_message = email_result.get("error")

        if existing_record:

            # Update existing record
            record = existing_record

        else:

            # Create new record
            record = EmailAnalysis(
                gmail_message_id=message_id
            )

            session.add(record)

        # Store email information
        record.sender = email.get("sender")
        record.subject = email.get("subject")
        record.body = email.get("body")
        record.received_at = email.get("date")

        # Store classification information
        record.job_score = classification.get("job_score")
        record.category = classification.get("category")
        record.is_job_related = classification.get(
            "is_job_related"
        )
        record.confidence = classification.get("confidence")

        # Store extracted details
        record.extracted_details = extracted_details

        # Store summary
        record.summary = summary

        # Store processing status
        record.processing_status = processing_status
        record.error = error_message

        session.commit()
        session.refresh(record)

        return record.id

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


def get_successfully_processed_message_ids():
    """
    Return Gmail message IDs that were successfully processed.

    Failed emails are intentionally excluded so they can be retried.
    """

    session = SessionLocal()

    try:
        records = (
            session.query(EmailAnalysis.gmail_message_id)
            .filter(
                EmailAnalysis.processing_status == "SUCCESS",
                EmailAnalysis.gmail_message_id.isnot(None)
            )
            .all()
        )

        return {
            record[0]
            for record in records
        }

    finally:
        session.close()
