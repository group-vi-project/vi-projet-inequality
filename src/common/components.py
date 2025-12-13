import dash_mantine_components as dmc

from common.constants import ComponentIds, Series


def seriesSelector():
    return dmc.SegmentedControl(
        id=ComponentIds.SERIES_SELECTOR,
        data=[
            {"label": "Salaires d'une région", "value": Series.REGION},
            {"label": "Salaires d'une position professionnelle", "value": Series.POSITION},
        ],
        fullWidth=True,
        size="md",
    )


def positionSelector():
    return dmc.SegmentedControl(
        id=ComponentIds.POSITION_SELECTOR,
        data=[
            {"label": "Toutes positions professionnelles", "value": "Position professionnelle - total"},
            {"label": "Cadre supérieur et moyen", "value": "Cadre supérieur et moyen"},
            {"label": "Cadre inférieur", "value": "Cadre inférieur"},
            {"label": "Responsable de l'exécution des travaux", "value": "Responsable de l'exécution des travaux"},
            {"label": "Sans fonction de cadre", "value": "Sans fonction de cadre"},
        ],
        fullWidth=True,
        size="md",
    )


def regionSelector():
    labels = [
        "Suisse",
        "Région lémanique",
        "Espace Mittelland",
        "Nordwestschweiz",
        "Zürich",
        "Ostschweiz",
        "Zentralschweiz",
        "Ticino",
    ]
    return dmc.SegmentedControl(
        id=ComponentIds.REGION_SELECTOR,
        data=[{"label": label, "value": label} for label in labels],
        fullWidth=True,
        size="md",
    )


def yearSelector():
    return dmc.Slider(
        id=ComponentIds.YEAR_SELECTOR,
        restrictToMarks=True,
        min=2012,
        max=2022,
        marks=[{"value": year, "label" : year} for year in range(2012, 2023, 2)],
    )

# a nice container
def dataContainer(id):
    return dmc.Paper(
        id=id,
        shadow="sm",
        radius="md",
        p="lg",
        withBorder=True,
    )