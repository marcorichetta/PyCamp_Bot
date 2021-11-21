import json

from pycamp_bot.models import Project, Slot, Vote

def  export_db_2_json():
    projects = Project.select()

    result = {"projects": {}, "responsable_available_slots": {}}

    available_slots = [slot.code for slot in Slot.select()]

    available_slots = [
        "A1", "A2", "A3", "A4",
        "B1", "B2", "B3", "B4", "B5", "B6", "B7",
    ]
    result["available_slots"] = available_slots
    all_responsables = []


    for project in projects:
        votes = list(Vote.select().where(Vote.project == project, Vote.interest))
        # responsables = list(ProjectOwner.select().where(ProjectOwner.project == project))
        # responsables = [responsable.username for responsable in responsables]
        responsables = [project.owner.username]
        if project.owner.username not in all_responsables:
            all_responsables.append(project.owner.username)
        votes_users = set([v.pycampista.username for v in votes])
        result["projects"][project.name] = {
            "priority_slots": [],
            "difficult_level": project.difficult_level,
            "responsables": responsables,
            "votes": list(votes_users),
            "theme": project.topic,
        }


    for responsable in all_responsables:
        result["responsable_available_slots"][responsable] = available_slots

    # with open('cualquiera.json', 'w') as fjson:
    #     json.dump(result, fjson, indent=2)

    return result