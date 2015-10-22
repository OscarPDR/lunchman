
def fix_meal_name(original_meal_name):

    return_string = original_meal_name

    return_string = original_meal_name.replace('c/', 'con ')

    if '/' in return_string:
        return_string = return_string[:return_string.rfind('/')]

    return return_string.strip()
