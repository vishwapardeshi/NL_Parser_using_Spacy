import unicodedata
unicodedata.numeric(u'⅕')
unicodedata.name(u'⅕')

def load_data(dir_path, test_data_filepath):
    """
        Load testing data from the csv.
    Args:
        test_data_filepath: the path of the test_data.csv file which is used for testing
    Returns:
        test_df (DataFrame): Dataframe containing annonated data
    """
    #load data
    test_df = pd.read_csv(os.path.join(dir_path,train_data_filepath))
    return test_df

def convert_vulgar_to_mixed_fraction(df):
    #convert vulgar fractions
    for ix, row in df.iterrows():
        for char in row['ingredient']:
            if unicodedata.name(char).startswith('VULGAR FRACTION'):
                normalized = unicodedata.normalize('NFKC', char)
                    df.iloc[ix, 2] = df.iloc[ix, 2].replace(char, normalized)
    return(df)

def save_data(df, filepath):
    """
    Takes clean dataframe from `clean_data` and saves it inside of an SQLite database with a desired filename.

    :Input:
        :train_df: Clean data frame from `clean_data`
        :clean_filename: String, csv file name
    :Returns:
        :None: Does not return anything but saves the csv file
    """
    df.to_csv(filepath, index = False, header = True)

def main():
    if len(sys.argv) == 3:

        data_path, final_filename = sys.argv[1:]

        raw_data_path = os.path.join(data_path, 'raw')
        proc_data_path = os.path.join(data_path, 'processed')

        print('Loading data...\n    RAW DATA: {}'
              .format(raw_data_path))
        test_df = load_data(raw_data_path, 'test_data.csv')

        print('Cleaning data...')
        test_df = convert_vulgar_to_mixed_fraction(test_df)

        print('Saving final test data...\n    CSV: {}'
            .format(os.path.join(proc_data_path, final_filename )))
        save_data(test_df, proc_data_path, final_filename )

    else:
        print('Please provide the directory path of data folder'\
              ' as well as the filename for cleaned and transformed data'\
              '\n\nExample: python process_data.py '\
              'data/ clean_train final_train')

if __name__ == '__main__':
    main()
