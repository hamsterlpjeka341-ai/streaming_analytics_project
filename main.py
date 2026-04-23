import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from faker import Faker
import random


DB_URL = "postgresql://postgres:1234@localhost:5432/streaming_db"
engine = create_engine(DB_URL)
fake = Faker()

def generate_data():
    """Генерация данных и полная перезапись таблиц"""
    print("Генерация данных...")
    

    genres = ['Sci-Fi', 'Drama', 'Comedy', 'Horror', 'Action']
    content_list = []
    for i in range(1, 51):
        content_list.append({
            'content_id': i, 
            'title': fake.catch_phrase(), 
            'genre': random.choice(genres), 
            'year': random.randint(2010, 2024), 
            'rating': round(random.uniform(4, 10), 1)
        })
    pd.DataFrame(content_list).to_sql('content', engine, if_exists='replace', index=False)

    # 2. Пользователи
    users_list = []
    for i in range(1, 201):
        users_list.append({
            'user_id': i,
            'username': fake.user_name(), 
            'reg_date': fake.date_between(start_date='-2y', end_date='-1y'),
            'sub_type': random.choice(['Free', 'Basic', 'Premium'])
        })
    pd.DataFrame(users_list).to_sql('users', engine, if_exists='replace', index=False)

    # 3. Просмотры (1000 строк)
    views_list = []
    for i in range(1, 1001):
        views_list.append({
            'view_id': i,
            'user_id': random.randint(1, 200), 
            'content_id': random.randint(1, 50),
            'view_date': fake.date_between(start_date='-1y', end_date='today'),
            'duration': random.randint(10, 180)
        })
    pd.DataFrame(views_list).to_sql('viewing_history', engine, if_exists='replace', index=False)
    print("Данные загружены в PostgreSQL!")

def perform_analytics():
    """Анализ и визуализация"""
    print("Анализ данных...")
    
    query = "SELECT v.*, c.genre, c.rating FROM viewing_history v JOIN content c ON v.content_id = c.content_id"
    df = pd.read_sql(query, engine)
    df['view_date'] = pd.to_datetime(df['view_date'])

    fig, axes = plt.subplots(3, 2, figsize=(15, 15))
    fig.suptitle('Streaming Analytics Dashboard', fontsize=20)
    
    daily = df.groupby('view_date')['duration'].sum().sort_index()
    daily.plot(ax=axes[0,0], title='Daily Viewing Minutes', color='blue')
    daily.rolling(window=7).mean().plot(ax=axes[0,0], label='7-day Trend', color='red')
    axes[0,0].legend()

    df.groupby('genre')['duration'].sum().plot(kind='bar', ax=axes[0,1], color='green', title='Top Genres')

    users_df = pd.read_sql("SELECT sub_type FROM users", engine)
    users_df['sub_type'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=axes[1,0], title='Subscription Plans')

    axes[1,1].scatter(df['rating'], df['duration'], alpha=0.5, color='purple')
    axes[1,1].set_title('Rating vs Duration')

    df['duration'].plot(kind='hist', bins=30, ax=axes[2,0], color='teal', title='Session Length Distribution')

    axes[2,1].axis('off')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig('dashboard.png')
    print("Dashboard сохранен в dashboard.png")
    plt.show()

if __name__ == "__main__":

    generate_data() 
    

    perform_analytics()