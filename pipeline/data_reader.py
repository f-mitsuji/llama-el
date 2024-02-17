import json


def read_json_file(file_path):
    with open(file_path, "r", encoding="UTF-8") as input_file:
        data = json.load(input_file)
        return data


def get_prompt(dataset, input):
    if dataset == 'lcquad2':
        return f'''INPUT: What does emigration mean?
                OUTPUT: \"entities_text\": [], \"wikipedia_urls\": []
                INPUT: Who is the child of Ranavalona I's husband?
                OUTPUT: \"entities_text\": [\"Ranavalona I\"], \"wikipedia_urls\": [\"https://en.wikipedia.org/wiki/Ranavalona_I\"]
                INPUT: What periodical literature does Delta Air Lines use as a moutpiece?
                OUTPUT: \"entities_text\": [\"periodical literature\", \"Delta Air Lines\"], \"wikipedia_urls\": [\"https://en.wikipedia.org/wiki/Periodical_literature\", \"https://en.wikipedia.org/wiki/Delta_Air_Lines\"]
                INPUT: What is award received of Hans Krebs where point in time is 1966-0-0?
                OUTPUT: \"entities_text\": [\"Hans Krebs\"], \"wikipedia_urls\": [\"https://en.wikipedia.org/wiki/Hans_Krebs_(biochemist)\"]
                INPUT: {input}
                OUTPUT:'''

    elif dataset == 'simpleqs':
        return f'''INPUT: How do plants grow?
                OUTPUT: \"entities_text\": [], \"wikipedia_urls\": []
                INPUT: what movie is produced by warner bros.
                OUTPUT: \"entities_text\": [\"warner bros.\"], \"wikipedia_urls\": [\"https://en.wikipedia.org/wiki/Warner_Bros.\"]
                INPUT: what is the gender of james hendry?
                OUTPUT: \"entities_text\": [\"james hendry\"], \"wikipedia_urls\": [\"https://en.wikipedia.org/wiki/James_Hendry_(obstetrician)\"]
                INPUT: {input}
                OUTPUT:'''

    elif dataset == 'webqsp':
        return f'''INPUT: what does the letters eu stand for?
                OUTPUT: \"entities_text\": [], \"wikipedia_urls\": []
                INPUT: what country is the grand bahama island in?
                OUTPUT: \"entities_text\": [\"grand bahama\"], \"wikipedia_urls\": [\"https://en.wikipedia.org/wiki/Grand_Bahama\"]
                INPUT: what character did john noble play in lord of the rings?
                OUTPUT: \"entities_text\": [\"john noble\", \"lord of the rings\"], \"wikipedia_urls\": [\"https://en.wikipedia.org/wiki/John_Noble\", \"https://en.wikipedia.org/wiki/The_Lord_of_the_Rings:_The_Two_Towers\"]
                INPUT: what city is the state capital of washington?
                OUTPUT: \"entities_text\": [\"washington\"], \"wikipedia_urls\": [\"https://en.wikipedia.org/wiki/Washington_(state)\"]
                INPUT: {input}
                OUTPUT:'''
