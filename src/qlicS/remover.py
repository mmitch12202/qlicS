# Very similar to pylion's sim.remove()
def remove_by_uid(s, uid):
    """
    Removes a simulation fix by its unique identifier (UID).

    This function constructs a command to unfix a specified simulation component 
    identified by its UID and appends this command to the provided simulation 
    object. It facilitates the management of simulation components by allowing 
    for the removal of fixes during the simulation process.

    Args:
        s (Simulation): The simulation object to which the unfix command will be appended.
        uid (str): The unique identifier of the fix to be removed.

    Returns:
        None: This function does not return a value; it modifies the simulation 
        object directly.
    """

    code = ["\n# Deleting a fix by uid", f"unfix {uid}\n"]
    s.append({"code": code, "type": "command"})


# TODO unit tests
def delete_atoms_by_uid(s, uid):
    """
    Deletes a group of atoms from the simulation by their unique identifier (UID).

    This function constructs a command to delete a specified group of atoms identified 
    by its UID and appends this command to the provided simulation object. It allows 
    for the effective management of atom groups within the simulation environment.

    Args:
        s (Simulation): The simulation object to which the delete command will be appended.
        uid (str): The unique identifier of the atom group to be deleted.

    Returns:
        None: This function does not return a value; it modifies the simulation 
        object directly.
    """

    code = ["\n# Deleting an atom group by uid", f"delete_atoms group {uid}\n"]
    s.append({"code": code})
