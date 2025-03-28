from ..objects import FirstCyclingObject
from .endpoints import RaceEndpoint, RaceVictoryTable, RaceStageVictories, RaceEditionResults
from ..api import fc
from ..constants import Classification
import re
import difflib
from bs4 import BeautifulSoup

class Race(FirstCyclingObject):
    """
    Wrapper to access endpoints associated with races.

    Attributes
    ----------
    ID : int
        The firstcycling.com ID for the race from the URL of the race page.
    """

    _default_endpoint = RaceEndpoint

    @classmethod
    def search(cls, query, year=None, category="1"):
        """
        Search for races by name using fuzzy matching.

        Parameters
        ----------
        query : str
            The search query string.
        year : int
            The year to search for races (e.g., 2025). If None, uses current year.
        category : str
            Category code - e.g., "1" for WorldTour, "2" for ProSeries.

        Returns
        -------
        list
            A list containing one dictionary with the race id and query as name if a match is found,
            or an empty list otherwise.
        """
        try:
            # Get HTML content using search_race API call
            html = fc.search_race(query, year, category)
            # Find best matching race ID using fuzzy matching
            race_id = search_race_id(query, html)
            if race_id is not None:
                # Return a dictionary with all expected keys
                return [{
                    'id': race_id,
                    'name': query,
                    'country': '',
                    'date': '',
                    'category': category
                }]
            else:
                return []
        except Exception as e:
            print(f"Error in Race.search: {str(e)}")
            return []

    def _get_response(self, **kwargs):
        return fc.get_race_endpoint(self.ID, **kwargs)

    def edition(self, year):
        """
        Get RaceEdition instance for edition of race.

        Parameters
        ----------
        year : int
            Year for edition of interest.

        Returns
        -------
        RaceEdition
        """
        return RaceEdition(self.ID, year)

    def overview(self, classification_num=None):
        """
        Get race overview for given classifications.

        Parameters
        ----------
        classification_num : int
            Classification for which to collect information.
            See utilities.Classifications for possible inputs.

        Returns
        -------
        RaceEndpoint
        """
        return self._get_endpoint(k=classification_num)

    def victory_table(self):
        """
        Get race all-time victory table.

        Returns
        -------
        RaceVictoryTable
        """
        return self._get_endpoint(endpoint=RaceVictoryTable, k='W')

    def year_by_year(self, classification_num=None):
        """
        Get year-by-year race statistics for given classification.

        Parameters
        ----------
        classification_num : int
            Classification for which to collect information.
            See utilities.Classifications for possible inputs.

        Returns
        -------
        RaceEndpoint
        """
        return self._get_endpoint(k='X', j=classification_num)    
    
    def youngest_oldest_winners(self):
        """
        Get race all-time victory table.

        Returns
        -------
        RaceYoungestOldestWinners
        """
        return self._get_endpoint(k='Y')
    
    def stage_victories(self):
        """
        Get race all-time stage victories.

        Returns
        -------
        RaceStageVictories
        """
        return self._get_endpoint(endpoint=RaceStageVictories, k='Z')


class RaceEdition(FirstCyclingObject):
    """
    Wrapper to access endpoints associated with specific editions of races.

    Attributes
    ----------
    ID : int
        The firstcycling.com ID for the race from the URL of the race page.
    year : int
        The year of the race edition.
    """

    _default_endpoint = RaceEndpoint
    
    def __init__(self, race_id, year):
        super().__init__(race_id)
        self.year = year

    def __repr__(self):
        return f"{self.__class__.__name__}({self.year} {self.ID})"

    def _get_response(self, **kwargs):
        return fc.get_race_endpoint(self.ID, y=self.year, **kwargs)

    def results(self, classification_num=None, stage_num=None):
        """
        Get race edition results for given classification or stage.

        Parameters
        ----------
        classification_num : int
            Classification for which to collect information.
            See utilities.Classifications for possible inputs.
        stage_num : int
            Stage number for which to collect results, if applicable.
            Input 0 for prologue.

        Returns
        -------
        RaceEditionResults
        """
        zero_padded_stage_num = f'{stage_num:02}' if isinstance(stage_num, int) else None
        if self.year >= 2023 and classification_num is not None and classification_num != Classification['gc'].value:
            print("Warning: results_table might show GC results. Check the standings attribute for other classifications.")
        return self._get_endpoint(endpoint=RaceEditionResults, l=classification_num, e=zero_padded_stage_num)

    def stage_profiles(self):
        """
        Get race edition stage profiles.

        Returns
        -------
        RaceEndpoint
        """
        return self._get_endpoint(e='all')

    def startlist(self):
        """
        Get race edition startlist in normal mode.

        Returns
        -------
        RaceEndpoint
        """
        return self._get_endpoint(k=8)

    def startlist_extended(self):
        """
        Get race edition startlist in extended mode.

        Returns
        -------
        RaceEndpoint
        """
        return self._get_endpoint(k=9)


def normalize(text):
    # Maak de tekst lowercase en vervang streepjes door spaties, verwijder overtollige witruimtes
    text = text.lower()
    text = re.sub(r'[-]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def search_race_id(query, html, threshold=0.7):
    """
    Zoekt naar de race id binnen de HTML-respons door de titels fuzzy te matchen met de query.
    
    Parameters:
        query (str): De zoekopdracht, bv. "Milan Sanremo".
        html (str): De HTML-respons van fc.search_race.
        threshold (float): De minimale overeenkomst (0.0 tot 1.0) om als match te beschouwen.
        
    Returns:
        int of None: Het race-ID als er een match is, anders None.
    """
    soup = BeautifulSoup(html, "html.parser")
    norm_query = normalize(query)
    matches = []
    
    # Zoek naar alle <a>-tags die een href bevatten met race.php?r=
    for a in soup.find_all("a", href=re.compile(r"race\.php\?r=")):
        title = a.get("title")
        if title:
            norm_title = normalize(title)
            ratio = difflib.SequenceMatcher(None, norm_query, norm_title).ratio()
            if ratio >= threshold:
                # Extraheer de race id uit de URL, bv. race.php?r=4&y=2025
                m = re.search(r"r=(\d+)", a["href"])
                if m:
                    race_id = int(m.group(1))
                    matches.append((race_id, title, ratio))
    
    if matches:
        # Geef de beste match (met de hoogste overeenkomst) terug
        best_match = max(matches, key=lambda x: x[2])
        return best_match[0]
    return None