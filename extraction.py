__author__ = 'Y.H.Wang, X.Y.Zhang'


def get_data_html( html ):
    ''' extract data from html file '''
    # html : file_name
    # return : text_data
    pass

def get_data_theme(data):
    '''judge the theme of text_data based on classification , such as economic, military'''
    # data: text_data
    # return : theme
    pass

def split_data(data):
    '''split the data into sentences'''
    # data :text_data
    # return : the list of sentences

def extract_rule(sentence):
    '''extract economic relation from sentence'''
    # sentence : text_data
    # return : list [entity, attribute, value]



if __name__ == "__main__":
    pass