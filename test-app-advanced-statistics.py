from flask import Flask, render_template # import bare minimum flask functions

app = Flask(__name__) # create a flask app

@app.route('/') # route to the index page
def index():
    followers_not_following = ["test1", "test2", "test3"]   
    following_not_followers = ["test4", "test5", "test6"]
    return render_template('advanced_statistics.html', followers_not_following=followers_not_following, following_not_followers=following_not_followers)

if __name__ == '__main__':
    app.run(debug=True)
