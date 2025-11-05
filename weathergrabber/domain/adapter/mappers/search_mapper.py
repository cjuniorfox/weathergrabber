from weathergrabber.domain.entities.search import Search

def search_to_dict(search: Search) -> dict:
    return {
        "id": search.id,
        "search_name": search.search_name,
    }

def dict_to_search(data: dict) -> Search:
    return Search(
        id=data["id"],
        search_name=data["search_name"],
    )
