import httplib2
from numbers import Number
# Imported numbers to be used when summing up the data.

PERCENT = 75  # This 75 will be used to split the data into the training/classifier set and the test set.
DATA_URL = "http://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data"

# First count the records below and under and the atributtes below and under inside  "for row in fh:" then
#  loops through the items and divides them by either the under or over list counter. The the ts_list is used for
# check the result of the classifier.

def create_data(DATA_URL):

    #Pulls in the data. Then cleans, sorts and then returns the list.

    ts_list = []
    working_class = {}
    marital_status = {}
    occupation = {}
    relationship = {}
    race = {}
    sex = {}
    under_list = 0
    over_list = 0

    # Pulls in the data, saves it in a folder called .cache and splits the data on every line.
    h = httplib2.Http(".cache")
    headers, fh = h.request(DATA_URL)
    fh = fh.decode().split("\n")

    # Loop through each row and strips away the the blank spaces.
    # Split the data on the comma's(the data is in CSV format(Comma Separate Values))
    # Get the int values for rows 0,1,4,10,11,12 and give rows 2,3,13 a None value
    # Checks if each item is in the dictionary, if it's there it adds one to it, if it's not it adds it the dictionary
    # it also adds one to the under and over list counters.
    for row in fh:

        try:
            row = row.strip("")
            row = row.split(",")
            row[0] = int(row[0])
            row[2] = None
            row[3] = None
            row[4] = int(row[4])
            row[10] = int(row[10])
            row[11] = int(row[11])
            row[12] = int(row[12])
            row[13] = None

            if row[-1].strip(" ") == "<=50K":
                under_list += 1
                if row[1] in working_class:
                    working_class[row[1]] += 1
                else:
                    working_class[row[1]] = 1
                if row[5] in marital_status:
                    marital_status[row[5]] += 1
                else:
                    marital_status[row[5]] = 1
                if row[6] in occupation:
                    occupation[row[6]] += 1
                else:
                    occupation[row[6]] = 1
                if row[7] in relationship:
                    relationship[row[7]] += 1
                else:
                    relationship[row[7]] = 1
                if row[8] in race:
                    race[row[8]] += 1
                else:
                    race[row[8]] = 1
                if row[9] in sex:
                    sex[row[9]] += 1
                else:
                    sex[row[9]] = 1

            else:
                over_list += 1
                if row[1] in working_class:
                    working_class[row[1]] += 1
                else:
                    working_class[row[1]] = 1
                if row[5] in marital_status:
                    marital_status[row[5]] += 1
                else:
                    marital_status[row[5]] = 1
                if row[6] in occupation:
                    occupation[row[6]] += 1
                else:
                    occupation[row[6]] = 1
                if row[7] in relationship:
                    relationship[row[7]] += 1
                else:
                    relationship[row[7]] = 1
                if row[8] in race:
                    race[row[8]] += 1
                else:
                    race[row[8]] = 1
                if row[9] in sex:
                    sex[row[9]] += 1
                else:
                    sex[row[9]] = 1

        # if there is data it can't read it prints out the line, throws it away and continues to the next one.
        except ValueError as v:
            print(row[0], v)
            continue

        # appends the ts_list
        ts_list.append(row)

    # loops through the items and divides them by either the under or over list counter.
    for row in ts_list:
        if row[-1].lstrip(" ") == "<=50K":

            row[1] = working_class[row[1]]/under_list
            row[5] = marital_status[row[5]]/under_list
            row[6] = occupation[row[6]]/under_list
            row[7] = relationship[row[7]]/under_list
            row[8] = race[row[8]]/under_list
            row[9] = sex[row[9]]/under_list

        elif row[-1].lstrip(" ") == ">50K":
            row[1] = working_class[row[1]]/over_list
            row[5] = marital_status[row[5]]/over_list
            row[6] = occupation[row[6]]/over_list
            row[7] = relationship[row[7]]/over_list
            row[8] = race[row[8]]/over_list
            row[9] = sex[row[9]]/over_list

    else:
        pass
    # returns the cleaned data

    print(*ts_list,sep="\n")
    return ts_list




def create_classifier(training_list):
    # Takes in 75% of the data.
    # Creates two list, an over list and an under list. These contain the average for both lists.
    # Creates a classifier_list by summing up the value's in the under and over list and dividing by two.
    # The classifier_list is returned and used to classify the test list

    under__list = []
    over__list = []
    under_num = 0
    over__num = 0
    for row in training_list:
        if row[-1].lstrip(" ") == "<=50K":

            under_num += 1
            under__list.append(row)

        elif row[-1].lstrip(" ") == ">50K":
            over__num += 1
            over__list.append(row)

        else:
            pass

    # The below conditional expressions checks for the numbers in the list and adds them
    # together,  otherwise it leaves it as it was,  a None or string.
    under__list = [sum(x)/under_num if isinstance(x[0], Number) else x[0] for x in zip(*under__list)]
    over__list = [sum(x)/over__num if isinstance(x[0], Number) else x[0] for x in zip(*over__list)]
    # adds the elements the the under and over list an divides them by two.
    classifier_list = [sum(x)/2 if isinstance(x[0], Number) else x[0] for x in zip(over__list, under__list)]

    # Prints a line gap and then prints out the under, over and classifier lists
    print("\n")
    print("Under list :", under__list)
    print("Over list :", over__list)
    print("Average list :", classifier_list)

    #returns the classifier list
    return classifier_list


create_data(DATA_URL)

data_list = create_data(DATA_URL)  # ends the data url through the create_data function
training_list = data_list[:int(len(data_list)*PERCENT / 100)]
test_list = data_list[:int(len(data_list)*PERCENT / 100)]
create_classifier(training_list)

def create_test(test_list, classifier_list):

    # Compares the elements in the test_list against the classifier_list
    # If an item in the test list is larger then an item in the classifier it adds adds one to the over50_count.
    # otherwise it adds one to the under50_count.


    # print(len(test_list))
    # print(len(classifier_list))

    result_list = []
    under50_count2 = 0
    over50_count2 = 0
    # for each record in the test_list


    for row in test_list:
        under50_count = 0
        over50_count = 0
        under_over_50k_string = row[-1]
        # for each attribute of the test_list
        for index in range(14):
            try:
                # if the attribute is greater than the average
                if row[index] > classifier_list[row[index]]:
                    # print(classifier_list[row[index]])
                    # add to the over50
                    over50_count += 1

                else:
                    # else add to the under50
                    under50_count += 1

                    # print(classifier_list[row[index]])

            except Exception as e:
                # print(e) #"unorderable types: NoneType() > NoneType()"
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
    for row in test_list:
        if row[-1].strip(" ") == "<=50K":
            under50actual += 1
        elif row[-1].strip(" ") == ">50K":
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
    print("The classifier is %.2f %%" % (under50actual / under50_count2*100), "accurate.")


create_test(test_list, create_classifier(training_list))
