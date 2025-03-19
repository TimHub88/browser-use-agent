from browser_use import Agent
from langchain_openai import ChatOpenAI
import asyncio
from dotenv import load_dotenv
import os
from pydantic import SecretStr

# Charger les variables d'environnement
load_dotenv()

async def main():
    # Récupérer la clé API depuis le fichier .env
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError("La variable DEEPSEEK_API_KEY n'est pas définie dans votre fichier .env")

    # Initialiser le LLM DeepSeek V3
    llm = ChatOpenAI(
        base_url='https://api.deepseek.com/v1',
        model='deepseek-v3',  # Utilisation de DeepSeek V3
        api_key=SecretStr(api_key),
        temperature=0.2,  # Température plus basse pour des réponses plus déterministes
        max_tokens=4096,  # Limiter l'utilisation des tokens
        timeout=60,  # Définir un timeout pour éviter les requêtes qui restent bloquées
    )

    # Instanciation de l'agent avec la tâche désirée
    agent = Agent(
        task="rends toi sur cette adresse : https://compact.univ-lorraine.fr/ et appuie sur connexion. Une fois sur la page de connexion, pour identifiant rentre 'e3611u' et mot de passe 'BACmention88250/' Une fois sur la page d'accueil clique sur 'Mon Portfolio' puis une fois sur le portfolio clique sur le lien 'Marketing', une fois sur page marketing appuie sur le crayon à droite de l'écran en dessous de la loupe, une fois la page chargé en version modification, clique sur le bouton crayon qui veut donc dire 'modifier' de la section 'conduire les actions marketing - description' puis dans la nouvelle page qui s'ouvre change le contenu de l'input de 'contenu du bloc' en reformulant toute cet input qui commence à partir de 'competences marketing et travaux réalisés' en ajoutant des projets de deuxieme année de BUT puisque la description actuelle vaut pour la première année, tu dois donc ajouter le projet suivant dans ta reformulation 'Projet Peel, création pendant deux jours d'une entreprise fictive basé à Gérardmer dans les Vosges, axée sur l'évènementiel qui aurait pour but de raviver le dynamisme culturelle de la région, nous avons fait des affiches de design, un dossier financier avec plan de vision de 1 à 3 ans, nos cibles, analyse du marché...' ",
        llm=llm,
        use_vision=False
    )

    # Exécuter l'agent
    await agent.run()

# Lancer l'agent
if __name__ == "__main__":
    asyncio.run(main())
