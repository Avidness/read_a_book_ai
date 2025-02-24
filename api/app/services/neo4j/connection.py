from neo4j import GraphDatabase

class Neo4jConnection:
    """Manages connection to the Neo4j database."""
    
    def __init__(self, uri="bolt://neo4j:7687", auth=("neo4j", "password"), db_name="neo4j"):
        """
        Initialize connection to Neo4j.
        
        Args:
            uri: Neo4j connection URI
            auth: Authentication credentials (username, password)
            db_name: Name of the database to use
        """
        self.driver = GraphDatabase.driver(uri, auth=auth)
        self.db_name = db_name
        
        # Create the database if it doesn't exist (only works with Neo4j Enterprise Edition)
        try:
            self._create_database_if_not_exists()
        except Exception as e:
            print(f"Warning: Could not create database '{db_name}'. Using default 'neo4j' database.")
            print(f"Error was: {str(e)}")
            self.db_name = "neo4j"
    
    def _create_database_if_not_exists(self):
        """Check if the database exists and create it if it doesn't."""
        # First, check if we can access the database
        try:
            self.driver.execute_query(
                "RETURN 1",
                database_=self.db_name
            )
            # If no error was thrown, the database exists
            return
        except Exception as e:
            if "Neo.ClientError.Database.DatabaseNotFound" in str(e):
                # Database doesn't exist, try to create it (requires admin privileges)
                try:
                    # This query needs to run against the system database
                    self.driver.execute_query(
                        f"CREATE DATABASE {self.db_name} IF NOT EXISTS",
                        database_="system"
                    )
                    print(f"Created database '{self.db_name}'")
                    
                    # Wait for the database to be available
                    import time
                    for _ in range(5):  # Try up to 5 times
                        try:
                            self.driver.execute_query(
                                "RETURN 1",
                                database_=self.db_name
                            )
                            print(f"Database '{self.db_name}' is now available")
                            return
                        except:
                            time.sleep(1)  # Wait a second before trying again
                    
                    # If we get here, the database still isn't available
                    raise Exception(f"Created database '{self.db_name}' but it's not yet available")
                except Exception as create_error:
                    # If we can't create the database, fall back to default
                    raise Exception(f"Failed to create database: {str(create_error)}")
            else:
                # If it's a different error, re-raise it
                raise
    
    def close(self):
        """Close the driver connection."""
        self.driver.close()
    
    def __enter__(self):
        """Enable usage with context manager."""
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        """Close the driver when exiting context manager."""
        self.close()