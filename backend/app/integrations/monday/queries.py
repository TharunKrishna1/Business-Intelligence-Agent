"""GraphQL queries for monday.com v2 API."""

GET_BOARD_ITEMS_QUERY = """
query GetBoardItems($board_id: [ID!]!, $limit: Int = 500, $cursor: String) {
  boards(ids: $board_id) {
    id
    name
    items_page(limit: $limit, cursor: $cursor) {
      cursor
      items {
        id
        name
        column_values {
          id
          title
          text
          value
          type
        }
      }
    }
  }
}
"""

GET_BOARD_METADATA_QUERY = """
query GetBoardMetadata($board_id: [ID!]!) {
  boards(ids: $board_id) {
    id
    name
    columns {
      id
      title
      type
    }
  }
}
"""
