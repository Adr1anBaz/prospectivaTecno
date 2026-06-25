"""
Database module for managing conversations and messages.
Uses SQLite for persistent storage of chat history.
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Database setup
DATABASE_URL = "sqlite:///./chatbot.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Conversation(Base):
    """Table for storing conversations/sessions"""
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=True)
    copilot_profile = Column(String(50), default="generico")
    model = Column(String(100), default="llama3.2:3b")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to messages
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")


class Message(Base):
    """Table for storing individual messages within conversations"""
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    role = Column(String(20), nullable=False)  # 'system', 'user', or 'assistant'
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to conversation
    conversation = relationship("Conversation", back_populates="messages")


# Create tables
Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_conversation(db, title: Optional[str] = None, copilot_profile: str = "generico", model: str = "llama3.2:3b") -> Conversation:
    """Create a new conversation"""
    conversation = Conversation(
        title=title or "New Conversation",
        copilot_profile=copilot_profile,
        model=model
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation


def get_conversation(db, conversation_id: int) -> Optional[Conversation]:
    """Get a conversation by ID"""
    return db.query(Conversation).filter(Conversation.id == conversation_id).first()


def get_all_conversations(db) -> List[Conversation]:
    """Get all conversations, ordered by most recent"""
    return db.query(Conversation).order_by(Conversation.updated_at.desc()).all()


def add_message(db, conversation_id: int, role: str, content: str) -> Message:
    """Add a message to a conversation"""
    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content
    )
    db.add(message)

    # Update conversation timestamp
    conversation = get_conversation(db, conversation_id)
    if conversation:
        conversation.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(message)
    return message


def get_conversation_messages(db, conversation_id: int) -> List[Message]:
    """Get all messages in a conversation"""
    return db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at.asc()).all()


def delete_conversation(db, conversation_id: int) -> bool:
    """Delete a conversation and all its messages"""
    conversation = get_conversation(db, conversation_id)
    if conversation:
        db.delete(conversation)
        db.commit()
        return True
    return False


def update_conversation_title(db, conversation_id: int, title: str) -> Optional[Conversation]:
    """Update the title of a conversation"""
    conversation = get_conversation(db, conversation_id)
    if conversation:
        conversation.title = title
        db.commit()
        db.refresh(conversation)
        return conversation
    return None
