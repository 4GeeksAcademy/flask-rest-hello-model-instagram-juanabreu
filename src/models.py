from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

#tabla



follower_table = Table(
    "follower",
    db.metadata,
    Column("followers_id", ForeignKey("user.id"), primary_key=True),
    Column("followed_id", ForeignKey("user.id"), primary_key=True),
)


class User(db.Model):
    id:Mapped[int]=mapped_column(primary_key=True)
    email:Mapped[str]=mapped_column(String(50), unique=True, nullable=False)
    password:Mapped[str]=mapped_column(nullable=False)

    post: Mapped[list["Post"]] = relationship(back_populates="user")

    comment: Mapped[list["Comment"]] = relationship(back_populates="user")

    follower: Mapped[list["User"]] = relationship(
        "User",
        secondary="follower_table",
        primaryjoin=(follower_table.c.followers_id == id),
        secondaryjoin=(follower_table.c.followed_id == id),
        back_populates= "followed",

    )

    followed: Mapped[list["User"]] = relationship(
        "User",
        secondary="follower_table",
        primaryjoin=(follower_table.c.followed_id == id),
        secondaryjoin=(follower_table.c.followers_id == id),
        back_populates= "follower",

    )
    

    

class Post(db.Model):
    id:Mapped[int]=mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    
    user: Mapped[User]= relationship(back_populates="post")

    media: Mapped[list["Media"]] = relationship(back_populates="post_media")
    
    

    comment:Mapped[list["Comment"]] = relationship(back_populates="post_comment") 




class Media(db.Model):
    id:Mapped[int]=mapped_column(primary_key=True)
    url:Mapped[str]=mapped_column(String(150),unique=True, nullable=False)

    post_media: Mapped["Post"] = relationship(back_populates="media")
    post_id:Mapped[int]=mapped_column(ForeignKey("post.id"))




class Comment(db.Model):
    id:Mapped[int]=mapped_column(primary_key=True)
    comments_text:Mapped[str]=mapped_column(String(150),unique=True, nullable=False)

    user: Mapped[User] = relationship(back_populates="comment")

    user_id:Mapped[int]=mapped_column(ForeignKey("user.id"))

    post_comment: Mapped[Post] = relationship(back_populates="comment")
    
    post_id:Mapped[int]=mapped_column(ForeignKey("post.id"))



