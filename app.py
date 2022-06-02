# save this as app.py
from flask import Flask,render_template
import pickle
from slugify import slugify
import numpy as np


## Model 
popular_df= pickle.load(open('model/popular.pkl','rb'))
pt= pickle.load(open('model/pt.pkl','rb'))
books= pickle.load(open('model/books.pkl','rb'))
similarity_score= pickle.load(open('model/similarity_score.pkl','rb'))

app = Flask(__name__,static_url_path='/static')

@app.route("/")
def index():
    return render_template('index.html',
        book_name= list(popular_df['Book-Title'].values),
        author= list(popular_df['Book-Author'].values),
        image= list(popular_df['Image-URL-M'].values),
        votes= list(popular_df['num_ratings'].values),
        ratings= list(popular_df['avg_ratings'].values),
        year_of_publication= list(popular_df['Year-Of-Publication'].values),
    )

@app.route("/book/<path:bookname>")
def book(bookname):
    index= np.where(pt.index==bookname)[0][0]
    similar_items= sorted(list(enumerate(similarity_score[index])),key=lambda x:x[1],reverse=True)[1:11]
    data= [] 
    for i in similar_items:
        item = []
        temp_df=books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Year-Of-Publication'].values))
        data.append(item)

        books_details = [] 
        book_items= []
        book_items.extend(list(books[books['Book-Title'] == bookname].drop_duplicates('Book-Title')['Book-Title'].values))
        book_items.extend(list(books[books['Book-Title'] == bookname].drop_duplicates('Book-Title')['Book-Author'].values))
        book_items.extend(list(books[books['Book-Title'] == bookname].drop_duplicates('Book-Title')['Image-URL-M'].values))
        book_items.extend(list(books[books['Book-Title'] == bookname].drop_duplicates('Book-Title')['Year-Of-Publication'].values))
        books_details.append(book_items)

    return render_template('book-recommeded.html',data= data,books_details=books_details)

if __name__ == '__main__':
    app.run(debug=True)
    