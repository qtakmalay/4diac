"""Task definitions for 4diac IDE usability assessment.
Based on the 4 maintenance tasks from Wiesmayr et al. (2023)."""

TASKS = {
    "task1_orientation": {
        "name": "Task 1: Orientation",
        "description": (
            "You are an automation engineer seeing the 4diac IDE for the first time. "
            "Your task is to explore and understand the structure of the project currently open in the IDE. "
            "Specifically:\n"
            "1. First, close the Welcome tab to see the main IDE workspace\n"
            "2. Find and explore the System Explorer or project tree on the left side\n"
            "3. Try to find a function block related to a 'motor' in the application\n"
            "4. Navigate through the hierarchy to understand how the application is structured\n\n"
            "As you work, note any usability issues you encounter: "
            "things that are confusing, hard to find, poorly labeled, or require too many steps. "
            "Report your observations at the end."
        ),
        "max_steps": 30,
    },
    "task2_hierarchy": {
        "name": "Task 2: Hierarchy Navigation",
        "description": (
            "You are working with the 4diac IDE. Your task is to navigate the application hierarchy. "
            "Specifically:\n"
            "1. Open the System Explorer if not already visible\n"
            "2. Expand the project tree to see all levels of the application\n"
            "3. Try to understand the nesting structure (Applications > SubApplications > Function Blocks)\n"
            "4. Navigate to a deeply nested function block (at least 3 levels deep)\n"
            "5. Try to determine your current location in the hierarchy at all times\n\n"
            "As you work, note any usability issues: "
            "Is it clear where you are in the hierarchy? Can you easily navigate back? "
            "Are the names and icons meaningful? Report your observations at the end."
        ),
        "max_steps": 30,
    },
    "task3_library": {
        "name": "Task 3: Library Usage",
        "description": (
            "You are working with the 4diac IDE. Your task is to add a function block from the library. "
            "Specifically:\n"
            "1. Find the Type Library or Palette that contains available function block types\n"
            "2. Browse the library to see what types are available\n"
            "3. Try to find a specific type (e.g., an E_SWITCH or E_SR block)\n"
            "4. Try to add/drag a block from the library into the application editor\n\n"
            "As you work, note any usability issues: "
            "Is the library easy to find and browse? Can you search for types? "
            "Is drag-and-drop intuitive? Report your observations at the end."
        ),
        "max_steps": 30,
    },
    "task4_editing": {
        "name": "Task 4: Editing & Type Changes",
        "description": (
            "You are working with the 4diac IDE. Your task is to edit function blocks. "
            "Specifically:\n"
            "1. Find a function block in the application editor\n"
            "2. Try to view and edit its properties (parameters, connections)\n"
            "3. Try to change the type of a function block using the context menu\n"
            "4. Observe what happens to existing connections after a type change\n"
            "5. Try to fix any broken connections\n\n"
            "As you work, note any usability issues: "
            "Is editing intuitive? What happens when you change a block's type? "
            "Are error messages helpful? Can you undo mistakes? Report your observations at the end."
        ),
        "max_steps": 30,
    },
}

# System prompt for the usability assessment agent
SYSTEM_PROMPT = (
    "You are a usability assessment expert evaluating the Eclipse 4diac IDE. "
    "You are interacting with the IDE running in a virtual display. "
    "Your goal is to complete the given task while carefully observing usability issues.\n\n"
    "Guidelines:\n"
    "- Take a screenshot first to see the current state before acting\n"
    "- Click precisely on UI elements you can see in the screenshot\n"
    "- If something doesn't work, try alternative approaches\n"
    "- Note every usability issue: confusing labels, hard-to-find features, "
    "unexpected behavior, missing feedback, too many steps required\n"
    "- When you're done or stuck, provide a detailed usability report\n"
    "- Be specific: mention exact UI elements, their locations, and what was problematic\n"
    "- Rate each issue by severity: Critical, Major, Minor, Cosmetic"
)
