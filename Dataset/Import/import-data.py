import datetime
import neo4jauth

from neo4j import GraphDatabase
from constants import NodeType


class Neo4jDriver:
    def __init__(self, uri, user, password, database):
        print("Initializing Neo4j driver...")
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.database = database

    def close(self):
        print("Closing Neo4j driver...")
        self.driver.close()
        
    def run_query(self, query, file_path=None):
        print(f"start at: {datetime.datetime.now()}")
        print("==== The process will take a while to complete. Please be patient and wait ====")
        with self.driver.session() as session:
            tx = session.begin_transaction()
            try:
                if file_path is None:
                    result = tx.run(query).single()
                    result = result[0] if result is not None else None
                else:
                    result = tx.run(query, filePath=file_path).single()
                    result = result[0] if result is not None else None
                tx.commit()
                if result is not None:
                    print("total {count} rows have been inserted".format(count=result))
            finally:
                tx.close()
        print(f"end at: {datetime.datetime.now()}")

    def clear_db(self):
        print("Clearing database...")
        query = """
            MATCH (n)
            DETACH DELETE n
        """
        with self.driver.session() as session:
            tx = session.begin_transaction()
            try:
                tx.run(query)
                tx.commit()
            finally:
                tx.close()

    def create_constraints(self):
        constraints = [
            "CREATE CONSTRAINT `pmid_Article_uniq` IF NOT EXISTS FOR (n: `Article`) REQUIRE (n.`pmid`) IS UNIQUE",
            "CREATE CONSTRAINT `journal_Journal_uniq` IF NOT EXISTS FOR (n: `Journal`) REQUIRE (n.`journal`) IS UNIQUE",
            "CREATE CONSTRAINT `author_Author_uniq` IF NOT EXISTS FOR (n: `Author`) REQUIRE (n.`author`) IS UNIQUE",
            "CREATE CONSTRAINT `country_Country_uniq` IF NOT EXISTS FOR (n: `Country`) REQUIRE (n.`country`) IS UNIQUE",
        ]
        for constraint in constraints:
            print(f"Creating constraint: {constraint}...")
            self.run_query(constraint)

    def load_nodes(self, node_type, file_path):
        print(f"Loading nodes of type {node_type}...")
        node_load_queries = {
            NodeType.ARTICLE: """
                LOAD CSV WITH HEADERS FROM $filePath AS row
                WITH row 
                WHERE NOT toInteger(trim(row.`pmid`)) IS NULL
                MERGE (n: `Article` { `pmid`: toInteger(trim(row.`pmid`)) })
                SET n.`pmid` = toInteger(trim(row.`pmid`))
                SET n.`doi` = row.`doi`
                SET n.`title` = row.`title`
                SET n.`citation_count` = toInteger(trim(row.`citation_count`))
            """,
            NodeType.JOURNAL: """
                LOAD CSV WITH HEADERS FROM $filePath AS row
                WITH row
                WHERE NOT row.`journal` IS NULL
                MERGE (n: `Journal` { `journal`: row.`journal` })
                SET n.`journal` = row.`journal`
            """,
            NodeType.AUTHOR: """
                LOAD CSV WITH HEADERS FROM $filePath AS row
                WITH row
                WHERE NOT row.`author` IS NULL
                MERGE (n: `Author` { `author`: row.`author` })
                SET n.`author` = row.`author`
            """,
            NodeType.COUNTRY: """
                LOAD CSV WITH HEADERS FROM $filePath AS row
                WITH row
                WHERE NOT row.`country` IS NULL
                MERGE (n: `Country` { `country`: row.`country` })
                SET n.`country` = row.`country`
            """,
        }
        self.run_query(node_load_queries[node_type], file_path)

    def load_relationships(self, file_path_root, file_0, file_1, chunk_size=1000):
        relationship_load_queries = [
            # PUBLISHED_BY and PUBLISHED_IN relationships
            {
                "query": """
                    LOAD CSV WITH HEADERS FROM $filePath AS row
                    WITH row 
                    MATCH (source: `Article` { `pmid`: toInteger(trim(row.`pmid`)) })
                    MATCH (target: `Journal` { `journal`: row.`journal` })
                    MERGE (source)-[r: `PUBLISHED_BY`]->(target)
                """,
                "file": file_0
            },
            {
                "query": """
                    LOAD CSV WITH HEADERS FROM $filePath AS row
                    WITH row 
                    MATCH (source: `Article` { `pmid`: toInteger(trim(row.`pmid`)) })
                    MATCH (target: `Country` { `country`: row.`country` })
                    MERGE (source)-[r: `PUBLISHED_IN`]->(target)
                """,
                "file": file_0
            },
            # AUTHORED relationship
            {
                "query": """
                    CALL apoc.periodic.iterate(
                        'LOAD CSV WITH HEADERS FROM $filePath AS row RETURN row',
                        'WITH row 
                        MATCH (source: `Author` { `author`: row.`author` })
                        MATCH (target: `Article` { `pmid`: toInteger(trim(row.`pmid`)) })
                        MERGE (source)-[r: `AUTHORED`]->(target)
                        SET r.`weightage` = toFloat(trim(row.`weightage`))',
                        {batchSize: 10000, iterateList: true, parallel: false, params: {filePath: $filePath}}
                    )
                """,
                "file": file_1
            }
        ]
        for item in relationship_load_queries:
            print(f"Loading relationships from {item['file']}...")
            self.run_query(item["query"], file_path_root + item["file"])


if __name__ == "__main__":
    driver = Neo4jDriver(
        neo4jauth.uri, neo4jauth.username, neo4jauth.password, neo4jauth.database
    )
    driver.clear_db()
    driver.create_constraints()
    local_file_base_path = "https://raw.githubusercontent.com/96TSH/Publications-Neo4j/main/Dataset/"
    # smalldata.csv
    smalldata_file_path = local_file_base_path + "smalldata.csv"
    smalldata_node_types = [NodeType.ARTICLE, NodeType.JOURNAL, NodeType.COUNTRY]
    for n in smalldata_node_types:
        driver.load_nodes(n, smalldata_file_path)

    # authored.csvW
    authored_file_path = local_file_base_path + "authored.csv"
    authored_node_types = [NodeType.AUTHOR]
    for n in authored_node_types:
        driver.load_nodes(n, authored_file_path)

    driver.load_relationships(local_file_base_path, 'smalldata.csv', 'authored.csv')
    driver.close()
