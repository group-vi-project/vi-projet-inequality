from dash import dcc
import dash_mantine_components as dmc

from views.view import View
from common.constants import ContainerIds
import common.components as components


class InfoView(View):

    id = "info"
    label = "Informations sur l'application"
    icon = "tabler:info-circle"

    def render(self):
        return dcc.Markdown(
            f"""
            ## {self.label}

            ### Auteurs
            - Aebischer Cyrill
            - Cavalli Andrea
            - Ngueukam Djeuda Wilfried Karel

            ### Source des données

            Le dataset utilisé dans cette
            application provient de l'Enquête suisse sur
            la structure des salaires (ESS) réalisée par
            l'Office fédéral de la statistique (OFS).
            Il est disponible sur le lien suivant [OFS - Enquête
            suisse sur la structure des salaires (ESS)]
            (https://www.bfs.admin.ch/bfs/fr/home/statistiques/travail-remuneration/enquetes/ess.html).
            Notre analyse s'est limité au secteur _26 Fabrication de
            produits informatiques, électroniques et optiques/horlogerie_.

            ### A propos de cette application

            L'analyse des écarts salariaux dans
            notre application repose sur la médiane des
            salaires. En effet, en utilisant la médiane,
            nous avons calculé le pourcentage d'écart
            des salaires entre les hommes et les femmes.
            Nous nous sommes basés sur l'étude [Ecart salarial selon le sexe](
            https://www.bfs.admin.ch/bfs/fr/home/statistiques/travail-remuneration/salaires-revenus-cout-travail/structure-salaires/ecart-salarial.html#:~:text=Salaire%20mensuel%20brut%20selon%20la%20position%20professionnelle%20et%20le%20sexe%2C%20en%202024%2C%20valeur%20centrale%20(m%C3%A9diane)%20en%20francs%2C%20secteur%20priv%C3%A9%20et%20secteur%20public%20ensemble)
            pour calculer les inégalités salariales.
            La formule utilisée, pour chaque région dans chaque position professionnelle et sur chaque année, est la suivante :

            > Ecart salarial (%) = ((Médiane des salaires des hommes - Médiane des salaires des femmes) / Médiane des salaires des hommes) * 100


            Ainsi une valeur de **20%** signifie : _Le salaire médian  des femmes est, **20%** inférieur à celui des hommes.

            ### Contexte du projet   
            Cette application a été développée dans le cadre d'un projet du cours _Visualisation de l'information_ au sein de la HES-SO Master.
            """, link_target="_blank"
        )
