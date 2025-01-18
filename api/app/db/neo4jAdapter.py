from neo4j import GraphDatabase, RoutingControl

class FriendshipGraph:
    def __init__(self, uri="bolt://neo4j:7687", auth=("neo4j", "password")):
        self.driver = GraphDatabase.driver(uri, auth=auth)

    def close(self):
        """Close the driver connection."""
        self.driver.close()

    def add_friend(self, name, friend_name):
        """Add a friendship relationship between two people."""
        self.driver.execute_query(
            "MERGE (a:Person {name: $name}) "
            "MERGE (friend:Person {name: $friend_name}) "
            "MERGE (a)-[:KNOWS]->(friend)",
            name=name, friend_name=friend_name, database_="neo4j",
        )

    def get_friends(self, name):
        """Get all friends of a person."""
        records, _, _ = self.driver.execute_query(
            "MATCH (a:Person)-[:KNOWS]->(friend) WHERE a.name = $name "
            "RETURN friend.name ORDER BY friend.name",
            name=name, database_="neo4j", routing_=RoutingControl.READ,
        )
        return [record["friend.name"] for record in records]

    def print_friends(self, name):
        """Print all friends of a person."""
        for friend_name in self.get_friends(name):
            print(friend_name)

    def __enter__(self):
        """Enable usage with context manager."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the driver when exiting context manager."""
        self.close()
