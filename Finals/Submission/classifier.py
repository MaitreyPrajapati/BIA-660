import xgboost as xgb
import pandas as pd
from sklearn import preprocessing
from sklearn.feature_extraction.text import CountVectorizer
import re, csv

REGEX_PATTERN = r'(\n|,|\.)'

def label_generator(label):
    if label.lower() == 'data engineer':
        return 0
    elif label.lower() == 'data scientist':
        return 1
    else:
        return 2

def remove_space_and_punctuation(paragraph):
    if isinstance(paragraph, str):
        paragraph = re.sub(REGEX_PATTERN, ' ', paragraph)
    else: paragraph = 'NAN'
    return paragraph

def write_csv(predictions):
    labels = {
        0: 'Data Engineer',
        1: 'Data Scientist',
        2: 'Software Engineer'
    }
    with open('CSVS/predictions.csv', 'w') as file:
        writer = csv.writer(file)
        for p in predictions:
            writer.writerow([labels[p]])
    return

def load_csv(path, test=None):
    if not test:
        all_data = pd.read_csv(path, index_col=None, names=['Description', 'Position'])
        return all_data
    else:
        all_data = pd.read_csv(path, index_col=None, names=['Description'])
        return all_data

def stage_data(data, test=None):
    if not test:
        data['labels'] = data.apply(lambda row : label_generator(row['Position']), axis=1)
        data = data.drop('Position', 1)
    data['Description'] = data.apply(lambda row: remove_space_and_punctuation(row['Description']), axis=1)
    return data

def get_model(train_data):
    lbl_enc = preprocessing.LabelEncoder()
    y_train = lbl_enc.fit_transform(train_data.labels)
    x_train = train_data.Description

    ctv = CountVectorizer(analyzer='word',token_pattern=r'\w{1,}', ngram_range=(1, 2), stop_words = 'english')
    ctv.fit(list(x_train))
    xtrain_ctv =  ctv.transform(x_train)

    clf = xgb.XGBClassifier(max_depth=7, n_estimators=200, colsample_bytree=0.8, subsample=0.8, nthread=10, learning_rate=0.1)
    clf.fit(xtrain_ctv.tocsc(), y_train)

    return clf, ctv

def predict(model, test_data):
    pred =  model.predict(test_data)
    return pred

def run(train_data_path, test_data_path):
    train_data = load_csv(train_data_path)
    print('Loaded Train CSV ...\n')
    train_staged = stage_data(train_data)
    print('Staged Training data ...\n')
    test_data = load_csv(test_data_path, True)
    test_data = stage_data(test_data, True)
    print('Loaded and staged test data..\n')
    clf, cv = get_model(train_staged)
    x_test = cv.transform(test_data.Description)
    print('Trained data ...\n')
    predictions = predict(clf, x_test)
    print('Predicted data')
    write_csv(predictions)


'''
    run(Training path, Testing path)
    The folder will be created in TextCSV
'''

TRAINING_PATH = 'CSVS/Combined.csv'
TESTING_PATH = 'Pass testing path here'

run(TRAINING_PATH, 'TESTING-PATH')