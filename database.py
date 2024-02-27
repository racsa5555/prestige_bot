import json
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    state = Column(String)


engine = create_engine('postgresql://ascar:1@localhost/aiogram_bot')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

async def save_state_to_db(user_id, state):
    session = Session()
    user = session.query(User).filter_by(id=user_id).first()
    state_json = json.dumps(state)
    if user:
        user.state = state_json
    else:
        user = User(id=user_id, state=state_json)
        session.add(user)
    session.commit()
    session.close()
    
async def load_all_states_from_db():
    session = Session()
    users = session.query(User).all()
    session.close()
    return {user.id: user.state for user in users}

async def set_user_state(user_id, state):
    session = Session()
    user_state = session.query(User).filter_by(id=user_id).first()
    if user_state:
        user_state.state = state
    else:
        user_state = User(id=user_id, state=state)
        session.add(user_state)
    session.commit()
    session.close()