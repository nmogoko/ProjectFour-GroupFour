# Configuration settings for example db, environment variables
class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres_user:yUbydg8bYK5GujDNfRy5fyRjhuvVNJus@dpg-cs0kerggph6c73aa9nig-a.oregon-postgres.render.com:5432/group_four"
    SQLALCHEMY_TRACK_MODIFICATION = False
    JWT_SECRET_KEY = '3259a843-5011-4b6c-8880-54b029aaa069'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'remmykiplangat4873@gmail.com'
    MAIL_PASSWORD = 'shcheihckaenzzkw'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True