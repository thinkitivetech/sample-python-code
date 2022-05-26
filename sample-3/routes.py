from __main__ import app
from flask import Flask, render_template, request
import config


# Display simple html form for survey
@app.route("/")
def display_form():
    questions_collection = config.get_db_questions_connection()
    data = questions_collection.find()
    return render_template('home.html', questions = data[0]['questions'])

# Store form data to database 
@app.route("/add-response", methods = ['POST'])
def add_response():
    data = request.form.to_dict()
    answers_collection = config.get_db_answers_connection()

    for key, value in data.items():
        answers_collection.update_one({'question_id': key}, {'$push': {'answer': value}})
    answers_data = config.get_db_answers_connection().find()
    age_label = ["Less than 18", "18 to 60", "More than 60"]
    edu_label = ["SSC", "HSC", "Graduate"]
    fav_color_label = ["Red", "Green", "Orange"]
    nationality_label = ["Indian", "German", "American"]
    income_label = ["Around 25K", "25K to 60K", "More than 100K"]
    label_list = [age_label, edu_label, fav_color_label, nationality_label, income_label]
    
    # Getting count of every age label 
    age_less_than_18_count = answers_data[0]['answer'].count("Less than 18")
    age_18_to_60_count = answers_data[0]['answer'].count("18 to 60")
    age_more_than_60_count = answers_data[0]['answer'].count("More than 60")
    age_count = [age_less_than_18_count, age_18_to_60_count, age_more_than_60_count]

    # Getting count of every educational qualification label
    edu_ssc_count = answers_data[1]['answer'].count("SSC")
    edu_hsc_count = answers_data[1]['answer'].count("HSC")
    edu_graduate_count = answers_data[1]['answer'].count("Graduate")
    edu_count = [edu_ssc_count, edu_hsc_count, edu_graduate_count]

    # Getting count of every color label
    fav_color_red_count = answers_data[2]['answer'].count("Red")
    fav_color_green_count = answers_data[2]['answer'].count("Green")
    fav_color_orange_count = answers_data[2]['answer'].count("Orange")
    fav_color_count = [fav_color_red_count, fav_color_green_count, fav_color_orange_count]

    # Getting count of every nationality label
    nationality_indian_count = answers_data[3]['answer'].count("Indian")
    nationality_german_count = answers_data[3]['answer'].count("German")
    nationality_american_count = answers_data[3]['answer'].count("American")
    nationality_count = [nationality_indian_count, nationality_german_count, nationality_american_count]

    # Getting count of every income label
    income_around_25k_count = answers_data[4]['answer'].count("Around 25K")
    income_25k_to_100k_count = answers_data[4]['answer'].count("25K to 100K")
    income_more_than_100k_count = answers_data[4]['answer'].count("More than 100K")
    income_count = [income_around_25k_count, income_25k_to_100k_count, income_more_than_100k_count]

    count_list = [age_count, edu_count, fav_color_count, nationality_count, income_count]
    return render_template('graph.html', label_list = label_list, count_list = count_list)
