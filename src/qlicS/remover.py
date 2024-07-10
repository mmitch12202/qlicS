# Very similar to pylion's sim.remove()
def remove_by_uid(s, uid):
    code = ["\n# Deleting a fix by uid", f"unfix {uid}\n"]
    s.append({"code": code, "type": "command"})
