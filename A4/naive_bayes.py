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
    # Restrict factors
    restricted_f = []
    for f in bayes_net.factors():
        # Restrict each variable to its observed value
        for var in varlist_evidence:
            evid = var.get_evidence()
            restricted_f.append(restrict(f, var, evid))

    # Eliminate the hidden variable
    hidden_var = []
    for var in bayes_net.variables():
        if (var != var_query) and (var not in varlist_evidence):
            hidden_var.append(var)
    print(hidden_var)
    if not hidden_var:
        factor = multiply(restricted_f)
        return normalize(factor)

    final_restricted_f = []
    for var in hidden_var:
        print(var)
        # Multiply to produce factor
        f_with_hidden = []
        for f in restricted_f:
            if var in f.get_scope():
                f_with_hidden.append(f)

        mul_f = multiply(f_with_hidden)

        # Sum out hidden variable from the factor
        print("sum")
        sum_out_f = sum_out(mul_f, var)
        print(sum_out_f)
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
def main():
    #     # Create variables
    A = Variable("A", [0, 1])
    B = Variable("B", [0, 1])
    C = Variable("C", ["red", "blue"])

    #     # Test restrict and sum out
    #     """
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
    #     new_factor = restrict(factor, B, "x")

    #     ### Test sum out
    #     new_factor = sum_out(factor, C)

    #     print("\nAfter operation:")
    #     print(new_factor.get_table())
    #     """

    #     # Test multiply
    #     # Create the first factor with scope [A, B]
    #     factor1 = Factor("Factor_AB", [A, B])
    #     factor1.add_values(
    #         [
    #             [1, "x", 0.5],
    #             [1, "y", 0.3],
    #             [2, "x", 0.7],
    #             [2, "y", 0.9],
    #         ]
    #     )

    #     # Create the second factor with scope [B, C]
    #     factor2 = Factor("Factor_BC", [B, C])
    #     factor2.add_values(
    #         [
    #             ["x", "red", 0.6],
    #             ["x", "blue", 0.8],
    #             ["y", "red", 0.4],
    #             ["y", "blue", 0.2],
    #         ]
    #     )

    #     # Create the third factor with scope [C]
    #     factor3 = Factor("Factor_C", [C])
    #     factor3.add_values(
    #         [
    #             ["red", 0.9],
    #             ["blue", 0.7],
    #         ]
    #     )

    #     # Print original factors
    #     print("Factor 1:")
    #     print(factor1.get_table())
    #     print("\nFactor 2:")
    #     print(factor2.get_table())
    #     print("\nFactor 3:")
    #     print(factor3.get_table())

    #     # Multiply the factors
    #     multiplied_factor = multiply([factor1, factor2, factor3])
    #     print("\nResulting Factor After Multiplication:")
    #     print(multiplied_factor.get_table())
    # Define Variables
    # A = Variable("A", [0, 1])
    # B = Variable("B", [0, 1])

    # Define Factors
    # Define Factors
    factor_A = Factor("P(A)", [A])
    factor_A.add_values([[0, 0.6], [1, 0.4]])

    factor_C_given_A = Factor("P(C|A)", [A, C])
    factor_C_given_A.add_values(
        [
            [0, "red", 0.7],
            [0, "blue", 0.3],  # P(C|A=0)
            [1, "red", 0.4],
            [1, "blue", 0.6],  # P(C|A=1)
        ]
    )

    factor_B_given_C = Factor("P(B|C)", [C, B])
    factor_B_given_C.add_values(
        [
            ["red", 0, 0.9],
            ["red", 1, 0.1],  # P(B|C=red)
            ["blue", 0, 0.2],
            ["blue", 1, 0.8],  # P(B|C=blue)
        ]
    )

    # Define Bayesian Network
    bayes_net = BN(
        "Hidden Variable BN", [A, B, C], [factor_A, factor_C_given_A, factor_B_given_C]
    )

    # Evidence and Query
    evidence = {A: 0}  # Evidence: A=0
    query_variable = B  # Query: Compute P(B | A=0)

    # Run variable elimination
    result = ve(bayes_net, query_variable, evidence)

    # Expected Result
    expected_factor = Factor("P(B|A=0)", [B])
    expected_factor.add_values([[0, 0.8], [1, 0.2]])

    # Validate Results
    print("Testing VE function...")

    # Check the scope
    if result.get_scope() != [B]:
        print(
            f"Test Failed: Scope should only contain the query variable B, got {result.get_scope()}"
        )
        return

    # Check the values
    expected_values = {0: 0.8, 1: 0.2}
    passed = True
    for value in B.domain():
        actual = result.get_value([value])
        expected = expected_values[value]
        if abs(actual - expected) >= 0.001:
            print(
                f"Test Failed: Incorrect probability for B={value}: expected {expected}, got {actual}"
            )
            passed = False

    if passed:
        print("All tests passed for VE!")


# Run the main function
if __name__ == "__main__":
    main()
