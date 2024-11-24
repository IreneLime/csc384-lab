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

        for value in variable.domain():
            ordered_assign = list(assign)
            ordered_assign.insert(factor.get_scope().index(variable), value)
            total_prob += factor.get_value(ordered_assign)
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
    mul_v = 1
    var_list = []
    name = ""
    for f in factor_list:
        for v in f.values:
            mul_v *= v
        name += f.name + "_"
        var_list.append(f.get_scope())
    mul_factor = Factor(f"{name}normalized", var_list)
    mul_factor.values = mul_v
    return mul_factor
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
    with open(data_file, newline="") as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader, None)  # skip header row
        for row in reader:
            input_data.append(row)

    ### YOUR CODE HERE ###
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
    input_data = []
    with open("data/adult-test.csv", newline="") as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader, None)  # skip header row
        for row in reader:
            input_data.append(row)
    print(input_data)
    raise NotImplementedError


# # Main function to test restrict
# def main():
#     # Create variables
#     A = Variable("A", [1, 2])
#     B = Variable("B", ["x", "y"])
#     C = Variable("C", ["red", "blue"])

#     # Create a factor with scope [A, B, C]
#     factor = Factor("Factor_ABC", [A, B, C])
#     factor.add_values(
#         [
#             [1, "x", "red", 0.1],
#             [1, "x", "blue", 0.2],
#             [1, "y", "red", 0.3],
#             [1, "y", "blue", 0.4],
#             [2, "x", "red", 0.5],
#             [2, "x", "blue", 0.6],
#             [2, "y", "red", 0.7],
#             [2, "y", "blue", 0.8],
#         ]
#     )

#     print("Original Factor Values:")
#     print(factor.get_table())

#     ### Test restrict
#     # new_factor = restrict(factor, B, "x")

#     ### Test sum out
#     new_factor = sum_out(factor, C)

#     print("\nAfter operation:")
#     print(new_factor.get_table())


# # Run the main function
# if __name__ == "__main__":
#     main()
