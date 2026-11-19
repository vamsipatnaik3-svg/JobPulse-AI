
from datetime import datetime
from zoneinfo import ZoneInfo


IST = ZoneInfo("Asia/Kolkata")


def generate_daily_briefing(analyzed_emails):

    today = datetime.now(IST).strftime("%d %B %Y")

    successful_emails = [
        item for item in analyzed_emails
        if item.get("processing_status") == "SUCCESS"
        and item.get("analysis")
        and item["analysis"].get("classification", {}).get("is_job_related")
    ]

    lines = [
        "Good morning! This is your JobPulse AI daily job update.",
        f"Here is your briefing for {today}."
    ]

    if not successful_emails:
        lines.append(
            "There are no new job-related email updates to report today."
        )
        lines.append("Have a great day, and good luck with your job search!")
        return " ".join(lines)

    lines.append(
        f"You have {len(successful_emails)} job-related email updates."
    )

    for index, item in enumerate(successful_emails, start=1):

        analysis = item["analysis"]
        classification = analysis.get("classification", {})
        details = analysis.get("extracted_details") or {}

        company = details.get("company") or "A company"
        role = details.get("job_role")
        category = classification.get("category", "JOB_UPDATE")
        status = details.get("application_status")
        action_required = details.get("action_required", False)
        action_details = details.get("action_details")

        lines.append(f"Update {index}.")

        if role:
            lines.append(f"{company} sent an update about the {role} position.")
        else:
            lines.append(f"You received a job-related email from {company}.")

        lines.append(f"The email category is {category.replace('_', ' ').lower()}.")

        if status:
            lines.append(f"The application status is {status}.")

        if action_required:
            lines.append("Action required.")

            if action_details:
                lines.append(str(action_details))
        else:
            lines.append("No specific action was identified.")

    lines.append(
        "That is your JobPulse AI update. Have a productive day!"
    )

    return " ".join(lines)
