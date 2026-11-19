'''
Great. Now we’ll connect the three GenAI modules into one intelligence pipeline.

So far, we have three separate responsibilities:
1. Classifier — identifies what kind of job email it is.
2. Extractor — extracts structured information such as company, role, status and required action.
3. Summarizer — creates a short explanation of the email.
We’ll create a new file for this integration. Do not modify your existing app/processing/pipeline.py; that file handles the earlier Gmail-processing stages.

What happens inside analyze_email()?
Stage	Function	Output
1	classify_email()	Category and confidence
2	Check is_job_related	Stops irrelevant emails
3	extract_job_details()	Structured job details
4	summarize_email()	Readable summary
5	Return dictionary	One combined result

Why do we stop for irrelevant emails? Because there's no reason to spend additional LLM calls extracting details and summarizing a promotional email. This also helps control API usage and cost.
'''


from app.intelligence.classifier import classify_email
from app.intelligence.extractor import extract_job_details
from app.intelligence.summarizer import summarize_email


def analyze_email(email):

    # Step 1: Classify the email
    classification = classify_email(email)

    category = classification["category"]
    is_job_related = classification["is_job_related"]

    # Step 2: Stop if the email is irrelevant
    if not is_job_related:
        return {
            "classification": classification,
            "extracted_details": None,
            "summary": None
        }

    # Step 3: Extract structured job information
    extracted_details = extract_job_details(
        email,
        category
    )

    # Step 4: Generate a human-readable summary
    summary = summarize_email(
        email,
        category,
        extracted_details
    )

    # Step 5: Return all results together
    return {
        "classification": classification,
        "extracted_details": extracted_details,
        "summary": summary
    }
