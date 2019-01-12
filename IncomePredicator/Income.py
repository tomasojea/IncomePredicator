__author__ = 'Tomás Ojea'
import httplib2
"""
1. Create training set from data
2. Create classifier using training data set to determine separator values for each attribute
3. Create test data set
4. Use classifier to classify data in test set while maintaining accuracy score
"""

h = httplib2.Http(".cache")
resp, content = h.request("http://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data", "GET")
count = 0
conv = content.decode("utf-8")
split = conv.split('\n')

records_above = []
records_below = []
workplace = []
marital_status = []
occupation = []
relationship = []
race = []
sex = []
dictionary_discrete = {
    "Positives_Records": {},
    "Negatives_Records": {}
}
numeric_attributes = {
    "Positives_Records": {0: 0, 4: 0, 10: 0, 11: 0, 12: 0},
    "Negatives_Records": {0: 0, 4: 0, 10: 0, 11: 0, 12: 0}
}
test_list = []


def create_data():
    """
    Checks for records below and above.
    Afterwards makes an averages of each and appends it into the data list(test_list).
    :return: data list to be split it into training and testing lists.
    """
    positive_records = 0
    negative_records = 0
    for line in split:
        if len(line) == 0:
            break
        line_split = line.split(",")
        for line_index, none_key in enumerate(line_split, start=0):
            if line_index == 2 or line_index == 3 or line_index == 13:
                line_split[line_index] = None
        for l_index, n_key in enumerate(line_split, start=0):
            if n_key is None:
                continue
            else:
                try:
                    line_split[l_index] = int(n_key)
                except ValueError:
                    line_split[l_index] = n_key
        if " >50K" in line:
            # Counting positives records for each numeric and discrete attribute.
            positive_records += 1
            for l_index, n_key in enumerate(line_split, start=0):
                if l_index in [0, 4, 10, 11, 12]:
                    numeric_attributes["Positives_Records"][l_index] += n_key
                elif l_index in [1, 5, 6, 7, 8, 9] and n_key not in dictionary_discrete:
                    dictionary_discrete["Positives_Records"][n_key] = 1
                elif l_index in [1, 5, 6, 7, 8, 9] and n_key in dictionary_discrete:
                    dictionary_discrete["Positives_Records"][n_key] += 1
                else:
                    pass
        else:
            # Counting negative records for each numeric and discrete attribute.
            negative_records += 1
            for l_index, n_key in enumerate(line_split, start=0):
                if l_index in [0, 4, 10, 11, 12]:
                    numeric_attributes["Negatives_Records"][l_index] += n_key
                elif l_index in [1, 5, 6, 7, 8, 9] and n_key not in dictionary_discrete:
                    dictionary_discrete["Negatives_Records"][n_key] = 1
                elif l_index in [1, 5, 6, 7, 8, 9] and n_key in dictionary_discrete:
                    dictionary_discrete["Negatives_Records"][n_key] += 1
                else:
                    pass
        test_list.append(line_split) # Data list
    # Making an average of positive and negatives for discrete attributes.
    for record in test_list:
        pos = positive_records
        neg = negative_records
        if " >50K" in record:
            for index,key in enumerate(record, start=0):
                if index in [1, 5, 6, 7, 8, 9]:
                    record[index] = dictionary_discrete["Positives_Records"][key] / pos
                elif index in [0, 4, 10, 11, 12]:
                    record[index] = numeric_attributes["Positives_Records"][index] / pos
        else:
            for index, key in enumerate(record, start=0):
                if index in [1, 5, 6, 7, 8, 9]:
                    record[index] = dictionary_discrete["Negatives_Records"][key] / neg
                elif index in [0, 4, 10, 11, 12]:
                    record[index] = numeric_attributes["Negatives_Records"][index] / neg
    return test_list


def create_classifier(tr_list):
    under = 0
    above = 0
    for record in tr_list:
        if " >50K" in record:
            above += 1
            records_above.append(record)
        else:
            under += 1
            records_below.append(record)

    avg_below = [sum(x) / under if isinstance(x[0], int) else x[0] for x in zip(*records_below)]
    avg_above = [sum(x) / above if isinstance(x[0], int) else x[0] for x in zip(*records_above)]
    classifier_list = []
    for i in range(14):
        if records_above[0][i] is not None and records_below[0][i] is not None:
            classifier_list.append((avg_above[i] + avg_below[i]) / 2)
    return classifier_list


def create_test(te_list, midpoint):

    result_list = []
    under50_count2 = 0
    over50_count2 = 0
    for row in te_list:
        under50_count = 0
        over50_count = 0
        under_over_50k_string = row[-1]
        # for each attribute of the test_list
        for index in range(14):
            try:
                # if the attribute is greater than the average
                if row[index] > midpoint[index]:
                    # print(classifier_list[row[index]])
                    # add to the over50
                    over50_count += 1
                else:
                    # else add to the under50
                    under50_count += 1
                    # print(classifier_list[row[index]])
            except Exception as e:
                #print(e) #"unorderable types: NoneType() > NoneType()"
                continue
        # below replaces the larger number with the string "Under 50K " or "Over 50K "
        if under50_count > over50_count:
            under50_count = "Under 50K "
            over50_count = ""
            # below adds one to the under50 counter
            under50_count2 += 1
        else:
            over50_count = "Over 50K "
            under50_count = ""
            # below adds one to the over50 counter
            over50_count2 += 1
        # creates list with over or under 50k and the classifiers predictions
        results = (["Actual : " + under_over_50k_string, "Classifiers prediction = ", under50_count, over50_count])
        result_list.append(results)
    # prints out whether the row was over or under 50K and the classifiers predictions
    print("\n")
    for line in result_list:
        print("Actual & Classifiers prediction : ", line)

    over50actual = 0
    under50actual = 0

    # loops through the test list and counts the number of over and under $50,000.
    for row in te_list:
        if " <=50K" in row:
            under50actual += 1
        elif " >50K" in row:
            over50actual += 1
        else:
            pass
    # Prints out the number people under $50,000
    print("Total number people under $50,000 : ", under50actual)
    # Prints out the number people the classifier predicts to be under $50,000
    print("Total number people under $50,000 (classifiers prediction) : ", under50_count2)
    # Prints out the number people over $50,000
    print("Total number people over $50,000 :  ", over50actual)
    # Prints out the number people the classifier predicts to be over $50,000
    print("Total number people over $50,000 (classifiers prediction) :  ", over50_count2)
    # Prints classifiers accuracy by dividing the actual over 50 by the classifiers prediction of over 50
    # and then multiplying it by 100
    print("The classifier is %.2f %%" % (under50actual / under50_count2 * 100), "accurate.")


def main():
    data_list = create_data()
    training_list = data_list[:int(len(data_list) * 75 / 100)]
    midpoints = create_classifier(training_list)
    te_list = data_list[int(len(data_list) * 75 / 100):]
    create_test(te_list, midpoints)


if __name__ == '__main__':  # checks if there is main and starts the program in the main function.
    main()




