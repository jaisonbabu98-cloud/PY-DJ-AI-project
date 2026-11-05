STEP_SYSTEM_PROMPT = """You are a patient mentor helping a beginner build a software project. Write a guide for ONE step of the build. Rules:
- Explain WHY each command or line of code is used, not just what to type.
- Use simple language and short paragraphs.
- Use Markdown. Put every command and all code in fenced code blocks.
- Cover only the current step. Do not describe other steps.
- Do not invent tools or packages. If something depends on the user's operating system, say so.
"""

def build_step_messages(project, step, previous_titles):
    done = "\n".join(f"- {title}" for title in previous_titles) or "- (none, this is the first step)"
    prompt = (
        f"Project name: {project.name}\n"
        f"Section: {step.get_section_display()}\n"
        f"Current step: {step.title}\n\n"
        f"Steps the user has already completed before this one:\n{done}\n\n"
        "Write the guide for the current step only."
    )
    return [{"role": "user", "content": prompt}]