############################################################
## CSC 384, Intro to AI, University of Toronto.
## Assignment 3 Starter Code
## v1.0
##
############################################################

from collections import deque


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
    # csp.print_all()

    # Check all the constraints that contain the last assigned variable.
    for c in cons_list:
        # Focus on the constraints with one unassigned variable
        if c.get_num_unassigned_vars() == 1:
            # Get the variable
            var = c.get_unassigned_vars()[0]

            # Loop through all available values
            for v in var.cur_domain():
                var.assign(v)
                test_val = []
                # Check all assigned values if they satisify the constraint
                for test_var in c.get_scope():
                    test_val.append(test_var.get_assigned_value())
                if not c.check(test_val):
                    var.prune_value(v)
                    prune_list.append((var, v))
                var.unassign()

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
    prune_list = []
    cons_list = deque()
    # Check all constraints if the last assigned variable is None
    if last_assigned_var == None:
        for v in csp.get_all_vars():
            for c in csp.get_cons_with_var(v):
                cons_list.append((v, c))
    else:
        # Only check constraints of the last variable
        for c in csp.get_cons_with_var(last_assigned_var):
            cons_list.append((last_assigned_var, c))

    # Loop through the constraint queue
    while cons_list:
        c_v, c = cons_list.popleft()

        # Get all variables in the constraint
        vars = c.get_scope()
        for var in vars:

            # Do not try assigned variables or variables of the current constraint
            if var == c_v or var.is_assigned():
                continue

            if c.get_num_unassigned_vars() == 1:
                b = False
                # Check all `values in the variable's domain
                for v in var.cur_domain():
                    var.assign(v)
                    test_val = []

                    # Obtain all assigned values in all variables
                    for test_var in vars:
                        test_val.append(test_var.get_assigned_value())
                    # print(test_var, test_val)
                    # Check if the assignment satisify the constraints
                    if not c.check(test_val):
                        var.prune_value(v)
                        prune_list.append((var, v))

                        # If pruned any value, add constraint associated with the variable back
                        for constraint in csp.get_cons_with_var(var):
                            # print((var, constraint))
                            # print(constraint)
                            # Do not add the same connection back
                            if (var, constraint) not in cons_list:

                                # print((var, constraint))
                                cons_list.append((var, constraint))
                        b = True

                    var.unassign()
                #             if var.cur_domain_size() == 0:
                #                 b = True
                # if b:
                #     for constraint in csp.get_cons_with_var(var):
                #         if (var, constraint) not in cons_list:
                #             cons_list.append((var, constraint))

                # Check if any pruning occurred
                for var in vars:
                    if var.cur_domain_size() == 0:
                        return False, prune_list
    return True, prune_list


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
