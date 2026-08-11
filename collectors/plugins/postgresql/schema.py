# Application
from base import BaseSchema


# PostgreSQL Schema
class PostgresSchema(BaseSchema):
    active_connections: int
    idle_connections: int
    total_commits: int
    total_rollbacks: int
