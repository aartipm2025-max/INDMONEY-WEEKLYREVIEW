from main_workflow import AIWorkflow

workflow = AIWorkflow()
test_text = "My email is test@example.com and my phone is 9876543210. Call me!"
scrubbed = workflow.scrub_pii(test_text)
print(f"Original: {test_text}")
print(f"Scrubbed: {scrubbed}")

if "[EMAIL]" in scrubbed and "[PHONE]" in scrubbed:
    print("PII Scrubbing Test: PASSED")
else:
    print("PII Scrubbing Test: FAILED")
