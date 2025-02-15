############################################################
## CSC 384, Intro to AI, University of Toronto.
## Assignment 4 Starter Code
## v1.0
############################################################

from bnetbase import Variable, Factor, BN
import csv
from itertools import product
import sys


def normalize(factor):
    """
    Normalize the factor such that its values sum to 1.
    Do not modify the input factor.

    :param factor: a Factor object.
    :return: a new Factor object resulting from normalizing factor.
    """

    ### YOUR CODE HERE ###
    norm_values = []
    sum_factor_values = sum(factor.values)
    # Corner case: Division by 0
    if sum_factor_values == 0:
        return factor
    # Calculate normalized version for each value
    for v in factor.values:
        norm_values.append(v / sum_factor_values)

    norm_factor = Factor(f"Normalilze {factor.name}", factor.get_scope())
    norm_factor.values = norm_values
    return norm_factor

    raise NotImplementedError


def restrict(factor, variable, value):
    """
    Restrict a factor by assigning value to variable.
    Do not modify the input factor.

    :param factor: a Factor object.
    :param variable: the variable to restrict.
    :param value: the value to restrict the variable to
    :return: a new Factor object resulting from restricting variable to value.
             This new factor no longer has variable in it.
    """

    ### YOUR CODE HERE ###
    # Corner case: variable not in the scope of the factor
    if factor.get_variable(variable.name) == None:
        return factor

    # The new factor no longer has the restricted variable
    scope = [v for v in factor.get_scope() if v != variable]
    restrict_factor = Factor(f"Restrict {factor.name}", scope)
    # Get all domains of all variables
    all_domain = [v.domain() for v in scope]
    # Cartesian product of all variable combinations
    assigned_list = []
    for assign in product(*all_domain):
        # Order in the scope's order to obtain the prob from the factor's table
        ordered_assign = list(assign)
        ordered_assign.insert(factor.get_scope().index(variable), value)

        # Append to prob to the new table that does not contain variable
        assign = list(assign)
        assign.append(factor.get_value(ordered_assign))
        assigned_list.append(list(assign))

    # Add the new table to the new factor
    restrict_factor.add_values(assigned_list)
    return restrict_factor

    raise NotImplementedError


def sum_out(factor, variable):
    """
    Sum out a variable variable from factor factor.
    Do not modify the input factor.

    :param factor: a Factor object.
    :param variable: the variable to sum out.
    :return: a new Factor object resulting from summing out variable from the factor.
             This new factor no longer has variable in it.
    """

    ### YOUR CODE HERE ###
    # Corner case: variable not in the scope of the factor
    if factor == None:
        return None
    if factor.get_variable(variable.name) == None:
        return factor

    scope = [v for v in factor.get_scope() if v != variable]
    sum_out_factor = Factor(f"Sum out {factor.name}", scope)
    # Get all domains of all variables
    all_domain = [v.domain() for v in scope]
    # Cartesian product of all variable combinations
    assigned_list = []
    total_prob = 0
    for assign in product(*all_domain):
        # Order in the scope's order to obtain the prob from the factor's table
        # Sum up all probabilities with the given variable
        for value in variable.domain():
            ordered_assign = list(assign)
            ordered_assign.insert(factor.get_scope().index(variable), value)
            total_prob += factor.get_value(ordered_assign)

        # Summed out combinations have the total probability based on Sum Rule
        assign = list(assign)
        assign.append(total_prob)
        assigned_list.append(list(assign))
        total_prob = 0

    sum_out_factor.add_values(assigned_list)

    return sum_out_factor
    raise NotImplementedError


def multiply(factor_list):
    """
    Multiply a list of factors together.
    Do not modify any of the input factors.

    :param factor_list: a list of Factor objects.
    :return: a new Factor object resulting from multiplying all the factors in factor_list.
    """
    ### YOUR CODE HERE ###
    # Corner case:list is empty
    if not factor_list:
        return None
    multiply_factor_name = "Multiply"

    # Get all possible variables in the factor list
    all_variables = []
    for f in factor_list:
        multiply_factor_name += f" {f.name}"
        for var in f.get_scope():
            if var not in all_variables:
                all_variables.append(var)

    # Iterate through all combinations of values
    all_domain = [v.domain() for v in all_variables]
    assigned_list = []
    for assign in product(*all_domain):
        assign = list(assign)
        total_prob = 1

        # Multiply probabilities from the same value
        for f in factor_list:
            factor_assign = []
            for v in f.get_scope():
                factor_assign.append(assign[all_variables.index(v)])
            total_prob *= f.get_value(factor_assign)

        # Add the multiplied probabilities to the set of variables
        assign.append(total_prob)
        assigned_list.append(list(assign))

    # Create new factor
    multiply_factor = Factor(multiply_factor_name, all_variables)
    multiply_factor.add_values(assigned_list)
    return multiply_factor

    raise NotImplementedError


def ve(bayes_net, var_query, varlist_evidence):
    """
    Execute the variable elimination algorithm on the Bayesian network bayes_net
    to compute a distribution over the values of var_query given the
    evidence provided by varlist_evidence.

    :param bayes_net: a BN object.
    :param var_query: the query variable. we want to compute a distribution
                     over the values of the query variable.
    :param varlist_evidence: the evidence variables. Each evidence variable has
                         its evidence set to a value from its domain
                         using set_evidence.
    :return: a Factor object representing a distribution over the values
             of var_query. that is a list of numbers, one for every value
             in var_query's domain. These numbers sum to 1. The i-th number
             is the probability that var_query is equal to its i-th value given
             the settings of the evidence variables.

    """
    ### YOUR CODE HERE ###

    if var_query is None:
        var_query = bayes_net.variables()[0]

    # Eliminate the hidden variable
    hidden_var = []
    for var in bayes_net.variables():
        if (var != var_query) and (var not in varlist_evidence):
            hidden_var.append(var)

    # Restrict factors
    restricted_f = []
    for f in bayes_net.factors():
        restrict_f = f
        # Restrict each variable to its observed value
        for var in varlist_evidence:
            if var in restrict_f.get_scope():
                evid = var.get_evidence()

                restrict_f = restrict(restrict_f, var, evid)
        restricted_f.append(restrict_f)

    # When there is no hidden variable
    if not hidden_var:
        factor = multiply(restricted_f)
        return normalize(factor)

    # When there are hidden variables
    final_restricted_f = restricted_f
    for var in hidden_var:
        factor = []
        restricted_f = final_restricted_f
        final_restricted_f = []
        for f in restricted_f:
            if var in f.get_scope():
                factor.append(f)
            else:
                final_restricted_f.append(f)
        # Multiply to produce factor
        mul_f = multiply(factor)

        # Sum out hidden variable from the factor
        sum_out_f = sum_out(mul_f, var)

        final_restricted_f.append(sum_out_f)
    factor = multiply(final_restricted_f)
    return normalize(factor)


    raise NotImplementedError


## The order of these domains is consistent with the order of the columns in the data set.
salary_variable_domains = {
    "Work": ["Not Working", "Government", "Private", "Self-emp"],
    "Education": [
        "<Gr12",
        "HS-Graduate",
        "Associate",
        "Professional",
        "Bachelors",
        "Masters",
        "Doctorate",
    ],
    "Occupation": [
        "Admin",
        "Military",
        "Manual Labour",
        "Office Labour",
        "Service",
        "Professional",
    ],
    "MaritalStatus": ["Not-Married", "Married", "Separated", "Widowed"],
    "Relationship": [
        "Wife",
        "Own-child",
        "Husband",
        "Not-in-family",
        "Other-relative",
        "Unmarried",
    ],
    "Race": ["White", "Black", "Asian-Pac-Islander", "Amer-Indian-Eskimo", "Other"],
    "Gender": ["Male", "Female"],
    "Country": [
        "North-America",
        "South-America",
        "Europe",
        "Asia",
        "Middle-East",
        "Carribean",
    ],
    "Salary": ["<50K", ">=50K"],
}

salary_variable = Variable("Salary", ["<50K", ">=50K"])


def naive_bayes_model(
    data_file, variable_domains=salary_variable_domains, class_var=salary_variable
):
    """
    NaiveBayesModel returns a BN that is a Naive Bayes model that represents
    the joint distribution of value assignments to variables in the given dataset.

    Remember a Naive Bayes model assumes P(X1, X2,.... XN, Class) can be represented as
    P(X1|Class) * P(X2|Class) * .... * P(XN|Class) * P(Class).

    When you generated your Bayes Net, assume that the values in the SALARY column of
    the dataset are the CLASS that we want to predict.

    Please name the factors as follows. If you don't follow these naming conventions, you will fail our tests.
    - The name of the Salary factor should be called "Salary" without the quotation marks.
    - The name of any other factor should be called "VariableName,Salary" without the quotation marks.
      For example, the factor for Education should be called "Education,Salary".

    @return a BN that is a Naive Bayes model and which represents the given data set.
    """
    ### READ IN THE DATA
    input_data = []
    with open(data_file, newline="", encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader, None)  # skip header row
        header = [header.strip() for header in headers] # Create header list without encoding
        for row in reader:
            input_data.append(row)

    ### YOUR CODE HERE ###
    var_list = list(variable_domains.keys())
    salary_idx = var_list.index(class_var.name)

    factor_list = []
    variable_list = []

    # Create a factor with only the class variable
    class_factor = Factor(class_var.name, [class_var])
    factor_element = [[d] for d in class_var.domain()]
    all_class_elements = []
    # Get all class variable occurrences in a list
    for r in input_data:
        all_class_elements.append(r[header.index(class_var.name)])
    # Calculate the probabilities of each class variable domain
    total_count = len(all_class_elements)
    for i, d in enumerate(class_var.domain()):
        factor_element[i].append(all_class_elements.count(d) / total_count)
    class_factor.add_values(factor_element)
    variable_list.append(class_var)
    factor_list.append(class_factor)

    # Check all variables
    for variable in var_list:
        if variable == class_var.name:
            continue

        # Create variables
        dependent_variable = Variable(f"{variable},{class_var.name}", variable_domains[variable])
        variable_list.append(dependent_variable)

        # Create a factor
        factor = Factor(f"{variable},{class_var.name}", [dependent_variable, class_var])

        # Obtain all combinations of dependent and class variables
        total_factor_element = []
        for var in class_var.domain():
            factor_element = list(product(variable_domains[variable], [var]))
            factor_count = [0] * len(factor_element)

            # Count the number of occurrences of the variable from each line
            for r in input_data:
                # Note: there may be mismatch in the csv order and input variable list order
                if tuple([r[header.index(variable)], r[salary_idx]]) in factor_element:
                    factor_index = factor_element.index(tuple([r[header.index(variable)], r[salary_idx]]))
                    factor_count[factor_index] += 1

            # Calculate the probability distribution and add them as values to the combinations
            total_count = sum(factor_count)
            if total_count != 0:
                factor_count = [count / total_count for count in factor_count]
            for j in range(len(factor_element)):
                factor_element[j] = list(factor_element[j])
                factor_element[j].append(factor_count[j])
                total_factor_element.append(factor_element[j])

        factor.add_values(total_factor_element)
        factor_list.append(factor)

    bayes_net = BN(f"NaiveBayes_{class_var.name}", variable_list, factor_list)
    return bayes_net

    raise NotImplementedError



def explore(bayes_net, question):
    """
    Return a probability given a Naive Bayes Model and a question number 1-6.

    The questions are below:
    1. What percentage of the women in the test data set does our model predict having a salary >= $50K?
    2. What percentage of the men in the test data set does our model predict having a salary >= $50K?
    3. What percentage of the women in the test data set satisfies the condition: P(S=">=$50K"|Evidence) is strictly greater than P(S=">=$50K"|Evidence,Gender)?
    4. What percentage of the men in the test data set satisfies the condition: P(S=">=$50K"|Evidence) is strictly greater than P(S=">=$50K"|Evidence,Gender)?
    5. What percentage of the women in the test data set with a predicted salary over $50K (P(Salary=">=$50K"|E) > 0.5) have an actual salary over $50K?
    6. What percentage of the men in the test data set with a predicted salary over $50K (P(Salary=">=$50K"|E) > 0.5) have an actual salary over $50K?

    @return a percentage (between 0 and 100)
    """
    ### YOUR CODE HERE ###
    if question not in [1, 2, 3, 4, 5, 6]:
        return 0
    input_data = []
    with open('data/adult-test.csv', newline="", encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader, None)  # skip header row
        header = [header.strip() for header in headers] # Create header list without encoding
        for row in reader:
            input_data.append(row)

    # Make a dictionary with key = variable name and value = class Variable
    var_dict = {}
    for var in header:
        if var != 'Salary':
            var_dict[var] = bayes_net.get_variable(f"{var},Salary")
        else:
            var_dict[var] = bayes_net.get_variable(var)

    gender_idx = header.index('Gender')
    salary_idx = header.index('Salary')
    work_idx = header.index('Work')
    education_idx = header.index('Education')
    occupation_idx = header.index('Occupation')
    relationship_idx = header.index('Relationship')
    salary_entry = '>=50K'
    pred = 0
    count = 0
    if question in [1, 2, 5, 6]:
        for r in input_data:
            if (r[gender_idx] != 'Female' and question in [1, 5]) or (r[gender_idx] != 'Male' and question in [2, 6]):
                continue

            evid_list = []
            # Create evidence based on the current value of the row
            for i, data in enumerate(r):
                if i in [work_idx, education_idx, occupation_idx, relationship_idx]:
                    var_dict[header[i]].set_evidence(data)
                    evid_list.append(var_dict[header[i]])

            ret = ve(bayes_net, var_dict["Salary"], evid_list)
            # Record when the model predicts >=50K
            if ret.get_value([salary_entry]) > 0.5:
                # Questions 1 and 2: Gender predicted with salary >= $50K
                if question in [1, 2]:
                    pred += 1
                # Questions 5 and 6: Gender predicted with (P(Salary=">=$50K"|E) > 0.5) have an actual salary over $50K
                elif question in [5, 6]:
                    count += 1
                    if r[salary_idx] == salary_entry:
                        pred += 1
            if question in [1, 2]:
                count += 1
    elif question in [3, 4]:
        for r in input_data:
            if (r[gender_idx] != 'Female' and question == 3) or (r[gender_idx] != 'Male' and question == 4):
                continue

            evid_list = []
            for i, data in enumerate(r):
                if i in [work_idx, education_idx, occupation_idx, relationship_idx]:
                    var_dict[header[i]].set_evidence(data)
                    evid_list.append(var_dict[header[i]])

            # P(S|Evidence)
            evid_ve = ve(bayes_net, var_dict["Salary"], evid_list)

            # P(S|Evidence,Gender)
            var_dict[header[gender_idx]].set_evidence(r[gender_idx])
            evid_list.append(var_dict[header[gender_idx]])
            evid_gender_ve = ve(bayes_net, var_dict["Salary"], evid_list)

            if evid_ve.get_value([salary_entry]) > evid_gender_ve.get_value([salary_entry]):
                pred += 1
            count += 1

    if count == 0:
        return 0
    return (pred / count) * 100


    raise NotImplementedError