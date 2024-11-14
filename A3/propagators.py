############################################################
## CSC 384, Intro to AI, University of Toronto.
## Assignment 3 Starter Code
## v1.0
##
############################################################


def prop_FC(csp, last_assigned_var=None):
    """
    This is a propagator to perform forward checking.

    First, collect all the relevant constraints.
    If the last assigned variable is None, then no variable has been assigned
    and we are performing propagation before search starts.
    In this case, we will check all the constraints.
    Otherwise, we will only check constraints involving the last assigned variable.

    Among all the relevant constraints, focus on the constraints with one unassigned variable.
    Consider every value in the unassigned variable's domain, if the value violates
    any constraint, prune the value.

    :param csp: The CSP problem
    :type csp: CSP

    :param last_assigned_var: The last variable assigned before propagation.
        None if no variable has been assigned yet (that is, we are performing
        propagation before search starts).
    :type last_assigned_var: Variable

    :returns: The boolean indicates whether forward checking is successful.
        The boolean is False if at least one domain becomes empty after forward checking.
        The boolean is True otherwise.
        Also returns a list of variable and value pairs pruned.
    :rtype: boolean, List[(Variable, Value)]
    """
    prune_list = []
    cons_list = []
    # Check all constraints if the last assigned variable is None
    if last_assigned_var == None:
        cons_list = csp.get_all_cons()
    else:
        cons_list = csp.get_cons_with_var(last_assigned_var)

    # Check all the constraints that contain the last assigned variable.
    for c in cons_list:
        if c.get_num_unassigned_vars() == 1:
            # Get the unassigned variable
            print(c.get_scope())
            var = c.get_scope()[0]

            # # Collect the values from the unassigned_var's current domain
            # values_to_prune = []
            # for value in unassigned_var.cur_domain():
            #     # Check if there's an assignment for all variables in the scope satisfying the constraint
            #     assigned_values = [var.get_assigned_value() if var.is_assigned() else value
            #                        for var in con.get_scope()]
            #     if not con.check(assigned_values):
            #         values_to_prune.append(value)

            # # Prune values and add them to prunings list
            # for value in values_to_prune:
            #     unassigned_var.prune_value(value)
            #     prunings.append((unassigned_var, value))

            # for val in var.cur_domain():
            #     assigned_val = []
            #     if var.is_assigned():
            #         assigned_val = var.get_assigned_value()
            #     else:
            #         for v in c.get_scope():
            #             assigned_val.append(v)
            #     if not c.check(assigned_val):
            #         var.prune_value(val)
            #         prune_list.append((var, val))

            # Prune the value that violates the constraint
            if not c.check(var.cur_domain()):
                for val in var.cur_domain():
                    print(val)

                    var.prune_value(val)
                    prune_list.append((var, val))
            if var.cur_domain_size() == 0:
                return False, prune_list

    return True, prune_list


def prop_AC3(csp, last_assigned_var=None):
    """
    This is a propagator to perform the AC-3 algorithm.

    Keep track of all the constraints in a queue (list).
    If the last_assigned_var is not None, then we only need to
    consider constraints that involve the last assigned variable.

    For each constraint, consider every variable in the constraint and
    every value in the variable's domain.
    For each variable and value pair, prune it if it is not part of
    a satisfying assignment for the constraint.
    Finally, if we have pruned any value for a variable,
    add other constraints involving the variable back into the queue.

    :param csp: The CSP problem
    :type csp: CSP

    :param last_assigned_var: The last variable assigned before propagation.
        None if no variable has been assigned yet (that is, we are performing
        propagation before search starts).
    :type last_assigned_var: Variable

    :returns: a boolean indicating if the current assignment satisifes
        all the constraints and a list of variable and value pairs pruned.
    :rtype: boolean, List[(Variable, Value)]
    """

    raise NotImplementedError


def ord_mrv(csp):
    """
    Implement the Minimum Remaining Values (MRV) heuristic.
    Choose the next variable to assign based on MRV.

    If there is a tie, we will choose the first variable.

    :param csp: A CSP problem
    :type csp: CSP

    :returns: the next variable to assign based on MRV

    """

    raise NotImplementedError


###############################################################################
# Do not modify the prop_BT function below
###############################################################################


def prop_BT(csp, last_assigned_var=None):
    """
    This is a basic propagator for plain backtracking search.

    Check if the current assignment satisfies all the constraints.
    Note that we only need to check all the fully instantiated constraints
    that contain the last assigned variable.

    :param csp: The CSP problem
    :type csp: CSP

    :param last_assigned_var: The last variable assigned before propagation.
        None if no variable has been assigned yet (that is, we are performing
        propagation before search starts).
    :type last_assigned_var: Variable

    :returns: a boolean indicating if the current assignment satisifes all the constraints
        and a list of variable and value pairs pruned.
    :rtype: boolean, List[(Variable, Value)]

    """

    # If we haven't assigned any variable yet, return true.
    if not last_assigned_var:
        return True, []

    # Check all the constraints that contain the last assigned variable.
    for c in csp.get_cons_with_var(last_assigned_var):

        # All the variables in the constraint have been assigned.
        if c.get_num_unassigned_vars() == 0:

            # get the variables
            vars = c.get_scope()

            # get the list of values
            vals = []
            for var in vars:  #
                vals.append(var.get_assigned_value())

            # check if the constraint is satisfied
            if not c.check(vals):
                return False, []

    return True, []
