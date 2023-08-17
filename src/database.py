import sys

from sqlalchemy import (
    DECIMAL,
    JSON,
    Boolean,
    Column,
    Float,
    ForeignKey,
    Index,
    String,
    Text,
    func,
    UniqueConstraint,
    create_engine,
    text,
)
from sqlalchemy.dialects.mysql import BIGINT, TINYINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.attributes import flag_modified

import utilities

DATABASE_URL = utilities.get_parameter_from_ssm("/planetscale/branch/connection")
CA_CERT_PATH = "/etc/ssl/certs/ca-certificates.crt"

ssl_args = {"ssl": {"ca": CA_CERT_PATH}}
engine = create_engine(DATABASE_URL, echo=True, connect_args=ssl_args)

Base = declarative_base()


class Artist(Base):
    __tablename__ = "artist"

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    uuid = Column(String(50), nullable=False)
    name = Column(String(50), nullable=True)
    slug = Column(String(50), nullable=True)
    imageURL = Column(String(255), nullable=True)
    artistData = Column(JSON, nullable=True)
    userId = Column(BIGINT(unsigned=True), nullable=True)

    __table_args__ = (
        Index("artists_uuid_idx", "uuid", unique=True),
        Index("userId_idx", "userId"),
        Index("name_idx", "name", mysql_length=50),  # For Fulltext search in MySQL
    )


class Creative(Base):
    __tablename__ = "creative"

    id = Column(BIGINT(unsigned=True), primary_key=True)
    name = Column(String(50))
    imageURL = Column(String(255))
    creativeData = Column(JSON)
    userId = Column(BIGINT(unsigned=True), index=True)

    __table_args__ = (Index("userId_idx", "userId"),)


class User(Base):
    __tablename__ = "user"

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    userId = Column(String(50), nullable=False)
    isArtist = Column(Boolean, nullable=False)
    isCreative = Column(Boolean, nullable=False)
    legalName = Column(String(255), nullable=False)
    stageName = Column(String(255), nullable=True)
    phoneNumber = Column(String(50), nullable=False)
    allowSms = Column(Boolean, nullable=False)
    bankingData = Column(JSON, nullable=True)
    email = Column(String(255), nullable=False)
    biography = Column(Text, nullable=True)
    termsApproved = Column(Boolean, nullable=False, default=False)
    primaryProfileId = Column(BIGINT(unsigned=True), nullable=True)
    currency = Column(String(3), nullable=False, default="USD")
    currentBalance = Column(DECIMAL(16, 4), nullable=False, default=0)
    primaryCreativeId = Column(BIGINT(unsigned=True), nullable=True)
    fromRate = Column(DECIMAL(16, 4), nullable=False, default=0)
    toRate = Column(DECIMAL(16, 4), nullable=False, default=0)
    isNegotiable = Column(Boolean, nullable=False, default=True)
    isIDVerified = Column(Boolean, default=False, nullable=False)
    isSocialVerified = Column(Boolean, default=False, nullable=False)
    isActive = Column(Boolean, default=True, nullable=False)

    __table_args__ = (
        Index("primaryProfileIdId_idx", "primaryProfileId"),
        Index("userId_idx", "userId", unique=True),
    )


class PaymentMethod(Base):
    __tablename__ = "paymentMethod"

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    paymentMethodName = Column(String(50), nullable=False)


class UserPaymentMethod(Base):
    __tablename__ = "userPaymentMethod"
    __table_args__ = (
        Index("userId_idx", "userId"),
        Index("paymentMethodId_idx", "paymentMethodId"),
    )

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    userId = Column(BIGINT(unsigned=True), nullable=False)
    paymentMethodId = Column(BIGINT(unsigned=True), nullable=False)
    paymentMethodData = Column(JSON, nullable=True)


class UserTrack(Base):
    __tablename__ = "userTrack"
    __table_args__ = (Index("userId_idx", "userId"),)

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    userId = Column(BIGINT(unsigned=True), nullable=False)
    trackUrl = Column(String(255), nullable=False)
    trimmedUrl = Column(String(255), nullable=True)
    name = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    isFeatured = Column(Boolean, default=False, nullable=False)
    duration = Column(Float, nullable=False)
    featuredStartTime = Column(Float, nullable=True)
    featuredStopTime = Column(Float, nullable=True)


class PurgatoryUser(Base):
    __tablename__ = "purgatoryUser"

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    phoneNumber = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False)
    artistUuid = Column(String(50), nullable=False)


Session = sessionmaker(bind=engine)

# ----------------------- Database functions -----------------------


def get_profile_id(uuid, session):
    """Gets the profile id for the given artist uuid

    Args:
        uuid        The artist uuid
        session     The database session
    Returns:
        The profile id
    """

    artist = session.query(Artist).filter(Artist.uuid == uuid).one_or_none()
    return artist.id if artist else None


def get_artist_data_from_db(uuid):
    """Get the artist data from the database

    Args:
        uuid    The artist uuid
    Returns:
        The artist data
    """

    session = Session()
    artist = session.query(Artist).filter(Artist.uuid == uuid).one_or_none()

    session.close()

    if artist:
        return artist.artistData
    else:
        return None
    
def get_artist_of_user(session, id):

    artist = session.query(Artist).filter(Artist.id == id).one_or_none()

    if artist:
        return artist
    else:
        return None

def save_message_to_db(uuid, platforms):
    """Save the message to the database

    Args:
        artist_data  The data to save
    Returns:
        None
    """

    session = Session()

    # Check if the artist exists in the database
    existing_artist = session.query(Artist).filter(Artist.uuid == uuid).one_or_none()

    if existing_artist:
        existing_artist.artistData = utilities.set_artist_data(existing_artist.artistData, platforms)
        # Need to force the update to the database
        flag_modified(existing_artist, "artistData")
    else:
        # Create a new artist
        artist = Artist(
            uuid=uuid,
            artistData=utilities.set_artist_data(None, platforms)
        )
        session.add(artist)

    session.commit()
    session.close()
