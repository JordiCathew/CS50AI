import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence = []
    labels = []
    months = {
        'Jan': 0,
        'Feb': 1,
        'Mar': 2,
        'Apr': 3,
        'May': 4,
        'June': 5,
        'Jul': 6,
        'Aug': 7,
        'Sep': 8,
        'Oct': 9,
        'Nov': 10,
        'Dec': 11
    }

    with open("shopping.csv") as f:
        reader = csv.reader(f)
        # Skip first row
        next(reader)

        for row in reader:
            # This list will store all the values for each row
            list_values = [None for i in range(17)]              
            for column, value in enumerate(row):
                # Cases int values 
                if (column == 0 or column == 2 or column == 4 or
                   column == 11 or column == 12 or column == 13 or
                   column == 14):
                   list_values[column] = int(value)
                # Case months
                elif (column == 10):
                    # More efficient that using if else clauses.
                    list_values[column] = months.get(value)
                # Case VisitorType
                elif (column == 15):
                    list_values[column] = 1 if value == "Returning_Visitor" else 0
                #Case Weekend
                elif (column == 16):
                    list_values[column] = 1 if value == "TRUE" else 0
                # This is the column labels, we don't touch it here.
                elif column == 17:
                    break
                # All the other are floating points types of data
                else:
                    list_values[column] = float(value)

            # At the end of each row we append all to the evidence and the labels.
            evidence.append(list_values)
            labels.append(1 if row[17] == "TRUE" else 0)
        all_data = (evidence, labels)
        #print(evidence[0], labels[0])
    return all_data


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    sensitivity = 0.0
    count_sensitivity = 0
    specificity = 0.0
    count_specificity = 0
    for value1, value2 in zip(labels, predictions):
        if value1 == value2:
            if value1 == 1:
                count_sensitivity += 1
            else:
                count_specificity += 1
    
    sensitivity = count_sensitivity / labels.count(1)
    specificity = count_specificity / labels.count(0)
    sensitivity_and_specificity = (sensitivity, specificity)

    return sensitivity_and_specificity


if __name__ == "__main__":
    main()
