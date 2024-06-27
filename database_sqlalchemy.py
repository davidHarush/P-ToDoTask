from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, index=True)
    email = db.Column(db.String, unique=True, index=True, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email
        }


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True, index=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    completed = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "due_date": self.due_date,
            "user_id": self.user_id
        }
