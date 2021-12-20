# -*- coding: utf-8 -*-
from time        import sleep
from context_search import ContextSearch


if __name__=="__main__":
    """
        Author:  Aline Rodrigues
        Created: 16/11/2021
        Run the context search
    """ 
    search = ContextSearch()
    
    try:
        #search.init_search()
        #while not search.status_thread:
        #   sleep(30)
        search.convert_data_to_csv()
    except Exception as error:
        print (f'Error: {error}')
