import os
import json
from mcp.server.fastmcp import FastMCP
from stage_04_ui_actions.actions import WorkflowActions

# Initialize FastMCP server
mcp = FastMCP("INDmoney Pulse Manager")

# Initialize our internal actions class
actions = WorkflowActions()

@mcp.tool()
def log_to_master_notes(pulse_json: str, fee_json: str) -> str:
    """
    Appends the weekly pulse and fee explainer results to the Master Notes file.
    
    Args:
        pulse_json: The JSON string containing themes, quotes, and action ideas.
        fee_json: The JSON string containing the fee explanation scenario and bullets.
    """
    try:
        pulse_data = json.loads(pulse_json)
        fee_data = json.loads(fee_json)
        success = actions.append_to_notes(pulse_data, fee_data)
        if success:
            return f"Successfully appended to {actions.notes_path}"
        return "Failed to append to notes."
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def create_report_email(pulse_json: str, fee_json: str, recipient: str = "") -> str:
    """
    Creates an .eml email draft with the weekly report.
    
    Args:
        pulse_json: The JSON string containing themes, quotes, and action ideas.
        fee_json: The JSON string containing the fee explanation.
        recipient: Optional recipient email address.
    """
    try:
        pulse_data = json.loads(pulse_json)
        fee_data = json.loads(fee_json)
        # We don't auto-send from MCP for safety, just draft.
        result = actions.create_email_draft(pulse_data, fee_data, send=False, recipient=recipient)
        return result
    except Exception as e:
        return f"Error drafting email: {str(e)}"

@mcp.tool()
def check_workflow_status() -> str:
    """Checks the status of the local environment and configured paths."""
    notes_exists = os.path.exists(actions.notes_path)
    drafts_count = len(os.listdir(actions.drafts_dir)) if os.path.exists(actions.drafts_dir) else 0
    
    return (f"Environment Status:\n"
            f"- Master Notes: {'Found' if notes_exists else 'Not Found'}\n"
            f"- Email Drafts: {drafts_count} files in {actions.drafts_dir}")

if __name__ == "__main__":
    # Start the fastmcp server
    mcp.run()
