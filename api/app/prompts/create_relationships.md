
    # Define relationships
    relationships = [
        ("Harry Potter", "Ron Weasley", {"type": "best_friend", "since": "first_year"}),
        ("Harry Potter", "Hermione Granger", {"type": "best_friend", "since": "first_year"}),
        ("Ron Weasley", "Hermione Granger", {"type": "best_friend", "since": "first_year"}),
        ("Harry Potter", "Luna Lovegood", {"type": "friend", "since": "fifth_year"}),
        ("Harry Potter", "Neville Longbottom", {"type": "friend", "since": "first_year"}),
        ("Harry Potter", "Ginny Weasley", {"type": "romantic", "since": "sixth_year"}),
        ("Harry Potter", "Draco Malfoy", {"type": "rival", "since": "first_year"}),
        ("Neville Longbottom", "Luna Lovegood", {"type": "friend", "since": "fifth_year"}),
        ("Ginny Weasley", "Luna Lovegood", {"type": "close_friend", "since": "fourth_year"})
    ]
    
    # Add all relationships
    for char1, char2, props in relationships:
        print(f"Adding relationship between {char1} and {char2}")
        graph.add_relationship(
            char1,
            char2,
            "RELATIONSHIP_WITH",
            props
        )
        