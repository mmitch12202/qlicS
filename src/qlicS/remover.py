# Very similar to pylion's sim.remove()
def remove_by_uid(s, uid):
    code = ["\n# Deleting a fix by uid", f"unfix {uid}\n"]
    s.append({"code": code, "type": "command"})

# TODO unit tests
def delete_atoms_by_uid(s, uid):
    code = ["\n# Deleting an atom group by uid", f"delete_atoms group {uid}\n"]
    s.append({"code": code})