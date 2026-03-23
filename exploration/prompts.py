"""Assessment prompts for 4diac IDE usability evaluation — 3 levels."""

BLIND_PROMPT = """You are a UX/usability expert. Watch this video of a user demonstrating tasks in an IDE (Integrated Development Environment) for industrial automation programming.

Assess the usability of this IDE. Focus on:
- What do you observe about the user interface?
- What seems easy or difficult for users?
- What usability issues can you identify?
- What are the strengths of this interface?
- What improvements would you suggest?

Be specific and reference particular moments or UI elements you observe in the video."""

CD_GUIDED_PROMPT = """You are a UX/usability expert. Watch this video of a user demonstrating tasks in an IDE for industrial automation programming (Eclipse 4diac IDE, based on IEC 61499 standard).

Evaluate the usability using the Cognitive Dimensions of Notations framework. For each dimension, assess what you observe:

1. **Viscosity** — How much effort is needed to make changes? Are there repetitive actions?
2. **Visibility** — Can users easily see all relevant information? Is anything buried or hidden?
3. **Premature Commitment** — Are users forced to make decisions before having enough information?
4. **Hidden Dependencies** — Are there important links between elements that aren't visible?
5. **Role-Expressiveness** — Can users easily understand the purpose of each UI element from its appearance?
6. **Error-Proneness** — Does the interface invite mistakes? Is there sufficient protection?
7. **Abstraction** — Are the abstraction mechanisms appropriate? Too many or too few?
8. **Secondary Notation** — Can users add informal notes/comments/colors beyond formal syntax?
9. **Closeness of Mapping** — How well does the visual representation match the domain concepts?
10. **Consistency** — Are similar things expressed in similar ways throughout the interface?
11. **Diffuseness** — Is the notation verbose? Do large icons/elements reduce working area?
12. **Hard Mental Operations** — Are there tasks that place high cognitive load on users?
13. **Provisionality** — Can users make tentative/provisional changes easily?
14. **Progressive Evaluation** — Can users check their work-in-progress at any time?

For each dimension, rate it as: GOOD, MODERATE, or POOR, and explain what you observed.
End with a summary of the top 5 most critical usability issues."""

TASK_SPECIFIC_PROMPTS = {
    "task1_orientation": """You are a UX/usability expert. Watch this video of an IDE for industrial automation (Eclipse 4diac IDE).

Evaluate how well the IDE supports this specific task:
TASK: A user needs to orient themselves in an unknown application. They must:
(i) Find the part of the application controlling a specific motor
(ii) Find all other motors and their locations
(iii) Follow an event connection to identify which part is triggered next

Focus on: How easy is it to navigate? Can users find what they're looking for? Is the hierarchy clear? Are search features available? Can users identify their current location?""",

    "task2_hierarchy": """You are a UX/usability expert. Watch this video of an IDE for industrial automation (Eclipse 4diac IDE).

Evaluate how well the IDE supports this specific task:
TASK: A user needs to create and manage hierarchies by:
- Grouping existing function blocks into a subapplication
- Naming it with a valid identifier
- Adding/removing blocks from the subapplication
- Verifying connections are maintained after grouping
- Flattening a subapplication (removing unnecessary grouping)

Focus on: How intuitive is the grouping mechanism? Are context menu options clear? Do connections update correctly? Is verification easy?""",

    "task3_library": """You are a UX/usability expert. Watch this video of an IDE for industrial automation (Eclipse 4diac IDE).

Evaluate how well the IDE supports this specific task:
TASK: A user needs to work with a type library:
- Save a created subapplication to the library for reuse
- Add an external file to the library
- Replace an instance with a new type while keeping connections

Focus on: How easy is it to save/load from the library? Are file system operations intuitive? Is type replacement straightforward?""",

    "task4_editing": """You are a UX/usability expert. Watch this video of an IDE for industrial automation (Eclipse 4diac IDE).

Evaluate how well the IDE supports editing tasks:
TASK: A user needs to:
- Convert a typed subapp to untyped
- Extend an interface with parameters
- Add function block instances from the library
- Edit and create connections
- Add constant parameters
- Identify variables in a structured data type

Focus on: How efficient is the editing workflow? Are there shortcuts? Is the interface responsive? Are structured data types easy to inspect?"""
}
