def setify_tags(tags_str):

    tags = tags_str.strip()
    tags_set = set()
    tags_list = list()
    try:
        tags_list = tags.split(',')
        for tag in tags_list:
            tag = tag.strip()
            tags_set.add(tag)
    except:
        tags_set.add(wanted_tags)
    
    return tags_set


def prompt_before_exit(question):
    while True:
        response = input(question)
        #response = input('WARNING, overwriting! Continue? (y/n) ')
        if response.lower() == 'y':
            break
        elif response.lower() == 'n':
            print('Exiting...')
            exit(1)
        else:
            print('Response not understood, please try again')
