:param {
  // Define the file path root and the individual file names required for loading.
  // https://neo4j.com/docs/operations-manual/current/configuration/file-locations/
  file_path_root: 'file:///', // Change this to the folder your script can access the files at.
  file_0: 'smalldata.csv',
  file_1: 'authored.csv'
};

// CONSTRAINT creation
// -------------------
//
// Create node uniqueness constraints, ensuring no duplicates for the given node label and ID property exist in the database. This also ensures no duplicates are introduced in future.
//
// NOTE: The following constraint creation syntax is generated based on the current connected database version 5.19-aura.
CREATE CONSTRAINT `pmid_Article_uniq` IF NOT EXISTS
FOR (n: `Article`)
REQUIRE (n.`pmid`) IS UNIQUE;
CREATE CONSTRAINT `journal_Journal_uniq` IF NOT EXISTS
FOR (n: `Journal`)
REQUIRE (n.`journal`) IS UNIQUE;
CREATE CONSTRAINT `author_Author_uniq` IF NOT EXISTS
FOR (n: `Author`)
REQUIRE (n.`author`) IS UNIQUE;
CREATE CONSTRAINT `country_Country_uniq` IF NOT EXISTS
FOR (n: `Country`)
REQUIRE (n.`country`) IS UNIQUE;

:param {
  idsToSkip: []
};

// NODE load
// ---------
//
// Load nodes in batches, one node label at a time. Nodes will be created using a MERGE statement to ensure a node with the same label and ID property remains unique. Pre-existing nodes found by a MERGE statement will have their other properties set to the latest values encountered in a load file.
//
// NOTE: Any nodes with IDs in the 'idsToSkip' list parameter will not be loaded.
LOAD CSV WITH HEADERS FROM ($file_path_root + $file_0) AS row
WITH row
WHERE NOT row.`pmid` IN $idsToSkip AND NOT toInteger(trim(row.`pmid`)) IS NULL
CALL {
  WITH row
  MERGE (n: `Article` { `pmid`: toInteger(trim(row.`pmid`)) })
  SET n.`pmid` = toInteger(trim(row.`pmid`))
  SET n.`doi` = row.`doi`
  SET n.`title` = row.`title`
  SET n.`citation_count` = toInteger(trim(row.`citation_count`))
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_0) AS row
WITH row
WHERE NOT row.`journal` IN $idsToSkip AND NOT row.`journal` IS NULL
CALL {
  WITH row
  MERGE (n: `Journal` { `journal`: row.`journal` })
  SET n.`journal` = row.`journal`
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_1) AS row
WITH row
WHERE NOT row.`author` IN $idsToSkip AND NOT row.`author` IS NULL
CALL {
  WITH row
  MERGE (n: `Author` { `author`: row.`author` })
  SET n.`author` = row.`author`
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_0) AS row
WITH row
WHERE NOT row.`country` IN $idsToSkip AND NOT row.`country` IS NULL
CALL {
  WITH row
  MERGE (n: `Country` { `country`: row.`country` })
  SET n.`country` = row.`country`
} IN TRANSACTIONS OF 10000 ROWS;


// RELATIONSHIP load
// -----------------
//
// Load relationships in batches, one relationship type at a time. Relationships are created using a MERGE statement, meaning only one relationship of a given type will ever be created between a pair of nodes.
LOAD CSV WITH HEADERS FROM ($file_path_root + $file_0) AS row
WITH row 
CALL {
  WITH row
  MATCH (source: `Article` { `pmid`: toInteger(trim(row.`pmid`)) })
  MATCH (target: `Journal` { `journal`: row.`journal` })
  MERGE (source)-[r: `PUBLISHED_BY`]->(target)
  // Your script contains the datetime datatype. Our app attempts to convert dates to ISO 8601 date format before passing them to the Cypher function.
  // This conversion cannot be done in a Cypher script load. Please ensure that your CSV file columns are in ISO 8601 date format to ensure equivalent loads.
  // SET r.`published_at` = datetime(row.`published_at`)
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_1) AS row
WITH row 
CALL {
  WITH row
  MATCH (source: `Author` { `author`: row.`author` })
  MATCH (target: `Article` { `pmid`: toInteger(trim(row.`pmid`)) })
  MERGE (source)-[r: `AUTHORED`]->(target)
  SET r.`weightage` = toFloat(trim(row.`weightage`))
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_0) AS row
WITH row 
CALL {
  WITH row
  MATCH (source: `Article` { `pmid`: toInteger(trim(row.`pmid`)) })
  MATCH (target: `Country` { `country`: row.`country` })
  MERGE (source)-[r: `PUBLISHED_IN`]->(target)
} IN TRANSACTIONS OF 10000 ROWS;
