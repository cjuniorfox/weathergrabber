from .city_location import CityLocation

class Location:
    def __init__(self, id: str, city_location: CityLocation, search_name: str | None = None):
        self._id = id
        self._city_location = city_location
        self._search_name = search_name

    @property
    def id(self) -> str:
        return self._id
    
    @property
    def city_location(self) -> CityLocation:
        return self._city_location
    
    @property
    def search_name(self) -> str:
        return self._search_name
    
    def __repr__(self):
        return (f"Location(id:'{self.id}', city_location:'{self.city_location}',"
                f"search_name: '{self._search_name}')")